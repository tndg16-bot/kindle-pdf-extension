# 🗣️ AskUserQuestionTool Skill (ask-user-question)

## 🎯 Goal
To implement Thariq's "Specification-First Development" methodology. Before generating any specs or code, conducting a deep-dive interview to gather comprehensive insights.

## 🔄 Workflow

### Phase 1: Deep Dive Interview (The 40 Questions)
Do not assume. Ask. Select relevant questions from the 5 categories below based on the project stage.
*   **I. Introduction & Background**: Understanding the user's context.
*   **II. Usage & Behavior**: How the solution fits into their workflow.
*   **III. Perception & Value**: Expected benefits and trust.
*   **IV. Future & Improvement**: Long-term vision and features.
*   **V. Closing**: Final thoughts.

### Phase 1.5: Core Logic & Mechanics Deep Dive (MANDATORY for Apps)
**⚠️ User Rule: Never stop at surface-level specs.**
If building an application/tool, you MUST ask about the "Soul" of the Logic:
1.  **Calculation Logic**: How are numbers/scores calculated? (Formulas, weights)
2.  **Feedback Loop**: How does the system respond to success/failure? (Visuals, penalties)
3.  **Workflow Trigger**: Exactly *when* and *how* does the user interact? (Real-time vs Batch)
4.  **Edge Cases**: What happens if the user does nothing? (Decay, Reset)
5.  **End Game**: What is the ultimate goal state? (Completion, Endless, Evolution)

### Phase 2: Specification Generation
Only after the interview is complete, generate the "Single Source of Truth" documents in `.claude/demand_definition/sessions/[feature-name]/`.

## 📋 Interview Question Bank (Select 5-10 relevant ones initially)

**I. Introduction & Background**
1. Can you tell me a bit about yourself and your professional field/daily routine?
2. What tools or services do you currently use that are similar?
3. What were your primary motivations or goals when you first started looking for a solution?

**II. Usage & Behavior**
4. Can you describe a typical scenario or task for which you use this product?
5. How often do you use it? (e.g., daily, weekly, monthly)
6. Describe a time when this product particularly helped you achieve a goal.
7. What other tools or systems do you need to use alongside this?

**III. Perception & Value**
8. What do you expect to benefit from using this?
9. Do you feel this product is created for you? Why or why not?
10. What would prevent you from using this in the future?

**IV. Future & Improvement**
11. Are there any features you wish this product had?
12. What are the most important tasks you need to perform that could be improved?
13. What comes to mind if you imagine this product five years from now?

**V. Closing**
14. Is there anything else about your experience that you'd like to share?
15. Have we missed anything important that you think we should know?
