# 🌲 Background Layer Spec: "Deep Forest Parallax" by Mia

## 🧩 Layer Configuration (Z-Index order)
1. **Layer 0 (Deepest/Static)**: `bali-bg` (Gradient + Sunset Image).
2. **Layer 1 (Forest Silhouette)**: 遠景の森。スクロールの0.2倍速で動く。霧(Mist)のエフェクトを薄く重ねる。
3. **Layer 2 (Main Forest)**: 中景の森。スクロールの0.5倍速。
4. **Layer 3 (Animated Leaves/Rain)**: 近景。マウスの動きに僅かに揺れる葉の影、または静かな雨滴。1.2倍速。

## 🎨 Visual Assets (Kaiへの指示)
- 各レイヤーは `absolute` 配置のフルスクリーンコンテナとする。
- 背景画像がない部分は `transparent` にし、背後が透けるように。
- **Leo's Suggestion**: 初期プロトタイプでは、画像アセットを待たずに「SVGのシンプルな図形やCSSグラデーション」で奥行きの動きを検証する。

## 💬 Mia's Note
「いきなり完璧な画像を探すより、まずは『動きの気持ちよさ』を Kai に作ってもらいます。背景が何層にも重なってズレて動くだけで、サイトの高級感が一気に上がりますよ。」
