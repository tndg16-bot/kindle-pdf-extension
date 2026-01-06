"use client";


import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, Clock, Circle, TrendingUp, Activity, ChevronRight } from "lucide-react";
import ProjectModal from "./ProjectModal";

interface Subtask {
    title: string;
    completed: boolean;
}

interface Project {
    name: string;
    status: "not_started" | "in_progress" | "completed";
    description?: string;
    issueNumber?: number;
    subtasks?: Subtask[];
    progress?: number;
}

interface Stats {
    total: number;
    inProgress: number;
    completed: number;
    notStarted: number;
}

interface ActivityItem {
    date: string;
    message: string;
    type: "milestone" | "update" | "completed";
}

export default function Dashboard() {
    const [projects, setProjects] = useState<Project[]>([]);
    const [stats, setStats] = useState<Stats>({ total: 0, inProgress: 0, completed: 0, notStarted: 0 });
    const [activities, setActivities] = useState<ActivityItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [lastUpdated, setLastUpdated] = useState<string>("");

    // Modal state
    const [selectedProject, setSelectedProject] = useState<Project | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        async function fetchData() {
            try {
                const [projectsRes, activitiesRes] = await Promise.all([
                    fetch("/api/projects"),
                    fetch("/api/activities"),
                ]);

                const projectsData = await projectsRes.json();
                const activitiesData = await activitiesRes.json();

                if (projectsData.success) {
                    setProjects(projectsData.projects);
                    setStats(projectsData.stats);
                    setLastUpdated(projectsData.lastUpdated);
                }

                if (activitiesData.success) {
                    setActivities(activitiesData.activities);
                }
            } catch (error) {
                console.error("Error fetching dashboard data:", error);
            } finally {
                setLoading(false);
            }
        }

        fetchData();

        // Refresh every 5 minutes
        const interval = setInterval(fetchData, 5 * 60 * 1000);
        return () => clearInterval(interval);
    }, []);

    const handleProjectClick = (project: Project) => {
        setSelectedProject(project);
        setIsModalOpen(true);
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case "completed":
                return <CheckCircle2 className="h-5 w-5 text-emerald-400" />;
            case "in_progress":
                return <Clock className="h-5 w-5 text-amber-400" />;
            default:
                return <Circle className="h-5 w-5 text-zinc-500" />;
        }
    };

    const getStatusLabel = (status: string) => {
        switch (status) {
            case "completed":
                return "完了";
            case "in_progress":
                return "進行中";
            default:
                return "未着手";
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-400"></div>
            </div>
        );
    }

    return (
        <section className="w-full max-w-6xl mx-auto px-4 py-16">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <h2 className="text-3xl font-bold text-white">
                        🎯 プロジェクト進捗
                    </h2>
                    <span className="text-sm text-zinc-500" suppressHydrationWarning>
                        最終更新: {lastUpdated ? new Date(lastUpdated).toLocaleString("ja-JP") : "-"}
                    </span>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                    <div className="glass-panel rounded-2xl p-4 text-center">
                        <div className="text-3xl font-bold text-white">{stats.total}</div>
                        <div className="text-sm text-zinc-400">合計</div>
                    </div>
                    <div className="glass-panel rounded-2xl p-4 text-center">
                        <div className="text-3xl font-bold text-amber-400">{stats.inProgress}</div>
                        <div className="text-sm text-zinc-400">進行中</div>
                    </div>
                    <div className="glass-panel rounded-2xl p-4 text-center">
                        <div className="text-3xl font-bold text-emerald-400">{stats.completed}</div>
                        <div className="text-sm text-zinc-400">完了</div>
                    </div>
                    <div className="glass-panel rounded-2xl p-4 text-center">
                        <div className="text-3xl font-bold text-zinc-500">{stats.notStarted}</div>
                        <div className="text-sm text-zinc-400">未着手</div>
                    </div>
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                    {/* Projects List */}
                    <div className="glass-panel rounded-3xl p-6">
                        <div className="flex items-center gap-2 mb-6">
                            <TrendingUp className="h-5 w-5 text-teal-400" />
                            <h3 className="text-xl font-bold text-white">プロジェクト一覧</h3>
                        </div>
                        <div className="space-y-3 max-h-80 overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-transparent">
                            {projects.map((project, index) => (
                                <motion.div
                                    key={project.name}
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{ delay: index * 0.1 }}
                                    onClick={() => handleProjectClick(project)}
                                    className="flex items-center gap-3 p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all cursor-pointer group border border-transparent hover:border-teal-500/20"
                                >
                                    {getStatusIcon(project.status)}
                                    <div className="flex-1 min-w-0">
                                        <div className="text-sm font-medium text-white truncate group-hover:text-teal-400 transition-colors">
                                            {project.name}
                                        </div>
                                        {project.description && (
                                            <div className="text-xs text-zinc-500 truncate">
                                                {project.description}
                                            </div>
                                        )}
                                        {project.progress !== undefined && project.progress > 0 && (
                                            <div className="w-full h-1 bg-zinc-800 rounded-full mt-2 overflow-hidden">
                                                <div
                                                    className="h-full bg-teal-500/50 rounded-full"
                                                    style={{ width: `${project.progress}%` }}
                                                />
                                            </div>
                                        )}
                                    </div>
                                    <div className="flex flex-col items-end gap-1">
                                        <span className={`text-xs px-2 py-1 rounded-full ${project.status === "completed" ? "bg-emerald-500/20 text-emerald-400" :
                                            project.status === "in_progress" ? "bg-amber-500/20 text-amber-400" :
                                                "bg-zinc-500/20 text-zinc-400"
                                            }`}>
                                            {getStatusLabel(project.status)}
                                        </span>
                                        <ChevronRight size={14} className="text-zinc-600 group-hover:text-teal-400 transition-colors opacity-0 group-hover:opacity-100" />
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>

                    {/* Activity Feed */}
                    <div className="glass-panel rounded-3xl p-6">
                        <div className="flex items-center gap-2 mb-6">
                            <Activity className="h-5 w-5 text-teal-400" />
                            <h3 className="text-xl font-bold text-white">最近の活動</h3>
                        </div>
                        <div className="space-y-4 max-h-80 overflow-y-auto pr-2 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-transparent">
                            {activities.length > 0 ? (
                                activities.map((activity, index) => (
                                    <motion.div
                                        key={`${activity.date}-${index}`}
                                        initial={{ opacity: 0, x: 10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                        className="flex gap-3"
                                    >
                                        <div className="flex-shrink-0 w-2 h-2 mt-2 rounded-full bg-teal-400" />
                                        <div>
                                            <div className="text-xs text-zinc-500">{activity.date}</div>
                                            <div className="text-sm text-zinc-200">{activity.message}</div>
                                        </div>
                                    </motion.div>
                                ))
                            ) : (
                                <div className="text-center text-zinc-500 py-8">
                                    最近の活動がありません
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <ProjectModal
                    isOpen={isModalOpen}
                    onClose={() => setIsModalOpen(false)}
                    project={selectedProject}
                />
            </motion.div>
        </section>
    );
}
