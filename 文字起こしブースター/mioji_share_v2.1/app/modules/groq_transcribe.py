"""
Groq Transcribe Module - V2 (Memory Optimized)
源流コードの良い部分を取り入れつつ、メモリ効率を最適化
"""

import os
import sys
import io
import time
import tempfile
from pathlib import Path
from typing import Tuple, List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import gc

# Windows環境での絵文字出力対応（cp932エラー回避）
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass  # 既に設定済みの場合はスキップ

from pydub import AudioSegment
import requests
from requests import HTTPError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def _create_session() -> requests.Session:
    """Create session with connection pooling and retry"""
    sess = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(
        max_retries=retry,
        pool_connections=20,
        pool_maxsize=20
    )
    sess.mount("https://", adapter)
    sess.mount("http://", adapter)
    return sess


def _split_audio_to_files(path: Path, chunk_seconds: int = 180) -> List[Path]:
    """
    Split audio into chunk FILES (not memory objects) to reduce memory usage.
    This is critical for large files.
    """
    import subprocess
    
    file_ext = path.suffix.lower()
    print(f"[DEBUG] Processing file: {path}")
    print(f"[DEBUG] File extension: {file_ext}")
    
    # Create temp directory for chunks
    from .. import get_temp_dir
    chunk_dir = get_temp_dir(prefix="groq_chunks_")
    chunks = []
    
    try:
        # Get duration first
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
               '-of', 'default=noprint_wrappers=1:nokey=1', str(path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = float(result.stdout.strip())
        
        print(f"[DEBUG] Audio duration: {duration:.1f} seconds")
        
        # 音声長をキャッシュ（後で再利用）
        _split_audio_to_files._last_duration = duration
        
        # Calculate number of chunks
        num_chunks = int(duration / chunk_seconds) + (1 if duration % chunk_seconds > 0 else 0)
        print(f"[DEBUG] Creating {num_chunks} chunks of {chunk_seconds} seconds each")
        
        # Use ffmpeg segment mode (より高速) 
        pattern = str(chunk_dir / "chunk_%04d.mp3")
        
        cmd = [
            'ffmpeg', '-y',
            '-i', str(path),
            '-f', 'segment',
            '-segment_time', str(chunk_seconds),
            '-vn',  # No video
            '-ar', '16000',  # 16kHz sample rate
            '-ac', '1',      # Mono
            '-b:a', '64k',   # Bitrate
            '-acodec', 'libmp3lame',
            '-reset_timestamps', '1',
            '-loglevel', 'error',
            pattern
        ]
        
        print(f"[DEBUG] Running ffmpeg segment mode...")
        subprocess.run(cmd, capture_output=True, check=True)
        
        # Collect generated chunks
        for i in range(num_chunks):
            chunk_path = chunk_dir / f"chunk_{i:04d}.mp3"
            if chunk_path.exists():
                chunks.append(chunk_path)
            else:
                # 最後のチャンクが短い場合は存在しない可能性
                if i < num_chunks - 1:  # 最後以外なら問題
                    print(f"[WARNING] Missing chunk {i}")
        
        print(f"[DEBUG] Created {len(chunks)} chunks using segment mode")
        
        print(f"[DEBUG] Successfully created {len(chunks)} chunk files")
        return chunks
        
    except Exception as e:
        print(f"[ERROR] Failed to split audio: {e}")
        # Clean up on error
        for chunk in chunks:
            try:
                chunk.unlink()
            except:
                pass
        try:
            chunk_dir.rmdir()
        except:
            pass
        raise


def _groq_transcribe_file(
    session: requests.Session,
    api_key: str,
    model: str,
    chunk_path: Path,
    language: str = None,
    max_retries: int = 3
) -> str:
    """Transcribe a single chunk file"""
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    
    for attempt in range(max_retries):
        try:
            with open(chunk_path, 'rb') as f:
                files = {'file': (chunk_path.name, f, 'audio/mpeg')}
                headers = {"Authorization": f"Bearer {api_key}"}
                data = {
                    'model': model,
                    'response_format': 'text',
                }
                if language:
                    data['language'] = language
                
                resp = session.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=120
                )
                
                if resp.status_code == 200:
                    return resp.text.strip()
                
                # Handle rate limits and server errors
                if resp.status_code == 429:
                    wait = min(30, 2 ** attempt)
                    print(f"[INFO] Rate limit, waiting {wait}s...")
                    time.sleep(wait)
                elif resp.status_code in [500, 502, 503, 504]:
                    wait = min(30, 5 * (2 ** attempt))
                    print(f"[INFO] Server error {resp.status_code}, waiting {wait}s...")
                    time.sleep(wait)
                else:
                    print(f"[ERROR] API error {resp.status_code}: {resp.text[:200]}")
                    
        except Exception as e:
            print(f"[ERROR] Request failed (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    
    return ""  # Return empty string on failure


def transcribe_file_with_groq(
    file_path: Path,
    api_key: str,
    model: str = "whisper-large-v3-turbo",
    chunk_seconds: int = 180,  # 3分チャンク（源流ver4と同じ）
    max_workers: int = 10,  # デフォルト並列数を増加
    progress_cb: Optional[Callable[[float, str], None]] = None,
) -> Tuple[str, str, float]:
    """
    Memory-optimized transcription for large files.
    Uses file-based chunking instead of memory-based.
    """
    start_time = time.time()
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Adjust parameters based on file type (源流ver4の最適化)
    file_ext = file_path.suffix.lower()
    if file_ext in ['.m4a', '.aac', '.mp4']:
        # m4aファイルは短めのチャンクで安定性重視
        chunk_seconds = min(chunk_seconds, 120)  # 2分
        if progress_cb:
            progress_cb(0.0, f"Processing {file_ext} file...")
    
    # Split audio into chunk FILES (not memory objects)
    try:
        chunk_files = _split_audio_to_files(file_path, chunk_seconds)
        # 音声長をキャッシュ（ffprobe重複実行を避けるため）
        transcribe_file_with_groq._cached_duration = getattr(_split_audio_to_files, '_last_duration', 0)
    except Exception as e:
        raise RuntimeError(f"Failed to split audio: {e}")
    
    total_chunks = len(chunk_files)
    
    # 源流ver4の動的並列数調整ロジック
    if total_chunks <= 10:
        max_workers = total_chunks  # 10個以下は全部並列
    elif total_chunks <= 30:
        max_workers = min(max_workers, 10)  # 30個以下は最大10並列
    elif total_chunks <= 50:
        max_workers = min(max_workers, 8)  # 50個以下は最大8並列
    elif total_chunks <= 100:
        max_workers = min(max_workers, 5)  # 100個以下は最大5並列
    else:
        max_workers = min(max_workers, 3)  # それ以上は最大3並列
    
    print(f"[INFO] {total_chunks} chunks, using {max_workers} parallel workers")
    
    # Create session
    session = _create_session()
    
    # Determine language
    language = "en" if model.endswith("-en") else None
    
    # Process chunks
    results = [None] * total_chunks
    completed = 0
    
    if progress_cb:
        progress_cb(0.0, f"Processing {total_chunks} chunks...")
    
    def process_chunk(idx: int, chunk_path: Path) -> Tuple[int, str]:
        """Process a single chunk"""
        text = _groq_transcribe_file(
            session, api_key, model, chunk_path, language
        )
        # Delete chunk file immediately after processing
        try:
            chunk_path.unlink()
        except:
            pass
        return idx, text
    
    # Process in batches for very large files
    if total_chunks > 30:
        batch_size = max_workers * 2
        print(f"[INFO] Processing in batches of {batch_size}")
        
        for batch_start in range(0, total_chunks, batch_size):
            batch_end = min(batch_start + batch_size, total_chunks)
            batch_chunks = chunk_files[batch_start:batch_end]
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {
                    executor.submit(process_chunk, batch_start + i, chunk): batch_start + i
                    for i, chunk in enumerate(batch_chunks)
                }
                
                for future in as_completed(futures):
                    try:
                        idx, text = future.result()
                        results[idx] = text
                        completed += 1
                        if progress_cb:
                            progress_cb(
                                completed / total_chunks,
                                f"Completed {completed}/{total_chunks} chunks"
                            )
                    except Exception as e:
                        idx = futures[future]
                        results[idx] = ""
                        completed += 1
                        print(f"[ERROR] Chunk {idx} failed: {e}")
                        if progress_cb:
                            progress_cb(
                                completed / total_chunks,
                                f"Chunk {idx} failed"
                            )
            
            # Wait between batches (源流ver4: 0.5秒)
            if batch_end < total_chunks:
                time.sleep(0.5)
                gc.collect()  # Force garbage collection
    else:
        # Process all at once for small files
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(process_chunk, i, chunk): i
                for i, chunk in enumerate(chunk_files)
            }
            
            for future in as_completed(futures):
                try:
                    idx, text = future.result()
                    results[idx] = text
                    completed += 1
                    if progress_cb:
                        progress_cb(
                            completed / total_chunks,
                            f"Completed {completed}/{total_chunks} chunks"
                        )
                except Exception as e:
                    idx = futures[future]
                    results[idx] = ""
                    completed += 1
                    print(f"[ERROR] Chunk {idx} failed: {e}")
    
    # Clean up chunk directory
    try:
        chunk_files[0].parent.rmdir()
    except:
        pass
    
    # Combine results (順番通りに結合される)
    combined_text = "\n".join([r for r in results if r])
    
    # 音声長は既にチャンク分割時に取得済み（重複実行を回避）
    audio_duration = getattr(transcribe_file_with_groq, '_cached_duration', total_chunks * chunk_seconds)
    
    # Save to file
    from .. import get_temp_dir
    output_dir = get_temp_dir(prefix="moji_groq_")
    output_file = output_dir / f"{file_path.stem}_transcript.txt"
    output_file.write_text(combined_text, encoding="utf-8")
    
    elapsed = time.time() - start_time
    
    if progress_cb:
        speed_ratio = audio_duration / elapsed if elapsed > 0 else 0
        progress_cb(1.0, f"完了！ {speed_ratio:.1f}倍速で処理")
    
    # 音声長も返すように変更
    return combined_text, str(output_file), elapsed, audio_duration
