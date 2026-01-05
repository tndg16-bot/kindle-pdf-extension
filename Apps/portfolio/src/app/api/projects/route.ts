import { NextResponse } from 'next/server';
import { promises as fs } from 'fs';
import path from 'path';

// Environment variables for GitHub integration
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'tndg16-bot';
const GITHUB_REPO = process.env.GITHUB_REPO || 'papa';
const GITHUB_FILE_PATH = process.env.GITHUB_FILE_PATH || '本山貴裕/やりたいことリスト.md';

// Fallback for local development
const OBSIDIAN_VAULT_PATH = process.env.OBSIDIAN_VAULT_PATH || 'C:/Users/chatg/Obsidian Vault/papa';
const YARITAI_FILE = '本山貴裕/やりたいことリスト.md';

interface Project {
    name: string;
    status: 'not_started' | 'in_progress' | 'completed';
    description?: string;
}

interface Stats {
    total: number;
    inProgress: number;
    completed: number;
    notStarted: number;
}

function parseYaritaiList(content: string): { projects: Project[]; stats: Stats } {
    const projects: Project[] = [];
    const lines = content.split('\n');

    let inWantSection = false;
    let inDoneSection = false;
    let inAntigravitySection = false;

    for (const line of lines) {
        if (line.includes('## 🚀 やりたいことリスト')) {
            inWantSection = true;
            inDoneSection = false;
            inAntigravitySection = false;
            continue;
        }
        if (line.includes('## ✅ やったことリスト')) {
            inWantSection = false;
            inDoneSection = true;
            inAntigravitySection = false;
            continue;
        }
        if (line.includes('## 🤖 Antigravityからの提案')) {
            inWantSection = false;
            inDoneSection = false;
            inAntigravitySection = true;
            continue;
        }
        if (line.startsWith('## ') && !line.includes('やりたい') && !line.includes('やったこと') && !line.includes('Antigravity')) {
            inWantSection = false;
            inDoneSection = false;
            inAntigravitySection = false;
            continue;
        }

        // Match M-items with various status formats:
        // [ ] = not started, [x] = completed, [/] = in progress, [3/10] = in progress with ratio
        const mItemMatch = line.match(/^\s*-\s*\[([^\]]*)\]\s*\*\*M\d+:\s*(.+?)\*\*/);
        if (mItemMatch && inWantSection) {
            const statusMark = mItemMatch[1].trim();
            let status: 'not_started' | 'in_progress' | 'completed' = 'not_started';
            let progress: string | undefined;

            if (statusMark === 'x') {
                status = 'completed';
            } else if (statusMark === '/') {
                status = 'in_progress';
            } else if (/^\d+\/\d+$/.test(statusMark)) {
                // Format like [3/10] - treat as in_progress with progress info
                status = 'in_progress';
                progress = statusMark;
            } else if (statusMark === '') {
                status = 'not_started';
            }

            projects.push({
                name: mItemMatch[2].trim(),
                status,
                description: progress ? `進捗: ${progress}` : undefined,
            });
        }


        // Match completed items in Done section (exclude date entries like "2026-01-05")
        const doneMatch = line.match(/^\d+\.\s*\*\*(.+?)\*\*:/);
        if (doneMatch && inDoneSection) {
            const projectName = doneMatch[1].trim();
            // Skip date entries (format: YYYY-MM-DD or similar)
            if (!/^\d{4}-\d{2}-\d{2}/.test(projectName)) {
                projects.push({
                    name: projectName,
                    status: 'completed',
                });
            }
        }


        const inProgressMatch = line.match(/^-\s*\*\*(.+?)\*\*\s*-\s*(.+)/);
        if (inProgressMatch && inAntigravitySection) {
            if (line.includes('進捗') || line.includes('進行中')) {
                projects.push({
                    name: inProgressMatch[1].trim(),
                    status: 'in_progress',
                    description: inProgressMatch[2].trim(),
                });
            }
        }
    }

    const stats: Stats = {
        total: projects.length,
        inProgress: projects.filter(p => p.status === 'in_progress').length,
        completed: projects.filter(p => p.status === 'completed').length,
        notStarted: projects.filter(p => p.status === 'not_started').length,
    };

    return { projects, stats };
}

async function fetchFromGitHub(): Promise<string> {
    if (!GITHUB_TOKEN) {
        throw new Error('GITHUB_TOKEN is not set');
    }

    const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${encodeURIComponent(GITHUB_FILE_PATH)}`;
    const response = await fetch(url, {
        headers: {
            'Authorization': `Bearer ${GITHUB_TOKEN}`,
            'Accept': 'application/vnd.github.v3.raw', // Request raw content directly
        },
        next: { revalidate: 300 } // Cache for 5 minutes (ISR)
    });

    if (!response.ok) {
        throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
    }

    // With v3.raw media type, the body is the raw content
    return response.text();
}

export async function GET() {
    try {
        let content = '';

        // Strategy: Try GitHub first if configured, otherwise fallback to local fs (dev mode)
        if (process.env.GITHUB_TOKEN) {
            try {
                content = await fetchFromGitHub();
                console.log('Successfully fetched project data from GitHub');
            } catch (ghError) {
                console.error('Failed to fetch from GitHub, falling back to local if available:', ghError);
                if (process.env.NODE_ENV === 'development') {
                    const filePath = path.join(OBSIDIAN_VAULT_PATH, YARITAI_FILE);
                    content = await fs.readFile(filePath, 'utf-8');
                } else {
                    throw ghError; // Re-throw in production if GitHub fails
                }
            }
        } else {
            // Local development without token
            const filePath = path.join(OBSIDIAN_VAULT_PATH, YARITAI_FILE);
            content = await fs.readFile(filePath, 'utf-8');
        }

        const { projects, stats } = parseYaritaiList(content);

        return NextResponse.json({
            success: true,
            projects,
            stats,
            lastUpdated: new Date().toISOString(),
            source: process.env.GITHUB_TOKEN ? 'github' : 'local'
        });
    } catch (error) {
        console.error('Error reading project data:', error);
        return NextResponse.json(
            {
                success: false,
                error: 'Failed to read project data',
                projects: [],
                stats: { total: 0, inProgress: 0, completed: 0, notStarted: 0 }
            },
            { status: 500 }
        );
    }
}
