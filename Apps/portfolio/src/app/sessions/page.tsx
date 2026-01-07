"use client";

import { motion, Variants } from "framer-motion";
import { CheckCircle2, ArrowRight, Clock, Video, MessageCircle, ShieldCheck, HelpCircle, CalendarDays } from "lucide-react";
import BookingForm from "@/components/BookingForm";
import Header from "@/components/Header";
import Link from "next/link";

export default function SessionsPage() {
    const containerVariants: Variants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: { staggerChildren: 0.15 }
        }
    };

    const itemVariants: Variants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
    };

    const targetAudience = [
        "「正解」を求め続けて、かえって迷子になっている方",
        "ノウハウを集めすぎて、行動できなくなっている方",
        "他人の期待ばかり満たして、自分の人生を生きていない感覚がある方",
        "AI時代に自分の価値をどう発揮すべきか模索している方",
        "一人で悩む時間を、建設的な対話に変えたい方",
    ];

    const transformations = [
        {
            before: "情報に振り回され、決断できない",
            after: "自分の判断軸で選び、迷わない",
        },
        {
            before: "他者の評価に依存し、自信がない",
            after: "揺るぎない自己確信を持つ",
        },
        {
            before: "AIに取り残される不安",
            after: "AIを「思考の拡張」として使いこなす",
        },
    ];

    const sessionFlow = [
        { step: 1, title: "事前ヒアリング", desc: "簡単なフォームで現状と関心をお伺いします" },
        { step: 2, title: "対話セッション", desc: "60〜90分のオンライン1on1。問いを通じて内面を整理" },
        { step: 3, title: "アクションプラン", desc: "セッション後、具体的な次のステップを言語化" },
    ];

    const faqs = [
        { q: "コーチング経験がなくても大丈夫ですか？", a: "はい。むしろ「初めての方」が多いです。構えず、お話しいただくだけで大丈夫です。" },
        { q: "どんな話をすればいいかわかりません", a: "問いかけを通じて自然と言葉が出てきます。準備は不要です。" },
        { q: "秘密は守られますか？", a: "はい。お話しいただいた内容は一切外部に漏らしません。" },
        { q: "1回で効果はありますか？", a: "1回でも「思考の整理」効果を実感される方が多いです。継続は任意です。" },
    ];

    return (
        <>
            <Header />
            <main className="flex min-h-screen flex-col items-center overflow-x-hidden pt-24 pb-16">
                {/* Hero */}
                <section className="w-full max-w-4xl px-4 mb-16">
                    <motion.div
                        initial="hidden"
                        animate="visible"
                        variants={containerVariants}
                        className="text-center"
                    >
                        <motion.div variants={itemVariants} className="mb-4 flex justify-center">
                            <span className="inline-block rounded-full bg-teal-500/10 px-4 py-1 text-sm font-medium text-teal-400 border border-teal-500/20">
                                Life Self-Determination Session
                            </span>
                        </motion.div>
                        <motion.h1 variants={itemVariants} className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
                            自分の人生を、<br />
                            <span className="text-forest">自分で決める力</span>を取り戻す
                        </motion.h1>
                        <motion.p variants={itemVariants} className="text-zinc-300 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
                            情報過多の時代に、外からの「正解」ではなく、内なる「確信」を再構築する。<br />
                            1on1の対話を通じて、あなたの判断軸を研ぎ澄まします。
                        </motion.p>
                    </motion.div>
                </section>

                {/* Who is this for */}
                <section className="w-full max-w-4xl px-4 mb-20">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                        className="glass-panel rounded-3xl p-8 md:p-12 border border-white/5"
                    >
                        <motion.h2 variants={itemVariants} className="text-2xl md:text-3xl font-bold text-white mb-8 flex items-center gap-3">
                            <CheckCircle2 className="text-teal-400" /> こんな方へ
                        </motion.h2>
                        <ul className="space-y-4">
                            {targetAudience.map((item, i) => (
                                <motion.li key={i} variants={itemVariants} className="flex items-start gap-3 text-zinc-100 leading-relaxed">
                                    <ArrowRight className="text-teal-400 shrink-0 mt-1" size={18} />
                                    <span>{item}</span>
                                </motion.li>
                            ))}
                        </ul>
                    </motion.div>
                </section>

                {/* Before / After */}
                <section className="w-full max-w-5xl px-4 mb-20">
                    <motion.h2
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="text-2xl md:text-3xl font-bold text-white mb-10 text-center"
                    >
                        セッションで得られる変化
                    </motion.h2>
                    <div className="grid md:grid-cols-3 gap-6">
                        {transformations.map((t, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 30 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.1 }}
                                className="glass-panel rounded-2xl p-6 border border-white/5 text-center"
                            >
                                <div className="text-zinc-300 text-base mb-2">Before</div>
                                <p className="text-zinc-200 mb-4 line-through decoration-red-400/50">{t.before}</p>
                                <ArrowRight className="mx-auto text-teal-400 mb-4" />
                                <div className="text-teal-400 text-base mb-2">After</div>
                                <p className="text-white font-semibold">{t.after}</p>
                            </motion.div>
                        ))}
                    </div>
                </section>

                {/* Session Flow */}
                <section className="w-full max-w-4xl px-4 mb-20">
                    <motion.h2
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="text-2xl md:text-3xl font-bold text-white mb-10 text-center flex items-center justify-center gap-3"
                    >
                        <Clock className="text-teal-400" /> セッションの進め方
                    </motion.h2>
                    <div className="grid md:grid-cols-3 gap-6">
                        {sessionFlow.map((s, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, scale: 0.95 }}
                                whileInView={{ opacity: 1, scale: 1 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.1 }}
                                className="glass-panel rounded-2xl p-6 border border-white/5"
                            >
                                <div className="w-10 h-10 rounded-full bg-teal-500/20 text-teal-400 flex items-center justify-center font-bold mb-4">
                                    {s.step}
                                </div>
                                <h3 className="text-white font-bold text-lg mb-2">{s.title}</h3>
                                <p className="text-zinc-300 text-base">{s.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                    <motion.div
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="mt-8 flex flex-wrap justify-center gap-6 text-zinc-300"
                    >
                        <span className="flex items-center gap-2"><Clock size={18} className="text-teal-400" /> 60〜90分</span>
                        <span className="flex items-center gap-2"><Video size={18} className="text-teal-400" /> オンライン (Zoom)</span>
                        <span className="flex items-center gap-2"><ShieldCheck size={18} className="text-teal-400" /> 完全守秘</span>
                    </motion.div>
                </section>

                {/* Pricing */}
                <section className="w-full max-w-3xl px-4 mb-20">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="glass-panel rounded-3xl p-8 md:p-12 text-center border border-teal-500/20"
                    >
                        <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">料金</h2>
                        <p className="text-zinc-200 mb-6">
                            現在、<span className="text-teal-400 font-semibold">審査制</span>にてご案内しております。<br />
                            詳細は個別にお伝えいたします。
                        </p>
                        <p className="text-base text-zinc-400">※ 初回のみ特別価格をご用意しています</p>
                    </motion.div>
                </section>

                {/* FAQ */}
                <section className="w-full max-w-4xl px-4 mb-20">
                    <motion.h2
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="text-2xl md:text-3xl font-bold text-white mb-10 text-center flex items-center justify-center gap-3"
                    >
                        <HelpCircle className="text-teal-400" /> よくある質問
                    </motion.h2>
                    <div className="space-y-4">
                        {faqs.map((faq, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, x: -20 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true }}
                                transition={{ delay: i * 0.05 }}
                                className="glass-panel rounded-xl p-6 border border-white/5"
                            >
                                <h3 className="text-white font-semibold mb-2 flex items-start gap-2">
                                    <MessageCircle className="text-teal-400 shrink-0 mt-1" size={18} />
                                    {faq.q}
                                </h3>
                                <p className="text-zinc-300 pl-6">{faq.a}</p>
                            </motion.div>
                        ))}
                    </div>
                </section>

                {/* After Booking Flow */}
                <section className="w-full max-w-3xl px-4 mb-20">
                    <motion.div
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="glass-panel rounded-3xl p-8 md:p-12 border border-white/5"
                    >
                        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                            <CalendarDays className="text-teal-400" /> お申込み後の流れ
                        </h2>
                        <ol className="space-y-4 text-zinc-200 leading-relaxed">
                            <li className="flex items-start gap-3">
                                <span className="w-6 h-6 rounded-full bg-teal-500/20 text-teal-400 flex items-center justify-center text-base font-bold shrink-0">1</span>
                                <span>フォーム送信後、<strong className="text-white">24時間以内</strong>にメールで返信いたします</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <span className="w-6 h-6 rounded-full bg-teal-500/20 text-teal-400 flex items-center justify-center text-base font-bold shrink-0">2</span>
                                <span>日程調整リンクから、ご都合の良い日時をお選びください</span>
                            </li>
                            <li className="flex items-start gap-3">
                                <span className="w-6 h-6 rounded-full bg-teal-500/20 text-teal-400 flex items-center justify-center text-base font-bold shrink-0">3</span>
                                <span>当日、Zoomリンクをお送りします</span>
                            </li>
                        </ol>
                    </motion.div>
                </section>

                {/* 診断誘導バナー */}
                <section className="w-full max-w-3xl px-4 mb-12">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="glass-panel rounded-3xl p-8 md:p-10 border border-purple-500/20 bg-gradient-to-r from-purple-500/5 to-pink-500/5"
                    >
                        <div className="flex flex-col md:flex-row items-center gap-6">
                            <div className="text-5xl">🤖</div>
                            <div className="flex-1 text-center md:text-left">
                                <h3 className="text-xl md:text-2xl font-bold text-white mb-2">
                                    まずは無料で適性診断
                                </h3>
                                <p className="text-zinc-300 text-base">
                                    5問の質問で、あなたに向いているAI副業タイプがわかります。<br />
                                    セッションを受ける前に、自分の傾向を把握しておきましょう。
                                </p>
                            </div>
                            <a
                                href="https://ai-diagnosis-six.vercel.app"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-full font-bold hover:brightness-110 transition-all whitespace-nowrap"
                            >
                                診断を受ける
                                <ArrowRight size={18} />
                            </a>
                        </div>
                    </motion.div>
                </section>

                {/* Booking Form */}
                <BookingForm />

                {/* Back Link */}
                <section className="w-full max-w-4xl px-4 py-12 text-center">
                    <Link href="/" className="text-zinc-400 hover:text-teal-400 transition-colors text-sm">
                        ← トップページへ戻る
                    </Link>
                </section>
            </main>
        </>
    );
}

