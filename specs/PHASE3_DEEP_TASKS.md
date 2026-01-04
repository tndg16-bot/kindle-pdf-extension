# 🦁 Phase 3: Deep Layer Task System (Team Spec)

## 📡 Team Assignments (Simulated Parallel Work)
*   **PM (Antigravity)**: Architecture & Schema Definition.
*   **Backend (Serena)**: Update `types.ts` and `actions.ts` to support 3-layer recursion.
*   **Frontend (Claude)**: Implement "Drill-Down Modal" and update Kanban to fetch Level 3 tasks.
*   **QA (Scout)**: Verify data persistence and Kanban sync.

## 🏗️ Architecture Change
We are moving from a 2-Level structure to a 3-Level structure.

### New Hierarchy
1.  **Level 1 (Center Core)**: Ideal Self (Vision).
2.  **Level 2 (8 Areas)**: Strategic Means (e.g., "Build Asset 100M").
3.  **Level 3 (New)**: Actionable Tasks (e.g., "Open Securities Account", "Read Book").

### 💾 Data Schema Changes (Serena's Task)
Modify `MandalaCell` (Level 2) to hold an array of specialized tasks.

```typescript
// src/lib/types.ts
export interface SubTask {
  id: string;
  title: string;
  completed: boolean;
  difficulty: TaskDifficulty;
  createdAt: string;
}

export interface MandalaCell {
  id: string;
  title: string;
  // New Field
  subTasks: SubTask[]; 
}
```

### 🎨 UI Changes (Claude's Task)
1.  **Mandala View**:
    *   Clicking a Level 2 Cell (Means) **opens a Modal** (Dialog).
    *   Modal shows list of `subTasks`.
    *   User can Add/Delete/Edit `subTasks` inside the modal.
2.  **Kanban View**:
    *   **STOP** showing Level 2 cells.
    *   **START** showing Level 3 `subTasks` in the "To Do" column.

## 🔄 Verification Plan (Scout's Task)
1.  Add a sub-task "Buy Apple" to "Asset" area via Modal.
2.  Check Kanban -> "Buy Apple" should appear.
3.  Move "Buy Apple" to Done -> Check Modal -> Should be crossed out.
4.  Reload -> Data persists.
