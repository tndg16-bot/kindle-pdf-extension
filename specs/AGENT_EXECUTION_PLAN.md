# 🤖 Agent Execution Plan: MVP Delivery
**Objective**: Build & Deploy Gamified Mandala by Jan 5th.
**PM**: Antigravity

## 👥 Agent Roster & Roles
*   **Antigravity (PM)**: Review code, manage state, deploy to Vercel.
*   **Claude (Frontend)**: React/Next.js UI, Tailwind, Framer Motion, Sounds.
*   **Serena (Backend)**: Firebase Setup, Auth Integration, Data Models (Types).
*   **Picasso (Designer)**: **[NEW]** UI/UX Design, Asset Generation (Tiger Images), Visual Review.
*   **Scout (QA)**: Manual Verification (Browser), Mobile Responsiveness check.

## 🚦 Agent Task Board (Parallel Execution)

### 👩‍💻 Serena (Backend & Data)
*   **Mission**: Ensure Data Persistence & Cloud Integration.
    *   [x] **Step 1 (Done)**: Create `lib/firestore_service.ts` & `firebase.ts`.
    *   [ ] **Step 2 [AUTO]**: Refactor `actions.ts` to use "Hybrid Logic" (Load from Firestore if logged in, else Local).
    *   [ ] **Step 3 [AUTO]**: Implement "Data Merge" (Import local JSON data to Firestore upon first login).
    *   [ ] **Step 4 [AUTO]**: Verify basic CRUD (Add/Toggle SubTask) interacts with Firestore.
    *   **🛑 CHECKPOINT**: "All Backend Logic Verified. Data is saving to Cloud."

### 🎨 Picasso (Design & Assets)
*   **Mission**: Create the Visual Identity.
    *   [x] **Step 1 (Done)**: Generate 4 Stages of Tiger Evolution (Baby, Child, Adult, God).
    *   [ ] **Step 2 [AUTO]**: Create "Favicon" and "OG Image" (Social Share card).
    *   [ ] **Step 3 [AUTO]**: Review the App UI and provide a "Design Polish List" to Claude.
    *   **🛑 CHECKPOINT**: "Design Assets Complete. UI Review Finished."

### 👓 Claude (Frontend & UX)
*   **Mission**: Build the Interface & Game Feel.
    *   [x] **Step 1 (Done)**: Implement `TigerAvatar` & Login Screen.
    *   [ ] **Step 2 [AUTO]**: **Integration**: Connect `page.tsx` to `TigerAvatar` (Show real level).
    *   [ ] **Step 3 [AUTO]**: **Gamification**: Play Sound Effects on Task Complete.
    *   [ ] **Step 4 [AUTO]**: **Kanban**: Implement Time/Category Filters.
    *   **🛑 CHECKPOINT**: "Frontend Features Complete. Ready for User Verification."

### 🕹️ Antigravity (PM & Deployment)
*   **Mission**: Orchestration & Final Delivery.
    *   [ ] **Step 1 [AUTO]**: Monitor Lint Errors & Fix them (Ongoing).
    *   [ ] **Step 2 [AUTO]**: Guide User through `firebase init` (Deployment Setup).
    *   [ ] **Step 3 [AUTO]**: Run final Build Check (`npm run build`).
    *   **🛑 CHECKPOINT**: "Ready to Deploy to Vercel/Firebase Hosting."

---
*Tags*:
*   **[AUTO]**: Agents execute immediately without stopping.
*   **[DONE]**: Completed tasks.
*   **🛑 CHECKPOINT**: User Alert required. Antigravity will notify you.
