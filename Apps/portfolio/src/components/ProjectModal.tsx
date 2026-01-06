'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { X, CheckCircle2, Circle, Clock } from 'lucide-react';

interface Subtask {
    title: string;
    completed: boolean;
}

interface Project {
    name: string;
    status: 'not_started' | 'in_progress' | 'completed';
    description?: string;
    issueNumber?: number;
    subtasks?: Subtask[];
    progress?: number;
}

interface ProjectModalProps {
    isOpen: boolean;
    onClose: () => void;
    project: Project | null;
}

export default function ProjectModal({ isOpen, onClose, project }: ProjectModalProps) {
    if (!project) return null;

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        onClick={onClose}
                        className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
                    />

                    {/* Modal */}
                    <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: 20 }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none"
                    >
                        <div className="w-full max-w-2xl bg-zinc-900/90 border border-teal-500/20 rounded-3xl p-6 shadow-2xl pointer-events-auto max-h-[85vh] overflow-y-auto scrollbar-custom">

                            {/* Header */}
                            <div className="flex justify-between items-start mb-6">
                                <div>
                                    <h2 className="text-2xl font-bold text-white mb-2">{project.name}</h2>
                                    <div className="flex items-center gap-3 text-sm">
                                        <span className={`px-3 py-1 rounded-full border ${project.status === 'completed'
                                                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                                                : project.status === 'in_progress'
                                                    ? 'bg-amber-500/10 border-amber-500/30 text-amber-400'
                                                    : 'bg-zinc-500/10 border-zinc-500/30 text-zinc-400'
                                            }`}>
                                            {project.status === 'completed' ? 'Completed' :
                                                project.status === 'in_progress' ? 'In Progress' : 'Not Started'}
                                        </span>
                                        {project.progress !== undefined && (
                                            <span className="text-teal-400 font-mono">
                                                {project.progress}% Complete
                                            </span>
                                        )}
                                    </div>
                                </div>
                                <button
                                    onClick={onClose}
                                    className="p-2 hover:bg-white/10 rounded-full transition-colors text-zinc-400 hover:text-white"
                                >
                                    <X size={24} />
                                </button>
                            </div>

                            {/* Description */}
                            {project.description && (
                                <p className="text-zinc-400 mb-8 leading-relaxed">
                                    {project.description}
                                </p>
                            )}

                            {/* Subtasks */}
                            {project.subtasks && project.subtasks.length > 0 ? (
                                <div className="space-y-3">
                                    <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                                        <Clock size={20} className="text-teal-400" />
                                        <span>Steps & Progress</span>
                                    </h3>
                                    {project.subtasks.map((task, index) => (
                                        <div
                                            key={index}
                                            className={`flex items-start gap-4 p-4 rounded-xl border transition-colors ${task.completed
                                                    ? 'bg-emerald-900/10 border-emerald-500/20'
                                                    : 'bg-zinc-800/30 border-white/5'
                                                }`}
                                        >
                                            <div className="mt-1">
                                                {task.completed ? (
                                                    <CheckCircle2 size={20} className="text-emerald-400" />
                                                ) : (
                                                    <Circle size={20} className="text-zinc-600" />
                                                )}
                                            </div>
                                            <span className={`${task.completed ? 'text-zinc-400 line-through' : 'text-zinc-200'}`}>
                                                {task.title}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="text-center py-8 text-zinc-500 bg-zinc-800/20 rounded-xl border border-white/5">
                                    サブタスク情報はありません
                                </div>
                            )}

                            {/* Footer (Issue Link) */}
                            {project.issueNumber && (
                                <div className="mt-8 pt-6 border-t border-white/5 flex justify-end">
                                    <a
                                        href={`https://github.com/tndg16-bot/papa/issues/${project.issueNumber}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-sm text-zinc-500 hover:text-teal-400 transition-colors flex items-center gap-2"
                                    >
                                        GitHub Issue #{project.issueNumber} を開く ↗
                                    </a>
                                </div>
                            )}
                        </div>
                    </motion.div>
                </>
            )}
        </AnimatePresence>
    );
}
