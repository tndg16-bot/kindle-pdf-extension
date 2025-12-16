import io
import os
import sys
import time
import math
import tempfile
import random
from pathlib import Path
from typing import Tuple, Callable, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import gc
import threading

# Windows環境での絵文字出力対応（cp932エラー回避）
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass  # 既に設定済みの場合はスキップ

from PIL import Image
import os as _os
# Render環境でのみPlaywrightパスを設定
if _os.environ.get("RENDER"):
    _os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/render/project/src/.playwright")
from playwright.sync_api import sync_playwright
import atexit
import ctypes

# Use the official google-genai client for Gemini 2.x OCR
try:
    from google import genai as genai_new  # type: ignore
    from google.genai import types as genai_types  # type: ignore
except Exception:  # pragma: no cover
    genai_new = None  # type: ignore
    genai_types = None  # type: ignore


# Concurrency limits (threading semaphores)
LP_CAPTURE_CONCURRENCY = int(os.getenv("LP_CAPTURE_CONCURRENCY", os.getenv("PLAYWRIGHT_CONCURRENCY", "1")))
GEMINI_OCR_CONCURRENCY = int(os.getenv("GEMINI_CONCURRENCY", "1"))
GEMINI_OCR_MAX_HEIGHT = int(os.getenv("GEMINI_OCR_MAX_HEIGHT", "32000"))
GEMINI_OCR_OVERLAP = int(os.getenv("GEMINI_OCR_OVERLAP", "200"))
GEMINI_OCR_PARALLEL = int(os.getenv("GEMINI_OCR_PARALLEL", "4"))
LP_FAST_CHUNK_HEIGHT = int(os.getenv("LP_FAST_CHUNK_HEIGHT", "5000"))
LP_FAST_PARALLEL = int(os.getenv("LP_FAST_PARALLEL", str(max(1, GEMINI_OCR_PARALLEL))))
_capture_sem = threading.Semaphore(LP_CAPTURE_CONCURRENCY)
_ocr_sem = threading.Semaphore(GEMINI_OCR_CONCURRENCY)

# 共有ブラウザ機能は削除（スレッドセーフでないため）

def _malloc_trim():
    """Linux の場合だけ malloc_trim() を呼び出してメモリを OS に返す"""
    try:
        if hasattr(ctypes, 'CDLL') and os.name == 'posix':
            libc = ctypes.CDLL("libc.so.6")
            libc.malloc_trim(0)
    except Exception:
        pass


class MemoryMonitor:
    def __init__(self):
        self.process = psutil.Process()
        self.logs = []
        self.start_memory = self.process.memory_info().rss / (1024 * 1024)

    def log_memory(self, label: str):
        current_memory = self.process.memory_info().rss / (1024 * 1024)
        diff = current_memory - self.start_memory
        self.logs.append(f"{label}: {current_memory:.1f}MB (+{diff:+.1f}MB)")

    def get_report(self) -> str:
        return "🧠 Memory Report:\n" + "\n".join(self.logs)


def _get_body_height(page) -> int:
    """Get the full height of the page content."""
    return page.evaluate("""() => {
        return Math.max(
            document.documentElement.scrollHeight,
            document.body.scrollHeight,
            document.documentElement.offsetHeight,
            document.body.offsetHeight,
            document.documentElement.clientHeight
        );
    }""")


def _get_viewport_height(page) -> int:
    """Get the current viewport height."""
    return page.evaluate("() => window.innerHeight")


def _staged_prerender_scroll(page, progress_cb=None, memory_monitor=None):
    """段階的プリレンダリング - 動的コンテンツを完全に展開"""
    viewport_height = _get_viewport_height(page)
    initial_height = _get_body_height(page)
    
    current_height = initial_height
    max_attempts = 15
    stable_count = 0
    
    for attempt in range(max_attempts):
        if progress_cb:
            progress_cb(0.15 + 0.05 * (attempt / max_attempts), 
                       f"段階的スクロール {attempt + 1}/{max_attempts}")
        
        # 現在の高さまでスクロール
        for pos in range(0, current_height, viewport_height // 2):
            page.evaluate(f"window.scrollTo(0, {pos});")
            time.sleep(0.3)
        
        # 最下部で待機
        page.evaluate(f"window.scrollTo(0, {current_height});")
        time.sleep(1.5)
        
        # 高さ再測定
        new_height = _get_body_height(page)
        
        if new_height <= current_height + 100:
            stable_count += 1
            if stable_count >= 2:
                break
        else:
            stable_count = 0
            current_height = new_height
    
    page.evaluate("window.scrollTo(0, 0);")
    time.sleep(1.0)
    return current_height


def _stitch_vertical(images, overlap: int = 0) -> Image.Image:
    """Stitch images vertically with overlap handling."""
    if not images:
        raise ValueError("No images to stitch")
    
    total_height = sum(img.height for img in images)
    if overlap > 0 and len(images) > 1:
        total_height -= overlap * (len(images) - 1)
    
    width = images[0].width
    out = Image.new("RGB", (width, total_height), color=(255, 255, 255))
    
    y = 0
    for i, im in enumerate(images):
        if i > 0 and overlap > 0:
            y -= overlap
        
        # Ensure we don't go beyond the output image bounds
        if y + im.height > total_height:
            crop_height = total_height - y
            if crop_height > 0:
                im = im.crop((0, 0, im.width, crop_height))
            else:
                break

        out.paste(im, (0, y))
        y += im.height
    return out


def capture_fullpage_tiled(
    url: str,
    out_png: Path,
    width: int = 640,
    tile_height: int = 2400,
    wait_after_load: float = 1.0,
    device_scale: float = 1.0,
    overlap: int = 200,
    pause_animations: bool = True,
    hide_fixed: bool = True,
    prerender_scroll: bool = True,
    goto_timeout_ms: int = 90_000,
    max_output_pixels: int = 100_000_000,
    progress_cb: Optional[Callable[[float, str], None]] = None,
) -> Tuple[Path, int]:
    
    # 🧠 メモリ監視開始
    memory_monitor = MemoryMonitor()
    memory_monitor.log_memory("🚀 処理開始")
    
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url

    # concurrency gate for capture
    _cap_acquired = _capture_sem.acquire(timeout=float(os.getenv("CAPTURE_SEMAPHORE_TIMEOUT_SEC", "300")))
    if not _cap_acquired:
        raise RuntimeError("現在サーバが混雑しています（capture同時実行の上限に達しました）")
    
    try:
        memory_monitor.log_memory("🌐 Playwright起動前")
        
        # 一時ディレクトリを明示的に作成（Chromiumキャッシュ用、処理後に削除）
        from .. import get_temp_dir
        browser_tmp_dir = get_temp_dir(prefix="moji_chromium_")
        
        # スレッドセーフな実装：各リクエストで新しいPlaywrightインスタンスを作成
        with sync_playwright() as p:
            browser = None
            try:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(browser_tmp_dir),
                    headless=True,
                    viewport={"width": int(width), "height": int(tile_height)},
                    device_scale_factor=float(device_scale),
                    extra_http_headers={'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8'},
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--disable-web-security",
                        "--disable-features=VizDisplayCompositor",
                        "--font-render-hinting=none",
                        "--disable-font-subpixel-positioning",
                        "--force-device-scale-factor=1",
                    ],
                )
                memory_monitor.log_memory("🔧 ブラウザ起動完了 (persistent)")
            except Exception as e:
                persistent_error = str(e)
                print(f"[WARN] launch_persistent_context failed: {persistent_error}")
                if "Executable doesn't exist" in persistent_error:
                    raise RuntimeError(
                        "Playwrightブラウザが見つかりません。\n"
                        "サーバー管理者にお問い合わせください。\n"
                        f"詳細: {persistent_error}\n"
                        f"PLAYWRIGHT_BROWSERS_PATH={_os.environ.get('PLAYWRIGHT_BROWSERS_PATH','<unset>')}"
                    )
                # Fallback to standard launch + new_context
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--disable-web-security",
                        "--disable-features=VizDisplayCompositor",
                        "--font-render-hinting=none",
                        "--disable-font-subpixel-positioning",
                        "--force-device-scale-factor=1",
                    ],
                )
                context = browser.new_context(
                    viewport={"width": int(width), "height": int(tile_height)},
                    device_scale_factor=float(device_scale),
                    extra_http_headers={'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8'},
                )
                memory_monitor.log_memory("🔧 ブラウザ起動完了 (fallback)")

            if context.pages:
                page = context.pages[0]
            else:
                page = context.new_page()
            page.set_default_navigation_timeout(int(goto_timeout_ms))
            memory_monitor.log_memory("📄 ページコンテキスト作成")

            if progress_cb:
                progress_cb(0.05, "ブラウザ起動")
            
            # Be tolerant on first load: wait for DOM, then optionally network idle
            page.goto(url, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=10_000)
            except Exception:
                pass
            time.sleep(wait_after_load)
            memory_monitor.log_memory("📥 ページ読み込み完了")
            
            if progress_cb:
                progress_cb(0.1, "ページ安定化")

            # Stabilize layout: pause animations and optionally hide fixed elements + 日本語フォント強制適用
            css_rules = []
            
            # 日本語フォント強制適用（文字化け対策）
            css_rules.append("""
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');
                * { 
                    font-family: 'Noto Sans JP', 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif !important; 
                    -webkit-font-smoothing: antialiased !important;
                    -moz-osx-font-smoothing: grayscale !important;
                }
            """)
            
            if pause_animations:
                css_rules.append("* { animation: none !important; transition: none !important; }")
            if hide_fixed:
                css_rules.append("* { scroll-behavior: auto !important; } .fixed, [style*='position: fixed'] { visibility: hidden !important; }")
            
            combined_css = " ".join(css_rules)
            page.add_style_tag(content=combined_css)
            time.sleep(1.0)  # フォント読み込みのため少し長めに待機

            # 段階的プリレンダリング（新実装）
            if prerender_scroll:
                body_height = _staged_prerender_scroll(page, progress_cb, memory_monitor)
            else:
                body_height = _get_body_height(page)
                memory_monitor.log_memory(f"📏 標準測定: {body_height}px")

            # Get viewport height for tiling
            viewport_height = _get_viewport_height(page)
            
            # Calculate output dimensions with pixel limit
            out_w = width
            out_h = min(body_height, max_output_pixels // out_w)
            
            if out_h < body_height:
                memory_monitor.log_memory(f"⚠️ ピクセル制限により高さを {body_height} -> {out_h} に制限")
            
            memory_monitor.log_memory(f"📏 出力サイズ: {out_w}x{out_h} (元: {width}x{body_height})")

            if progress_cb:
                progress_cb(0.2, f"スクリーンショット開始 ({out_w}x{out_h})")

            # Calculate tiling parameters
            step = max(1, tile_height - overlap)
            last_start = max(0, out_h - tile_height)
            
            # Create output canvas
            canvas = Image.new("RGB", (out_w, out_h), color=(255, 255, 255))
            memory_monitor.log_memory("🖼️ キャンバス作成")

            # Capture tiles
            i = 0
            prev_y = -1
            est_last_start = max(0, int(out_h - tile_height))
            est_tiles = max(1, int((est_last_start // step) + 1))
            pasted_tiles = 0
            
            while True:
                y = min(i * step, last_start)
                if prev_y == y:
                    break
                if y >= out_h:
                    break

                page.evaluate(f"window.scrollTo(0, {int(y)});")
                time.sleep(0.15)
                
                # 📸 5タイルごとにメモリをログ
                if pasted_tiles % 5 == 0:
                    memory_monitor.log_memory(f"📸 タイル{pasted_tiles}撮影前")
                
                buf = page.screenshot(full_page=False)
                img = Image.open(io.BytesIO(buf)).convert("RGB")

                # 下端がはみ出す場合は切り詰め
                if y + img.height > out_h:
                    crop_h = max(0, out_h - y)
                    if crop_h <= 0:
                        break
                    img = img.crop((0, 0, img.width, crop_h))

                canvas.paste(img, (0, y))
                # 画像バッファを直ちに解放してピークRSSを抑制
                try:
                    img.close()
                except Exception:
                    pass
                del img, buf
                pasted_tiles += 1

                if progress_cb and est_tiles > 0:
                    progress = 0.2 + 0.7 * (pasted_tiles / est_tiles)
                    progress_cb(progress, f"タイル {pasted_tiles}/{est_tiles}")

                prev_y = y
                i += 1

            memory_monitor.log_memory("📸 全タイル処理完了")

            # 画像保存
            canvas.save(out_png)
            memory_monitor.log_memory("💾 画像保存完了")
            
            # リソース解放
            canvas.close()  # PIL画像を明示的にclose（Cバッファ解放）
            del canvas
            page.close()
            context.close()
            if browser is not None:
                browser.close()
        
        # withブロックを抜けた後にクリーンアップとGC実行
        # （Playwrightのリソースが確実に解放される）
        
        # Chromiumキャッシュディレクトリを削除
        try:
            import shutil
            if browser_tmp_dir.exists():
                shutil.rmtree(browser_tmp_dir)
                print(f"🗑️ [CLEANUP] Chromiumキャッシュ削除: {browser_tmp_dir.name}")
        except Exception as e:
            print(f"⚠️ [CLEANUP] Chromiumキャッシュ削除エラー: {e}")
        
        # 強制的なメモリ解放（Playwrightスコープ外で実行）
        gc.collect()
        memory_monitor.log_memory("🧹 第1回GC後")
        
        # さらに強制解放
        time.sleep(0.1)  # 少し待つ
        gc.collect()
        memory_monitor.log_memory("🧹 第2回GC後")
        
        # 最終確認
        time.sleep(0.2)
        gc.collect()
        _malloc_trim()
        memory_monitor.log_memory("🧹 最終リソース解放後")
        
        # メモリレポートを出力
        print(memory_monitor.get_report())
        
        # 注意: ファイルクリーンナップはOCR完了後に実行
        return out_png, pasted_tiles
            
    except Exception as e:
        memory_monitor.log_memory("💥 エラー発生時")
        print(memory_monitor.get_report())
        # エラー時はクリーンナップしない（OCRでファイルが必要なため）
        if progress_cb:
            progress_cb(0, f"エラー: {str(e)}")
        raise RuntimeError(f"スクリーンショットの取得に失敗しました: {str(e)}")
    finally:
        if _cap_acquired:
            _capture_sem.release()


def gemini_ocr_image(image_path: Path, api_key: str, model: str = "gemini-2.5-flash", log_fn: Optional[Callable[[str], None]] = None) -> str:
    # retry/backoff settings
    max_retries = 3
    base_delay = 1.0
    max_delay = 16.0
    
    # Acquire OCR semaphore
    acquired = _ocr_sem.acquire(timeout=float(os.getenv("OCR_SEMAPHORE_TIMEOUT_SEC", "300")))
    if not acquired:
        raise RuntimeError("OCR処理が混雑しています。しばらく待ってから再試行してください。")
    
    try:
        for attempt in range(max_retries):
            try:
                return _gemini_ocr_attempt(image_path, api_key, model, log_fn=log_fn)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                
                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                print(f"OCR attempt {attempt + 1} failed, retrying in {delay:.1f}s: {e}")
                time.sleep(delay)
        
        raise RuntimeError("Max retries exceeded")
    finally:
        _ocr_sem.release()


def _gemini_ocr_attempt(image_path: Path, api_key: str, model: str, log_fn: Optional[Callable[[str], None]] = None) -> str:
    """Single OCR attempt with the specified model."""

    if not genai_new:
        raise RuntimeError("google-genai クライアントが利用できません。'google-genai' パッケージをインストールしてください。")

    if not genai_types:
        raise RuntimeError("google-genai types を読み込めません。パッケージを確認してください。")

    suffix = image_path.suffix.lower()
    if suffix in [".jpg", ".jpeg"]:
        mime_type = "image/jpeg"
    elif suffix == ".png":
        mime_type = "image/png"
    elif suffix == ".webp":
        mime_type = "image/webp"
    else:
        mime_type = "image/png"

    segments, total_height = _split_image_with_overlap(image_path, max_height=GEMINI_OCR_MAX_HEIGHT, overlap=GEMINI_OCR_OVERLAP)

    if log_fn:
        if len(segments) > 1:
            log_fn(
                f"📐 高さ{total_height}px のスクショを {len(segments)} 分割（オーバーラップ {GEMINI_OCR_OVERLAP}px）で処理します。"
            )
        else:
            log_fn(f"📐 高さ{total_height}px のスクショを1回で処理します。")

    results: List[str] = []
    for idx, segment in enumerate(segments, start=1):
        seg_bytes = segment["bytes"]
        if len(seg_bytes) > 20 * 1024 * 1024:
            raise RuntimeError("分割後の画像サイズが大きすぎます（20MB超）。縮小または分割を調整してください。")
        if log_fn and len(segments) > 1:
            log_fn(
                f"🧠 チャンク {idx}/{len(segments)} (y={segment['start']}〜{segment['end']}px) をOCR中…"
            )
        text = _gemini_ocr_new_client(seg_bytes, mime_type, api_key, model)
        results.append(text.strip())

    return _merge_segment_texts(results)


def _gemini_ocr_new_client(image_bytes: bytes, mime_type: str, api_key: str, model: str) -> str:
    """OCR using the new google-genai client (Gemini 2.x)."""
    if not genai_types:
        raise RuntimeError("google-genai types を読み込めません。パッケージを確認してください。")

    client = genai_new.Client(api_key=api_key)

    image_part = genai_types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    response = client.models.generate_content(
        model=model,
        contents=[
            "Please transcribe all visible text in the image. Output only the raw transcribed text, no commentary.",
            image_part,
        ],
    )

    text = response.text or ""
    if not text and response.candidates:
        parts = response.candidates[0].content.parts
        texts: List[str] = []
        for part in parts:
            part_text = getattr(part, "text", None)
            if part_text:
                texts.append(part_text)
        text = "\n".join(texts)
    return text or ""


def _merge_segment_texts(texts: List[str]) -> str:
    merged: List[str] = []
    for text in texts:
        if not text:
            continue
        for line in text.splitlines():
            line = line.rstrip()
            stripped = line.strip()
            if not stripped:
                if merged and merged[-1] != "":
                    merged.append("")
                continue
            if merged and merged[-1].strip() == stripped:
                continue
            merged.append(line)
        if merged and merged[-1] != "":
            merged.append("")
    if merged and merged[-1] == "":
        merged.pop()
    return "\n".join(merged)


def gemini_ocr_image_parallel(
    image_path: Path,
    api_key: str,
    model: str = "gemini-2.5-flash",
    chunk_height: int = LP_FAST_CHUNK_HEIGHT,
    overlap: int = GEMINI_OCR_OVERLAP,
    parallel_workers: Optional[int] = None,
    log_fn: Optional[Callable[[str], None]] = None,
) -> str:
    parallel_workers = parallel_workers or LP_FAST_PARALLEL
    acquired = _ocr_sem.acquire(timeout=float(os.getenv("OCR_SEMAPHORE_TIMEOUT_SEC", "300")))
    if not acquired:
        raise RuntimeError("OCR処理が混雑しています。しばらく待ってから再試行してください。")
    try:
        return _gemini_ocr_parallel(
            image_path,
            api_key,
            model,
            chunk_height=chunk_height,
            overlap=overlap,
            parallel_workers=parallel_workers,
            log_fn=log_fn,
        )
    finally:
        _ocr_sem.release()


def _gemini_ocr_parallel(
    image_path: Path,
    api_key: str,
    model: str,
    chunk_height: int,
    overlap: int,
    parallel_workers: int,
    log_fn: Optional[Callable[[str], None]] = None,
) -> str:
    if not genai_new or not genai_types:
        raise RuntimeError("google-genai クライアントが利用できません。パッケージを確認してください。")

    suffix = image_path.suffix.lower()
    if suffix in [".jpg", ".jpeg"]:
        mime_type = "image/jpeg"
    elif suffix == ".png":
        mime_type = "image/png"
    elif suffix == ".webp":
        mime_type = "image/webp"
    else:
        mime_type = "image/png"

    segments, total_height = _split_image_with_overlap(image_path, max_height=chunk_height, overlap=overlap)
    if not segments:
        return ""

    if log_fn:
        desc = "並列" if len(segments) > 1 else "単一"
        log_fn(
            f"⚡ {desc}OCRモード: 高さ{total_height}px を最大{min(len(segments), parallel_workers)}並列で処理します。"
        )

    workers = max(1, min(parallel_workers, len(segments)))
    results: List[str] = [""] * len(segments)

    def worker(idx: int, seg: dict) -> str:
        seg_bytes = seg["bytes"]
        text = _gemini_ocr_new_client(seg_bytes, mime_type, api_key, model) or ""
        return text.strip()

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(worker, idx, seg): (idx, seg)
            for idx, seg in enumerate(segments)
        }
        for future in as_completed(future_map):
            idx, seg = future_map[future]
            try:
                results[idx] = future.result()
                if log_fn and len(segments) > 1:
                    log_fn(
                        f"✅ チャンク {idx + 1}/{len(segments)} 完了 (y={seg['start']}〜{seg['end']}px)"
                    )
            except Exception as exc:
                if log_fn:
                    log_fn(
                        f"⚠️ チャンク {idx + 1}/{len(segments)} でエラー: {exc}"
                    )
                results[idx] = ""

    return _merge_segment_texts(results)

def lp_capture_and_ocr(
    url: str,
    gemini_api_key: str,
    model: str = "gemini-2.5-flash",
    width: int = 640,
    tile_height: int = 2400,
    device_scale: float = 1.0,
    overlap: int = 200,
    pause_animations: bool = True,
    hide_fixed: bool = True,
    prerender_scroll: bool = True,
    goto_timeout_ms: int = 90_000,
    max_output_pixels: int = 100_000_000,
    progress_cb: Optional[Callable[[float, str], None]] = None,
) -> Tuple[str, str, str, int]:
    """Convenience wrapper to capture a full LP screenshot and run Gemini OCR.

    Returns tuple of (png_path, text, txt_path, tiles_count).
    """
    from .. import get_temp_dir
    tmpdir = get_temp_dir(prefix="moji_lp_")
    png_path = tmpdir / "lp_screenshot.png"
    txt_path = tmpdir / "lp_text_gemini.txt"

    out_png, tiles_count = capture_fullpage_tiled(
        url=url,
        out_png=png_path,
        width=width,
        tile_height=tile_height,
        device_scale=device_scale,
        overlap=overlap,
        pause_animations=pause_animations,
        hide_fixed=hide_fixed,
        prerender_scroll=prerender_scroll,
        goto_timeout_ms=goto_timeout_ms,
        max_output_pixels=max_output_pixels,
        progress_cb=progress_cb,
    )

    if progress_cb:
        progress_cb(0.85, "OCR実行中(Gemini)")

    text = gemini_ocr_image(out_png, api_key=gemini_api_key, model=model)

    if progress_cb:
        progress_cb(1.0, "完了")

    txt_path.write_text(text, encoding="utf-8")
    return str(out_png), text, str(txt_path), tiles_count
def _split_image_with_overlap(image_path: Path, max_height: int, overlap: int) -> Tuple[List[dict], int]:
    """Split tall image into overlapping segments and return metadata."""
    img = Image.open(image_path).convert("RGB")
    height = img.height
    segments: List[dict] = []
    base_top = 0
    idx = 0

    while base_top < height:
        slice_bottom = min(base_top + max_height, height)
        slice_top = base_top if idx == 0 else max(0, base_top - overlap)
        crop = img.crop((0, slice_top, img.width, slice_bottom))
        buf = io.BytesIO()
        crop.save(buf, format="PNG")
        segments.append({
            "bytes": buf.getvalue(),
            "start": slice_top,
            "end": slice_bottom,
            "height": crop.height,
        })
        if slice_bottom >= height:
            break
        base_top = slice_bottom
        idx += 1

    return segments, height
