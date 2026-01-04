# 🦁 Project Organization Chart: Gamified Mandala

## 👑 Main Agent (Project Manager & Approver)
**Gravity (Antigravity)**
*   **Role**: Project Manager, Architect, Final Decision Maker.
*   **Authority**: Has full authority to approve/reject code from Sub-Agents on behalf of the User.
*   **Responsibility**:
    *   Defines Specifications (Demand Definition).
    *   Reviews Implementation Plans.
    *   Verifies Deliverables (QA).

## 🛠️ Sub-Agents (Specialists)
**Claude (The Builder)**
*   **Role**: Lead Developer (Frontend/Backend).
*   **Responsibility**:
    *   Writing Next.js / React code.
    *   Implementing Game Logic (XP, mechanics).
    *   UI Design (Tailwind/Shadcn).

**Serena (The Scribe)**
*   **Role**: Documentation & Python Specialist.
*   **Responsibility**:
    *   Writing Documentation (README, Mechanics).
    *   Data Analysis (if needed).

**Scout (The Navigator)**
*   **Role**: Research & Environment Setup.
*   **Responsibility**:
    *   Web Research (Tech stack solutions).
    *   Initial Scaffolding (Creating folders, installing deps).

---

## 📜 Approval Workflow
1.  **Gravity** defines the task.
2.  **Claude/Scout** executes the task.
3.  **Gravity** verifies the result.
    *   *If Good*: Gravity approves and proceeds.
    *   *If Bad*: Gravity creates a fix ticket.
4.  **User** is notified only upon major milestones or completion.
