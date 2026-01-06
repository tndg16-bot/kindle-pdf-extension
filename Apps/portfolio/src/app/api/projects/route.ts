import { NextResponse } from 'next/server';

// Environment variables for GitHub integration
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'tndg16-bot';
const GITHUB_REPO = process.env.GITHUB_REPO || 'papa';

interface GitHubIssue {
    number: number;
    title: string;
    state: string;
    labels: { name: string }[];
    body: string | null;
}

interface Project {
    name: string;
    status: 'not_started' | 'in_progress' | 'completed';
    description?: string;
    issueNumber?: number;
}

interface Stats {
    total: number;
    inProgress: number;
    completed: number;
    notStarted: number;
}

function parseIssueStatus(issue: GitHubIssue): 'not_started' | 'in_progress' | 'completed' {
    // Check if issue is closed
    if (issue.state === 'closed') {
        return 'completed';
    }

    // Check for in-progress labels
    const inProgressLabels = ['in-progress', 'in progress', 'wip', 'doing'];
    const hasInProgressLabel = issue.labels.some(label =>
        inProgressLabels.includes(label.name.toLowerCase())
    );

    if (hasInProgressLabel) {
        return 'in_progress';
    }

    // Check title for M-number items with progress indicators
    const progressMatch = issue.title.match(/\[(\d+)\/(\d+)\]/);
    if (progressMatch) {
        const current = parseInt(progressMatch[1]);
        const total = parseInt(progressMatch[2]);
        if (current > 0 && current < total) return 'in_progress';
        if (current >= total) return 'completed';
    }

    // Default to not_started for open issues
    return 'not_started';
}

async function fetchGitHubIssues(): Promise<GitHubIssue[]> {
    const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/issues?state=all&per_page=100`;

    const headers: HeadersInit = {
        'Accept': 'application/vnd.github.v3+json',
    };

    if (GITHUB_TOKEN) {
        headers['Authorization'] = `Bearer ${GITHUB_TOKEN}`;
    }

    const response = await fetch(url, {
        headers,
        cache: 'no-store' // Disable caching for real-time data
    });

    if (!response.ok) {
        throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
    }

    const issues: GitHubIssue[] = await response.json();

    // Filter to only M-numbered issues (project items)
    return issues.filter(issue =>
        issue.title.match(/^\[M\d+\]/) ||
        issue.title.includes('[Portfolio]') ||
        issue.title.includes('[Infra]')
    );
}

function parseGitHubIssues(issues: GitHubIssue[]): { projects: Project[]; stats: Stats } {
    const projects: Project[] = issues.map(issue => {
        // Extract clean name from title (remove [M1] etc.)
        const cleanName = issue.title
            .replace(/^\[M\d+\]\s*/, '')
            .replace(/^\[Portfolio\]\s*/, '')
            .replace(/^\[Infra\]\s*/, '');

        return {
            name: cleanName,
            status: parseIssueStatus(issue),
            description: issue.body?.slice(0, 100) || undefined,
            issueNumber: issue.number,
        };
    });

    const stats: Stats = {
        total: projects.length,
        inProgress: projects.filter(p => p.status === 'in_progress').length,
        completed: projects.filter(p => p.status === 'completed').length,
        notStarted: projects.filter(p => p.status === 'not_started').length,
    };

    return { projects, stats };
}

export async function GET() {
    try {
        const issues = await fetchGitHubIssues();
        const { projects, stats } = parseGitHubIssues(issues);

        return NextResponse.json({
            success: true,
            projects,
            stats,
            lastUpdated: new Date().toISOString(),
            source: 'github-issues'
        });
    } catch (error) {
        console.error('Error fetching GitHub issues:', error);

        // Return mock data for development/fallback
        const fallbackProjects = [
            { name: 'ノウハウ依存脱却ワークの開発', status: 'in_progress' as const, issueNumber: 6 },
            { name: '自己肯定感の源泉発見セッション', status: 'not_started' as const, issueNumber: 7 },
            { name: '過去の解釈変換メソッド', status: 'not_started' as const, issueNumber: 8 },
            { name: '人は人を通して磨かれる', status: 'not_started' as const, issueNumber: 9 },
            { name: '独自の商品設計', status: 'not_started' as const, issueNumber: 10 },
            { name: '案件獲得戦略', status: 'not_started' as const, issueNumber: 11 },
            { name: '最速収益化ロードマップ', status: 'not_started' as const, issueNumber: 12 },
            { name: '本業×副業統合戦略', status: 'not_started' as const, issueNumber: 13 },
            { name: 'Claude Code並列開発', status: 'in_progress' as const, issueNumber: 14 },
            { name: 'Git/GitHub連携', status: 'not_started' as const, issueNumber: 15 },
            { name: 'ポートフォリオサイト完成', status: 'completed' as const, issueNumber: 1 },
        ];

        return NextResponse.json({
            success: true,
            projects: fallbackProjects,
            stats: {
                total: fallbackProjects.length,
                inProgress: fallbackProjects.filter(p => p.status === 'in_progress').length,
                completed: fallbackProjects.filter(p => p.status === 'completed').length,
                notStarted: fallbackProjects.filter(p => p.status === 'not_started').length,
            },
            lastUpdated: new Date().toISOString(),
            source: 'fallback'
        });
    }
}

