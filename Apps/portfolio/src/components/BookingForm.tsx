"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { Send, User, Mail, Briefcase, MessageSquare, Calendar, HelpCircle, AlertCircle } from "lucide-react";

interface FormData {
    name: string;
    email: string;
    occupation: string;
    goal: string;
    motivation: string;
    preferredDate1: string;
    preferredDate2: string;
    message: string;
}

// ============================================
// Google Forms Configuration
// ユーザーがGoogle Formsを作成後にentry IDを設定
// ============================================
const GOOGLE_FORMS_CONFIG = {
    // Google Forms の formResponse URL
    // 例: https://docs.google.com/forms/d/e/1FAI.../formResponse
    actionUrl: process.env.NEXT_PUBLIC_GOOGLE_FORMS_URL || '',

    // 各フィールドの entry ID
    // Google Forms > ... > Get pre-filled link で取得可能
    entryIds: {
        name: process.env.NEXT_PUBLIC_ENTRY_NAME || 'entry.1234567890',
        email: process.env.NEXT_PUBLIC_ENTRY_EMAIL || 'entry.1234567891',
        occupation: process.env.NEXT_PUBLIC_ENTRY_OCCUPATION || 'entry.1234567892',
        goal: process.env.NEXT_PUBLIC_ENTRY_GOAL || 'entry.1234567893',
        motivation: process.env.NEXT_PUBLIC_ENTRY_MOTIVATION || 'entry.1234567894',
        preferredDate1: process.env.NEXT_PUBLIC_ENTRY_DATE1 || 'entry.1234567895',
        preferredDate2: process.env.NEXT_PUBLIC_ENTRY_DATE2 || 'entry.1234567896',
        message: process.env.NEXT_PUBLIC_ENTRY_MESSAGE || 'entry.1234567897',
    }
};

export default function BookingForm({ className = "" }: { className?: string }) {
    const [formData, setFormData] = useState<FormData>({
        name: "",
        email: "",
        occupation: "",
        goal: "",
        motivation: "",
        preferredDate1: "",
        preferredDate2: "",
        message: "",
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [isError, setIsError] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);
        setIsError(false);

        try {
            if (!GOOGLE_FORMS_CONFIG.actionUrl) {
                throw new Error('Google Forms URL is not configured');
            }

            const googleFormData = new FormData();
            googleFormData.append(GOOGLE_FORMS_CONFIG.entryIds.name, formData.name);
            googleFormData.append(GOOGLE_FORMS_CONFIG.entryIds.email, formData.email);
            googleFormData.append(GOOGLE_FORMS_CONFIG.entryIds.occupation, formData.occupation);
            googleFormData.append(GOOGLE_FORMS_CONFIG.entryIds.goal, formData.goal);
            googleFormData.append(GOOGLE_FORMS_CONFIG.entryIds.motivation, formData.motivation);
            googleFormData.append(GOOGLE_FORMS_CONFIG.entryIds.preferredDate1, formData.preferredDate1);
            googleFormData.append(GOOGLE_FORMS_CONFIG.entryIds.preferredDate2, formData.preferredDate2);
            googleFormData.append(GOOGLE_FORMS_CONFIG.entryIds.message, formData.message);

            // Google Formsへの送信（no-corsモード）
            const response = await fetch(GOOGLE_FORMS_CONFIG.actionUrl, {
                method: 'POST',
                body: googleFormData,
                mode: 'no-cors',
            });

            const isOpaqueSuccess = response.type === 'opaque';

            if (!isOpaqueSuccess && !response.ok) {
                throw new Error(`Google Forms submission failed with status: ${response.status || 'unknown'}`);
            }

            console.log('📧 Form submitted to Google Forms', { responseType: response.type, status: response.status });

            setIsSubmitted(true);
        } catch (error) {
            console.error('❌ Form submission error:', error);
            setIsError(true);
        } finally {
            setIsSubmitting(false);
        }
    };

    // エラー時のUI
    if (isError) {
        return (
            <section id="booking" className={`w-full max-w-4xl mx-auto px-4 py-16 ${className}`}>
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="glass-panel rounded-3xl p-12 text-center"
                >
                    <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-rose-500 to-amber-500 flex items-center justify-center">
                        <AlertCircle className="w-10 h-10 text-white" />
                    </div>
                    <h2 className="text-3xl font-bold text-white mb-4">
                        送信に失敗しました
                    </h2>
                    <p className="text-zinc-300 max-w-md mx-auto mb-8">
                        お手数ですが、もう一度お試しください。<br />
                        問題が続く場合はSNSでご連絡ください。
                    </p>
                    <button
                        onClick={() => setIsError(false)}
                        className="px-8 py-3 rounded-full bg-white/10 border border-white/20 text-white font-medium hover:bg-white/20 transition-all"
                    >
                        再試行
                    </button>
                </motion.div>
            </section>
        );
    }

    if (isSubmitted) {
        return (
            <section id="booking" className={`w-full max-w-4xl mx-auto px-4 py-16 ${className}`}>
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="glass-panel rounded-3xl p-12 text-center"
                >
                    <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center">
                        <Send className="w-10 h-10 text-white" />
                    </div>
                    <h2 className="text-3xl font-bold text-white mb-4">
                        送信完了しました
                    </h2>
                    <p className="text-zinc-300 max-w-md mx-auto">
                        3営業日以内にご連絡いたします。<br />
                        お問い合わせいただきありがとうございます。
                    </p>
                </motion.div>
            </section>
        );
    }

    return (
        <section id="booking" className={`w-full max-w-4xl mx-auto px-4 py-16 ${className}`}>
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6 }}
                className="glass-panel rounded-3xl p-8 md:p-12 border border-white/10"
            >
                {/* Header */}
                <div className="text-center mb-10">
                    <motion.div
                        initial={{ opacity: 0, y: -10 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                        className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-400 text-sm font-medium mb-4"
                    >
                        <Calendar size={16} />
                        <span>審査制セッション</span>
                    </motion.div>
                    <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                        「人生の再定義」セッション予約
                    </h2>
                    <p className="text-zinc-400 max-w-xl mx-auto">
                        あなたの内なる羅針盤を見つけ、人生の自己決定を加速させます。
                    </p>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Row 1: Name & Email */}
                    <div className="grid md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                                <User size={16} className="text-teal-400" />
                                お名前 <span className="text-rose-400">*</span>
                            </label>
                            <input
                                type="text"
                                name="name"
                                required
                                value={formData.name}
                                onChange={handleChange}
                                placeholder="山田 太郎"
                                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                                <Mail size={16} className="text-teal-400" />
                                メールアドレス <span className="text-rose-400">*</span>
                            </label>
                            <input
                                type="email"
                                name="email"
                                required
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="example@email.com"
                                className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all"
                            />
                        </div>
                    </div>

                    {/* Row 2: Occupation */}
                    <div className="space-y-2">
                        <label className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                            <Briefcase size={16} className="text-teal-400" />
                            現在のお仕事・活動 <span className="text-rose-400">*</span>
                        </label>
                        <input
                            type="text"
                            name="occupation"
                            required
                            value={formData.occupation}
                            onChange={handleChange}
                            placeholder="例: フリーランスエンジニア、会社員、起業準備中"
                            className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all"
                        />
                    </div>

                    {/* Row 3: Goal */}
                    <div className="space-y-2">
                        <label className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                            <MessageSquare size={16} className="text-teal-400" />
                            セッションで解決したいこと <span className="text-rose-400">*</span>
                        </label>
                        <textarea
                            name="goal"
                            required
                            value={formData.goal}
                            onChange={handleChange}
                            rows={3}
                            placeholder="例: 副業で独立したいが、何から始めればいいかわからない。自分軸を確立したい。"
                            className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all resize-none"
                        />
                    </div>

                    {/* Row 4: Motivation */}
                    <div className="space-y-2">
                        <label className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                            <HelpCircle size={16} className="text-teal-400" />
                            なぜこのセッションに興味を持ちましたか？
                        </label>
                        <textarea
                            name="motivation"
                            value={formData.motivation}
                            onChange={handleChange}
                            rows={2}
                            placeholder="任意: きっかけや期待することなど"
                            className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all resize-none"
                        />
                    </div>

                    {/* Row 5: Preferred Dates */}
                    <div className="space-y-4">
                        {/* Date 1 */}
                        <div className="space-y-2">
                            <label className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                                <Calendar size={16} className="text-teal-400" />
                                希望日時（第1希望） <span className="text-rose-400">*</span>
                            </label>
                            <div className="grid grid-cols-2 gap-3">
                                <input
                                    type="date"
                                    name="preferredDate1Date"
                                    required
                                    value={formData.preferredDate1.split('T')[0] || ''}
                                    onChange={(e) => {
                                        const time = formData.preferredDate1.split('T')[1] || '13:00';
                                        setFormData({ ...formData, preferredDate1: `${e.target.value}T${time}` });
                                    }}
                                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all [color-scheme:dark]"
                                />
                                <select
                                    name="preferredDate1Time"
                                    required
                                    value={formData.preferredDate1.split('T')[1] || '13:00'}
                                    onChange={(e) => {
                                        const date = formData.preferredDate1.split('T')[0] || '';
                                        setFormData({ ...formData, preferredDate1: `${date}T${e.target.value}` });
                                    }}
                                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all [color-scheme:dark]"
                                >
                                    <option value="09:00">09:00</option>
                                    <option value="09:30">09:30</option>
                                    <option value="10:00">10:00</option>
                                    <option value="10:30">10:30</option>
                                    <option value="11:00">11:00</option>
                                    <option value="11:30">11:30</option>
                                    <option value="12:00">12:00</option>
                                    <option value="12:30">12:30</option>
                                    <option value="13:00">13:00</option>
                                    <option value="13:30">13:30</option>
                                    <option value="14:00">14:00</option>
                                    <option value="14:30">14:30</option>
                                    <option value="15:00">15:00</option>
                                    <option value="15:30">15:30</option>
                                    <option value="16:00">16:00</option>
                                    <option value="16:30">16:30</option>
                                    <option value="17:00">17:00</option>
                                    <option value="17:30">17:30</option>
                                    <option value="18:00">18:00</option>
                                    <option value="18:30">18:30</option>
                                    <option value="19:00">19:00</option>
                                    <option value="19:30">19:30</option>
                                    <option value="20:00">20:00</option>
                                    <option value="20:30">20:30</option>
                                    <option value="21:00">21:00</option>
                                </select>
                            </div>
                        </div>

                        {/* Date 2 */}
                        <div className="space-y-2">
                            <label className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                                <Calendar size={16} className="text-zinc-500" />
                                希望日時（第2希望）
                            </label>
                            <div className="grid grid-cols-2 gap-3">
                                <input
                                    type="date"
                                    name="preferredDate2Date"
                                    value={formData.preferredDate2.split('T')[0] || ''}
                                    onChange={(e) => {
                                        const time = formData.preferredDate2.split('T')[1] || '13:00';
                                        setFormData({ ...formData, preferredDate2: `${e.target.value}T${time}` });
                                    }}
                                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all [color-scheme:dark]"
                                />
                                <select
                                    name="preferredDate2Time"
                                    value={formData.preferredDate2.split('T')[1] || '13:00'}
                                    onChange={(e) => {
                                        const date = formData.preferredDate2.split('T')[0] || '';
                                        setFormData({ ...formData, preferredDate2: `${date}T${e.target.value}` });
                                    }}
                                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all [color-scheme:dark]"
                                >
                                    <option value="09:00">09:00</option>
                                    <option value="09:30">09:30</option>
                                    <option value="10:00">10:00</option>
                                    <option value="10:30">10:30</option>
                                    <option value="11:00">11:00</option>
                                    <option value="11:30">11:30</option>
                                    <option value="12:00">12:00</option>
                                    <option value="12:30">12:30</option>
                                    <option value="13:00">13:00</option>
                                    <option value="13:30">13:30</option>
                                    <option value="14:00">14:00</option>
                                    <option value="14:30">14:30</option>
                                    <option value="15:00">15:00</option>
                                    <option value="15:30">15:30</option>
                                    <option value="16:00">16:00</option>
                                    <option value="16:30">16:30</option>
                                    <option value="17:00">17:00</option>
                                    <option value="17:30">17:30</option>
                                    <option value="18:00">18:00</option>
                                    <option value="18:30">18:30</option>
                                    <option value="19:00">19:00</option>
                                    <option value="19:30">19:30</option>
                                    <option value="20:00">20:00</option>
                                    <option value="20:30">20:30</option>
                                    <option value="21:00">21:00</option>
                                </select>
                            </div>
                        </div>
                    </div>


                    {/* Row 6: Additional Message */}
                    <div className="space-y-2">
                        <label className="flex items-center gap-2 text-sm font-medium text-zinc-300">
                            <MessageSquare size={16} className="text-zinc-500" />
                            その他ご質問・メッセージ
                        </label>
                        <textarea
                            name="message"
                            value={formData.message}
                            onChange={handleChange}
                            rows={2}
                            placeholder="任意: 事前に伝えておきたいことなど"
                            className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-zinc-500 focus:outline-none focus:border-teal-500/50 focus:ring-2 focus:ring-teal-500/20 transition-all resize-none"
                        />
                    </div>

                    {/* Submit Button */}
                    <motion.button
                        type="submit"
                        disabled={isSubmitting}
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        className="w-full py-4 rounded-xl bg-gradient-to-r from-teal-500 to-emerald-500 text-white font-bold text-lg flex items-center justify-center gap-2 hover:shadow-2xl hover:shadow-teal-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isSubmitting ? (
                            <>
                                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                送信中...
                            </>
                        ) : (
                            <>
                                <Send size={20} />
                                予約リクエストを送信
                            </>
                        )}
                    </motion.button>

                    {/* Note */}
                    <p className="text-center text-sm text-zinc-500">
                        ※ 審査制のため、後日ご連絡いたします（3営業日以内）
                    </p>
                </form>
            </motion.div>
        </section>
    );
}
