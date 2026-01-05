# 🎨 Visual Spec: "Bali Forest" by Mia

## 🧩 Color Palette (Extracted from Images)
- **Deep Dusk**: `hsl(260, 40%, 15%)` - バリの夕暮れの深い紫。
- **Sunset Ember**: `hsl(15, 90%, 60%)` - 残照のオレンジ。
- **Tropical Moss**: `hsl(140, 30%, 25%)` - 湿り気のある森の緑。
- **Liquid Pearl**: `hsl(190, 100%, 95%)` - 水面きらめき、水滴の白。

## 🎬 Animation Parameters
- **Fluidity**: `ease: [0.22, 1, 0.36, 1]` (Smooth Out)
- **Parallax Speed**:
    - Fore (Rain/Leaves): `1.2x scroll`
    - Mid (The Bali Structure): `1.0x scroll`
    - Back (Forest Silhouette): `0.5x scroll`

## 💬 Mia's Note
「本山さん、画像の『光の入り方』が本当に美しいです。これを直接的な画像だけでなく、CSSのグラデーション・オーバーレイで表現して、時間やマウスの動きで光が差し込む角度が変わるように設計しています。Kai、このパラメータをFramer Motionの `useTransform` で制御できる？」
