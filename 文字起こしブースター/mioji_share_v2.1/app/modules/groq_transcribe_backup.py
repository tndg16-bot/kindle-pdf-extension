import os
import io
import time
import tempfile
from pathlib import Path
from typing import Tuple, List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from pydub import AudioSegment
import requests
from requests import HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def _split_audio_chunks(path: Path, chunk_seconds: int = 180) -> List[AudioSegment]:
    """Load audio robustly (handles m4a) and split into chunks."""
    import subprocess
    
    audio = None
    tmp_file = None
    file_ext = path.suffix.lower()
    
    # Log file info for debugging
    print(f"[DEBUG] Processing file: {path}")
    print(f"[DEBUG] File extension: {file_ext}")
    print(f"[DEBUG] File exists: {path.exists()}")
    if path.exists():
        print(f"[DEBUG] File size: {path.stat().st_size / (1024*1024):.2f} MB")
    
    # For m4a files, always use ffmpeg conversion
    if file_ext in ['.m4a', '.aac', '.mp4']:
        print(f"[DEBUG] {file_ext} file detected, using ffmpeg conversion")
        tmp_file = Path(tempfile.gettempdir()) / f"temp_audio_{os.getpid()}_{time.time()}.wav"
        
        try:
            # Check if ffmpeg exists
            ffmpeg_check = subprocess.run(["ffmpeg", "-version"], 
                                         capture_output=True, text=True, timeout=5)
            if ffmpeg_check.returncode != 0:
                raise FileNotFoundError("ffmpeg not found")
            
            print(f"[DEBUG] Converting {file_ext} to WAV using ffmpeg...")
            
            # Run ffmpeg with better compatibility options
            cmd = [
                "ffmpeg", 
                "-y",  # overwrite output
                "-i", str(path),  # input file
                "-vn",  # no video
                "-acodec", "pcm_s16le",  # PCM 16-bit little-endian
                "-ar", "16000",  # 16kHz sample rate
                "-ac", "1",  # mono
                "-f", "wav",  # force wav format
                str(tmp_file)
            ]
            
            print(f"[DEBUG] FFmpeg command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"[ERROR] FFmpeg stderr: {result.stderr}")
                print(f"[ERROR] FFmpeg stdout: {result.stdout}")
                raise RuntimeError(f"ffmpeg変換エラー (code {result.returncode}): {result.stderr[:500]}")
            
            if not tmp_file.exists():
                raise RuntimeError(f"変換後のファイルが作成されませんでした: {tmp_file}")
            
            print(f"[DEBUG] Conversion successful, loading WAV file...")
            # Load the converted wav file
            audio = AudioSegment.from_file(tmp_file, format="wav")
            print(f"[DEBUG] WAV file loaded successfully")
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("音声ファイルの変換がタイムアウトしました（ファイルが大きすぎる可能性があります）")
        except FileNotFoundError:
            raise RuntimeError("ffmpegが見つかりません。ffmpegをインストールしてください\n" +
                             "macOS: brew install ffmpeg\n" +
                             "Windows: choco install ffmpeg")
        except Exception as e:
            print(f"[ERROR] Exception during conversion: {type(e).__name__}: {str(e)}")
            raise RuntimeError(f"音声の読み込みに失敗しました: {str(e)}")
        finally:
            # Clean up temporary file
            if tmp_file and tmp_file.exists():
                try:
                    tmp_file.unlink()
                    print(f"[DEBUG] Temporary file deleted: {tmp_file}")
                except Exception as e:
                    print(f"[WARNING] Could not delete temp file: {e}")
    else:
        # For other formats, try direct load first
        try:
            print(f"[DEBUG] Attempting direct load with pydub...")
            audio = AudioSegment.from_file(path)
            print(f"[DEBUG] Direct load successful")
        except Exception as e1:
            print(f"[DEBUG] Direct load failed: {e1}, trying ffmpeg conversion...")
            # Fallback to ffmpeg conversion
            tmp_file = Path(tempfile.gettempdir()) / f"temp_audio_{os.getpid()}_{time.time()}.wav"
            
            try:
                result = subprocess.run([
                    "ffmpeg", "-y", "-i", str(path),
                    "-vn", "-acodec", "pcm_s16le",
                    "-ar", "16000", "-ac", "1",
                    "-f", "wav", str(tmp_file)
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    raise RuntimeError(f"ffmpeg変換エラー: {result.stderr[:500]}")
                
                audio = AudioSegment.from_file(tmp_file, format="wav")
                
            except Exception as e:
                raise RuntimeError(f"音声の読み込みに失敗しました: {str(e)}")
            finally:
                if tmp_file and tmp_file.exists():
                    try:
                        tmp_file.unlink()
                    except Exception:
                        pass
    
    # Split audio into chunks
    if audio is None:
        raise RuntimeError("音声データの読み込みに失敗しました")
    
    print(f"[DEBUG] Audio duration: {len(audio)/1000:.1f} seconds")
    print(f"[DEBUG] Splitting into {chunk_seconds} second chunks...")
    
    chunks = []
    step = chunk_seconds * 1000  # Convert to milliseconds
    for start in range(0, len(audio), step):
        end = min(len(audio), start + step)
        chunks.append(audio[start:end])
    
    print(f"[DEBUG] Created {len(chunks)} chunks")
    return chunks


def _create_session() -> requests.Session:
    sess = requests.Session()
    retry = Retry(total=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    sess.mount("https://", adapter)
    sess.mount("http://", adapter)
    return sess


def _groq_transcribe_bytes(session: requests.Session, api_key: str, model: str, audio_bytes: bytes, mime: str, filename: str, language: str | None = None) -> str:
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {
        "file": (filename, audio_bytes, mime),
    }
    data = {
        "model": model,
        "response_format": "text",
    }
    if language and language.lower() not in ("auto", ""):  # optional
        data["language"] = language
    
    # Longer timeout for large files
    timeout = 600 if len(audio_bytes) > 10 * 1024 * 1024 else 300  # 10MB threshold
    
    resp = session.post(url, headers=headers, files=files, data=data, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def transcribe_file_with_groq(
    file_path: Path,
    api_key: str,
    model: str = "whisper-large-v3-turbo",
    chunk_seconds: int = 120,
    max_workers: int = 4,
    progress_cb: Optional[Callable[[float, str], None]] = None,
) -> Tuple[str, str, float]:
    """Transcribe an audio file by chunking and parallelizing requests.

    Returns combined_text and path to saved txt file.
    """
    # Validate file exists
    if not file_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
    
    # Check file extension and adjust chunk size for m4a files
    file_ext = file_path.suffix.lower()
    if file_ext in ['.m4a', '.aac']:
        # m4a files may need smaller chunks due to codec complexity
        chunk_seconds = min(chunk_seconds, 90)
        if progress_cb:
            progress_cb(0.0, f"m4aファイルを処理中...")
    
    try:
        chunks = _split_audio_chunks(file_path, chunk_seconds=chunk_seconds)
    except Exception as e:
        if progress_cb:
            progress_cb(0.0, f"エラー: {str(e)}")
        raise
    
    # Check total duration and warn if very long
    total_duration_sec = sum(len(chunk) / 1000.0 for chunk in chunks)
    if total_duration_sec > 3600:  # More than 1 hour
        hours = total_duration_sec / 3600
        print(f"[WARNING] Very long audio file: {hours:.1f} hours")
        print(f"[WARNING] This will create {len(chunks)} API requests")
        if len(chunks) > 100:
            print(f"[WARNING] Too many chunks ({len(chunks)}). Consider using a shorter file.")
            # Limit workers for very large files to avoid overwhelming the API
            max_workers = min(max_workers, 2)
            print(f"[INFO] Reducing parallel workers to {max_workers} for stability")
    session = _create_session()
    # Heuristic: English-only model name includes '-en'
    language = "en" if model.endswith("-en") else None
    start_ts = time.time()
    results = [None] * len(chunks)

    def transcribe_segment(seg: AudioSegment, bitrate: str = "64k", retry_count: int = 0) -> str:
        max_retries = 3
        # Export to mp3 mono 16kHz to reduce payload size
        buf = io.BytesIO()
        seg.set_channels(1).set_frame_rate(16000).export(buf, format="mp3", bitrate=bitrate)
        
        try:
            return _groq_transcribe_bytes(session=session, api_key=api_key, model=model, audio_bytes=buf.getvalue(), mime="audio/mpeg", filename="audio.mp3", language=language)
        except HTTPError as e:
            code = e.response.status_code if e.response is not None else None
            
            # 429: Rate limit - exponential backoff
            if code == 429:
                if retry_count < max_retries:
                    wait_time = min(30, 2 ** retry_count)
                    print(f"[INFO] Rate limit hit, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    return transcribe_segment(seg, bitrate, retry_count + 1)
                raise
            
            # 500-504: Server errors - retry with backoff
            if code in [500, 502, 503, 504]:
                if retry_count < max_retries:
                    wait_time = min(30, 5 * (2 ** retry_count))
                    print(f"[INFO] Server error {code}, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    return transcribe_segment(seg, bitrate, retry_count + 1)
                raise
            
            # 413: Payload Too Large -> split further or reduce bitrate
            if code == 413:
                duration_sec = seg.duration_seconds
                if duration_sec > 30:
                    mid_ms = int(len(seg) / 2)
                    left = seg[:mid_ms]
                    right = seg[mid_ms:]
                    return transcribe_segment(left, bitrate) + "\n" + transcribe_segment(right, bitrate)
                # try lower bitrate
                if bitrate != "64k":
                    return transcribe_segment(seg, "48k")  # Try 48k like in source
            
            # 400: Bad Request (often unsupported format). Fallback to WAV PCM.
            if code == 400:
                buf2 = io.BytesIO()
                seg.set_channels(1).set_frame_rate(16000).export(buf2, format="wav")
                try:
                    return _groq_transcribe_bytes(session=session, api_key=api_key, model=model, audio_bytes=buf2.getvalue(), mime="audio/wav", filename="audio.wav", language=language)
                except HTTPError as e2:
                    code2 = e2.response.status_code if e2.response is not None else None
                    if code2 == 400 and seg.duration_seconds > 30:
                        mid_ms = int(len(seg) / 2)
                        left = seg[:mid_ms]
                        right = seg[mid_ms:]
                        return transcribe_segment(left, bitrate) + "\n" + transcribe_segment(right, bitrate)
                    raise
            raise

    def work(i, seg: AudioSegment):
        return i, transcribe_segment(seg)

    done = 0
    total = len(chunks)
    if progress_cb:
        progress_cb(0.0, f"送信準備 ({total} チャンク)")

    # Adjust max_workers based on chunk count (like source code)
    if total > 100:
        max_workers = min(max_workers, 2)  # Very large files: limit to 2 parallel
        print(f"[INFO] Large file detected ({total} chunks), limiting to {max_workers} parallel workers")
    elif total > 50:
        max_workers = min(max_workers, 3)  # Large files: limit to 3 parallel
        print(f"[INFO] Large file detected ({total} chunks), limiting to {max_workers} parallel workers")
    else:
        max_workers = max(1, min(max_workers, len(chunks), 6))
    
    # Process in batches for very large files (inspired by source)
    if total > 30:
        batch_size = max_workers * 2  # Process in batches
        print(f"[INFO] Processing in batches of {batch_size}")
        
        for batch_start in range(0, total, batch_size):
            batch_end = min(batch_start + batch_size, total)
            batch_chunks = chunks[batch_start:batch_end]
            batch_indices = list(range(batch_start, batch_end))
            
            with ThreadPoolExecutor(max_workers=max_workers) as ex:
                # Create futures with correct indices
                futures = []
                for i, (idx, seg) in enumerate(zip(batch_indices, batch_chunks)):
                    futures.append(ex.submit(work, idx, seg))
                
                # Process results
                for fut in as_completed(futures):
                    try:
                        idx, text = fut.result()
                        results[idx] = text
                        done += 1
                        if progress_cb:
                            progress_cb(done / total, f"{done}/{total} チャンク完了")
                    except Exception as e:
                        print(f"[ERROR] Failed to process chunk: {e}")
                        done += 1
                        if progress_cb:
                            progress_cb(done / total, f"{done}/{total} チャンク（エラー）")
            
            # Wait between batches to avoid overwhelming the API
            if batch_end < total:
                time.sleep(0.5)
                # Force garbage collection between batches
                import gc
                gc.collect()
    else:
        # Original code for small files
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(work, i, seg) for i, seg in enumerate(chunks)]
            for fut in as_completed(futures):
                try:
                    idx, text = fut.result()
                    results[idx] = text
                    done += 1
                    if progress_cb:
                        progress_cb(done / total, f"{done}/{total} チャンク完了")
                except Exception as e:
                    print(f"[ERROR] Failed to process chunk: {e}")
                    done += 1
                    if progress_cb:
                        progress_cb(done / total, f"{done}/{total} チャンク（エラー）")

    # Filter out None values and join results
    combined = "\n".join([r for r in results if r is not None])
    tmpdir = Path(tempfile.mkdtemp(prefix="moji_groq_"))
    out = tmpdir / (file_path.stem + "_transcript.txt")
    out.write_text(combined, encoding="utf-8")
    elapsed = time.time() - start_ts
    if progress_cb:
        progress_cb(1.0, f"完了: {elapsed:.1f}s")
    return combined, str(out), elapsed
