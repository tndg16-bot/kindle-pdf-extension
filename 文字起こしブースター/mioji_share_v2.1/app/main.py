import os
import sys
import tempfile
from pathlib import Path
from queue import SimpleQueue
import json
import threading
import time as _time
import psutil

# Windows環境での絵文字出力対応（cp932エラー回避）
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import gradio as gr
from gradio.themes import Soft
import subprocess

from .modules.lp_gemini import capture_fullpage_tiled, gemini_ocr_image, gemini_ocr_image_parallel
from .modules.groq_transcribe import transcribe_file_with_groq
from .modules.hls_extractor import extract_audio_from_hls
from .job_manager import start_workers, start_janitor


def _resolve_gemini_key(session_val: str, inline_val: str | None = None) -> str:
    """Prefer inline textbox value, otherwise fall back to session textbox."""
    t = (inline_val or "").strip() if inline_val is not None else ""
    if t:
        return t
    return (session_val or "").strip()


def _check_screenshot_quality(png_path: str, width: int) -> dict:
    """スクショの品質をチェック（見切れ検出）
    
    Returns:
        {
            "has_issues": bool,
            "warnings": list[str],
            "suggestions": list[str]
        }
    """
    from PIL import Image
    import io
    
    try:
        img = Image.open(png_path)
        img_width, img_height = img.size
        
        warnings = []
        suggestions = []
        
        # 1. 横スクロールバーの検出（下端をチェック）
        bottom_region = img.crop((0, max(0, img_height - 50), img_width, img_height))
        # 下端50pxの平均明度をチェック（スクロールバーは暗い）
        bottom_gray = bottom_region.convert('L')
        pixels = list(bottom_gray.getdata())
        avg_brightness = sum(pixels) / len(pixels)
        
        # 明度が低い＋細長い領域がある場合は横スクロールの可能性
        if avg_brightness < 200 and img_width < 1000:
            warnings.append("⚠️ 横スクロールバーが検出された可能性があります")
            suggestions.append("💡 画面幅を1280px以上に変更することをお勧めします")
        
        # 2. 画面幅が小さすぎる場合
        if width < 1000:
            warnings.append(f"⚠️ 画面幅が小さい ({width}px) - 見切れの可能性")
            suggestions.append("💡 推奨画面幅: 1280px以上")
        
        # 3. 画像が異常に高い場合（無限スクロール等）
        if img_height > 50000:
            warnings.append(f"⚠️ スクショが非常に長い ({img_height}px)")
            suggestions.append("💡 ページが無限スクロールの場合、適切に撮影できていない可能性があります")
        
        has_issues = len(warnings) > 0
        
        return {
            "has_issues": has_issues,
            "warnings": warnings,
            "suggestions": suggestions,
            "width": img_width,
            "height": img_height
        }
    except Exception as e:
        print(f"[DEBUG] スクショ品質チェックエラー: {e}")
        return {
            "has_issues": False,
            "warnings": [],
            "suggestions": [],
            "width": 0,
            "height": 0
        }


def _resolve_groq_key(session_val: str, inline_val: str | None = None) -> str:
    """Prefer inline textbox value, otherwise fall back to session textbox."""
    t = (inline_val or "").strip() if inline_val is not None else ""
    if t:
        return t
    return (session_val or "").strip()


APP_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');
* { font-family: 'Noto Sans JP', 'Noto Sans', sans-serif !important; }
.header { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; border-radius:10px; background:linear-gradient(90deg,#0ea5e9,#6366f1); color:#fff; box-shadow:0 4px 16px rgba(0,0,0,.08); }
.title { font-size:20px; font-weight:700; letter-spacing:.2px; }
.badges { display:flex; gap:8px; flex-wrap:wrap; }
.badge { padding:4px 8px; border-radius:999px; font-size:12px; background:rgba(255,255,255,.15); backdrop-filter:blur(4px); }
.ok { background:rgba(16,185,129,.25); }
.warn { background:rgba(245,158,11,.25); }
.file-upload-area { 
    border: 3px dashed #667eea !important; 
    border-radius: 15px !important; 
    background: linear-gradient(135deg, rgba(102,126,234,0.05), rgba(118,75,162,0.05)) !important;
    transition: all 0.3s ease !important;
}
.file-upload-area:hover {
    border-color: #764ba2 !important;
    background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1)) !important;
}
.card { border:1px solid #e5e7eb; border-radius:12px; padding:14px; background:#fff; box-shadow:0 2px 10px rgba(0,0,0,.03); }
.section-title { font-weight:700; margin:4px 0 6px; font-size:16px; }
.status-large { font-size:18px; font-weight:700; color:#374151; }
#screenshot_card { overflow: visible !important; }
#screenshot_card img, #screenshot_card canvas { display: block; max-width: 100% !important; height: auto !important; }
#screenshot_card [data-testid="loader"], #screenshot_card [data-testid="block-progress"], #screenshot_card .loading { display: none !important; }
.
.prog-wrap { display:flex; align-items:center; gap:10px; }
.prog { flex:1; background:#e5e7eb; height:10px; border-radius:8px; overflow:hidden; }
.prog > span { display:block; height:100%; width:0%; background:#6366f1; transition: width .2s ease; }
.prog-text { min-width:110px; font-size:12px; color:#374151; }
.copy-btn { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white !important; 
    border: none; 
    padding: 8px 16px; 
    border-radius: 6px; 
    cursor: pointer; 
    font-size: 12px; 
    margin: 8px 0;
    transition: all 0.3s ease;
    font-family: 'Noto Sans JP', sans-serif !important;
}
.copy-btn:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 4px 12px rgba(102,126,234,0.4); 
}
.copy-btn:active { 
    transform: translateY(0px); 
}
"""


def _is_cmd_available(cmd: str) -> bool:
    try:
        subprocess.run([cmd, "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        return True
    except Exception:
        return False


def _start_metrics_logger():
    """Log RSS and load average periodically to stdout."""
    try:
        interval = int(os.environ.get("METRICS_INTERVAL_SEC", "30"))
    except Exception:
        interval = 30
    proc = psutil.Process()

    def _loop():
        while True:
            try:
                rss = proc.memory_info().rss
                try:
                    la1 = os.getloadavg()[0]
                except Exception:
                    la1 = 0.0
                # include queue stats and outcome counters if available
                try:
                    from .job_manager import get_queue_stats as _gqs
                    qs = _gqs()
                    qlen = qs.get("queue_len", -1)
                    running = qs.get("running", 0)
                    done = qs.get("done", 0)
                    failed = qs.get("failed", 0)
                    r429 = qs.get("r429", 0)
                    fail_rate = (failed / max(1, done + failed)) * 100.0
                    print(f"metrics rss_mb={rss/1024/1024:.1f} load1={la1:.2f} queue_len={qlen} running={running} done={done} failed={failed} r429={r429} fail_rate={fail_rate:.1f}%")
                except Exception:
                    print(f"metrics rss_mb={rss/1024/1024:.1f} load1={la1:.2f}")
            except Exception:
                pass
            _time.sleep(max(2, interval))

    threading.Thread(target=_loop, daemon=True).start()


def _status_badges_html() -> str:
    # 初期表示はセッション未確定のため、キーは未設定扱いにする
    groq = False
    gem = False
    ffm = _is_cmd_available("ffmpeg")
    
    # Playwrightの状態チェック
    pw_disabled = bool(os.environ.get("DISABLE_PLAYWRIGHT", "false").lower() == "true")
    if pw_disabled:
        pw = False
    else:
        try:
            # Playwright import可否
            from playwright.sync_api import sync_playwright  # type: ignore
            # ローカル環境向けの起動フラグで検証
            with sync_playwright() as p:
                try:
                    b = p.chromium.launch(headless=True)
                    b.close()
                    pw = True
                except Exception as e:
                    print(f"[DEBUG] Playwright browser launch failed: {e}")
                    pw = False
        except Exception as e:
            print(f"[DEBUG] Playwright import failed: {e}")
            pw = False
    def b(label, ok):
        cls = "badge ok" if ok else "badge warn"
        return f"<span class=\"{cls}\">{label}: {'OK' if ok else '未設定'}</span>"
    return f"<div class=\"badges\">{b('GROQ', groq)}{b('Gemini', gem)}{b('ffmpeg', ffm)}{b('Playwright', pw)}</div>"


def make_app():
    # NOTE: All components must be created inside the Blocks context.
    # Creating components (even hidden ones) outside can cause KeyError in Gradio's state map on some versions.
    import json as _json  # local for parsing

    theme = Soft(primary_hue="indigo", secondary_hue="blue", neutral_hue="gray")
    with gr.Blocks(title="Moji Booster (Local)", theme=theme, css=APP_CSS) as demo:
        # Hidden session fields (avoid gr.State due to instability on some versions)
        state_groq = gr.Textbox(value="", visible=False)
        state_gemini = gr.Textbox(value="", visible=False)
        with gr.Row():
            gr.HTML("<div class='header'><div class='title'>🧰 Moji Booster — ローカル配布版</div></div>")
            status_html = gr.HTML(_status_badges_html())

        with gr.Accordion("APIキー設定", open=True, elem_classes=["card"]):
            with gr.Row():
                with gr.Column():
                    groq_key = gr.Textbox(
                        label="GROQ_API_KEY",
                        type="password",
                        placeholder="gsk_... (GroqのAPIキー)",
                    )
                    gr.Markdown("🔗 GroqのAPIキー取得はこちら ➝ [https://console.groq.com/keys](https://console.groq.com/keys)")
                with gr.Column():
                    gemini_key = gr.Textbox(
                        label="GEMINI_API_KEY / GOOGLE_API_KEY",
                        type="password",
                        placeholder="AI StudioのAPIキー",
                    )
                    gr.Markdown("🔗 Gemini / Google AI StudioのAPIキー発行はこちら ➝ [https://aistudio.google.com/](https://aistudio.google.com/)")
            with gr.Row():
                save_btn = gr.Button("キーを保存 (このセッションのみ)", variant="primary")
                clear_btn = gr.Button("全キーをクリア", variant="secondary")
                check_btn = gr.Button("🔎 現在のキー表示", variant="secondary")
            out_info = gr.Markdown("未保存")
            gr.Markdown("💡 **ヒント**: 片方のキーだけを入力して保存すると、既存の他方のキーはそのまま保持されます。")

        # 入力欄に値が入った時点でセッション状態にも反映（保存ボタンを押し忘れても拾えるように）
        def _echo_merge_groq(new_val, prev_val):
            s = (new_val or "").strip()
            return prev_val if not s else s
        def _echo_merge_gemini(new_val, prev_val):
            s = (new_val or "").strip()
            return prev_val if not s else s
        groq_key.change(fn=_echo_merge_groq, inputs=[groq_key, state_groq], outputs=[state_groq])
        gemini_key.change(fn=_echo_merge_gemini, inputs=[gemini_key, state_gemini], outputs=[state_gemini])

        def save_keys(groq, gemini, state_groq_val, state_gemini_val):
            """Save keys only inside this browser session."""
            new_groq = (state_groq_val or "").strip()
            new_gemini = (state_gemini_val or "").strip()

            if isinstance(groq, str) and groq.strip():
                new_groq = groq.strip()
            if isinstance(gemini, str) and gemini.strip():
                new_gemini = gemini.strip()

            def mask(k) -> str:
                s = (k or "")
                if not isinstance(s, str):
                    s = str(s)
                s = s.strip()
                if not s:
                    return "(未設定)"
                return f"****{s[-4:]} （{len(s)}桁）"
            message = (
                "✅ セッションにキーを保存しました\n\n"
                f"- Gemini: {mask(new_gemini)}\n"
                f"- Groq: {mask(new_groq)}\n\n"
                "この保存はこのブラウザのこのセッションのみ有効です。"
            )
            
            # セッション別ステータスバッジを作成
            def session_status_badges_html(groq_key, gemini_key):
                # Show effective availability (session value or env fallback)
                groq_ok = bool(_resolve_groq_key(groq_key))
                gemini_ok = bool(_resolve_gemini_key(gemini_key))
                ffm = _is_cmd_available("ffmpeg")
                pw = not os.environ.get("DISABLE_PLAYWRIGHT", "false").lower() == "true"
                
                def b(label, ok):
                    color = "#10b981" if ok else "#ef4444"
                    return f"<span style='background:{color};color:white;padding:4px 8px;border-radius:12px;font-size:12px;margin-right:8px;'>{label}: {'OK' if ok else 'NG'}</span>"
                
                return f"<div class=\"badges\">{b('GROQ', groq_ok)}{b('Gemini', gemini_ok)}{b('ffmpeg', ffm)}{b('Playwright', pw)}</div>"
            
            return (new_groq or ""), (new_gemini or ""), message, session_status_badges_html(new_groq, new_gemini)

        def clear_keys():
            # セッションのキーをクリア（他のユーザーに影響しない）
            def session_status_badges_html_empty():
                ffm = _is_cmd_available("ffmpeg")
                pw = not os.environ.get("DISABLE_PLAYWRIGHT", "false").lower() == "true"
                
                def b(label, ok):
                    color = "#10b981" if ok else "#ef4444"
                    return f"<span style='background:{color};color:white;padding:4px 8px;border-radius:12px;font-size:12px;margin-right:8px;'>{label}: {'OK' if ok else 'NG'}</span>"
                
                return f"<div class=\"badges\">{b('GROQ', False)}{b('Gemini', False)}{b('ffmpeg', ffm)}{b('Playwright', pw)}</div>"
            
            return "", "", "", "", "🗑️ 全てのキーをクリアしました（このセッションのみ）", session_status_badges_html_empty()

        save_btn.click(
            fn=save_keys,
            inputs=[groq_key, gemini_key, state_groq, state_gemini],
            outputs=[state_groq, state_gemini, out_info, status_html],
        )
        
        clear_btn.click(
            fn=clear_keys,
            inputs=[],
            outputs=[state_groq, state_gemini, groq_key, gemini_key, out_info, status_html],
        )

        def show_keys(state_groq_val, state_gemini_val, ui_groq, ui_gemini):
            def mask(k) -> str:
                s = (k or "")
                if not isinstance(s, str):
                    s = str(s)
                s = s.strip()
                if not s:
                    return "(未設定)"
                return f"****{s[-4:]} （{len(s)}桁）"
            eff_gem = _resolve_gemini_key(state_gemini_val, ui_gemini)
            eff_groq = _resolve_groq_key(state_groq_val, ui_groq)
            msg = (
                "🔎 キー状態（このセッション内）\n\n"
                f"- Gemini(Session): {mask(state_gemini_val)}\n"
                f"- Gemini(InputBox): {mask(ui_gemini)}\n"
                f"- Gemini(Effective): {mask(eff_gem)}\n"
                f"- Groq(Session): {mask(state_groq_val)}\n"
                f"- Groq(InputBox): {mask(ui_groq)}\n"
                f"- Groq(Effective): {mask(eff_groq)}"
            )
            # バッジは Effective で更新
            ffm = _is_cmd_available("ffmpeg")
            pw = not os.environ.get("DISABLE_PLAYWRIGHT", "false").lower() == "true"
            def b(label, ok):
                color = "#10b981" if ok else "#ef4444"
                return f"<span style='background:{color};color:white;padding:4px 8px;border-radius:12px;font-size:12px;margin-right:8px;'>{label}: {'OK' if ok else 'NG'}</span>"
            badges = f"<div class=\"badges\">{b('GROQ', bool(eff_groq))}{b('Gemini', bool(eff_gem))}{b('ffmpeg', ffm)}{b('Playwright', pw)}</div>"
            return msg, badges

        check_btn.click(
            fn=show_keys,
            inputs=[state_groq, state_gemini, groq_key, gemini_key],
            outputs=[out_info, status_html],
        )

        def _run_groq_transcription(
            file,
            model,
            chunk_sec,
            workers,
            state_groq_val,
            ui_groq_key,
            progress=gr.Progress(track_tqdm=True),
        ):
            """Common Groq transcription runner used across audio/video tabs."""
            api_key = _resolve_groq_key(state_groq_val, ui_groq_key)
            print(
                "[DEBUG] run_transcription",
                {
                    "state_key": bool(state_groq_val),
                    "ui_key": bool(ui_groq_key),
                    "effective_key": bool(api_key),
                },
            )
            if not api_key:
                raise gr.Error("GroqのAPIキーが未設定です。上部の『APIキー設定』で保存してください。")
            if not file:
                raise gr.Error("ファイルを選択してください。")

            file_path = Path(file)
            file_ext = file_path.suffix.lower()

            try:
                import time

                start_time = time.time()
                file_size_mb = file_path.stat().st_size / (1024 * 1024)

                progress(0, desc=f"ファイル形式: {file_ext} | サイズ: {file_size_mb:.1f}MB")

                if file_size_mb > 50:
                    progress(0.01, desc=f"⚠️ 大きなファイル ({file_size_mb:.1f}MB) - 処理に時間がかかります...")

                def progress_with_keepalive(p, d):
                    progress(p, desc=d)
                    if 0 < p < 1:
                        gr.Info(f"処理中: {d}", duration=2)

                result = transcribe_file_with_groq(
                    file_path,
                    api_key=api_key,
                    model=model,
                    chunk_seconds=int(chunk_sec),
                    max_workers=int(workers),
                    progress_cb=progress_with_keepalive,
                )

                if len(result) == 4:
                    txt, path, elapsed, audio_duration = result
                else:
                    txt, path, elapsed = result
                    audio_duration = 0

                elapsed = max(elapsed, 0.0001)  # Avoid division by zero
                speed_ratio = audio_duration / elapsed if elapsed > 0 else 0
                char_count = len(txt)

                stats_html = f"""
                <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                    <div style="font-size: 64px; font-weight: bold; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        🎉 完了！
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; max-width: 700px; margin: 0 auto;">
                        <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
                            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">元メディア長</div>
                            <div style="font-size: 32px; font-weight: bold;">{audio_duration/60:.1f}分</div>
                            <div style="font-size: 14px; opacity: 0.8;">({audio_duration:.0f}秒)</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
                            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">処理時間</div>
                            <div style="font-size: 32px; font-weight: bold;">{elapsed:.1f}秒</div>
                            <div style="font-size: 14px; opacity: 0.8;">({elapsed/60:.1f}分)</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px;">
                            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 5px;">文字数</div>
                            <div style="font-size: 32px; font-weight: bold;">{char_count:,}</div>
                            <div style="font-size: 14px; opacity: 0.8;">文字</div>
                        </div>
                    </div>
                    <div style="margin-top: 20px; font-size: 48px; font-weight: bold; color: #FFD700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        ⚡ {speed_ratio:.1f}倍速！
                    </div>
                    <div style="margin-top: 10px; font-size: 16px; opacity: 0.9;">
                        {audio_duration/60:.1f}分の音声をたった{elapsed:.1f}秒で文字起こし完了 • {char_count:,}文字生成
                    </div>
                </div>
                """

                status = f"⏱ 処理時間: {elapsed:.1f}s  •  音声長: {audio_duration/60:.1f}分  •  速度: {speed_ratio:.1f}倍速"

                return txt, path, status, stats_html
            except RuntimeError as e:
                error_msg = str(e)
                if "ffmpeg" in error_msg.lower():
                    raise gr.Error(
                        f"⚠️ {error_msg}\n\n💡 解決方法:\n1. ターミナルで 'ffmpeg -version' を実行して確認\n2. インストールされていない場合:\n   macOS: brew install ffmpeg\n   Windows: choco install ffmpeg"
                    )
                elif "m4a" in file_ext or "aac" in file_ext:
                    raise gr.Error(
                        f"⚠️ m4aファイルの処理エラー: {error_msg}\n\n💡 ffmpegが必要です。setup.shを再実行してください"
                    )
                else:
                    raise gr.Error(f"エラー: {error_msg}")
            except Exception as e:
                import traceback

                tb = traceback.format_exc()
                print(f"[ERROR] Transcription failed:\n{tb}")
                raise gr.Error(f"予期しないエラー: {str(e)}\n\nファイル形式: {file_path.suffix}")

        def _start_transcription_timer():
            """Shared timer UI updater."""
            timer_html = """
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
                <div style="font-size: 48px; font-weight: bold; margin-bottom: 10px;">
                    ⏱️ 処理開始！
                </div>
                <div style="font-size: 18px; opacity: 0.9;">高速文字起こし処理中...</div>
            </div>
            """
            return gr.update(value=timer_html, visible=True), gr.update(visible=False)


        with gr.Tab("LPスクショ + Gemini"):
            gr.Markdown("<div class='section-title'>LPスクショ + Gemini文字起こし</div>")
            with gr.Row():
                # Left: inputs
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["card"]):
                        url = gr.Textbox(label="LPのURL", placeholder="https://example.com/long-page")
                        model = gr.Dropdown(
                            [
                                "gemini-2.5-flash",
                                "gemini-2.0-flash",
                                "gemini-1.5-flash",
                                "gemini-1.5-pro",
                            ],
                            value="gemini-2.5-flash",
                            label="Geminiモデル",
                        )
                        width = gr.Slider(640, 1920, value=640, step=10, label="画面幅(px)")
                        tile_h = gr.Slider(1200, 4000, value=2400, step=100, label="タイル高さ(px)")
                        scale = gr.Slider(1.0, 3.0, value=1.0, step=0.1, label="デバイススケール")
                        overlap = gr.Slider(0, 400, value=200, step=10, label="タイル重なり(px)")
                        pause_anim = gr.Checkbox(value=True, label="アニメーション停止")
                        hide_fixed = gr.Checkbox(value=True, label="固定要素を非表示")
                        pre_scroll = gr.Checkbox(value=True, label="遅延読み込みを事前スクロールで描画")
                        timeout_ms = gr.Slider(30000, 180000, value=90000, step=5000, label="ナビゲーションタイムアウト(ms)")
                        with gr.Accordion("撮影が不安定なページのコツ", open=False):
                            gr.Markdown(
                                "- タイムアウトを 120,000〜150,000 ms に上げる\n"
                                "- 固定要素を非表示: OFF（ヘッダ固定で崩れる場合）\n"
                                "- タイル高さ: 2000〜2600、オーバーラップ: 200\n"
                                "- デバイススケール: 1.25〜1.5（文字が小さい時）\n"
                                "- 事前スクロール: ON（遅延読み込みを描画）\n"
                                "- うまくいかないサイト例: synqai.jp は上記推奨\n"
                            )
                            preset_btn = gr.Button("⚙ 安定化プリセットを適用")
                        
                        # 2段階ボタン
                        capture_only_btn = gr.Button("📸 スクショを撮影", variant="primary")
                        
                        # スクショ確認用の警告表示
                        screenshot_warning = gr.Markdown("", visible=False)
                        
                        with gr.Row():
                            run_ocr_btn = gr.Button("✅ このスクショで文字起こし", variant="primary", interactive=False)
                            recapture_btn = gr.Button("↻ 画面幅を変えて再撮影", variant="secondary", visible=False)
                        
                        rerun_lp = gr.Button("↻ 再実行（同じ設定で）")
                # Center: screenshot only
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["card"], elem_id="screenshot_card"):
                        screenshot = gr.Image(label="スクショプレビュー")
                # Right: text + downloads + status + logs
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["card"]):
                        lp_text = gr.Textbox(label="抽出テキスト", lines=15, elem_id="lp_text")
                        with gr.Row():
                            lp_copy_btn = gr.Button("📋 テキストをコピー", elem_classes=["copy-btn"])
                            dl_txt = gr.DownloadButton(label="📥 テキストをダウンロード", elem_classes=["copy-btn"])
                        dl_img = gr.DownloadButton(label="📥 スクショをダウンロード")
                        lp_status = gr.Markdown("⏳ 未実行", elem_classes=["status-large"]) 
                        lp_prog = gr.HTML("<div class='prog-wrap'><div class='prog'><span style='width:0%'></span></div><div class='prog-text'>0% 準備中</div></div>")
                        lp_log = gr.Textbox(label="進捗ログ", lines=10, interactive=False)
                        # hidden fields used to chain steps (capture -> ocr)
                        lp_tmp_png = gr.Textbox(visible=False)
                        lp_params_json = gr.Textbox(visible=False)
                        lp_last_json = gr.Textbox(visible=False)

            def _prog_html(pct: float, text: str) -> str:
                pct = max(0.0, min(100.0, float(pct)))
                return f"<div class='prog-wrap'><div class='prog'><span style='width:{pct:.0f}%'></span></div><div class='prog-text'>{pct:.0f}% {text}</div></div>"

            def do_lp_capture_only(url, model, width, tile_h, scale, overlap, pause_anim, hide_fixed, pre_scroll, timeout_ms, state_gemini_val):
                """スクショのみ取得（文字起こしはしない）+ 品質チェック"""
                import time as _t
                t0 = _t.time()
                logs = []
                
                # 初期状態
                yield (
                    gr.update(),  # screenshot
                    "",  # lp_text
                    None,  # dl_img
                    None,  # dl_txt
                    "🚀 撮影開始…",  # lp_status
                    _prog_html(1, "準備中"),  # lp_prog
                    "",  # lp_tmp_png
                    "",  # lp_params_json
                    "開始",  # lp_log
                    gr.update(visible=False),  # screenshot_warning
                    gr.update(interactive=False),  # run_ocr_btn
                    gr.update(visible=False),  # recapture_btn
                )
                
                # スクショ撮影
                import threading, time as _time
                progress_state = {"p": 1.0, "desc": "準備中"}
                result = {"png": None, "tiles": 0, "err": None}
                
                def cb(p, d):
                    progress_state["p"] = float(p) * 100.0
                    progress_state["desc"] = d or "撮影中"
                
                def worker():
                    try:
                        png, t = capture_fullpage_tiled(
                            url=url,
                            out_png=Path(tempfile.mkdtemp(prefix="moji_lp_")) / "lp_screenshot.png",
                            width=int(width),
                            tile_height=int(tile_h),
                            device_scale=float(scale),
                            overlap=int(overlap),
                            pause_animations=bool(pause_anim),
                            hide_fixed=bool(hide_fixed),
                            prerender_scroll=bool(pre_scroll),
                            goto_timeout_ms=int(timeout_ms),
                            max_output_pixels=100_000_000,
                            progress_cb=cb,
                        )
                        result["png"] = png
                        result["tiles"] = t
                    except Exception as e:
                        result["err"] = e
                
                th = threading.Thread(target=worker, daemon=True)
                th.start()
                
                while th.is_alive():
                    pct = progress_state["p"]
                    desc = progress_state["desc"]
                    logs.append(f"{pct:.0f}% {desc}")
                    yield (
                        gr.update(),
                        "",
                        None,
                        None,
                        f"📸 撮影中…",
                        _prog_html(pct, desc),
                        "",
                        "",
                        "\n".join(logs[-10:]),
                        gr.update(visible=False),
                        gr.update(interactive=False),
                        gr.update(visible=False),
                    )
                    _time.sleep(0.4)
                
                if result["err"] is not None:
                    raise result["err"]
                
                png_path = result["png"]
                tiles = result["tiles"]
                
                # 品質チェック実行
                quality_check = _check_screenshot_quality(str(png_path), int(width))
                
                # 警告メッセージを作成
                if quality_check["has_issues"]:
                    warning_lines = ["## 📸 スクショ品質チェック\n"]
                    warning_lines.extend(quality_check["warnings"])
                    warning_lines.append("")
                    warning_lines.extend(quality_check["suggestions"])
                    warning_lines.append("\n**このまま文字起こしを実行しますか？**")
                    warning_msg = "\n".join(warning_lines)
                    warning_visible = True
                    recapture_visible = True
                else:
                    warning_msg = "✅ スクショの品質に問題ありません"
                    warning_visible = True
                    recapture_visible = False
                
                status1 = f"📸 スクショ完了: タイル{tiles}枚 ({quality_check['width']}×{quality_check['height']}px)"
                
                params_dict = {
                    "url": url, "model": model, "width": width, "tile_h": tile_h, "scale": scale, "overlap": overlap,
                    "pause_anim": pause_anim, "hide_fixed": hide_fixed, "pre_scroll": pre_scroll, "timeout_ms": timeout_ms,
                    "t0": t0, "tiles": tiles,
                }
                if state_gemini_val and state_gemini_val.strip():
                    params_dict["api_key"] = state_gemini_val.strip()
                
                params_json = _json.dumps(params_dict, ensure_ascii=False)
                
                # 最終結果
                yield (
                    str(png_path),  # screenshot
                    "",  # lp_text
                    str(png_path),  # dl_img
                    None,  # dl_txt
                    status1,  # lp_status
                    _prog_html(100, "スクショ完了"),  # lp_prog
                    str(png_path),  # lp_tmp_png
                    params_json,  # lp_params_json
                    "\n".join(logs),  # lp_log
                    gr.update(value=warning_msg, visible=warning_visible),  # screenshot_warning
                    gr.update(interactive=True),  # run_ocr_btn（有効化）
                    gr.update(visible=recapture_visible),  # recapture_btn
                )

            def do_lp_ocr_only(tmp_png_path, params_json, state_gemini_val, ui_gemini_key):
                """文字起こしのみ実行（スクショは既に取得済み）"""
                if not tmp_png_path or not params_json:
                    raise gr.Error("スクリーンショットが見つかりません。先に『📸 スクショを撮影』を実行してください。")
                
                # ボタンを無効化（処理中）
                yield (
                    gr.update(),  # screenshot
                    "",  # lp_text
                    gr.update(),  # dl_img
                    None,  # dl_txt
                    "⚡ 文字起こし開始…",  # lp_status
                    _prog_html(85, "文字起こし準備中"),  # lp_prog
                    None,  # lp_last_json
                    "文字起こし開始",  # lp_log
                    gr.update(visible=False),  # screenshot_warning
                    gr.update(interactive=False),  # run_ocr_btn（無効化）
                    gr.update(visible=False),  # recapture_btn
                )
                p = _json.loads(params_json)
                import time as _t
                api_key = _resolve_gemini_key(state_gemini_val, ui_gemini_key)
                if not api_key:
                    api_key = (p.get("api_key") or "").strip()
                if not api_key:
                    last_json = _json.dumps({k: p[k] for k in ["url","model","width","tile_h","scale","overlap","pause_anim","hide_fixed","pre_scroll","timeout_ms"]}, ensure_ascii=False)
                    msg = "🗝️ GeminiのAPIキーが未設定です。上部の『APIキー設定』で保存してから再実行してください。"
                    yield (
                        gr.update(),  # screenshot
                        gr.update(),  # lp_text
                        str(tmp_png_path),  # dl_img
                        None,  # dl_txt
                        msg,  # lp_status
                        _prog_html(85, "キー待ち"),  # lp_prog
                        last_json,  # lp_last_json
                        "キー未設定",  # lp_log
                        gr.update(),  # screenshot_warning
                        gr.update(interactive=True),  # run_ocr_btn（有効化）
                        gr.update(),  # recapture_btn
                    )
                    return

                text_holder = {"text": None, "err": None}
                log_queue: SimpleQueue[str] = SimpleQueue()
                log_lines: list[str] = ["⚡ 高速スクショ文字起こしモードを開始"]

                def _log_enqueue(msg: str):
                    try:
                        log_queue.put(msg)
                    except Exception:
                        pass

                def worker():
                    try:
                        text_holder["text"] = gemini_ocr_image_parallel(
                            Path(tmp_png_path),
                            api_key=api_key,
                            model=p["model"],
                            log_fn=_log_enqueue,
                        )
                    except Exception as e:
                        text_holder["err"] = e

                import threading
                th = threading.Thread(target=worker, daemon=True)
                th.start()
                pct = 85
                import time as _t
                while th.is_alive() and pct < 95:
                    while not log_queue.empty():
                        log_lines.append(log_queue.get())
                    log_output = "\n".join(log_lines[-10:])
                    yield (
                        gr.update(),  # screenshot
                        "",  # lp_text
                        None,  # dl_img
                        None,  # dl_txt
                        "⚡ 文字起こし実行中…",  # lp_status
                        _prog_html(pct, "文字起こし中"),  # lp_prog
                        None,  # lp_last_json
                        log_output,  # lp_log
                        gr.update(visible=False),  # screenshot_warning
                        gr.update(interactive=False),  # run_ocr_btn
                        gr.update(visible=False),  # recapture_btn
                    )
                    pct += 1
                    _t.sleep(0.35)
                th.join()
                while not log_queue.empty():
                    log_lines.append(log_queue.get())
                if text_holder["err"] is not None:
                    raise text_holder["err"]
                text = text_holder["text"] or ""
                txt_path = Path(tmp_png_path).with_suffix("")
                txt_path = txt_path.parent / "lp_text_gemini.txt"
                txt_path.write_text(text, encoding="utf-8")
                elapsed = _t.time() - float(p.get("t0", _t.time()))
                status = f"⏱ 処理時間: {elapsed:.1f}s  •  タイル: {p['tiles']}  •  モデル: {p['model']}  •  幅: {p['width']}px"
                last_json = _json.dumps({k: p[k] for k in ["url","model","width","tile_h","scale","overlap","pause_anim","hide_fixed","pre_scroll","timeout_ms"]}, ensure_ascii=False)
                log_lines.append("✅ 文字起こし完了")
                yield (
                    gr.update(),  # screenshot
                    text,  # lp_text
                    str(tmp_png_path),  # dl_img
                    str(txt_path),  # dl_txt
                    status,  # lp_status
                    _prog_html(100, "完了"),  # lp_prog
                    last_json,  # lp_last_json
                    "\n".join(log_lines[-10:]),  # lp_log
                    gr.update(visible=False),  # screenshot_warning
                    gr.update(interactive=True),  # run_ocr_btn（再有効化）
                    gr.update(visible=False),  # recapture_btn
                )

            # スクショのみ取得ボタン
            capture_only_btn.click(
                fn=do_lp_capture_only,
                inputs=[url, model, width, tile_h, scale, overlap, pause_anim, hide_fixed, pre_scroll, timeout_ms, state_gemini],
                outputs=[screenshot, lp_text, dl_img, dl_txt, lp_status, lp_prog, lp_tmp_png, lp_params_json, lp_log, screenshot_warning, run_ocr_btn, recapture_btn],
                show_progress="hidden",
            )
            
            # 文字起こし実行ボタン（スクショ後に有効化）
            run_ocr_btn.click(
                fn=do_lp_ocr_only,
                inputs=[lp_tmp_png, lp_params_json, state_gemini, gemini_key],
                outputs=[screenshot, lp_text, dl_img, dl_txt, lp_status, lp_prog, lp_last_json, lp_log, screenshot_warning, run_ocr_btn, recapture_btn],
                show_progress="hidden",
            )
            
            # 再撮影ボタン（画面幅を変える）
            def reset_and_suggest_width():
                """画面幅を1280に変更してリセット"""
                return (
                    1280,  # width
                    gr.update(interactive=False),  # run_ocr_btn（無効化）
                    gr.update(visible=False),  # recapture_btn（非表示）
                    gr.update(visible=False),  # screenshot_warning
                    "💡 画面幅を1280pxに変更しました。再度『📸 スクショを撮影』を押してください。",  # lp_status
                )
            
            recapture_btn.click(
                fn=reset_and_suggest_width,
                inputs=[],
                outputs=[width, run_ocr_btn, recapture_btn, screenshot_warning, lp_status],
            )

            def apply_stable_preset():
                # tile_h, overlap, scale, hide_fixed, pre_scroll, timeout_ms
                return 2400, 200, 1.25, False, True, 120000

            preset_btn.click(
                fn=apply_stable_preset,
                inputs=[],
                outputs=[tile_h, overlap, scale, hide_fixed, pre_scroll, timeout_ms],
            )

            def do_lp_rerun(last_json, state_gemini_val, ui_gemini_key):
                """前回の設定で再実行"""
                if not last_json:
                    raise gr.Error("前回の設定がありません。左の設定を入力して実行してください。")
                last = _json.loads(last_json)
                # スクショのみ取得（品質チェック付き）
                return do_lp_capture_only(
                    last["url"], last["model"], last["width"], last["tile_h"], last["scale"], last["overlap"],
                    last["pause_anim"], last["hide_fixed"], last["pre_scroll"], last["timeout_ms"], state_gemini_val,
                )

            rerun_lp.click(
                fn=do_lp_rerun, 
                inputs=[lp_last_json, state_gemini, gemini_key], 
                outputs=[screenshot, lp_text, dl_img, dl_txt, lp_status, lp_prog, lp_tmp_png, lp_params_json, lp_log, screenshot_warning, run_ocr_btn, recapture_btn],
                show_progress="hidden"
            )
            
            # LPコピー機能
            lp_copy_btn.click(
                fn=lambda: None,
                inputs=[],
                outputs=[],
                js="() => { const app = window.gradioApp?.() || document; const node = app.querySelector('#lp_text textarea'); if (node) navigator.clipboard.writeText(node.value); }"
            )

        with gr.Tab("音声→文字起こし"):
            gr.Markdown("<div class='section-title'>🎵 音声ファイル → Groq Whisper 高速文字起こし</div>")
            
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["card"]):
                        # 統一された入力方法 - Fileコンポーネント（全サイズ対応）
                        gr.Markdown("""
                        ### 📁 音声ファイルを選択
                        **ドラッグ&ドロップ** または **クリックして選択**
                        """)
                        
                        audio_input = gr.File(
                            label="音声ファイル（すべてのサイズに対応）",
                            file_types=[".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".mp4", ".webm"],
                            type="filepath",  # メモリ効率化
                            file_count="single",
                            elem_classes=["file-upload-area"]
                        )
                        
                        # ファイル情報表示
                        file_info = gr.Markdown("", visible=False)
                        
                        # ファイル選択時の処理
                        def show_file_info(file_path):
                            if not file_path:
                                return "", gr.update(visible=False)
                            
                            path = Path(file_path)
                            size_mb = path.stat().st_size / (1024 * 1024)
                            
                            # ファイルサイズに応じたメッセージ
                            if size_mb < 60:
                                status = "✅ 標準処理"
                                color = "green"
                            elif size_mb < 200:
                                status = "⚡ 大容量処理"
                                color = "orange"
                            else:
                                status = "🔥 超大容量処理"
                                color = "red"
                            
                            info_html = f"""
                            <div style="padding: 15px; background: linear-gradient(135deg, #f5f5f5, #e0e0e0); border-radius: 10px; margin: 10px 0;">
                                <div style="font-size: 16px; font-weight: bold; color: #333;">📁 {path.name}</div>
                                <div style="margin-top: 8px; display: flex; justify-content: space-between;">
                                    <span>サイズ: <b>{size_mb:.1f} MB</b></span>
                                    <span style="color: {color}; font-weight: bold;">{status}</span>
                                </div>
                            </div>
                            """
                            return info_html, gr.update(visible=True)
                        
                        audio_input.change(
                            fn=show_file_info,
                            inputs=[audio_input],
                            outputs=[file_info, file_info]
                        )
                        model2 = gr.Dropdown(
                            [
                                "whisper-large-v3-turbo",
                                "whisper-large-v3",
                                "distil-whisper-large-v3-en",
                            ],
                            value="whisper-large-v3-turbo",
                            label="Groq Whisperモデル",
                        )
                        chunk_sec = gr.Slider(60, 600, value=180, step=30, label="チャンク長(秒)", info="3分推奨（源流ver4準拠）")
                        workers = gr.Slider(1, 20, value=10, step=1, label="並列数", info="環境に応じて自動調整")
                        run_groq = gr.Button("▶ 文字起こしを実行", variant="primary")
                        rerun_groq = gr.Button("↻ 再実行（同じ設定で）")
                with gr.Column(scale=1):
                    # 大きなタイマー表示
                    with gr.Group(elem_classes=["card"]):
                        timer_display = gr.HTML("""
                            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
                                <div style="font-size: 48px; font-weight: bold; margin-bottom: 10px;">
                                    ⏱️ <span id="timer">00:00</span>
                                </div>
                                <div style="font-size: 18px; opacity: 0.9;">処理中...</div>
                            </div>
                        """, visible=False)
                        
                        # 処理結果の統計表示
                        stats_display = gr.HTML(visible=False)
                    
                    with gr.Group(elem_classes=["card"]):
                        out_text = gr.Textbox(label="文字起こし結果", lines=15, elem_id="out_text")
                        with gr.Row():
                            audio_copy_btn = gr.Button("📋 テキストをコピー", elem_classes=["copy-btn"])
                            dl_txt2 = gr.DownloadButton(label="📥 テキストをダウンロード", elem_classes=["copy-btn"])
                        groq_status = gr.Markdown("⏳ 未実行", elem_classes=["status-large"]) 

            def do_transcribe(file, model, chunk_sec, workers, state_groq_val, ui_groq_key, progress=gr.Progress(track_tqdm=True)):
                txt, path, status, stats_html = _run_groq_transcription(
                    file,
                    model,
                    chunk_sec,
                    workers,
                    state_groq_val,
                    ui_groq_key,
                    progress,
                )
                return txt, path, status, gr.update(visible=False), gr.update(value=stats_html, visible=True)
            
            # ボタンクリック時の処理（audio_inputに変更）
            run_groq.click(
                fn=_start_transcription_timer,
                outputs=[timer_display, stats_display],
                queue=False
            ).then(
                fn=do_transcribe,
                inputs=[audio_input, model2, chunk_sec, workers, state_groq, groq_key],  # セッション+UIキー
                outputs=[out_text, dl_txt2, groq_status, timer_display, stats_display],
                api_name="transcribe",
                show_progress="full",
            )

            def do_groq_rerun(file, model, chunk_sec_v, workers_v, state_groq_val, ui_groq_key):
                return do_transcribe(file, model, chunk_sec_v, workers_v, state_groq_val, ui_groq_key)

            rerun_groq.click(
                fn=_start_transcription_timer,
                outputs=[timer_display, stats_display],
                queue=False
            ).then(
                fn=do_groq_rerun, 
                inputs=[audio_input, model2, chunk_sec, workers, state_groq, groq_key],  # セッション+UIキー
                outputs=[out_text, dl_txt2, groq_status, timer_display, stats_display]
            )
            # 音声コピー機能
            audio_copy_btn.click(
                fn=lambda: None,
                inputs=[],
                outputs=[],
                js="() => { const app = window.gradioApp?.() || document; const node = app.querySelector('#out_text textarea'); if (node) navigator.clipboard.writeText(node.value); }"
            )

        with gr.Tab("UTAGE/Loom/スタエフ文字起こし"):
            gr.Markdown("<div class='section-title'>動画/音声URL → 文字起こし → Groq Whisper</div>")
            gr.Markdown("💡 **対応URL**: UTAGE (.m3u8)、Loom (luna.loom.com)、スタンドFM (.m4a)、直接音声ファイル")
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["card"]):
                        urls = gr.Textbox(
                            label="動画/音声URL (改行で複数可)", 
                            lines=4, 
                            placeholder="https://luna.loom.com/id/VIDEO_ID/...\nhttps://www.loom.com/share/VIDEO_ID\nhttps://cdncf.stand.fm/audios/xxxx.m4a\nhttps://example.com/stream.m3u8"
                        )
                        model3 = gr.Dropdown(
                            [
                                "whisper-large-v3-turbo",
                                "whisper-large-v3",
                                "distil-whisper-large-v3-en",
                            ],
                            value="whisper-large-v3-turbo",
                            label="Groq Whisperモデル",
                        )
                        chunk_sec2 = gr.Slider(60, 600, value=180, step=30, label="チャンク長(秒)", info="3分推奨")
                        workers2 = gr.Slider(1, 20, value=10, step=1, label="並列数", info="環境に応じて自動調整")
                        run_hls = gr.Button("▶ ダウンロード→文字起こし", variant="primary")
                        rerun_hls = gr.Button("↻ 再実行（同じ設定で）")
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["card"]):
                        hls_text = gr.Textbox(label="文字起こし結果 (結合)", lines=15, elem_id="hls_text")
                        with gr.Row():
                            hls_copy_btn = gr.Button("📋 テキストをコピー", elem_classes=["copy-btn"])
                            dl_txt3 = gr.DownloadButton(label="📥 テキストをダウンロード", elem_classes=["copy-btn"])
                        hls_status = gr.Markdown("⏳ 未実行", elem_classes=["status-large"]) 
                        hls_last_json = gr.Textbox(visible=False)

            def do_hls(hls_urls, model, chunk_sec, workers, state_groq_val, ui_groq_key, progress=gr.Progress()):
                api_key = _resolve_groq_key(state_groq_val, ui_groq_key)
                if not api_key:
                    raise gr.Error("GroqのAPIキーが未設定です。上部の『APIキー設定』で保存してください。")
                if not hls_urls.strip():
                    raise gr.Error("HLSのURLを入力してください。")
                import time as _t
                t0 = _t.time()
                results = []
                tmpdir = Path(tempfile.mkdtemp(prefix="moji_hls_"))
                urls_list = [s.strip() for s in hls_urls.splitlines() if s.strip()]
                n = len(urls_list)
                total_audio_duration = 0
                
                for i, u in enumerate(urls_list):
                    progress(i / max(n, 1), desc=f"{i+1}/{n} ダウンロード中…")
                    audio_path = tmpdir / f"hls_{i}.wav"
                    extract_audio_from_hls(u, audio_path)
                    
                    # transcribe_file_with_groqの戻り値を確認
                    result = transcribe_file_with_groq(
                        audio_path,
                        api_key=api_key,
                        model=model,
                        chunk_seconds=int(chunk_sec),
                        max_workers=int(workers),
                        progress_cb=lambda p, d: progress((i + p) / max(n, 1), desc=d),
                    )
                    
                    # 4つの値が返される場合（新版）
                    if len(result) == 4:
                        txt, _, _elapsed, audio_duration = result
                        total_audio_duration += audio_duration
                    else:
                        # 3つの値が返される場合（旧版）
                        txt, _, _elapsed = result
                    
                    results.append(f"# {u}\n\n{txt}\n\n")
                
                all_text = "\n".join(results)
                out = tmpdir / "hls_transcripts.txt"
                out.write_text(all_text, encoding="utf-8")
                elapsed = _t.time() - t0
                
                # 文字数を計算
                char_count = len(all_text)
                
                # 処理速度を計算
                if total_audio_duration > 0:
                    speed_ratio = total_audio_duration / elapsed if elapsed > 0 else 0
                    status = f"⏱ 処理時間: {elapsed:.1f}s  •  URL数: {n}  •  速度: {speed_ratio:.1f}倍速  •  文字数: {char_count:,}"
                else:
                    status = f"⏱ 処理時間: {elapsed:.1f}s  •  モデル: {model}  •  URL数: {n}  •  文字数: {char_count:,}"
                
                params = {"urls": hls_urls, "model": model, "chunk_sec": chunk_sec, "workers": workers}
                return all_text, str(out), status, _json.dumps(params, ensure_ascii=False)

            run_hls.click(
                fn=do_hls,
                inputs=[urls, model3, chunk_sec2, workers2, state_groq, groq_key],  # セッション+UIキー
                outputs=[hls_text, dl_txt3, hls_status, hls_last_json],
            )

            def do_hls_rerun(last_json, state_groq_val, ui_groq_key):
                if not last_json:
                    raise gr.Error("前回の設定がありません。左の設定を入力して実行してください。")
                last = _json.loads(last_json)
                return do_hls(last["urls"], last["model"], last["chunk_sec"], last["workers"], state_groq_val, ui_groq_key)

            rerun_hls.click(fn=do_hls_rerun, inputs=[hls_last_json, state_groq, groq_key], outputs=[hls_text, dl_txt3, hls_status, hls_last_json])
            # HLSコピー機能
            hls_copy_btn.click(
                fn=lambda: None,
                inputs=[],
                outputs=[],
                js="() => { const app = window.gradioApp?.() || document; const node = app.querySelector('#hls_text textarea'); if (node) navigator.clipboard.writeText(node.value); }"
            )

        with gr.Tab("動画→高速文字起こし"):
            gr.Markdown("<div class='section-title'>動画ファイル (mp4 / mov / webm) → 音声抽出 → Groq Whisper</div>")
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["card"]):
                        video_input = gr.File(
                            label="動画ファイル（mp4, mov, webm 等）",
                            file_types=[".mp4", ".mov", ".m4v", ".webm", ".mkv"],
                            type="filepath",
                            file_count="single",
                            elem_classes=["file-upload-area"],
                        )
                        video_file_info = gr.Markdown("", visible=False)

                        def show_video_info(file_path):
                            if not file_path:
                                return "", gr.update(visible=False)

                            path = Path(file_path)
                            size_mb = path.stat().st_size / (1024 * 1024)

                            if size_mb < 60:
                                status = "✅ 標準処理"
                                color = "green"
                            elif size_mb < 200:
                                status = "⚡ 大容量処理"
                                color = "orange"
                            else:
                                status = "🔥 超大容量処理"
                                color = "red"

                            info_html = f"""
                            <div style="padding: 15px; background: linear-gradient(135deg, #f5f5f5, #e0e0e0); border-radius: 10px; margin: 10px 0;">
                                <div style="font-size: 16px; font-weight: bold; color: #333;">🎬 {path.name}</div>
                                <div style="margin-top: 8px; display: flex; justify-content: space-between;">
                                    <span>サイズ: <b>{size_mb:.1f} MB</b></span>
                                    <span style="color: {color}; font-weight: bold;">{status}</span>
                                </div>
                            </div>
                            """
                            return info_html, gr.update(visible=True)

                        video_input.change(
                            fn=show_video_info,
                            inputs=[video_input],
                            outputs=[video_file_info, video_file_info]
                        )
                        video_model = gr.Dropdown(
                            [
                                "whisper-large-v3-turbo",
                                "whisper-large-v3",
                                "distil-whisper-large-v3-en",
                            ],
                            value="whisper-large-v3-turbo",
                            label="Groq Whisperモデル",
                        )
                        video_chunk_sec = gr.Slider(60, 600, value=180, step=30, label="チャンク長(秒)", info="抽出した音声をこの長さで分割します")
                        video_workers = gr.Slider(1, 20, value=10, step=1, label="並列数", info="環境に応じて自動調整")
                        run_video = gr.Button("▶ 動画から文字起こし", variant="primary")
                        rerun_video = gr.Button("↻ 再実行（同じ設定で）")
                with gr.Column(scale=1):
                    with gr.Group(elem_classes=["card"]):
                        video_timer_display = gr.HTML("""
                            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
                                <div style="font-size: 48px; font-weight: bold; margin-bottom: 10px;">
                                    ⏱️ <span id="video_timer">00:00</span>
                                </div>
                                <div style="font-size: 18px; opacity: 0.9;">動画から音声抽出中...</div>
                            </div>
                        """, visible=False)
                        video_stats_display = gr.HTML(visible=False)

                    with gr.Group(elem_classes=["card"]):
                        video_out_text = gr.Textbox(label="文字起こし結果", lines=15, elem_id="video_out_text")
                        with gr.Row():
                            video_copy_btn = gr.Button("📋 テキストをコピー", elem_classes=["copy-btn"])
                            video_dl_txt = gr.DownloadButton(label="📥 テキストをダウンロード", elem_classes=["copy-btn"])
                        video_status = gr.Markdown("⏳ 未実行", elem_classes=["status-large"]) 

            def do_video_transcribe(file, model, chunk_sec, workers, state_groq_val, ui_groq_key, progress=gr.Progress(track_tqdm=True)):
                txt, path, status, stats_html = _run_groq_transcription(
                    file,
                    model,
                    chunk_sec,
                    workers,
                    state_groq_val,
                    ui_groq_key,
                    progress,
                )
                return txt, path, status, gr.update(visible=False), gr.update(value=stats_html, visible=True)

            def do_video_rerun(file, model, chunk_sec, workers, state_groq_val, ui_groq_key):
                return do_video_transcribe(file, model, chunk_sec, workers, state_groq_val, ui_groq_key)

            run_video.click(
                fn=_start_transcription_timer,
                outputs=[video_timer_display, video_stats_display],
                queue=False
            ).then(
                fn=do_video_transcribe,
                inputs=[video_input, video_model, video_chunk_sec, video_workers, state_groq, groq_key],
                outputs=[video_out_text, video_dl_txt, video_status, video_timer_display, video_stats_display],
                show_progress="full",
            )

            rerun_video.click(
                fn=_start_transcription_timer,
                outputs=[video_timer_display, video_stats_display],
                queue=False
            ).then(
                fn=do_video_rerun,
                inputs=[video_input, video_model, video_chunk_sec, video_workers, state_groq, groq_key],
                outputs=[video_out_text, video_dl_txt, video_status, video_timer_display, video_stats_display],
            )
            video_copy_btn.click(
                fn=lambda: None,
                inputs=[],
                outputs=[],
                js="() => { const app = window.gradioApp?.() || document; const node = app.querySelector('#video_out_text textarea'); if (node) navigator.clipboard.writeText(node.value); }"
            )

        gr.Markdown(
            """
            ---
            ### 💡 使い方
            
            1. **APIキーを設定** - 上部でGroqとGeminiのAPIキーを入力・保存
            2. **機能を選択** - 4つのタブから用途に応じて選択
            3. **ファイル・URLを入力** - ドラッグ&ドロップまたは直接入力
            4. **実行** - 各タブの実行ボタンをクリック
            
            ### ⚙️ システム要件
            
            - Python 3.10以上
            - ffmpeg（音声・動画処理用）
            - Playwright Chromium（LP OCR用）
            
            ### 🔗 関連リンク
            
            - [Groq APIキー取得](https://console.groq.com/keys)
            - [Gemini APIキー取得](https://aistudio.google.com/)
            """
        )

        def initial_load():
            # セッション開始時はキーは未設定
            message = "⚠️ APIキーを設定してください（セッション別管理）"
            # セッション開始時のステータスバッジ（全てNG）
            ffm = _is_cmd_available("ffmpeg")
            pw = not os.environ.get("DISABLE_PLAYWRIGHT", "false").lower() == "true"
            
            def b(label, ok):
                color = "#10b981" if ok else "#ef4444"
                return f"<span style='background:{color};color:white;padding:4px 8px;border-radius:12px;font-size:12px;margin-right:8px;'>{label}: {'OK' if ok else 'NG'}</span>"
            
            initial_badges = f"<div class=\"badges\">{b('GROQ', False)}{b('Gemini', False)}{b('ffmpeg', ffm)}{b('Playwright', pw)}</div>"
            return message, initial_badges

        # Initial status badges update
        demo.load(initial_load, outputs=[out_info, status_html])

    try:
        print(
            "[init] component ids",
            {
                "lp_last_json": lp_last_json._id,
                "lp_params_json": lp_params_json._id,
                "hls_last_json": hls_last_json._id,
            },
        )
    except Exception:
        pass
    return demo


if __name__ == "__main__":
    import os
    # 大きなファイルのアップロードを許可（500MB）
    os.environ["GRADIO_MAX_FILE_SIZE"] = "500mb"
    
    app = make_app()
    # metrics logger (RSS/load1)
    _start_metrics_logger()
    # start background workers (queue skeleton)
    try:
        start_workers(n_workers=2)
    except Exception as _:
        pass
    try:
        start_janitor()
    except Exception:
        pass

    # Configure for long-running tasks and large files - NO AUTH for local distribution
    app.queue(
        max_size=10,  # Maximum queue size
        default_concurrency_limit=2,  # 同時処理数を制限（メモリ管理）
    ).launch(
        max_threads=40,  # Increase thread pool for concurrent requests
        show_error=True,  # Show detailed errors
        max_file_size="500mb",  # 500MBまでのファイルを許可
        quiet=False,  # ローカル版はログ表示
        # NO AUTH for local distribution
        server_name="127.0.0.1",  # ローカルのみ
        server_port=7860,
        share=False
    )