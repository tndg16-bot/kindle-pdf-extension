# 4. ✅ Requirements & Acceptance Criteria

## 👤 User Stories
*   As a user, I want to manage tasks in a **Kanban Board** (To Do / Doing / Done) so I can visualize my daily workflow.
*   As a user, I want to **track time** on tasks in the "Doing" column to earn time-based XP.
*   As a user, I want to set a **Difficulty Rank (S/A/B/C)** for each task.
*   As a user, I want to see visual feedback (Clouds/Sun) based on my task balance.
*   As a user, I want a "Pokedex" to view my past successes (Evolved Tigers).

## 🧪 Acceptance Criteria (MVP)

### 🎨 UI/UX (Frontend)
- [ ] **Mandala View**: 3x3 Zoom Grid (Unchanged).
- [ ] **Kanban View**: Drag & Drop board. Cards show color tags matching Mandala categories.
- [ ] **Timer Widget**: Start/Stop button on "Doing" cards.
- [ ] **Tiger HUD**:
    - [ ] Display XP/Level.
    - [ ] **Weather System**: Background changes based on "Mood" state.
    - [ ] **Action**: "Promise" button appears if Tiger has 'Runaway'.

### ⚙️ Logic & Data (Backend)
- [ ] **XP Calculation**: Implement Formula `(Base * Diff) + Time`.
- [ ] **Inactivity Tracker**: Timestamp last login. If > 3 days, set status to `RUNAWAY`.
- [ ] **Evolution Logic**: Thresholds for evolution (e.g., Lvl 10 -> Adult).
- [ ] **Data Structure**: `tasks.json` (Kanban items), `user_stats.json` (Tiger data).

### 📄 Add-on: Goal Setting
- [ ] A dedicated "Goal Setting Mode" that guides the user to fill out the Mandala Chart.
