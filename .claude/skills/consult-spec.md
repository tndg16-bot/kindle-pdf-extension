# 🗣️ Consultation-First Requirements Definition Skill (consult-spec)

## 🎯 Goal
To eliminate "Ambiguous Implementation" by conducting a structured consultation session with the user *before* writing any code. The output is a set of defined Markdown files that serve as the blueprint for development.

## 🔄 Workflow

### Phase 1: Hearing (Deep Dive)
Antigravity asks clarifying questions to uncover the true "Why" and "What".
*   "What is the core problem being solved?"
*   "Who is the user?"
*   "What are the 'Must-Haves' vs 'Nice-to-Haves'?"

### Phase 2: Definition (Document Generation)
Once aligned, generate the following artifacts in `.claude/demand_definition/sessions/[feature-name]/`:
1.  **`1_purpose.md`**: Problem statement and core value proposition.
2.  **`2_alternatives.md`**: Alternative approaches considered and why this one was chosen.
3.  **`3_scope.md`**: MVP scope definition (In/Out).
4.  **`4_requirements.md`**: Detailed user stories and acceptance criteria (The "Spec").
5.  **`5_ui_prompt.md`**: (Optional) UI design prompts if applicable.

### Phase 3: Agreement
Present the summary to the user. Only when approved, invoke the `feature-tdd` skill to begin Implementation.

## 📝 Output Format Example (4_requirements.md)
```markdown
## User Stories
- [ ] As a user, I want to...

## Acceptance Criteria (Tests)
- [ ] [UI] It should display...
- [ ] [Logic] It should calculate...
```
