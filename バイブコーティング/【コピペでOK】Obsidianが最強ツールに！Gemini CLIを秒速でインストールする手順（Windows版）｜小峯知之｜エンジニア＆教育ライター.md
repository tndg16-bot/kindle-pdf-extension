---
title: "【コピペでOK】Obsidianが最強ツールに！Gemini CLIを秒速でインストールする手順（Windows版）｜小峯知之｜エンジニア＆教育ライター"
source: "https://note.com/csfive/n/nd5a41a6e0333?magazine_key=m8acd92ce4f40"
author:
  - "[[小峯知之｜エンジニア＆教育ライター]]"
published: 2025-07-06
created: 2025-08-06
description: "「Obsidianのめんどうな操作は、Geminiにお願いしたい！」    「けれどもGemini CLIってなんか難しそう…」    「でもGemini 2.5 PROがGoogleアカウントさえあれば無料は魅力.…」    この記事では、Windowsパソコンをお使いのすべての方、特にプログラミング経験のない方でも安心して設定できるよう、コピー＆ペースト中心のステップ・バイ・ステップで、Obsidian×Gemini CLIを構築する方法をお伝えしていきます。  10分後にはこんな画面になっていますよ！     ▼Udemy ChatGPT講座｜AIライティングの土台固めに最適！▼"
tags:
  - "clippings"
---
![見出し画像](https://assets.st-note.com/production/uploads/images/200428219/rectangle_large_type_2_68d32e6954b35c68705f07023a2b0540.png?width=1200)

## 【コピペでOK】Obsidianが最強ツールに！Gemini CLIを秒速でインストールする手順（Windows版）

[小峯知之｜エンジニア＆教育ライター](https://note.com/csfive)

- **「Obsidianのめんどうな操作は、Geminiにお願いしたい！」**
- **「けれどもGemini CLIってなんか難しそう…」**
- **「でもGemini 2.5 PROがGoogleアカウントさえあれば無料は魅力.…」**

この記事では、Windowsパソコンをお使いのすべての方、特に **プログラミング経験のない方** でも安心して設定できるよう、コピー＆ペースト中心のステップ・バイ・ステップで、Obsidian×Gemini CLIを構築する方法をお伝えしていきます。

10分後にはこんな画面になっていますよ！

  

▼Udemy ChatGPT講座｜AIライティングの土台固めに最適！▼

**＞＞** [**無料クーポンはこちら**](https://www.udemy.com/course/markdown-ai/?couponCode=NOTEFREERADIO) **＜＜**

（★4.4のChatGPT講座が～2025/8/16まで無料！）

  

![画像](https://assets.st-note.com/img/1751763049-ptJzSFNCARjiP1Tobh2DWuUc.png?width=1200)

Obsidian × Gemini CLI

実は簡単なので、一緒にセットアップしていきましょう。

  

## ステップ1：準備編 - 必要なツールを揃えよう

まず、Geminiを動かすための土台となる「Node.js」というツールをPCにインストールします。

「Node.jsって何？」と不安に思う必要はありません。これは、便利なツール（今回の場合はGemini）をあなたのPC上で動かすための\*\*「共通の実行エンジン」\*\*のようなものだと思ってください。これを一つ入れておくだけで、世界中の様々な便利ツールが使えるようになります。

① [Node.js公式サイト](https://nodejs.org/ja) にアクセスします。

② 緑色のボタンをクリックします。

![画像](https://assets.st-note.com/img/1751762302-tcoisQg80YrFRLaZfV4OGNHS.png?width=1200)

Node.jsのインストール

③ Windoesインストーラー（.msi）をクリックします。

![画像](https://assets.st-note.com/img/1751762374-FDvAQSnf0UytCOqioeEkzKhB.png?width=1200)

Node.jsのインストール

④ ダウンロードしたファイルを開き、あとはインストーラーの指示に従って「Next」や「Install」をクリックしていくだけで完了です。特に設定を変える必要はありません。

これで、最初の準備は完了です。簡単でしたね。

> Node.jsが何かわからなくても、まったく問題ないです。簡単にいえば、Node.jsはGemini CLIを動かす「土台」を意味します。

  

## ステップ2：インストール編 - Gemini CLIをWindowsに入れよう

次に、主役である「Gemini CLI」をあなたのPCにインストールします。CLIとは「コマンドライン・インターフェース」の略ですが、要は「コマンド（命令文）で動くGemini」のことです。しかも月額数千円のGeminiが無料で使えます。

1. キーボードの **Windowsキー** を押し、検索バーに「 **cmd** 」と入力します。「 **コマンド プロンプト** 」というアプリが表示されるので、クリックして起動してください。黒い画面が出てきても、怖がらなくて大丈夫です。
2. 表示された黒い画面に、以下のコマンドをコピー＆ペーストして、Enterキーを押してください。

**👇これをCtrl+Cでコピーし、Ctrl＋Vで張り付けてENTERでOK  
**

![画像](https://assets.st-note.com/img/1751763366-PAtI8Yj91vhCzbS6aqcTW0Bn.png?width=1200)

張り付けたらENTERを押すだけ

```
npm install -g @google/gemini-cli
```

  

## ステップ3： WindowsにGeminiの居場所を教えよう（最重要）

さて、ここが **この記事で最も重要** で、あなたのPCを一つ上のステージに引き上げるためのステップです。

今の状態は、あなたの家に優秀な執事（Gemini）がやってきたのに、あなたがその執事室の場所を知らないようなものです。これから、PCに「geminの居場所」と、その居場所への道筋（Path）\*\*を教えてあげます。

1. **Geminiの居場所を確認する**
	1. 先ほどの黒い画面（コマンドプロンプト）で、以下のコマンドを打ち込んでEnterキーを押してください
	2. **「npm config get prefix」** の **npm～prefix** を **cmd** にコピペします（ **Ctrl+C→Ctrl＋V** ）
	3. C:\\Users\\あなたのユーザー名\\AppData\\Roaming\\npm のような **パス（文字列）** が表示されるはずです。これがGeminiの居場所です。この文字列を **マウスで選択** して **CTRL＋Cでコピー** し、 **メモ帳** などに貼り付けておきましょう。
2. **Windowsに道筋を教える**
	1. さあ、いよいよ設定です。画像を見ながら、ゆっくり進めていきましょう。
	2. ① キーボードの **Windowsキー** を押し、「 **環境変数** 」と入力。「 **システム環境変数の編集** 」をクリックします。
	3. ② 出てきたウィンドウで「 **環境変数...**」ボタンをクリックします。
	4. ③ 上半分の「 **ユーザー環境変数** 」のリストから「 **Path** 」を選び、「 **編集...**」ボタンをクリックします。
	5. ④ 右側の「 **新規** 」ボタンを押し、先ほどメモ帳にコピーした **Geminiの居場所のパス** を貼り付けます。
	6. ⑤ 「OK」ボタンをすべてのウィンドウで押して、設定を完了します。
3. **確認作業**
	1. 新しいコマンドプロンプトを起動して（ここ重要です！）、以下のコマンドを打ってみてください。

```
gemini --version
```

下記画面のようにバージョン番号がでれば成功です！

  

![画像](https://assets.st-note.com/img/1751763773-EGuVJyeROZiInHLW9dc1krPB.png)

geminiのパスがとおった

## ステップ4：実践編 - ObsidianからGeminiを呼び出そう！

いよいよObsidianとの連携です。ここでは、Obsidianの非常に便利なプラグイン「 **Obsidian Terminal** 」を使います。

1. **プラグインのインストール**
	- Obsidianの「左下の⚙設定」→「コミュニティプラグイン」を開き、「閲覧」をクリックします。
	- 検索窓に「 **Terminal** 」と入力し、出てきたプラグインをインストールし、 **有効化** します。

するとObsidian画面の左メニューに下記の緑枠のように四角いボタンが出現します。  

![画像](https://assets.st-note.com/img/1751763981-B2t05HhPTJWpSbVL4IU8ZN76.png?width=1200)

Terminalを起動するボタン

  

このボタンを押すと、画面上部に選択肢がでてきます。そこで、

**"".integrated. win32IntegratedDefault.**

を選択！ すると画面下部にcmdのような真っ黒いコンソールが出現しますね。

  

![画像](https://assets.st-note.com/img/1751764262-ElB7QracNMVmq3oHjTCOzxfp.png?width=1200)

Obsidianでコンソールを開いたところ

この黒いコンソール。なにやら難しいオーラを放っていますが、実はめちゃくちゃ簡単です。

ただたんに、

**gemini**

とだけ入力し、Enterを押すだけ！

10秒～30秒ほど待っていると…

  

![画像](https://assets.st-note.com/img/1751764517-Dodfi6Q38nwjmMgxRB91utcY.png?width=1200)

Obsidianでgeminiが使える状態に！

あとは下方向にスクロールすると、

  

![画像](https://assets.st-note.com/img/1751764589-Ydh8RZ26JeWLCn543A9rVSUw.png?width=1200)

上記画像のように「質問ボックス」が出てきます。

例えば、

> 「Gemini CLIをObsidianで使い倒すコツ」についてのノートを新規作成して完成させて

と入力してみましょう。

  

![画像](https://assets.st-note.com/img/1751765008-qMDyU8h6HxRrfXz0BoF4bIOW.png?width=1200)

無事に新規ノートが作成されました！

今後は要約に翻訳、ブレストなどなど、なんでもござれです。

> **【使い方のコツ】  
> **半角「 **@** 」を入力すると参照してほしいノートを選択できます。

## まとめ：あなたの知的生産は、今日から新しいステージへ

少し手順は多かったかもしれませんが、一つ一つは簡単な作業だったはずです。

あなたは今、Obsidianから離れることなく、思考の流れを止めずに、いつでもAIの力を借りられる環境を手に入れました。

- 長文の議事録を選択して、 **要点を抽出する** 。
- 新しいアイデアのキーワードを選択して、 **関連アイデアをブレインストーミング** してもらう。
- 書いた文章を選択して、 **より良い表現にリライト** してもらう。

使い方は無限大です！

---

▼Udemy ChatGPT講座｜AIライティングの土台固めに最適！▼

**＞＞** [**無料クーポンはこちら**](https://www.udemy.com/course/markdown-ai/?couponCode=NOTEFREERADIO) **＜＜**

（★4.4のChatGPT講座が～2025/8/16まで無料！）

## いいなと思ったら応援しよう！

![](https://d2l930y2yx77uc.cloudfront.net/assets/default/default_magazine_header-fcef937b52acc29928856475838f16e16c530559fc5e72d04d56d795ceb0dc0f.png?width=200)

### Obsidian関連

- 205本

![](https://assets.st-note.com/production/uploads/images/167921646/magazine_cover_landscape_878d7b15d7edf7e0279a819c7a5aab1d.png?width=200)

### Obsidianの使い方講座

- 20本

![](https://d2l930y2yx77uc.cloudfront.net/assets/default/default_magazine_header-fcef937b52acc29928856475838f16e16c530559fc5e72d04d56d795ceb0dc0f.png?width=200)

### AI＆ChatGPT

- 171本

![](https://d2l930y2yx77uc.cloudfront.net/assets/default/default_magazine_header-fcef937b52acc29928856475838f16e16c530559fc5e72d04d56d795ceb0dc0f.png?width=200)

### AIツール

- 7本

![](https://d2l930y2yx77uc.cloudfront.net/assets/default/default_magazine_header-fcef937b52acc29928856475838f16e16c530559fc5e72d04d56d795ceb0dc0f.png?width=200)

### Obsidian

- 17本

## コメント

【コピペでOK】Obsidianが最強ツールに！Gemini CLIを秒速でインストールする手順（Windows版）｜小峯知之｜エンジニア＆教育ライター