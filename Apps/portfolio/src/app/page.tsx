"use client";

import { motion, Variants } from "framer-motion";
import { ArrowRight, Compass, Cpu, Target, CheckCircle2, Sparkles, Zap, Shield } from "lucide-react";
import Header from "@/components/Header";
import Dashboard from "@/components/Dashboard";
import BookingForm from "@/components/BookingForm";

export default function Home() {
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.8,
        ease: "easeOut"
      }
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center overflow-x-hidden pt-20">
      <Header />
      {/* Hero Section */}
      <section id="section-hero" className="relative flex min-h-screen w-full flex-col items-center justify-center px-4">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={containerVariants}
          className="glass-panel z-10 w-full max-w-4xl rounded-3xl p-8 md:p-16 text-center shadow-2xl backdrop-blur-xl"
        >
          <motion.div variants={itemVariants} className="mb-6 flex justify-center">
            <div className="flex items-center gap-2 rounded-full bg-teal-500/10 px-4 py-1 text-sm font-medium text-teal-400 border border-teal-500/20">
              <Sparkles size={16} />
              <span>Life Self-Determination Protocol</span>
            </div>
          </motion.div>

          <motion.h1
            variants={itemVariants}
            className="mb-6 text-4xl font-bold tracking-tight md:text-7xl leading-tight text-white drop-shadow-sm"
          >
            静寂の中で、<br />
            <span className="text-forest">「自分の直感」</span>を再編する
          </motion.h1>

          <motion.p
            variants={itemVariants}
            className="mb-10 text-lg text-zinc-200 md:text-2xl font-light leading-relaxed max-w-2xl mx-auto"
          >
            溢れる情報と「正解」の押し付けから、魂の呼吸を守り抜く。<br />
            深い静寂の中で研ぎ澄まされる直感と、最先端AIの力が、<br />
            妥協のない「人生の再定義」を静かに加速させます。
          </motion.p>

          <motion.div
            variants={itemVariants}
            className="flex flex-wrap justify-center gap-4"
          >
            <button className="flex h-14 items-center gap-2 rounded-full bg-white px-8 text-lg font-bold text-teal-900 transition-all hover:bg-teal-50 hover:scale-105 active:scale-95 shadow-xl group">
              羅針盤を手にする
              <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </button>
            <a
              href="https://ai-diagnosis-six.vercel.app"
              target="_blank"
              rel="noopener noreferrer"
              className="flex h-14 items-center gap-2 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 px-8 text-lg font-bold text-white transition-all hover:brightness-110 hover:scale-105 active:scale-95 shadow-xl group"
            >
              <Sparkles className="h-5 w-5" />
              無料で適性診断
              <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </a>
            <button className="glass-card flex h-14 items-center gap-2 rounded-full px-8 text-lg font-bold text-teal-50 border border-white/10 hover:bg-white/5 transition-all">
              メソッドを探究する
            </button>
          </motion.div>
        </motion.div>

        {/* Floating Icons Background */}
        <div className="absolute inset-0 z-0 opacity-10">
          {[
            { top: "15%", left: "10%", duration: 6 },
            { top: "25%", left: "80%", duration: 7 },
            { top: "40%", left: "20%", duration: 8 },
            { top: "60%", left: "70%", duration: 6 },
            { top: "75%", left: "30%", duration: 9 },
            { top: "10%", left: "60%", duration: 7 },
            { top: "85%", left: "85%", duration: 10 },
            { top: "50%", left: "5%", duration: 8 },
          ].map((pos, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0 }}
              animate={{
                opacity: [0.1, 0.4, 0.1],
                y: [0, -60, 0],
                x: [0, 30, 0],
              }}
              transition={{
                duration: pos.duration,
                repeat: Infinity,
                delay: i * 0.7,
              }}
              className="absolute text-teal-400/30"
              style={{
                top: pos.top,
                left: pos.left,
              }}
            >
              {i % 3 === 0 ? <Compass size={40} /> : i % 3 === 1 ? <Cpu size={40} /> : <Target size={40} />}
            </motion.div>
          ))}
        </div>
      </section>

      {/* Philosophy Section */}
      <section id="section-philosophy" className="w-full max-w-7xl px-4 py-24 min-h-screen flex items-center">
        <div className="grid gap-8 md:grid-cols-2 lg:gap-12 w-full">
          <motion.div
            whileInView="visible"
            initial="hidden"
            viewport={{ once: true, margin: "-100px" }}
            variants={itemVariants}
            className="glass-panel group relative flex flex-col justify-center rounded-3xl p-10 md:p-14 border border-white/5 hover:border-teal-500/30 transition-all duration-700 bg-black/20"
          >
            <div className="absolute -top-6 -left-6 bg-teal-500/20 p-4 rounded-2xl backdrop-blur-md border border-teal-500/30 text-teal-400 group-hover:scale-110 transition-transform duration-500">
              <Shield size={32} />
            </div>
            <h2 className="mb-6 text-3xl font-bold md:text-5xl leading-tight">
              内なる聖域。<br />
              <span className="text-forest font-light">Spiritual Resilience</span>
            </h2>
            <p className="mb-8 text-zinc-300 leading-relaxed text-lg">
              外部の評価や「稼げるノウハウ」に依存するほど、人生の主導権は遠のきます。
              自身の過去を冷徹に再定義し、他者の期待に侵食されない「自己決定の核」を確立します。
            </p>
            <div className="space-y-5">
              {[
                { title: "ノウハウ依存からの「卒業」", desc: "情報の奴隷から、知恵の主へ。" },
                { title: "自己確信の再構築", desc: "揺るぎない根源的な自信の復元。" },
                { title: "メンタル・レジリエンス", desc: "荒波を乗りこなす精神の柔軟性。" }
              ].map((item) => (
                <div key={item.title} className="flex gap-4 group/item">
                  <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-teal-500/20 text-teal-400 group-hover/item:scale-110 transition-all">
                    <CheckCircle2 className="h-4 w-4" />
                  </div>
                  <div>
                    <h4 className="font-bold text-teal-50">{item.title}</h4>
                    <p className="text-sm text-zinc-400">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            whileInView="visible"
            initial="hidden"
            viewport={{ once: true, margin: "-100px" }}
            variants={itemVariants}
            className="glass-panel group relative flex flex-col justify-center rounded-3xl p-10 md:p-14 border border-white/5 hover:border-teal-500/30 transition-all duration-700 bg-black/20"
          >
            <div className="absolute -top-6 -right-6 bg-teal-500/20 p-4 rounded-2xl backdrop-blur-md border border-teal-500/30 text-teal-400 group-hover:scale-110 transition-transform duration-500">
              <Zap size={32} />
            </div>
            <h2 className="mb-6 text-3xl font-bold md:text-5xl leading-tight">
              創造の武器。<br />
              <span className="text-forest font-light">AI practical Wisdom</span>
            </h2>
            <p className="mb-8 text-zinc-300 leading-relaxed text-lg">
              意志を社会へ実装するための「加速装置」としてのAI。
              単なる「使い方」ではなく、あなたの思想を自律的に拡張させる「デジタル分身」としてのAI設計を伝授します。
            </p>
            <div className="space-y-5">
              {[
                { title: "AI思考パートナーシップ", desc: "LLMを「道具」から「鏡」へ変える。" },
                { title: "高付加価値のプロダクト化", desc: "独自の思想をデジタル資産へ転換。" },
                { title: "自律型ビジネスモデル", desc: "時間と場所を自己決定するための構造。" }
              ].map((item) => (
                <div key={item.title} className="flex gap-4 group/item">
                  <div className="mt-1 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-teal-500/20 text-teal-400 group-hover/item:scale-110 transition-all">
                    <CheckCircle2 className="h-4 w-4" />
                  </div>
                  <div>
                    <h4 className="font-bold text-teal-50">{item.title}</h4>
                    <p className="text-sm text-zinc-400">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Future Section (Indoor Focus) */}
      <section id="section-future" className="w-full max-w-6xl px-4 py-24 min-h-screen flex items-center justify-center">
        <motion.div
          whileInView={{ opacity: 1, scale: 1 }}
          initial={{ opacity: 0, scale: 0.95 }}
          viewport={{ once: true }}
          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
          className="glass-panel relative max-w-3xl rounded-3xl p-12 md:p-20 text-center overflow-hidden border border-teal-500/10 shadow-3xl"
        >
          {/* Subtle Glow Effect */}
          <div className="absolute -inset-10 bg-teal-500/5 blur-[100px] pointer-events-none" />

          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.8 }}
            className="mb-8 text-4xl font-bold md:text-6xl text-white leading-tight"
          >
            静かな確信から、<br />
            <span className="text-forest">世界を変える一歩</span>を。
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="mb-12 text-zinc-300 text-lg md:text-xl font-light leading-relaxed"
          >
            あなたの内なる静寂から紡がれる「問い」こそが、<br />
            AI時代における最強のコモディティ化への対抗手段となります。
          </motion.p>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, duration: 0.5 }}
          >
            <button className="flex h-16 w-full max-w-md mx-auto items-center justify-center gap-3 rounded-full bg-gradient-to-r from-teal-500 to-teal-400 text-xl font-bold text-white transition-all hover:brightness-110 hover:shadow-2xl active:scale-95 shadow-xl">
              「人生の再定義」セッションを予約
              <ArrowRight className="h-6 w-6" />
            </button>
            <p className="mt-6 text-sm text-zinc-500">※限定枠のため、審査制とさせていただいております。</p>
          </motion.div>
        </motion.div>
      </section>

      {/* Dashboard Section */}
      <Dashboard />

      {/* Projects Section */}
      <section id="section-projects" className="w-full max-w-7xl px-4 py-24 min-h-[70vh] flex flex-col items-center justify-center">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={containerVariants}
          className="text-center mb-16"
        >
          <motion.div variants={itemVariants} className="mb-4 flex justify-center">
            <div className="flex items-center gap-2 rounded-full bg-teal-500/10 px-4 py-1 text-sm font-medium text-teal-400 border border-teal-500/20">
              <Cpu size={16} />
              <span>AI Tools</span>
            </div>
          </motion.div>
          <motion.h2 variants={itemVariants} className="text-4xl font-bold md:text-5xl text-white mb-4">
            AI活用プロジェクト
          </motion.h2>
          <motion.p variants={itemVariants} className="text-zinc-400 text-lg max-w-2xl mx-auto">
            自己決定力を加速させるためのAIツールを開発しています
          </motion.p>
        </motion.div>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3 w-full">
          {/* AI副業適性診断ツール */}
          <motion.a
            href="https://ai-diagnosis-six.vercel.app"
            target="_blank"
            rel="noopener noreferrer"
            whileInView="visible"
            initial="hidden"
            viewport={{ once: true }}
            variants={itemVariants}
            whileHover={{ scale: 1.02, y: -5 }}
            className="glass-panel group relative flex flex-col rounded-3xl p-8 border border-white/5 hover:border-teal-500/30 transition-all duration-500 bg-black/20 cursor-pointer"
          >
            <div className="absolute -top-4 -right-4 bg-gradient-to-br from-purple-500/30 to-pink-500/30 p-3 rounded-xl backdrop-blur-md border border-purple-500/30 text-purple-400 group-hover:scale-110 transition-transform duration-500">
              <Sparkles size={24} />
            </div>
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold text-white mb-2">AI副業適性診断</h3>
            <p className="text-zinc-400 text-sm mb-4 flex-grow">
              5問の質問で、あなたに向いているAI副業タイプを診断。MBTI分析も可能。
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              <span className="text-xs bg-teal-500/20 text-teal-400 px-2 py-1 rounded-full">React</span>
              <span className="text-xs bg-purple-500/20 text-purple-400 px-2 py-1 rounded-full">TypeScript</span>
              <span className="text-xs bg-pink-500/20 text-pink-400 px-2 py-1 rounded-full">Vercel</span>
            </div>
            <div className="flex items-center text-teal-400 text-sm font-medium group-hover:gap-3 transition-all">
              診断を試す <ArrowRight size={16} className="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </motion.a>

          {/* タスク管理ツール */}
          <motion.div
            whileInView="visible"
            initial="hidden"
            viewport={{ once: true }}
            variants={itemVariants}
            className="glass-panel group relative flex flex-col rounded-3xl p-8 border border-white/5 hover:border-teal-500/30 transition-all duration-500 bg-black/20"
          >
            <div className="absolute -top-4 -right-4 bg-gradient-to-br from-blue-500/30 to-cyan-500/30 p-3 rounded-xl backdrop-blur-md border border-blue-500/30 text-blue-400 group-hover:scale-110 transition-transform duration-500">
              <Target size={24} />
            </div>
            <div className="text-4xl mb-4">📋</div>
            <h3 className="text-xl font-bold text-white mb-2">タスク管理ツール</h3>
            <p className="text-zinc-400 text-sm mb-4 flex-grow">
              Google Calendar/Tasks連携。音声入力対応で、素早くタスクを登録。
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              <span className="text-xs bg-blue-500/20 text-blue-400 px-2 py-1 rounded-full">React</span>
              <span className="text-xs bg-cyan-500/20 text-cyan-400 px-2 py-1 rounded-full">Google API</span>
              <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded-full">Voice</span>
            </div>
            <div className="text-zinc-500 text-sm">
              🔒 プライベート利用
            </div>
          </motion.div>

          {/* Coming Soon */}
          <motion.div
            whileInView="visible"
            initial="hidden"
            viewport={{ once: true }}
            variants={itemVariants}
            className="glass-panel group relative flex flex-col items-center justify-center rounded-3xl p-8 border border-dashed border-white/10 hover:border-teal-500/20 transition-all duration-500 bg-black/10 min-h-[280px]"
          >
            <div className="text-4xl mb-4 opacity-50">🚀</div>
            <h3 className="text-xl font-bold text-zinc-500 mb-2">Coming Soon</h3>
            <p className="text-zinc-600 text-sm text-center">
              新しいAIツールを開発中...<br />
              お楽しみに！
            </p>
          </motion.div>
        </div>
      </section>

      {/* Booking Form Section */}
      <BookingForm />

      {/* Footer */}
      <footer className="w-full py-20 text-center border-t border-white/5 bg-black/20">
        <div className="max-w-4xl mx-auto px-4">
          {/* LINE CTA */}
          <div className="mb-12 p-8 rounded-2xl bg-gradient-to-r from-purple-500/10 to-pink-500/10 border border-purple-500/20">
            <div className="flex flex-col md:flex-row items-center justify-center gap-6">
              <div className="text-center md:text-left">
                <h3 className="text-xl font-bold text-white mb-2">🎁 LINE登録で無料特典</h3>
                <p className="text-zinc-400 text-sm">AI副業ロードマップPDF + 初回相談無料</p>
              </div>
              <a
                href="https://lin.ee/VAYurUv"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 bg-[#06C755] text-white px-6 py-3 rounded-full font-bold hover:brightness-110 transition-all"
              >
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.349 0 .63.285.63.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314" />
                </svg>
                LINEで友だち追加
              </a>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex flex-wrap justify-center gap-6 md:gap-8 mb-8 text-zinc-300 font-medium">
            <a href="/philosophy" className="hover:text-teal-400 transition-colors">Philosophy</a>
            <a href="/sessions" className="hover:text-teal-400 transition-colors">Sessions</a>
            <a href="https://ai-diagnosis-six.vercel.app" target="_blank" rel="noopener noreferrer" className="hover:text-purple-400 transition-colors">🤖 AI診断</a>
            <a href="https://lin.ee/VAYurUv" target="_blank" rel="noopener noreferrer" className="hover:text-green-400 transition-colors">LINE</a>
          </div>
          <p className="text-zinc-500 text-sm tracking-widest uppercase">© 2026 Takahiro Motoyama. Designed for Self-Determination.</p>
        </div>
      </footer>
    </main>
  );
}
