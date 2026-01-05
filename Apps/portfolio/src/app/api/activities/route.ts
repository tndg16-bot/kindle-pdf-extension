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

interface Activity {
    date: string;
    message: string;
    type: 'milestone' | 'update' | 'completed';
}

function parseActivities(content: string): Activity[] {
    const activities: Activity[] = [];
    const lines = content.split('\n');

    let inMilestonesSection = false;

    for (const line of lines) {
        // Detect milestones section
        if (line.includes('### 🛠️ 開発の歩み')) {
            inMilestonesSection = true;
            continue;
        }
        if (line.startsWith('##') && !line.includes('開発の歩み')) {
            inMilestonesSection = false;
            continue;
        }

        // Parse milestone entries like "1. **2026-01-05**: Description"
        const milestoneMatch = line.match(/^\d+\.\s*\*\*(\d{4}-\d{2}-\d{2})\*\*:\s*(.+)/);
        if (milestoneMatch && inMilestonesSection) {
            activities.push({
                date: milestoneMatch[1],
                message: milestoneMatch[2].trim(),
                type: 'milestone',
            });
        }
    }

    // Sort by date descending (newest first)
    activities.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

    return activities.slice(0, 10); // Return only the 10 most recent
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

    return response.text();
}


export async function GET() {
    try {
        let content = '';

        if (process.env.GITHUB_TOKEN) {
            try {
                content = await fetchFromGitHub();
            } catch (ghError) {
                console.error('Failed to fetch from GitHub, falling back to local if available:', ghError);
                if (process.env.NODE_ENV === 'development') {
                    const filePath = path.join(OBSIDIAN_VAULT_PATH, YARITAI_FILE);
                    content = await fs.readFile(filePath, 'utf-8');
                } else {
                    throw ghError;
                }
            }
        } else {
            const filePath = path.join(OBSIDIAN_VAULT_PATH, YARITAI_FILE);
            content = await fs.readFile(filePath, 'utf-8');
        }

        const activities = parseActivities(content);

        return NextResponse.json({
            success: true,
            activities,
            lastUpdated: new Date().toISOString(),
            source: process.env.GITHUB_TOKEN ? 'github' : 'local'
        });
    } catch (error) {
        console.error('Error reading activities:', error);
        return NextResponse.json(
            {
                success: false,
                error: 'Failed to read activity data',
                activities: []
            },
            { status: 500 }
        );
    }
}
