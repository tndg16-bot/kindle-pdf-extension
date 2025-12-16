# 🚀 Moji Booster - 高速文字起こし＆OCRツール（ローカル配布版 v2.1）

**97倍速**の文字起こしを実現するWebベースツール

> **v2.1 新機能：** Windows環境での絵文字エラー（cp932）を完全修正！全モジュールでUTF-8対応

## 📋 v2.1 更新内容（2025年10月）

### 🔧 Windows環境の完全対応

**問題：** Windows環境でcp932エラー（`'cp932' codec can't encode character '\U0001f9e0'`）が発生

**修正内容：**
- ✅ 全モジュール（5ファイル）にUTF-8強制コードを追加
- ✅ マルチスレッド/マルチプロセス環境でも絵文字が正常に動作
- ✅ コンソールログでも絵文字が正しく表示されるように修正

**対応ファイル：**
1. `app/main.py` - メインアプリケーション
2. `app/job_manager.py` - ジョブキュー管理
3. `app/modules/lp_gemini.py` - スクリーンショットOCR
4. `app/modules/groq_transcribe.py` - 音声文字起こし
5. `app/modules/hls_extractor.py` - HLS音声抽出

**結果：** Windows / macOS / Linux 全てで同じコードで動作！

---

## ✨ 主な機能

- 🎵 **音声ファイル** → Groq Whisperで**超高速文字起こし**（97倍速！）
- 🎬 **動画ファイル** → 音声抽出→Groq文字起こし（mp4/mov/webm対応）
- 🌐 **UTAGE/Loom/スタエフ** → URL入力で直接文字起こし
- 📄 **LPページ** → Geminiで全体スクリーンショット＆文字抽出  
- 💾 **大容量ファイル対応** → 500MBまでの音声・動画ファイル処理可能

## 🎯 驚異的な処理速度
- **53分の音声** → **32秒で処理** → **97.8倍速！**
- **チャンク並列処理** → 最大20並列で高速化
- **メモリ最適化** → 大容量ファイルも安定処理

---

## ⚡ クイックスタート

Cursorでこのフォルダを開いて、以下のコマンドを順番に実行してください：

```bash
# 1. Pythonバージョン確認（3.10以上が必要）
python3 --version

# 2. ffmpegのインストール（音声・動画処理に必須）
# macOS:
brew install ffmpeg

# Windows:
# winget install ffmpeg
# または choco install ffmpeg

# Linux:
# sudo apt install ffmpeg

# 3. 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. 依存関係のインストール
pip install -r requirements.txt

# 5. Playwrightブラウザのインストール
python -m playwright install chromium

# 6. yt-dlpのインストール（Loom動画用）
brew install yt-dlp  # macOS
# winget install yt-dlp  # Windows
# sudo apt install yt-dlp  # Linux

# 7. アプリの起動
python -m app.main
```

ブラウザで http://127.0.0.1:7860 が開きます。APIキーを設定して利用開始！

**⚠️ 重要：ffmpegは必須です！**
- **音声ファイルの文字起こし**
- **動画ファイルからの音声抽出**
- **UTAGE/Loom/スタエフのURL処理**

これらの機能を使う場合は、必ず手順2でffmpegをインストールしてください。

詳細な手順は以下を参照してください。

---

## 🛠️ 開発環境セットアップ（詳細）

このプロジェクトをCursorで開いて、以下の手順でセットアップしてください。

### 前提条件

#### 1. Python 3.10以上のインストール

まずPythonがインストールされているか確認：
```bash
python3 --version
```

**Pythonがインストールされていない場合：**

- **macOS**
  ```bash
  # Homebrewでインストール（推奨）
  brew install python
  
  # または公式サイトからダウンロード
  # https://www.python.org/downloads/
  ```

- **Windows**
  - [Python公式サイト](https://www.python.org/downloads/)からインストーラーをダウンロード
  - または Microsoft Store から「Python 3.12」をインストール
  - **重要**: インストール時に「Add Python to PATH」にチェック

- **Linux**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip
  ```

#### 2. ffmpeg（音声・動画処理に必須）

ffmpegがインストールされているか確認：
```bash
ffmpeg -version
```

**ffmpegがインストールされていない場合：**

- **macOS**
  ```bash
  brew install ffmpeg
  ```

- **Windows**
  ```bash
  # wingetでインストール（Windows 10/11）
  winget install ffmpeg
  
  # またはChocolateyでインストール
  choco install ffmpeg
  ```

- **Linux**
  ```bash
  sudo apt install ffmpeg
  ```

---

### セットアップ手順

Cursorでこのフォルダを開いた後、以下を実行してください。

**⚠️ 重要: 仮想環境の使用を強く推奨**
- macOSのHomebrewでPythonをインストールした場合は**必須**
- システム全体にインストールするとPEP 668エラーが発生します

#### 1. **Pythonバージョンの確認**

```bash
python3 --version
```

**Python 3.10以上が必要です**。3.9以下だと型ヒント構文エラーが発生します。

複数のPythonバージョンがインストールされている場合：
```bash
# 利用可能なバージョンを確認
which python3.10
which python3.11
which python3.12

# 最新バージョンを使用（例: 3.12）
python3.12 --version
```

#### 2. **仮想環境の作成と有効化**

```bash
# 仮想環境の作成（3.10以上のバージョンを指定）
python3 -m venv venv
# または明示的にバージョン指定
python3.12 -m venv venv

# 仮想環境の有効化
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

仮想環境が有効化されると、プロンプトに `(venv)` が表示されます。

#### 3. **依存関係のインストール**

```bash
pip install -r requirements.txt
```

**✅ 依存関係の競合を解決済み：**
- このプロジェクトは `google-genai`（新しいGeminiクライアント）を使用
- 古い `google-generativeai` は削除済み
- クリーンインストールで問題なく動作します

#### 4. **Playwrightブラウザのインストール**

```bash
python -m playwright install chromium
```

これでLP OCR機能に必要なChromiumブラウザがインストールされます。

**注意**: `pip install playwright` だけではブラウザはインストールされません。上記コマンドが必須です。

#### 5. **yt-dlpのインストール（Loom動画用）**

```bash
# macOS
brew install yt-dlp

# Windows
winget install yt-dlp

# Linux
sudo apt install yt-dlp
```

yt-dlpがインストールされているか確認：
```bash
yt-dlp --version
```

**注意**: 
- Loom動画のダウンロードにのみ必要です
- `pip install -r requirements.txt`でも自動的にインストールされますが、システム全体で使用する場合は上記の方法が推奨されます
- 音声ファイルや他の機能は影響を受けません

#### 6. **APIキーの取得**

以下のサービスでAPIキーを取得してください：

- **Groq API Key**（必須 - 文字起こし用）
  1. [Groq Console](https://console.groq.com/keys)にアクセス
  2. アカウント作成（無料）
  3. 「Create API Key」でキーを作成
  4. `gsk_...`で始まるキーをコピー

- **Google AI Studio API Key**（必須 - OCR用）
  1. [Google AI Studio](https://aistudio.google.com/app/apikey)にアクセス
  2. Googleアカウントでログイン
  3. 「Create API Key」でキーを作成
  4. キーをコピー

**💡 APIキーの設定方法：**
- アプリ起動後、UI上部の「APIキー設定」で入力できます

#### 7. **アプリの起動**

```bash
python -m app.main
```

ブラウザで http://127.0.0.1:7860 が自動的に開きます。

**✅ 起動成功すると：**
- GradioのUIが表示されます
- 「LPスクショ + Gemini」「音声→文字起こし」「UTAGE/Loom/スタエフ文字起こし」「動画→高速文字起こし」の4タブが表示されます
- 上部でAPIキーを設定できます

**起動確認コマンド：**
```bash
# アプリが起動したか確認
curl -s http://127.0.0.1:7860/ | head -5
# または直接ブラウザでアクセス
```

### 🪟 Windows環境での注意事項

**絵文字の表示について：**
このアプリは絵文字（🎵, 📸, ✅, 🧠 など）を多用していますが、**Windows環境でも正常に動作するよう最適化されています**。

- **ブラウザUI**: 問題なく絵文字が表示されます（UTF-8で処理）
- **コンソールログ**: 全てのモジュールで自動的にUTF-8に変換されます

**v2.1での対応内容：**
以下のファイルで Windows cp932エラーを完全に回避しています：
- `app/main.py` - メインアプリ
- `app/job_manager.py` - ジョブ管理
- `app/modules/lp_gemini.py` - スクショOCR
- `app/modules/groq_transcribe.py` - 文字起こし
- `app/modules/hls_extractor.py` - 音声抽出

各モジュールで以下のコードを追加し、Windows環境でも確実に動作するようにしています：
```python
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
```

**それでもcp932エラーが出る場合：**

1. **PowerShellで起動する場合：**
   ```powershell
   # UTF-8に切り替え
   chcp 65001
   
   # アプリを起動
   python -m app.main
   ```

2. **コマンドプロンプトで起動する場合：**
   ```cmd
   chcp 65001
   python -m app.main
   ```

3. **VS Code等のIDEで起動する場合：**
   - ターミナルの設定でUTF-8を有効化してください
   - VS Code: `settings.json`に `"terminal.integrated.defaultProfile.windows": "PowerShell"` を追加

**注意：**
- Windows 10/11の最新版では通常問題ありません
- 古いWindows環境では `chcp 65001` が必要な場合があります
- ブラウザUI（Gradio）は常に正常に動作します（コンソールログのみの問題）

---

## 📂 プロジェクト構成

```
moji_booster/
├── app/
│   ├── __init__.py           # パッケージ初期化
│   ├── main.py              # メインアプリケーション（Gradio UI）
│   ├── job_manager.py       # ジョブキュー管理
│   └── modules/
│       ├── groq_transcribe.py    # Groq Whisper文字起こし
│       ├── hls_extractor.py      # HLS音声抽出
│       └── lp_gemini.py          # Gemini OCR
└── requirements.txt         # Python依存関係
```

---

## 🔧 主要モジュール

### `app/main.py`
- Gradio UIの構築
- 4タブ構成：LPスクショ / 音声文字起こし / URL文字起こし / 動画文字起こし
- APIキー管理（セッション別）
- ジョブキューによる並列処理

### `app/modules/groq_transcribe.py`
- pydubで音声をチャンク分割
- Groq Whisper APIに並列リクエスト
- 最大20並列処理で高速化
- 動画ファイルにも対応（音声抽出）

### `app/modules/lp_gemini.py`
- Playwrightでタイル撮影（大きなページも対応）
- Pillowで画像結合
- Gemini APIでOCR（gemini-2.5-flash、フォールバック対応）
- スクリーンショット品質チェック機能

### `app/modules/hls_extractor.py`
- ffmpegでHLSストリームから音声抽出
- .m3u8ファイルからmp3を生成
- Loom、スタンドFM、UTAGE対応

---

## 💡 使い方

### 1. LPスクショ + Gemini文字起こし

1. 「LPスクショ + Gemini」タブを選択
2. URLを入力（例: `https://example.com`）
3. 「📸 スクショを撮影」をクリック
4. スクリーンショットの品質を確認
5. 「✅ このスクショで文字起こし」をクリック
6. 結果が表示されます

### 2. 音声文字起こし

1. 「音声→文字起こし」タブを選択
2. 音声ファイルをドラッグ&ドロップ（mp3, wav, m4a, etc.）
3. 「▶ 文字起こしを実行」をクリック
4. 処理完了後、テキストエリアに結果が表示されます
5. 「📋 テキストをコピー」でコピー可能

**対応フォーマット：**
- mp3, wav, m4a, aac, ogg, flac, mp4, webm

**最大ファイルサイズ：**
- 500MB（設定変更可能）

### 3. UTAGE/Loom/スタエフ文字起こし

1. 「UTAGE/Loom/スタエフ文字起こし」タブを選択
2. URLを入力（改行で複数可能）
   - UTAGE: `.m3u8`のURL
   - Loom: `https://luna.loom.com/...` または `https://www.loom.com/share/...`
   - スタンドFM: `https://cdncf.stand.fm/audios/xxxx.m4a`
3. 「▶ ダウンロード→文字起こし」をクリック
4. 結果が表示されます

### 4. 動画文字起こし

1. 「動画→高速文字起こし」タブを選択
2. 動画ファイルをドラッグ&ドロップ（mp4, mov, webm等）
3. 「▶ 動画から文字起こし」をクリック
4. 音声が抽出され、文字起こしが実行されます

**対応フォーマット：**
- mp4, mov, m4v, webm, mkv

---

## 🐛 トラブルシューティング

### ❌ Windows環境での絵文字エラー (cp932)

**症状：**
```
'cp932' codec can't encode character '\U0001f9e0' in position 0: illegal multibyte sequence
```

**原因：**
- Windowsのデフォルト文字コード（cp932 / Shift_JIS）が絵文字を扱えない
- 古いコンソール環境でUTF-8が有効化されていない
- 複数のモジュール（マルチスレッド/マルチプロセス）で絵文字が使われている

**解決策（v2.1で完全対応済み）：**

✅ **このエラーは v2.1 で完全に修正されています！**

以下の5つのモジュール全てにUTF-8強制コードを追加しました：
1. `app/main.py` - メインアプリ
2. `app/job_manager.py` - ジョブ管理
3. `app/modules/lp_gemini.py` - スクショOCR（🧠絵文字を使用）
4. `app/modules/groq_transcribe.py` - 文字起こし
5. `app/modules/hls_extractor.py` - 音声抽出（🎵絵文字を使用）

**それでもエラーが出る場合：**

1. **最も簡単な方法：PowerShellで起動**
   ```powershell
   # UTF-8モードで起動
   chcp 65001
   python -m app.main
   ```

2. **環境変数を設定（推奨）**
   ```powershell
   # PowerShellのプロファイルに追加（永続化）
   $PROFILE | notepad
   # 以下を追加：
   [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
   ```

3. **VS Code / PyCharmで起動する場合**
   - ターミナルを UTF-8 モードにする
   - VS Code: `settings.json`に以下を追加
     ```json
     {
       "terminal.integrated.defaultProfile.windows": "PowerShell",
       "terminal.integrated.profiles.windows": {
         "PowerShell": {
           "source": "PowerShell",
           "args": ["-NoExit", "-Command", "chcp 65001"]
         }
       }
     }
     ```

**動作確認：**
- ✅ ブラウザUI（Gradio）は問題なく絵文字を表示します
- ✅ コンソールログも正常に絵文字が出力されます（v2.1で修正済み）
- ✅ Windows 10/11の最新版では通常問題ありません

**まだエラーが出る場合：**
- PowerShellではなく**コマンドプロンプト**を使っている可能性があります
- `chcp 65001` を実行してからアプリを起動してください
- または、PowerShellを使用してください（推奨）

---

### ❌ ffmpegが見つからない（最重要！）

**症状：**
```
RuntimeError: ffmpegが見つかりません
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**原因：**
音声・動画処理に必須の ffmpeg がインストールされていません。

**解決策：**
```bash
# macOS
brew install ffmpeg

# Windows
winget install ffmpeg
# または
choco install ffmpeg

# Linux
sudo apt install ffmpeg
```

**インストール確認：**
```bash
ffmpeg -version
```

バージョン情報が表示されればOKです。

**注意：**
- ✅ **このツールの主要機能（音声文字起こし、動画処理、URL抽出）は全てffmpegが必要です**
- ✅ 仮想環境の外（システム全体）にインストールしてください
- ✅ インストール後、ターミナルを再起動してパスを反映させてください

---

### ❌ Python 3.9での型ヒント構文エラー

**症状：**
```
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

**原因：**
- このプロジェクトはPython 3.10+の新しい型ヒント構文（`str | None`）を使用
- Python 3.9以下では動作しません

**解決策：**
```bash
# Pythonバージョンを確認
python3 --version

# 3.10以上をインストール
# macOS
brew install python@3.12

# 明示的にバージョン指定して実行
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ PEP 668エラー（外部管理環境）

**症状：**
```
error: externally-managed-environment
This environment is externally managed
```

**原因：**
- macOSのHomebrewでインストールしたPythonは外部管理環境
- システム全体へのインストールが制限されています

**解決策：**
```bash
# 仮想環境を使用（推奨）
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# または --break-system-packages（非推奨）
pip install -r requirements.txt --break-system-packages
```

**⚠️ macOS Homebrew環境では仮想環境が必須です**

### ❌ 依存関係の競合（websockets等）

**症状：**
```
ERROR: Cannot install ... because these package versions have conflicting dependencies.
```

**解決策：**
```bash
# 既存の環境をクリーンアップ
pip uninstall google-generativeai -y
pip uninstall google-genai -y

# 再インストール
pip install -r requirements.txt
```

このプロジェクトは `google-genai`（新しいクライアント）のみを使用しています。古い `google-generativeai` は不要です。

### ❌ "python: command not found"

**解決策：**
```bash
# macOS/Linux
python3 -m app.main

# Windows
py -m app.main
```

または、Pythonをインストールしてください（前提条件を参照）。

### ❌ "pip: command not found"

**解決策：**
```bash
# macOS/Linux
python3 -m pip install -r requirements.txt

# Windows
py -m pip install -r requirements.txt
```

### ❌ Playwrightエラー

**解決策：**
```bash
python -m playwright install chromium --force

# システム依存関係のインストール（Linuxの場合）
python -m playwright install-deps chromium
```

### ❌ ポート衝突（7860番ポートが既に使用中）

**解決策：**
```bash
# 使用中のポートを確認
lsof -i :7860

# プロセスを終了
kill -9 [PID]
```

または、`app/main.py`の最後の行を編集してポートを変更：
```python
server_port=7860  # ← ここを変更（例: 7861）
```

### ❌ "APIキーが無効です"

**解決策：**
1. Groq API Key: `gsk_`で始まる正しいキーか確認
2. Gemini API Key: [Google AI Studio](https://aistudio.google.com/app/apikey)で再取得
3. キーにスペースや改行が入っていないか確認

### ❌ "ModuleNotFoundError"

**解決策：**
```bash
pip install -r requirements.txt
```

特定のパッケージが見つからない場合：
```bash
pip install [パッケージ名]
```

---

## 🎨 カスタマイズ

### UIのポート変更

`app/main.py`の最後の行を編集：
```python
app.launch(
    server_port=7860,  # ← ここを変更
    share=False
)
```

### チャンクサイズの変更

音声ファイルの分割サイズを変更する場合、環境変数を設定：
```bash
export CHUNK_SEC=30  # デフォルト: 25秒
```

---

## 🔗 関連リンク

- [Groq](https://groq.com/) - 高速Whisper API
- [Google Gemini](https://ai.google.dev/) - OCR API
- [Gradio](https://gradio.app/) - UI フレームワーク
- [Playwright](https://playwright.dev/) - ブラウザ自動化

---

## 🆘 サポート

問題が発生した場合：

1. このREADMEの「トラブルシューティング」セクションを確認
2. エラーメッセージをコピーして検索
3. 環境（OS、Pythonバージョン）を確認

---

**🎉 Happy Coding!**