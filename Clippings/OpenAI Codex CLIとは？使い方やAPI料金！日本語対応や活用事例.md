---
title: "OpenAI Codex CLIとは？使い方やAPI料金！日本語対応や活用事例"
source: "https://miralab.co.jp/media/openai-codex-cli/"
author:
  - "[[平岡将和]]"
published: 2025-04-24
created: 2025-08-15
description: "OpenAI Codex CLIは、ターミナル上で動作するマルチモーダルに対応したコーディングエージェントです。 コードの読み取り・編集・実行にはAPIが必要となるので、無料では利用できませんが、UIやゲームなどを簡単に自動で作成できます。"
tags:
  - "clippings"
---
![](https://miralab.co.jp/media/wp-content/uploads/2025/04/399.png)

OpenAI Codex CLIは、ターミナル上で動作するマルチモーダルに対応したコーディングエージェントです。

コードの読み取り・編集・実行にはAPIが必要となるので、無料では利用できませんが、UIやゲームなどを簡単に自動で作成できます。

この記事では、OpenAI Codex CLIの使い方やAPI料金、そして日本語対応状況や活用事例などを解説します。

## OpenAI Codex CLIとは？

OpenAI Codex CLIとは、OpenAIが2025年4月16日にリリースした **コーディングエージェント** です。

まずはOpenAI Codex CLIの概要と特徴を見ていきましょう。

### OpenAI Codex CLIの概要

OpenAI Codex CLIは **ターミナルで動作するオープンソースの軽量コーディングエージェントです。**

自然言語で指示を出すことで、コードの生成、実行、改善ができます。

セットアップは不要であり、OpenAIのAPI キーがあればすぐに利用可能です。

また、 **ローカルで実行されるため、共有を選択しない限り、ソースコードは環境外に持ち出されることはありません。**

### OpenAI Codex CLIの特徴

OpenAI Codex CLIは **マルチモーダル** 入力に対応しており、テキスト、スクリーンショット、または図を渡すと、エージェントがそれに応じてコードを生成または編集可能です。

OpenAI Codex CLIと似たツールに、同じくターミナルで動作するAnthropicのClaude Codeがありますが、こちらはマルチモーダル入力に対応していません。

**ターミナル環境でもマルチモーダル入力を受け付けられるのはOpenAI Codex CLIの利点でしょう。**

また、従来のコード生成AIはプラグインなどを使ってコードエディタで動作するものでしたが、OpenAI Codex CLIはコマンドラインで動作します。

そのため、ネットワークを無効化し、ディレクトリをサンドボックス化することで、 **安全かつセキュアに完全自動動作させることもできます。**

## OpenAI Codex CLIの導入方法

OpenAI Codex CLIは、 **セットアップ不要** で簡単に導入することができます。

OpenAI Codex CLIは以下の手順で導入できます。

STEP

WSL2のインストール（Windowsユーザーの場合）

OpenAI Codex CLIは動作プラットフォームとしてMacOSとLinuxが公式にサポートされており、Windowsで使いたい場合には **WSL2（Windows Subsystem for Linux）** が必要となります。

WSL2は、Windows上でLinuxを仮想的に動かすことができるシステム環境であり、 **Ubuntu** というLinuxディストリビューションが採用されています。

まず、Windows PowerShellを管理者として実行し、以下のコマンドを実行します。

```
wsl --install
```

インストールが完了した後、以下のコマンドでUbuntuを起動できます。

```
wsl.exe -d Ubuntu
```

起動すると、ユーザー名とパスワードの設定を求められます。

設定が完了したら、WSL2が使用できるようになります。

コマンドプロンプトで `wsl -l -v` と入力し、応答があれば大丈夫です。

STEP

Node.jsのインストール

OpenAI Codex CLIをインストールするには、Node.jsが必要です。

バージョン22以上のLTSが推奨されているので、お使いの環境に入っていない場合はインストールしましょう。

[Node.jsの公式サイト](https://nodejs.org/en/download/) から自分の環境に合ったインストーラを選択してダウンロードします。

インストーラを起動して、Node.jsをインストールします。

インストールが正常に完了したかどうかは、以下のコマンドで確認できます。

```
node -v
npm -v
```

なお、 **WindowsユーザーはWSL2のUbuntuにインストールする必要がある** ので気を付けてください。

以下のコマンドを実行した後、ターミナルを再起動します。

```
sudo apt update && sudo apt install curl build-essential #必要なパッケージのインストール
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash #nvmのインストール
```

nvmを使用すると複数のNode.jsバージョンを管理できます。

以下のコマンドで、WSL2にNode.jsをインストールできます。

```
nvm install 22.14.0 #v22.14.0をインストール
node use 22.14.0    #v22.14.0をデフォルトに設定
```

STEP

インストール

以下のコマンドを実行してCodexをインストールします。

```
npm install -g @openai/codex
```

STEP

OpenAI APIキーを取得

OpenAI Codex CLIを使用するにはOpenAIの **APIキー** が必要です。

[OpenAI Platform](https://platform.openai.com/api-keys) にアクセスしてログインします。

アカウントを持っていない方はアカウント登録をしましょう。

「API keys」タブを選択し、「Create new secret key」をクリックします。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/24ffbf73aac5d6921bb4b3a6798e3917-scaled.png)

キーに任意の名前を付け、「Create secret key」をクリックするとキーが発行されます。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/7c8f688b9bca3608a105e02e4a4802b7-1-scaled.png)

作成したAPIキーはコピーして安全に保管しましょう。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/135bd7c33498d922c8d5130648c34a02-scaled.png)

STEP

APIキーを設定

続いて、以下のコマンドでOpenAI APIキーを環境変数として設定します。

```
export OPENAI_API_KEY="your-api-key-here"
```

your-api-key-hereには取得したAPIキーを入力してください。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/c413ecd7274dd9a4fdfb31630975dd32.png)

なお、このコマンドで設定したキーは現在のターミナルセッションでのみ有効です。

永続的に設定したい場合は、シェルの設定ファイル（例：\`~/.zshrc\`, \`~/.bashrc\`）に上記の行を追加してください。

また、API キーをプロジェクトのルートにある.envファイルに配置することもできます。

```
OPENAI_API_KEY=your-api-key-here
```

STEP

実行

APIキーを設定できたら、実行が可能です。

インタラクティブに実行する場合は、以下のコマンドを入力します。

```
codex
```

また、プロンプトを入力に含めることもできます。

```
codex "explain this codebase to me"
```

なお、ホームディレクトリでコマンドを実行すると次のような警告が出ます。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/68bf2861754f9f0644b6d0e7e76efad8.png)

コマンドを実行する際は、適当なリポジトリに移動しておきましょう。

問題なければ、以下のように表示されます。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/2edd5bbb09b3f55980930e2f4366a664-1.png)

## OpenAI Codex CLIの使い方

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/17a0ad132989d275844fe82ce0a6927c.png)

ここからは、OpenAI Codex CLIの具体的な使い方を解説します。

まずは基本コマンドをご紹介します。

### OpenAI Codex CLIの基本コマンド

OpenAI Codex CLIの基本的なコマンドの一覧は以下の通りです。

| コマンド | 内容 | 具体例 |
| --- | --- | --- |
| `codex` | インタラクティブに実行 | `codex` |
| `codex "…"` | 初期プロンプトを入力して実行 | `codex "explain this codebase to me"` |
| `codex -q "…"` | 非対話型の「静音モード」を実行 | `codex -q --json "explain utils.ts"` |
| `codex completion <bash\|zsh\|fish>` | シェル補完スクリプトを出力 | `codex completion bash` |
| `codex -m` | モデルを選択 | `codex -m o4-mini` |
| `codex -i` | ファイルを入力として実行 | `codex -i screenshot.png` |
| `codex -d` | 作業ディレクトリを指定 | `codex -d ~/projects` |
| `codex --suggest` | Suggestモードで起動 | `codex --suggest` |
| `codex --auto-edit` | Auto Editモードで起動 | `codex --auto-edit` |
| `codex --full-auto` | Full Autoモードで起動 | `codex --full-auto` |
| `codex --upgrade` | Codexの更新 | `codex --upgrade` |
| `codex --help` | ヘルプを表示 | `codex --help` |

OpenAI Codex CLIでは、 **実行にあたりユーザーがどの程度直接的に承認を行うかを、3つのモードから選択できます。**

それぞれのモードの概要は以下のようになっています。

| モード       | エージェントができること                                                                | 使用場面                           |
| --------- | --------------------------------------------------------------------------- | ------------------------------ |
| Suggest   | ファイルの読み込みが可能。編集やシェルコマンドを提案するが、変更やコマンド実行の前に承認が必要。                            | 安全な探索・コードレビュー・コードベースの学習        |
| Auto Edit | 自動的なファイルの読み書きが可能。シェルコマンドを実行する前には承認が必要。                                      | リファクタリングや反復的な編集において副作用に注意したい場合 |
| Full Auto | カレントディレクトリをスコープとする、サンドボックス化されたネットワーク無効化環境内で、自律的にコマンドの読み取り、書き込み、実行を行う。承認は不要。 | 壊れたビルドの修復・機能のプロトタイプの作成など長時間の作業 |

なお、デフォルトはSuggestモードとなっています。

### OpenAI Codex CLIの使用例

この記事では、OpenAI Codex CLIの使用例として、 **スクリーンショットからUIを作成していきます。**

今回は、Amazonのサイトのスクリーンショットを入力し、UIを再現してもらいました。

使用したスクリーンショットはこちらです。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/ad9f3b96a407a051d8e439a371187ea3-scaled.png)

出典： [Amazon](https://www.amazon.co.jp/?&tag=hydraamazonav-22&ref=pd_sl_8eaqjij3p0_e&adgrpid=157529193801&hvpone=&hvptwo=&hvadid=675152705458&hvpos=&hvnetw=g&hvrand=11843768342975043369&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9198481&hvtargid=kwd-893523692&hydadcr=27920_14701882&gad_source=1)

STEP

スクリーンショットと指示を入力

スクリーンショットが保存されているディレクトリで、以下のコマンドを入力します。

```
codex -i <file_name> "このUIを実装してください"
```

モデルは好みに応じて選びましょう。

STEP

Codexが指示を実行

コマンドを実行すると、Codexが指示に応じてファイルの読み取り、作成を行います。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/a0c10563f8f6f6a82748009d75ae02b5.png)

今回はUIの作成なので、CodexがHTMLファイルを作成しています。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/b90ee6e54b312448cecbac56ff27247d.png)

STEP

コマンドを承認

SuggestモードやAuto Editモードで使用している場合は、Codexがコマンドを実行する際に承認が必要です。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/1dae548c314d934a459de064e0a75591.png)

「Yes」を選択するとCodexがコマンドを実行します。

また、「Explain this command」を選択してコマンドの説明をしてもらうことも可能です。

STEP

完成したファイルを確認

しばらくすると、Codexがファイルを作成し終えます。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/87336e1312a14ef9187b4fbb9ff35c37.png)

今回はUIの作成だったので、HTMLファイル、CSSファイル、JSファイルが作成されていました。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/28a26b6e22770f9601373c77a6ddd9ca.png)

index.htmlを開くと、このようなページができていました。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/feb1f342fb8651499ff214de06e55183-scaled.png)

画像は用意していなかったので入っていませんが、タブや検索バー、ボタンなどは再現されていることがわかります。

また、左上の「すべて」をクリックすると、メニューバーも再現されていました。

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/e3d6010f22f6b14780efe35a9a072685-scaled.png)

Codexを使用すれば、このようにスクリーンショットからUIの大枠を作ることができます。

## OpenAI Codex CLIの活用事例

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/09976bef8c2c4531a9ad8ab0be0f1200.png)

OpenAI Codex CLIは、UIの作成以外にもさまざまな用途で利用できます。

例えば、 **ターミナル上でソースコードの説明をしてもらうことができます。**

また、数回の指示だけで **ゲームを作成** している方もいました。

**アプリの開発** も可能です。

このように、ホームページの作成から、ゲーム・アプリの開発まで、自動で行うことが可能となります。

## OpenAI Codex CLIは無料で使える？API料金を紹介

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/ec842a9e2243be4bc14ee1a4d3009d94.png)

OpenAI Codex CLIの利用にはOpenAIのAPIが必要です。

そのため、 **使用する際に各モデルに応じたAPI料金がかかります。**

現時点における代表的なモデル別の **100万トークンあたり** の料金は以下のようになっています。

| モデル | 入力 | キャッシュされた入力 | 出力 |
| --- | --- | --- | --- |
| gpt-4.1 | $2.00 | $0.50 | $8.00 |
| gpt-4o | $2.50 | $1.25 | $10.00 |
| o1 | $15.00 | $7.50 | $60.00 |
| o3 | $10.00 | $2.50 | $40.00 |
| o4-mini | $1.10 | $0.275 | $4.40 |

基本的に無料での利用はできませんが、 **OpenAIはCodex CLIやその他のOpenAIのAIモデルを使用するプロジェクトの開発者に対し、最大25,000ドル分のAPIクレジットを提供する取り組みを行っています。**

> We’re excited to launch a **$1 million initiative** supporting open source projects that use Codex CLI and other OpenAI models.
> 
> - Grants are awarded in **$25,000** API credit increments.
> - Applications are reviewed **on a rolling basis**.
> 出典： [codex](https://github.com/openai/codex)

プロジェクトでの利用を考えている方は、申請してみることをおすすめします。

## OpenAI Codex CLIの日本語対応状況

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/acf5061c3d5183c0e8705bf80ac74eed.png)

以前のCodexは日本語に非対応でしたが、OpenAI Codex CLIでは使用例でもお見せしたように **日本語での指示に対応しています。**

入力はもちろん、出力も日本語で返ってくるため、ChatGPTを使用する際と同じ感覚で使うことができます。

また、 **画像内の日本語も精度良く読み取れます。**

使用言語については特に心配する必要はないでしょう。

## OpenAI Codex CLIを使う上での注意点

![](https://miralab.co.jp/media/wp-content/uploads/2025/04/a6849875573157c20dffa0472577150e.png)

OpenAI Codex CLIを使用する際は、かかるコストに注意しましょう。

入力に対して毎回APIを呼び出すため、 **何度もやり取りをすると予算以上にコストがかかってしまう可能性があります。**

また、ソースコードを入力する際は **機密保持** にも注意が必要です。

OpenAIのAPIはユーザーがオプトインしない限り学習には利用されず、30日後にデータは消去されます。

> OpenAI は、プラットフォームの説明ページ⁠（新しいウィンドウで開く）にリストアップされた特定のエンドポイントを除き、サービスを提供し不正利用を特定するために、API で入出力されたデータを30日間安全に保持します。30日後には、API の入力と出力は、その保持が法的義務でない限り、当社のシステムから消去されます。
> 
> 出典： [OpenAI におけるエンタープライズプライバシー](https://openai.com/ja-JP/enterprise-privacy/)

ただし、もしオプトインしている場合は入力データを学習に利用されるため、機密情報となるようなソースコードやファイルは入力しないようにしましょう。

## まとめ

OpenAI Codex CLIは、 **ターミナル上で動作するマルチモーダルに対応したコーディングエージェント** であり、UIの作成やゲーム・アプリの開発を自動化できます。

導入は簡単で、APIキーを設定すればすぐに使用可能です。

日本語にも対応しているため、難なく使い始められるでしょう。

ターミナルで利用できるコーディングエージェントを求めている方におすすめのツールです。