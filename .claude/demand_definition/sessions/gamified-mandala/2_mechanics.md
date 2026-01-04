# 2. ⚙️ Game Mechanics & Logic

## 🎮 Core Loop
1.  **Define**: Create tasks in the Mandala Chart.
2.  **Plan**: Move tasks to "To Do" or "Doing" on the Kanban Board.
3.  **Execute**: Track time spent on the task.
4.  **Reward**: Task Complete -> XP Gained (based on Difficulty & Time) -> Tiger Grows.
5.  **Penalty**: Inactivity (3 days) -> Tiger Runs Away (Action required to bring back).

---

## 📐 Logic 1: XP & Difficulty (User Request Answered)
Combining "Difficulty" with "Time Tracking" for a robust XP formula.

### Calculation Formula
`Total XP = (Base XP * Difficulty Multiplier) + (Time Bonus)`

### Difficulty Tiers (Criteria Proposal)
*   **Rank S (Legendary)**: "Life Changing / High Anxiety". Something you've avoided for months.
    *   *Base XP*: 100
    *   *Example*: Filing Taxes, Major Client Presentation.
*   **Rank A (Hard)**: "Heavy Lift". requires deep focus, 2+ hours.
    *   *Base XP*: 50
    *   *Example*: Writing a spec doc, Coding a feature.
*   **Rank B (Normal)**: "Standard Work". Routine but necessary, 30-60 mins.
    *   *Base XP*: 20
    *   *Example*: Meeting, debugging, email clearing.
*   **Rank C (Tiny)**: "Micro Task". < 15 mins.
    *   *Base XP*: 5
    *   *Example*: Slack reply, payment transfer.

### Time Bonus
*   +1 XP per 10 minutes focused.

---

## 🐅 Logic 2: Tiger State
### Balance & Mood (The "Unbalanced" Feedback)
*   **Balance Graph**: The Mandala's 9 categories must grow evenly.
*   **Mood System**:
    *   **Happy**: All active categories > 50% fulfilled. Theme: Sunny.
    *   **Moody (Cloudy)**: Neglecting 1-2 major categories. Theme: Cloudy/Rainy. Tiger looks away.
    *   **Runaway (House Left)**: 3 Days of **0 Login/Activity**.
        *   *Recovery*: User must make a "Promise Contract" (Input a text promise) to bring the Tiger back.

### Evolution & Pokedex
*   **Generations**: Tiger starts as "Egg" -> "Cub" -> "Adult" -> "Awakened".
*   **Clear Condition**: Reaching "Awakened" form (Max Level).
*   **Pokedex**: Cleared Tigers are registered in a "Tiger History" gallery. User starts a new Generation (Gen 2).

---

## 📋 Logic 3: Workflow (Kanban)
The UI bridges the Mandala (Goal View) and Kanban (Task View).

*   **View 1: Mandala Map**: Big picture.
*   **View 2: Kanban Board**: The "Cockpit" for daily work.
    *   **To Do**: Tasks linked from Mandala.
    *   **Doing**: Timer active. (Time tracking happens here).
    *   **Done**: XP collected.
*   **Consistent Tags**: Kanban cards have the color of their Mandala Category.
