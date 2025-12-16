import asyncio
import sys
import uuid
import time
import os
import gc
import threading
from typing import Dict, Any, Optional
from collections import deque

# Windows環境での絵文字出力対応（cp932エラー回避）
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass  # 既に設定済みの場合はスキップ

# Concurrency config
TRANSCRIBE_CONCURRENCY = int(os.getenv("TRANSCRIBE_CONCURRENCY", "6"))
GEMINI_CONCURRENCY = int(os.getenv("GEMINI_CONCURRENCY", "1"))
FFMPEG_CONCURRENCY = int(os.getenv("FFMPEG_CONCURRENCY", "2"))

API_RATE_PER_SEC = float(os.getenv("API_RATE_PER_SEC", "3"))
OCR_RATE_PER_SEC = float(os.getenv("OCR_RATE_PER_SEC", "1"))

# Semaphores
transcribe_sem = asyncio.Semaphore(TRANSCRIBE_CONCURRENCY)
gemini_sem = asyncio.Semaphore(GEMINI_CONCURRENCY)
ffmpeg_sem = asyncio.Semaphore(FFMPEG_CONCURRENCY)

# Simple token bucket limiter
class TokenBucket:
    def __init__(self, rate_per_sec: float):
        self.rate = rate_per_sec
        self._tokens = rate_per_sec
        self._last = time.time()
        self._lock = asyncio.Lock()

    async def wait(self, n: float = 1.0):
        while True:
            async with self._lock:
                now = time.time()
                elapsed = now - self._last
                self._tokens = min(self.rate, self._tokens + elapsed * self.rate)
                self._last = now
                if self._tokens >= n:
                    self._tokens -= n
                    return
            await asyncio.sleep(max(0.01, 1.0 / max(1e-6, self.rate)))


api_bucket = TokenBucket(API_RATE_PER_SEC)
ocr_bucket = TokenBucket(OCR_RATE_PER_SEC)

# In-memory queue and registry
JOB_QUEUE_MAXSIZE = int(os.getenv("JOB_QUEUE_MAXSIZE", "200"))
job_queue: asyncio.Queue = asyncio.Queue(maxsize=JOB_QUEUE_MAXSIZE)
jobs: Dict[str, Dict[str, Any]] = {}
_pending_ids = deque()  # FIFO order of queued jobs
_running_jobs = 0
_canceled_ids = set()

# Simple moving averages for ETA estimation per job type
_eta_stats: Dict[str, Dict[str, float]] = {
    # defaults as fallbacks
    "lp_ocr": {"avg": 60.0, "n": 0},
    "audio_transcribe": {"avg": 120.0, "n": 0},
    "hls_transcribe": {"avg": 180.0, "n": 0},
}

# basic outcome counters
_metrics = {"done": 0, "failed": 0, "r429": 0}

# Background asyncio loop in a dedicated thread
_loop: Optional[asyncio.AbstractEventLoop] = None
_loop_thread: Optional[threading.Thread] = None


def _run_loop(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def ensure_loop() -> asyncio.AbstractEventLoop:
    global _loop, _loop_thread
    if _loop is not None:
        return _loop
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=_run_loop, args=(loop,), daemon=True)
    t.start()
    _loop = loop
    _loop_thread = t
    return loop


async def worker_loop():
    while True:
        job = await job_queue.get()
        jid = job["id"]
        # Skip if canceled before start
        if jobs.get(jid, {}).get("status") == "canceled" or jid in _canceled_ids:
            try:
                _pending_ids.remove(jid)
            except Exception:
                pass
            job_queue.task_done()
            continue
        jobs[jid]["status"] = "running"
        jobs[jid]["started_at"] = time.time()
        try:
            jtype = job.get("type")
            print(f"[job] start id={jid} type={jtype}")
        except Exception:
            pass
        try:
            # Remove from pending list upon actual start
            try:
                _pending_ids.remove(jid)
            except ValueError:
                pass
        except Exception:
            pass
        global _running_jobs
        _running_jobs += 1
        try:
            if job["type"] == "transcribe":
                async with transcribe_sem:
                    await api_bucket.wait()
                    # placeholder: call real transcribe here
                    await asyncio.sleep(0.1)
                    jobs[jid]["result"] = {"ok": True}
            elif job["type"] == "ocr":
                async with gemini_sem:
                    await ocr_bucket.wait()
                    await asyncio.sleep(0.1)
                    jobs[jid]["result"] = {"ok": True}
            elif job["type"] == "audio_transcribe":
                # Audio file transcription using Groq
                async with transcribe_sem:
                    await api_bucket.wait()
                    from .modules.groq_transcribe import transcribe_file_with_groq
                    loop = asyncio.get_running_loop()
                    p = job.get("payload", {})
                    file_path = p.get("file_path")
                    model = p.get("model", "whisper-large-v3-turbo")
                    chunk_seconds = int(p.get("chunk_seconds", 180))
                    max_workers = int(p.get("max_workers", 10))
                    api_key = p.get("groq_api_key")
                    if not api_key:
                        raise RuntimeError("Groq APIキーが未設定です（上部のAPIキー設定で保存してください）")

                    def _prog(frac: float, desc: str):
                        jobs[jid]["progress"] = max(0.0, min(1.0, float(frac)))
                        jobs[jid]["desc"] = desc
                        if jobs.get(jid, {}).get("cancel", False):
                            raise RuntimeError("canceled")
                        if jobs.get(jid, {}).get("cancel", False):
                            raise RuntimeError("canceled")
                        if jobs.get(jid, {}).get("cancel", False):
                            raise RuntimeError("canceled")

                    def run_blocking():
                        txt, out_path, elapsed, audio_duration = transcribe_file_with_groq(
                            file_path=Path(file_path),
                            api_key=api_key,
                            model=model,
                            chunk_seconds=chunk_seconds,
                            max_workers=max_workers,
                            progress_cb=_prog,
                        )
                        return txt, out_path, elapsed, audio_duration

                    from pathlib import Path
                    txt, out_path, elapsed, audio_duration = await loop.run_in_executor(None, run_blocking)
                    jobs[jid]["result"] = {
                        "text": txt,
                        "text_path": out_path,
                        "elapsed": elapsed,
                        "audio_duration": audio_duration,
                        "model": model,
                    }
            elif job["type"] == "lp_ocr":
                # Combined capture + OCR for LP
                async with gemini_sem:
                    await ocr_bucket.wait()
                    # Run blocking lp capture+ocr in executor
                    from .modules.lp_gemini import lp_capture_and_ocr
                    loop = asyncio.get_running_loop()

                    # pull params
                    p = job.get("payload", {})
                    url = p.get("url")
                    model = p.get("model", "gemini-2.5-flash")
                    width = int(p.get("width", 1280))
                    tile_height = int(p.get("tile_height", 2400))
                    device_scale = float(p.get("device_scale", 1.0))
                    overlap = int(p.get("overlap", 200))
                    pause_animations = bool(p.get("pause_animations", True))
                    hide_fixed = bool(p.get("hide_fixed", True))
                    prerender_scroll = bool(p.get("prerender_scroll", True))
                    goto_timeout_ms = int(p.get("goto_timeout_ms", 90_000))
                    api_key = p.get("gemini_api_key")
                    if not api_key:
                        raise RuntimeError("Gemini APIキーが未設定です（上部のAPIキー設定で保存してください）")

                    def _prog(frac: float, desc: str):
                        jobs[jid]["progress"] = max(0.0, min(1.0, float(frac)))
                        jobs[jid]["desc"] = desc

                    def run_blocking():
                        png_path, text, txt_path, tiles = lp_capture_and_ocr(
                            url=url,
                            gemini_api_key=api_key,
                            model=model,
                            width=width,
                            tile_height=tile_height,
                            device_scale=device_scale,
                            overlap=overlap,
                            pause_animations=pause_animations,
                            hide_fixed=hide_fixed,
                            prerender_scroll=prerender_scroll,
                            goto_timeout_ms=goto_timeout_ms,
                            max_output_pixels=100_000_000,
                            progress_cb=_prog,
                        )
                        return png_path, text, txt_path, tiles

                    png_path, text, txt_path, tiles = await loop.run_in_executor(None, run_blocking)
                    jobs[jid]["result"] = {
                        "png_path": png_path,
                        "text_path": txt_path,
                        "text": text,
                        "tiles": tiles,
                        "model": model,
                        "width": width,
                    }
            elif job["type"] == "hls_transcribe":
                # HLS URLs -> extract audio -> Groq transcribe (concatenate)
                async with transcribe_sem:
                    await api_bucket.wait()
                    from .modules.hls_extractor import extract_audio_from_hls
                    from .modules.groq_transcribe import transcribe_file_with_groq
                    from pathlib import Path
                    from . import get_temp_dir

                    p = job.get("payload", {})
                    urls_text = p.get("urls", "")
                    model = p.get("model", "whisper-large-v3-turbo")
                    chunk_seconds = int(p.get("chunk_seconds", 180))
                    max_workers = int(p.get("max_workers", 10))

                    # Resolve API key (payload first, then env)
                    api_key = p.get("groq_api_key")
                    if not api_key:
                        raise RuntimeError("Groq APIキーが未設定です（上部のAPIキー設定で保存してください）")

                    urls = [u.strip() for u in str(urls_text).splitlines() if u.strip()]
                    tmpdir = get_temp_dir(prefix="moji_hls_")
                    texts = []
                    out_files = []
                    total_audio = 0.0

                    def _prog(frac: float, desc: str):
                        jobs[jid]["progress"] = max(0.0, min(1.0, float(frac)))
                        jobs[jid]["desc"] = desc

                    # Run blocking pipeline in executor
                    loop = asyncio.get_running_loop()

                    def run_blocking():
                        for idx, u in enumerate(urls, 1):
                            wav = tmpdir / f"hls_{idx:02d}.wav"
                            extract_audio_from_hls(u, wav)
                            txt, path, elapsed, audio_duration = transcribe_file_with_groq(
                                file_path=wav,
                                api_key=api_key,
                                model=model,
                                chunk_seconds=chunk_seconds,
                                max_workers=max_workers,
                                progress_cb=_prog,
                            )
                            texts.append(f"# {u}\n\n{txt}\n\n")
                            out_files.append(path)
                            total_audio += audio_duration
                        combined = "\n".join(texts)
                        out_all = tmpdir / "hls_transcripts.txt"
                        out_all.write_text(combined, encoding="utf-8")
                        return combined, str(out_all), total_audio

                    combined, out_all, total_audio = await loop.run_in_executor(None, run_blocking)
                    jobs[jid]["result"] = {
                        "text": combined,
                        "text_path": out_all,
                        "audio_duration": total_audio,
                        "model": model,
                    }
            else:
                raise ValueError(f"unknown job type: {job['type']}")
            jobs[jid]["status"] = "done"
        except Exception as e:
            msg = str(e)
            if "canceled" in msg.lower():
                jobs[jid]["status"] = "canceled"
            else:
                jobs[jid]["status"] = "failed"
                jobs[jid]["error"] = msg
        finally:
            job_queue.task_done()
            if jobs[jid]["status"] in {"done", "failed"}:
                gc.collect()
            _running_jobs = max(0, _running_jobs - 1)

            # Update ETA stats on success
            try:
                if jobs[jid]["status"] == "done":
                    jtype = jobs[jid].get("type") or job.get("type")
                    st = jobs[jid].get("started_at") or jobs[jid].get("created_at")
                    if jtype and st:
                        dur = max(0.0, time.time() - float(st))
                        s = _eta_stats.setdefault(jtype, {"avg": dur, "n": 0})
                        # EWMA: 0.8 old, 0.2 new
                        s["avg"] = 0.8 * float(s.get("avg", dur)) + 0.2 * dur
                        s["n"] = float(s.get("n", 0)) + 1.0
                    _metrics["done"] = _metrics.get("done", 0) + 1
                elif jobs[jid]["status"] == "failed":
                    _metrics["failed"] = _metrics.get("failed", 0) + 1
                    err = (jobs[jid].get("error") or "").lower()
                    if "429" in err or "rate limit" in err:
                        _metrics["r429"] = _metrics.get("r429", 0) + 1
            except Exception:
                pass
            # final log
            try:
                st = jobs[jid].get("status")
                dur = None
                if jobs[jid].get("started_at"):
                    dur = time.time() - float(jobs[jid]["started_at"])
                if dur is not None:
                    print(f"[job] end id={jid} status={st} dur={dur:.1f}s")
                else:
                    print(f"[job] end id={jid} status={st}")
            except Exception:
                pass


def enqueue_job(job_type: str, payload: Dict[str, Any]):
    jid = str(uuid.uuid4())
    jobs[jid] = {
        "id": jid,
        "type": job_type,
        "status": "queued",
        "created_at": time.time(),
        "payload": payload,
    }
    loop = ensure_loop()
    asyncio.run_coroutine_threadsafe(job_queue.put({"id": jid, "type": job_type, "payload": payload}), loop)
    try:
        _pending_ids.append(jid)
    except Exception:
        pass
    return jid


def start_workers(n_workers: int = 2):
    loop = ensure_loop()
    for _ in range(n_workers):
        asyncio.run_coroutine_threadsafe(worker_loop(), loop)


def get_job(job_id: str) -> Optional[Dict[str, Any]]:
    return jobs.get(job_id)


def get_queue_stats() -> Dict[str, Any]:
    try:
        qlen = job_queue.qsize()
    except Exception:
        qlen = -1
    return {
        "queue_len": qlen,
        "running": _running_jobs,
        "transcribe_concurrency": TRANSCRIBE_CONCURRENCY,
        "gemini_concurrency": GEMINI_CONCURRENCY,
        "ffmpeg_concurrency": FFMPEG_CONCURRENCY,
        "done": _metrics.get("done", 0),
        "failed": _metrics.get("failed", 0),
        "r429": _metrics.get("r429", 0),
    }


def get_job_position(job_id: str) -> Dict[str, int]:
    try:
        qlen = job_queue.qsize()
    except Exception:
        qlen = -1
    try:
        pos = list(_pending_ids).index(job_id)
    except ValueError:
        pos = 0
    except Exception:
        pos = -1
    return {"position": pos, "queue_len": qlen}


def estimate_eta_seconds(job_id: str) -> Optional[float]:
    """Estimate ETA in seconds based on position and avg duration per job type.
    Rough but useful. Returns None if unknown.
    """
    j = jobs.get(job_id)
    if not j:
        return None
    jtype = j.get("type")
    if not jtype:
        return None
    # concurrency per family
    if jtype in ("lp_ocr", "ocr"):
        conc = max(1, GEMINI_CONCURRENCY)
    else:
        conc = max(1, TRANSCRIBE_CONCURRENCY)
    # position in pending queue
    try:
        pos = list(_pending_ids).index(job_id)
    except ValueError:
        # if already running, estimate remaining as avg * 0.5
        st = j.get("started_at")
        if st:
            avg = float(_eta_stats.get(jtype, {}).get("avg", 60.0))
            elapsed = max(0.0, time.time() - float(st))
            return max(0.0, avg - elapsed)
        return None
    avg = float(_eta_stats.get(jtype, {}).get("avg", 60.0))
    # Jobs ahead divided by concurrency gives batches to wait
    batches_ahead = pos / float(conc)
    return max(0.0, batches_ahead * avg)


# Optional janitor: cleanup temp outputs after TTL
# デフォルト10分（600秒）に短縮（Render /tmp容量対策）
JOB_TTL_SEC = int(os.getenv("JOB_TTL_SEC", "600"))


async def _janitor_loop():
    while True:
        now = time.time()
        try:
            for jid, meta in list(jobs.items()):
                st = meta.get("status")
                if st in {"done", "failed"} and (now - meta.get("created_at", now)) > JOB_TTL_SEC:
                    res = meta.get("result", {})
                    for key in ("png_path", "text_path"):
                        p = res.get(key)
                        if p:
                            try:
                                import os as _os
                                from pathlib import Path as _Path
                                _p = _Path(p)
                                if _p.exists():
                                    _p.unlink()
                                    print(f"🗑️ [JANITOR] ファイル削除: {_p.name}")
                                # try remove parent tmp dir if ours
                                par = _p.parent
                                if par.name.startswith(("moji_lp_", "moji_groq_", "moji_hls_", "moji_chromium_")):
                                    for child in par.iterdir():
                                        try:
                                            child.unlink()
                                        except Exception:
                                            pass
                                    try:
                                        par.rmdir()
                                        print(f"🗑️ [JANITOR] ディレクトリ削除: {par.name}")
                                    except Exception:
                                        pass
                            except Exception:
                                pass
                    jobs.pop(jid, None)
            
            # 追加：一時ディレクトリの古いファイルを直接スキャンして削除
            try:
                from pathlib import Path as _Path
                
                # Render環境では /var/data/temp (Persistent Disk)、ローカルでは /tmp
                persistent_temp = _Path("/var/data/temp")
                if persistent_temp.exists():
                    tmp_dir = persistent_temp
                else:
                    import tempfile
                    tmp_dir = _Path(tempfile.gettempdir())
                
                # NOTE: psutil.disk_usage()がホスト全体を返してしまい正確な値が取れないため
                # ディスク使用率監視は無効化し、時間ベースのクリーンアップのみ使用
                force_cleanup = False
                
                for item in tmp_dir.iterdir():
                    # moji_*, groq_chunks_*, yt-dlp の一時ファイルを削除
                    if item.is_dir() and item.name.startswith(("moji_", "groq_chunks_", "yt-dlp_", "tmp")):
                        try:
                            mtime = item.stat().st_mtime
                            age_seconds = now - mtime
                            
                            # LP処理は時間がかかるので30分TTL、その他は10分TTL
                            if item.name.startswith("moji_lp_"):
                                ttl = 1800  # 30分（LP処理用）
                            else:
                                ttl = JOB_TTL_SEC  # 10分（その他）
                            
                            # TTL超過の場合のみ削除（時間ベース）
                            if age_seconds > ttl:
                                import shutil
                                shutil.rmtree(item)
                                print(f"🗑️ [JANITOR] 一時ディレクトリ削除: {item.name} (経過時間: {age_seconds/60:.1f}分)")
                        except Exception:
                            pass
                    
                    # yt-dlpの一時ファイル（単体ファイル）も削除
                    elif item.is_file() and (".tmp" in item.name or ".part" in item.name or item.name.startswith("yt-dlp")):
                        try:
                            mtime = item.stat().st_mtime
                            age_seconds = now - mtime
                            
                            # 5分以上経過した一時ファイルを削除
                            if age_seconds > 300:
                                item.unlink()
                                print(f"🗑️ [JANITOR] 一時ファイル削除: {item.name}")
                        except Exception:
                            pass
            except Exception:
                pass
            
            gc.collect()
        except Exception:
            pass
        await asyncio.sleep(30)  # 30秒ごとにクリーンアップ（元は60秒）


def start_janitor():
    loop = ensure_loop()
    asyncio.run_coroutine_threadsafe(_janitor_loop(), loop)


def cancel_job(job_id: str) -> bool:
    j = jobs.get(job_id)
    if not j:
        return False
    j["cancel"] = True
    if j.get("status") == "queued":
        j["status"] = "canceled"
        _canceled_ids.add(job_id)
        try:
            _pending_ids.remove(job_id)
        except Exception:
            pass
    return True
