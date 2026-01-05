import type { Metadata } from "next";
import { Inter, Noto_Sans_JP } from "next/font/google";
import "./globals.css";
import { LiquidCursor } from "@/components/LiquidCursor";
import { SectionBackground } from "@/components/SectionBackground";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const notoJP = Noto_Sans_JP({
  variable: "--font-noto-jp",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "本山 貴裕 | Life Self-Determination",
  description: "「ノウハウ依存」から「人生の自己決定」へ。AIと哲学で、自律的な人生をデザインする。",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja" className="scroll-smooth">
      <body className={`${inter.variable} ${notoJP.variable} font-sans antialiased bali-bg overflow-x-hidden`}>
        <SectionBackground />
        <LiquidCursor />
        {children}
      </body>
    </html>
  );
}
