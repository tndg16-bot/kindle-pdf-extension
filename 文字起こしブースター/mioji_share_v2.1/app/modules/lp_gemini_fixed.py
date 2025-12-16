import io
import os
import sys
import time
import math
import base64
import tempfile
import random
from pathlib import Path
from typing import Tuple, Callable, Optional
import psutil
import gc
import threading

from PIL import Image
import os as _os
# Render環境でのみPlaywrightパスを設定
if _os.environ.get("RENDER"):
    _os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/render/project/src/.playwright")
from playwright.sync_api import sync_playwright
import atexit
import ctypes

# We'll try the new google-genai client first (supports Gemini 2.x),
# then fall back to google-generativeai for older models.
try:
    from google import genai as genai_new  # type: ignore
except Exception:  # pragma: no cover
    genai_new = None
try:
    import google.generativeai as genai_old  # type: ignore
except Exception:  # pragma: no cover
    genai_old = None


# Concurrency limits (threading semaphores)
LP_CAPTURE_CONCURRENCY = int(os.getenv("LP_CAPTURE_CONCURRENCY", os.getenv("PLAYWRIGHT_CONCURRENCY", "1")))
GEMINI_OCR_CONCURRENCY = int(os.getenv("GEMINI_CONCURRENCY", "1"))
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
    width: int = 1280,
    tile_height: int = 2400,
    wait_after_load: float = 1.0,
    device_scale: float = 1.0,
    overlap: int = 200,
    pause_animations: bool = True,
    hide_fixed: bool = True,
    prerender_scroll: bool = True,
    goto_timeout_ms: int = 90_000,
    max_output_pixels: int = 40_000_000,
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
        
        # スレッドセーフな実装：各リクエストで新しいPlaywrightインスタンスを作成
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True, args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-web-security",
                    "--disable-features=VizDisplayCompositor",
                ])
                memory_monitor.log_memory("🔧 ブラウザ起動完了")
            except Exception as e:
                if "Executable doesn't exist" in str(e):
                    raise RuntimeError(
                        "Playwrightブラウザが見つかりません。\n"
                        "サーバー管理者にお問い合わせください。\n"
                        f"詳細: {str(e)}\n"
                        f"PLAYWRIGHT_BROWSERS_PATH={_os.environ.get('PLAYWRIGHT_BROWSERS_PATH','<unset>')}"
                    )
                else:
                    raise RuntimeError(f"ブラウザの起動に失敗しました: {str(e)}")

            context = browser.new_context(
                viewport={"width": int(width), "height": int(tile_height)},
                device_scale_factor=float(device_scale),
            )
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

            # Stabilize layout: pause animations and optionally hide fixed elements
            if pause_animations or hide_fixed:
                css_rules = []
                if pause_animations:
                    css_rules.append("* { animation: none !important; transition: none !important; }")
                if hide_fixed:
                    css_rules.append("* { scroll-behavior: auto !important; } .fixed, [style*='position: fixed'] { visibility: hidden !important; }")
                
                combined_css = " ".join(css_rules)
                page.add_style_tag(content=combined_css)
                time.sleep(0.5)  # Let CSS take effect

            # Pre-render scroll if enabled
            if prerender_scroll:
                if progress_cb:
                    progress_cb(0.15, "プリレンダリング")
                body_height = _get_body_height(page)
                viewport_height = _get_viewport_height(page)
                scroll_steps = max(1, body_height // viewport_height)
                for i in range(scroll_steps):
                    y = (i * body_height) // scroll_steps
                    page.evaluate(f"window.scrollTo(0, {y});")
                    time.sleep(0.1)
                page.evaluate("window.scrollTo(0, 0);")
                time.sleep(0.5)
                memory_monitor.log_memory("🎬 プリレンダリング完了")

            # Get actual page dimensions
            body_height = _get_body_height(page)
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
            del canvas
            page.close()
            context.close()
            browser.close()  # ブラウザを明示的にクローズ
            
            # 強制的なメモリ解放
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


def gemini_ocr_image(image_path: Path, api_key: str, model: str = "gemini-2.5-flash") -> str:
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
                return _gemini_ocr_attempt(image_path, api_key, model)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                
                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                print(f"OCR attempt {attempt + 1} failed, retrying in {delay:.1f}s: {e}")
                time.sleep(delay)
        
        raise RuntimeError("Max retries exceeded")
    finally:
        _ocr_sem.release()


def _gemini_ocr_attempt(image_path: Path, api_key: str, model: str) -> str:
    """Single OCR attempt with the specified model."""
    
    # Read and encode image
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    image_b64 = base64.b64encode(image_data).decode("utf-8")
    
    # Determine MIME type
    suffix = image_path.suffix.lower()
    if suffix in [".jpg", ".jpeg"]:
        mime_type = "image/jpeg"
    elif suffix == ".png":
        mime_type = "image/png"
    elif suffix == ".webp":
        mime_type = "image/webp"
    else:
        mime_type = "image/png"  # fallback
    
    # Try new google-genai client first (supports Gemini 2.x)
    if genai_new and model.startswith("gemini-2"):
        try:
            return _gemini_ocr_new_client(image_b64, mime_type, api_key, model)
        except Exception as e:
            print(f"New client failed, falling back to old client: {e}")
    
    # Fall back to google-generativeai
    if genai_old:
        return _gemini_ocr_old_client(image_b64, mime_type, api_key, model)
    
    raise RuntimeError("No Gemini client available")


def _gemini_ocr_new_client(image_b64: str, mime_type: str, api_key: str, model: str) -> str:
    """OCR using the new google-genai client."""
    client = genai_new.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model=model,
        contents=[
            {
                "parts": [
                    {"text": "この画像に含まれるテキストをすべて抽出してください。レイアウトや構造を保持して、読みやすい形で出力してください。"},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_b64
                        }
                    }
                ]
            }
        ]
    )
    
    if not response.candidates or not response.candidates[0].content.parts:
        raise RuntimeError("Gemini API returned empty response")
    
    return response.candidates[0].content.parts[0].text


def _gemini_ocr_old_client(image_b64: str, mime_type: str, api_key: str, model: str) -> str:
    """OCR using the old google-generativeai client."""
    genai_old.configure(api_key=api_key)
    
    # Map model names for old client
    if model.startswith("gemini-2"):
        model = "gemini-1.5-flash"  # fallback for old client
    
    model_instance = genai_old.GenerativeModel(model)
    
    image_part = {
        "mime_type": mime_type,
        "data": base64.b64decode(image_b64)
    }
    
    prompt = "この画像に含まれるテキストをすべて抽出してください。レイアウトや構造を保持して、読みやすい形で出力してください。"
    
    response = model_instance.generate_content([prompt, image_part])
    
    if not response.text:
        raise RuntimeError("Gemini API returned empty text")
    
    return response.text
