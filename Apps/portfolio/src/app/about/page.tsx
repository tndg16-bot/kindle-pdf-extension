'use client';

import { motion, Variants } from 'framer-motion';
import { Target, Brain, Briefcase, Heart, CheckCircle, XCircle, ArrowRight, Sparkles } from 'lucide-react';
import Link from 'next/link';
import Header from '@/components/Header';

export default function AboutPage() {
    const containerVariants: Variants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: { staggerChildren: 0.15 }
        }
    };

    const itemVariants: Variants = {
        hidden: { opacity: 0, y: 30 },
        visible: {
            opacity: 1,
            y: 0,
            transition: { duration: 0.6, ease: "easeOut" }
        }
    };

    const services = [
        { icon: Target, text: "意思決定の整理（価値観／理想／現状／ギャップ／次の一歩）" },
        { icon: Brain, text: "期限に向けたロードマップ設計（3ヶ月プラン、週次の型、今週の行動3つ）" },
        { icon: Briefcase, text: "現実面（キャリア／収入設計／AI活用）を「価値観に沿う範囲で」整理" },
    ];

    const career = [
        { area: "金融領域", description: "個人や中小企業のオーナー／経営者向けに資産形成の提案（株式・債券・投信・保険など）" },
        { area: "人材領域", description: "新卒採用支援・キャリア相談（法人支援／登壇等）" },
        { area: "AI領域", description: "AI活用のコンサルティング／講師（法人支援・中小企業中心）" },
    ];

    const promises = [
        "否定しません。裁きません。",
        "上から教えません。価値観を押し付けません。",
        "その人に合った言葉で問いを立てます。",
        "最後は必ず「あなたが選ぶ」形で終わらせます。",
    ];

    const fitFor = [
        "自分の人生を変えたい／動きたい気持ちがある",
        "モヤモヤを言語化して、次の一歩を決めたい",
        "\"選ぶ力\"を取り戻したい",
    ];

    const notFitFor = [
        "何もせずに正解だけ欲しい",
        "自分の前提を変える気がない",
        "行動のコミットが難しい状態",
    ];

    return (
        <>
            <Header />
            <main className="flex min-h-screen flex-col items-center overflow-x-hidden pt-20">
                {/* Hero Section */}
                <section className="relative w-full py-24 px-4">
                    <div className="absolute inset-0 bg-gradient-to-b from-teal-500/5 via-purple-500/5 to-transparent" />

                    <motion.div
                        initial="hidden"
                        animate="visible"
                        variants={containerVariants}
                        className="relative z-10 max-w-4xl mx-auto text-center"
                    >
                        <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-teal-500/20 to-purple-500/20 border border-white/10 mb-8">
                            <Sparkles className="w-4 h-4 text-teal-400" />
                            <span className="text-sm text-zinc-300">About</span>
                        </motion.div>

                        <motion.h1 variants={itemVariants} className="text-4xl md:text-6xl font-bold mb-6">
                            <span className="bg-gradient-to-r from-white via-teal-200 to-purple-200 bg-clip-text text-transparent">
                                判断軸を取り戻して、
                            </span>
                            <br />
                            <span className="text-white">自分で決められる人を増やしたい</span>
                        </motion.h1>

                        <motion.p variants={itemVariants} className="text-xl text-zinc-300 max-w-2xl mx-auto leading-relaxed">
                            情報も正解も溢れている時代だからこそ、<br />
                            最後に頼れるのは「自分で決められる力」だと思っています。
                        </motion.p>
                    </motion.div>
                </section>

                {/* Introduction */}
                <section className="w-full max-w-4xl px-4 py-16">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                        className="p-8 rounded-2xl bg-white/5 border border-white/10"
                    >
                        <motion.p variants={itemVariants} className="text-lg text-zinc-300 leading-relaxed">
                            はじめまして、<span className="text-teal-400 font-bold">本山 貴裕</span>です。<br /><br />
                            「モヤモヤ整理セッション」は、答えを渡す場所ではありません。<br />
                            自分の価値観と判断軸を言語化して、次の一歩を決めるための時間です。<br /><br />
                            そのために、<span className="text-purple-400">否定せず、裁かず、押し付けず、伴走します。</span>
                        </motion.p>
                    </motion.div>
                </section>

                {/* What I Do */}
                <section className="w-full max-w-4xl px-4 py-16">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                    >
                        <motion.h2 variants={itemVariants} className="text-3xl font-bold text-white mb-8 text-center">
                            私がやっていること
                        </motion.h2>

                        <div className="space-y-4">
                            {services.map((service, index) => (
                                <motion.div
                                    key={index}
                                    variants={itemVariants}
                                    className="flex items-start gap-4 p-6 rounded-xl bg-white/5 border border-white/10 hover:border-teal-500/30 transition-colors"
                                >
                                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-teal-500/20 to-purple-500/20 flex items-center justify-center flex-shrink-0">
                                        <service.icon className="w-6 h-6 text-teal-400" />
                                    </div>
                                    <p className="text-zinc-200 leading-relaxed pt-2">{service.text}</p>
                                </motion.div>
                            ))}
                        </div>

                        <motion.p variants={itemVariants} className="text-center text-zinc-400 mt-6 text-base">
                            ※「売り込み」が目的ではありません。必要な場合にだけ、次の選択肢を提示します。
                        </motion.p>
                    </motion.div>
                </section>

                {/* Why I Do This */}
                <section className="w-full max-w-4xl px-4 py-16">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                        className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-500/10 to-teal-500/10 border border-white/10 p-8"
                    >
                        <motion.h2 variants={itemVariants} className="text-3xl font-bold text-white mb-6">
                            なぜこれをやっているのか
                        </motion.h2>

                        <motion.div variants={itemVariants} className="space-y-4 text-zinc-200 leading-relaxed">
                            <p>多くの人が、答えを持っていないわけではなくて、</p>
                            <ul className="list-disc list-inside space-y-3 pl-4 text-zinc-300 leading-relaxed">
                                <li>自分を信じきれない</li>
                                <li>言葉にするのが怖い</li>
                                <li>何から手をつけていいか分からない</li>
                            </ul>
                            <p>このあたりで止まっていることが多いと感じています。</p>
                            <p className="text-teal-400 font-medium pt-4">
                                だから私は、まず「自分の意思を言っていい」状態をつくる。<br />
                                そのうえで、行動まで落とし込む。<br />
                                この順番を大事にしています。
                            </p>
                        </motion.div>
                    </motion.div>
                </section>

                {/* Career */}
                <section className="w-full max-w-4xl px-4 py-16">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                    >
                        <motion.h2 variants={itemVariants} className="text-3xl font-bold text-white mb-8 text-center">
                            経歴（できることの裏付け）
                        </motion.h2>

                        <motion.p variants={itemVariants} className="text-center text-zinc-400 mb-8">
                            これまで、<span className="text-teal-400">金融・人材・AIの領域</span>で現場を見てきました。
                        </motion.p>

                        <div className="grid gap-4 md:grid-cols-3">
                            {career.map((item, index) => (
                                <motion.div
                                    key={index}
                                    variants={itemVariants}
                                    className="p-6 rounded-xl bg-white/5 border border-white/10"
                                >
                                    <h3 className="text-lg font-bold text-teal-400 mb-3">{item.area}</h3>
                                    <p className="text-base text-zinc-300">{item.description}</p>
                                </motion.div>
                            ))}
                        </div>

                        <motion.p variants={itemVariants} className="text-center text-zinc-300 mt-8 p-4 rounded-xl bg-white/5 border border-white/10">
                            「精神面（価値観・直感）」だけでも、「実務（AIやキャリア）」だけでもなく、<br />
                            <span className="text-purple-400 font-medium">両方をつないで"意思決定"に落とすのが私のスタイルです。</span>
                        </motion.p>
                    </motion.div>
                </section>

                {/* Promises */}
                <section className="w-full max-w-4xl px-4 py-16">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                    >
                        <motion.h2 variants={itemVariants} className="text-3xl font-bold text-white mb-8 text-center flex items-center justify-center gap-3">
                            <Heart className="w-8 h-8 text-pink-400" />
                            大切にしている約束
                        </motion.h2>

                        <div className="grid gap-3 md:grid-cols-2">
                            {promises.map((promise, index) => (
                                <motion.div
                                    key={index}
                                    variants={itemVariants}
                                    className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10"
                                >
                                    <CheckCircle className="w-5 h-5 text-teal-400 flex-shrink-0" />
                                    <p className="text-zinc-200">{promise}</p>
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                </section>

                {/* Fit / Not Fit */}
                <section className="w-full max-w-4xl px-4 py-16">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                    >
                        <motion.h2 variants={itemVariants} className="text-3xl font-bold text-white mb-8 text-center">
                            セッションが合う人／合わない人
                        </motion.h2>

                        <div className="grid gap-6 md:grid-cols-2">
                            <motion.div variants={itemVariants} className="p-6 rounded-2xl bg-teal-500/10 border border-teal-500/30">
                                <h3 className="text-xl font-bold text-teal-400 mb-4 flex items-center gap-2">
                                    <CheckCircle className="w-6 h-6" /> 合う人
                                </h3>
                                <ul className="space-y-3">
                                    {fitFor.map((item, index) => (
                                        <li key={index} className="flex items-start gap-2 text-zinc-200">
                                            <span className="text-teal-400 mt-1">•</span>
                                            {item}
                                        </li>
                                    ))}
                                </ul>
                            </motion.div>

                            <motion.div variants={itemVariants} className="p-6 rounded-2xl bg-red-500/10 border border-red-500/30">
                                <h3 className="text-xl font-bold text-red-400 mb-4 flex items-center gap-2">
                                    <XCircle className="w-6 h-6" /> 合わない人
                                </h3>
                                <ul className="space-y-3">
                                    {notFitFor.map((item, index) => (
                                        <li key={index} className="flex items-start gap-2 text-zinc-200">
                                            <span className="text-red-400 mt-1">•</span>
                                            {item}
                                        </li>
                                    ))}
                                </ul>
                            </motion.div>
                        </div>
                    </motion.div>
                </section>

                {/* Why Free */}
                <section className="w-full max-w-4xl px-4 py-16">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                        className="p-8 rounded-2xl bg-white/5 border border-white/10 text-center"
                    >
                        <motion.h2 variants={itemVariants} className="text-2xl font-bold text-white mb-4">
                            無料モニターでやっている理由
                        </motion.h2>
                        <motion.p variants={itemVariants} className="text-zinc-300 leading-relaxed">
                            将来的に「意思決定できる人を増やす」活動をしていきたいからです。<br />
                            そのために、いまは悩みの構造を多角的に理解し、セッションの質を磨いています。
                        </motion.p>
                    </motion.div>
                </section>

                {/* CTA */}
                <section className="w-full max-w-4xl px-4 py-24">
                    <motion.div
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        variants={containerVariants}
                        className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-teal-500/20 via-purple-500/10 to-pink-500/20 border border-white/10 p-12 text-center"
                    >
                        <motion.h2 variants={itemVariants} className="text-3xl font-bold text-white mb-4">
                            頭の中が散らかっていて進めないなら、まずは整理しましょう
                        </motion.h2>
                        <motion.p variants={itemVariants} className="text-xl text-zinc-300 mb-8">
                            60分で、価値観と判断軸を言語化して、次の一歩まで落とします。
                        </motion.p>
                        <motion.div variants={itemVariants}>
                            <Link
                                href="/sessions"
                                className="inline-flex items-center gap-2 px-8 py-4 rounded-full bg-gradient-to-r from-teal-400 to-purple-500 text-white font-bold text-lg hover:opacity-90 transition-opacity"
                            >
                                セッション詳細はこちら
                                <ArrowRight className="w-5 h-5" />
                            </Link>
                        </motion.div>
                    </motion.div>
                </section>

                {/* Footer */}
                <footer className="w-full py-12 border-t border-white/5 bg-black/20">
                    <div className="max-w-6xl mx-auto px-4">
                        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
                            <div className="flex gap-6 text-zinc-400 text-sm">
                                <Link href="/" className="hover:text-teal-400 transition-colors">Home</Link>
                                <Link href="/about" className="hover:text-teal-400 transition-colors">About</Link>
                                <Link href="/sessions" className="hover:text-teal-400 transition-colors">Sessions</Link>
                                <Link href="/contact" className="hover:text-teal-400 transition-colors">Contact</Link>
                            </div>
                            <p className="text-zinc-500 text-sm">
                                © 2026 Takahiro Motoyama. All rights reserved.
                            </p>
                        </div>
                    </div>
                </footer>
            </main>
        </>
    );
}
