'use client';

import { motion } from 'framer-motion';
import { Compass, Heart, Zap, Shield, Target, Sparkles } from 'lucide-react';
import Header from '@/components/Header';

export default function PhilosophyPage() {
    const principles = [
        {
            icon: Shield,
            title: '内なる聖域を守る',
            subtitle: 'Spiritual Resilience',
            description: '外部の評価や「正解」に振り回されない、自己決定の核を確立する。',
        },
        {
            icon: Heart,
            title: '自分の価値は自分で決める',
            subtitle: 'Self-Determination',
            description: '他者の期待ではなく、自身の内なる声に従う勇気を育む。',
        },
        {
            icon: Zap,
            title: 'AIを創造の武器に',
            subtitle: 'AI Practical Wisdom',
            description: 'テクノロジーを「道具」から「思考パートナー」へ昇華させる。',
        },
        {
            icon: Target,
            title: '静寂の中の確信',
            subtitle: 'Quiet Confidence',
            description: '情報の洪水から距離を置き、直感を研ぎ澄ませる。',
        },
    ];

    return (
        <main className="flex min-h-screen flex-col items-center overflow-x-hidden pt-20">
            <Header />

            {/* Hero Section */}
            <section className="relative flex min-h-[60vh] w-full flex-col items-center justify-center px-4">
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8 }}
                    className="text-center"
                >
                    <div className="mb-6 flex justify-center">
                        <div className="flex items-center gap-2 rounded-full bg-teal-500/10 px-4 py-1 text-sm font-medium text-teal-400 border border-teal-500/20">
                            <Compass size={16} />
                            <span>Core Philosophy</span>
                        </div>
                    </div>
                    <h1 className="mb-6 text-4xl font-bold tracking-tight md:text-6xl text-white">
                        人生の<span className="text-forest">自己決定</span>を取り戻す
                    </h1>
                    <p className="text-lg text-zinc-300 md:text-xl max-w-2xl mx-auto leading-relaxed">
                        溢れる情報と「正解」の押し付けから、魂の呼吸を守り抜く。<br />
                        外部依存を脱却し、自分だけの羅針盤を手にする旅路。
                    </p>
                </motion.div>
            </section>

            {/* Principles Grid */}
            <section className="w-full max-w-6xl px-4 py-16">
                <motion.div
                    initial={{ opacity: 0 }}
                    whileInView={{ opacity: 1 }}
                    transition={{ duration: 0.6 }}
                    className="grid md:grid-cols-2 gap-8"
                >
                    {principles.map((principle, index) => (
                        <motion.div
                            key={principle.title}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1, duration: 0.5 }}
                            className="glass-panel rounded-3xl p-8 hover:border-teal-500/30 transition-all duration-500"
                        >
                            <div className="flex items-start gap-4">
                                <div className="bg-teal-500/20 p-3 rounded-2xl text-teal-400">
                                    <principle.icon size={28} />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white mb-1">
                                        {principle.title}
                                    </h3>
                                    <p className="text-sm text-teal-400 mb-3">
                                        {principle.subtitle}
                                    </p>
                                    <p className="text-zinc-400 leading-relaxed">
                                        {principle.description}
                                    </p>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </motion.div>
            </section>

            {/* Quote Section */}
            <section className="w-full max-w-4xl px-4 py-16">
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    whileInView={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6 }}
                    className="glass-panel rounded-3xl p-12 text-center"
                >
                    <Sparkles className="mx-auto mb-6 text-teal-400" size={32} />
                    <blockquote className="text-2xl md:text-3xl font-light text-white mb-6 leading-relaxed">
                        「ノウハウ依存」から卒業した先に、<br />
                        <span className="text-forest font-medium">本当の自由</span>がある。
                    </blockquote>
                    <p className="text-zinc-400">
                        — Life Self-Determination Protocol
                    </p>
                </motion.div>
            </section>

            {/* Footer */}
            <footer className="w-full py-12 text-center border-t border-white/5">
                <p className="text-zinc-500 text-sm">
                    © 2026 Takahiro Motoyama. Designed for Self-Determination.
                </p>
            </footer>
        </main>
    );
}
