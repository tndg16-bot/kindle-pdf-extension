import subprocess
import sys
from pathlib import Path
import shutil
import re

# Windows環境での絵文字出力対応（cp932エラー回避）
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass  # 既に設定済みの場合はスキップ


def extract_audio_from_hls(hls_url: str, out_wav: Path, sample_rate: int = 16000):
    """HLS/動画/音声URLから音声を抽出
    
    対応URL:
    - Loom URLの場合はyt-dlpを使用（認証付きURL対応）
    - スタンドFM等の直接音声URL (.m4a, .mp3, .wav等)
    - 通常のHLS URLはffmpegで処理
    """
    out_wav = Path(out_wav)
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    
    # 直接音声ファイル（スタンドFM等）の場合
    if any(ext in hls_url.lower() for ext in ['.m4a', '.mp3', '.wav', '.aac', '.ogg', '.flac']):
        print(f"🎵 [スタンドFM/音声] 直接音声ファイルをダウンロード中...")
        
        cmd = [
            "ffmpeg",
            "-y",
            "-i", hls_url,
            "-vn",  # 映像なし
            "-acodec", "pcm_s16le",
            "-ar", str(sample_rate),
            "-ac", "1",  # モノラル
            str(out_wav),
        ]
        
        try:
            result = subprocess.run(
                cmd, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"✅ [スタンドFM/音声] 音声ダウンロード完了: {out_wav.name}")
            
        except FileNotFoundError:
            raise RuntimeError("ffmpeg が見つかりません。インストールしてください。")
        except subprocess.CalledProcessError as e:
            err = e.stderr if e.stderr else ''
            raise RuntimeError(f"音声ダウンロードに失敗しました: {err[:500]}")
    
    # Loom URLの場合はyt-dlpを使う
    elif 'loom.com' in hls_url:
        # HLS URL形式の場合は動画ページURLに変換
        # 例: https://luna.loom.com/id/VIDEO_ID/... → https://www.loom.com/share/VIDEO_ID
        if 'luna.loom.com/id/' in hls_url or '/resource/hls/' in hls_url:
            match = re.search(r'/id/([a-f0-9]+)', hls_url)
            if match:
                video_id = match.group(1)
                hls_url = f'https://www.loom.com/share/{video_id}'
                print(f"🔄 [Loom] HLS URLを動画ページURLに変換: {video_id}")
            else:
                raise RuntimeError(
                    "Loom HLS URLから動画IDを抽出できませんでした。\n"
                    "動画ページURL（https://www.loom.com/share/VIDEO_ID）を使用してください。"
                )
        # yt-dlpの存在確認
        if not shutil.which("yt-dlp"):
            raise RuntimeError(
                "yt-dlp が見つかりません。\n"
                "インストール方法:\n"
                "  pip install yt-dlp\n"
                "または:\n"
                "  brew install yt-dlp (macOS)\n"
                "  apt install yt-dlp (Linux)"
            )
        
        # 一時ファイル（yt-dlpが.wavを自動追加するため）
        temp_base = out_wav.with_suffix('')
        
        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "wav",
            "--audio-quality", "0",
            "--postprocessor-args", f"ffmpeg:-ar {sample_rate} -ac 1",
            "-o", str(temp_base),
            hls_url
        ]
        
        try:
            result = subprocess.run(
                cmd, 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # yt-dlpが出力したファイルを確認
            expected_output = temp_base.with_suffix('.wav')
            if expected_output.exists() and expected_output != out_wav:
                # 期待通りの場所に移動
                shutil.move(str(expected_output), str(out_wav))
            elif not out_wav.exists():
                raise RuntimeError(f"音声ファイルが生成されませんでした: {out_wav}")
                
        except FileNotFoundError:
            raise RuntimeError("yt-dlp が見つかりません。pip install yt-dlp でインストールしてください。")
        except subprocess.CalledProcessError as e:
            err = e.stderr if e.stderr else ''
            raise RuntimeError(f"yt-dlp 実行に失敗しました: {err[:500]}")
    
    else:
        # 通常のHLS URLはffmpegで処理
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            hls_url,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            str(sample_rate),
            "-ac",
            "1",
            str(out_wav),
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except FileNotFoundError:
            raise RuntimeError("ffmpeg が見つかりません。インストールしてください。")
        except subprocess.CalledProcessError as e:
            err = e.stderr.decode(errors='ignore') if e.stderr else ''
            raise RuntimeError(f"ffmpeg 実行に失敗しました: {err[:500]}")
