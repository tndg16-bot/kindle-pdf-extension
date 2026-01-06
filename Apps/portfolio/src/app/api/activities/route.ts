import { NextResponse } from 'next/server';

// Environment variables for GitHub integration
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'tndg16-bot';
const GITHUB_REPO = process.env.GITHUB_REPO || 'papa';

interface GitHubCommit {
    sha: string;
    commit: {
        message: string;
        author: {
            name: string;
            date: string;
        };
    };
}

interface Activity {
    date: string;
    message: string;
    type: 'milestone' | 'update' | 'completed';
    sha?: string;
}

function determineActivityType(message: string): 'milestone' | 'update' | 'completed' {
    const lowerMessage = message.toLowerCase();

    if (lowerMessage.includes('feat:') || lowerMessage.includes('feature')) {
        return 'milestone';
    }
    if (lowerMessage.includes('fix:') || lowerMessage.includes('complete') || lowerMessage.includes('close')) {
        return 'completed';
    }
    return 'update';
}

function formatCommitMessage(message: string): string {
    // Remove conventional commit prefixes and clean up
    return message
        .replace(/^(feat|fix|chore|docs|style|refactor|perf|test|build|ci)(\(.+?\))?:\s*/i, '')
        .split('\n')[0] // Get only first line
        .trim();
}

function formatDate(isoDate: string): string {
    const date = new Date(isoDate);
    return date.toISOString().split('T')[0]; // YYYY-MM-DD format
}

async function fetchGitHubCommits(): Promise<GitHubCommit[]> {
    const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/commits?per_page=10`;

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

    return response.json();
}

function parseCommitsToActivities(commits: GitHubCommit[]): Activity[] {
    return commits.map(commit => ({
        date: formatDate(commit.commit.author.date),
        message: formatCommitMessage(commit.commit.message),
        type: determineActivityType(commit.commit.message),
        sha: commit.sha.substring(0, 7),
    }));
}

export async function GET() {
    try {
        const commits = await fetchGitHubCommits();
        const activities = parseCommitsToActivities(commits);

        return NextResponse.json({
            success: true,
            activities,
            lastUpdated: new Date().toISOString(),
            source: 'github-commits'
        });
    } catch (error) {
        console.error('Error fetching GitHub commits:', error);

        // Return fallback activities
        const fallbackActivities: Activity[] = [
            { date: '2026-01-07', message: 'Add custom dark-themed scrollbar with teal accent', type: 'update', sha: '093b1ae' },
            { date: '2026-01-07', message: 'Add scrollable lists to Dashboard', type: 'milestone', sha: '7319b88' },
            { date: '2026-01-07', message: 'Add fallback data when GitHub API fails', type: 'completed', sha: '00e26e3' },
            { date: '2026-01-07', message: 'Switch activities API to GitHub commits integration', type: 'milestone', sha: 'eb718d0' },
            { date: '2026-01-07', message: 'Switch API from yaritai list to GitHub Issues integration', type: 'milestone', sha: '45bed17' },
            { date: '2026-01-06', message: 'Add About page and Header to Sessions page', type: 'milestone', sha: '7fb7e0a' },
        ];

        return NextResponse.json({
            success: true,
            activities: fallbackActivities,
            lastUpdated: new Date().toISOString(),
            source: 'fallback'
        });
    }
}

