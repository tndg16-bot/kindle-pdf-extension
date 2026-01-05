# 🌲 Portfolio Design Concept: "Intelligent Nature x Bali Luxury"

本山さんから提供された「バリのリゾート」画像と「森・風・雨」のコンセプトを融合させたデザイン仕様書です。

## 🎨 Visual Identity (Inspired by Reference Images)
提供された5枚の画像（バリのリゾート：プール、天蓋付きベッド、夕暮れの寺院、水面の反射）から、以下の要素を抽出しました。

- **Lighting**: 
    - 「マジックアワー」の深い紫からオレンジへのグラデーション。
    - 木漏れ日（光が差し込む）の動的な演出。
- **Materials**: 
    - 水面の反射（鏡面効果）。
    - 透過感のある素材と、温かみのある木材・自然素材の質感。
- **Perspective**: 
    - ダイナミックな視点。マクロ（水滴、葉脈）から広角（森の引き、リゾートの全景）までの流れるような切り替え。

## 🌊 Interaction & UX (The Liquid Experience)
「ヌルヌル動く滑らかな質感」を実現するための技術要件。

- **Liquid Cursor**: 
    - マウスカーソルが水滴のように振る舞い、要素に吸い付いたり、後ろに波紋（Trails）を残す演出。
- **Smooth Transition**: 
    - スクロールに合わせて、背景の森やリゾートの画像が「溶けるように」あるいは「風に吹かれるように」切り替わる（WebGL or Framer Motion）。
- **Interactive Rain**: 
    - 画面上を静かに流れる雨滴が、マウスの動きに僅かに反応するインタラクション。

## ⚖️ Immutable Rules for this Build (不変の定義)
1. **Core Concept**: 「人生の自己決定」を主軸とし、それを「リゾートの解放感と森の静謐さ」で包み込むこと。
2. **UX Standard**: 反応速度よりも「情緒的な滑らかさ（Fluidity）」を優先する。
3. **Typography**: Noto Sans JP（ビジネスの信頼性）と、雰囲気に合った美しい明朝体（情緒性）の組み合わせ。

## 📋 Task Checklist for AI Team
- [ ] **Mia (Designer)**: 画像から抽出したカラーパレット（HSL）と、詳細なアニメーション・タイムラインの定義書作成。
- [ ] **Kai (Frontend)**: Liquid Cursorと背景のパララックス・エフェクト（水の質感）の実装調査。
- [ ] **Leo (PM)**: 本山さんへの「用語解説付き」初期プロトタイプ提案書の作成。
