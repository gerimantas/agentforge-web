# Development Plan: agentforge-web

> Purpose: Build an advanced web interface for the AgentForge framework that enables prompt engineering, agent orchestration, and cog/memory debugging—using fullstack-fastapi-starter as the scaffold, and preserving AgentForge as a clean, reusable library.

---

## 1. Project Architecture Overview

**1.1 DONE:**
- Scaffolding of FastAPI backend (from fullstack-fastapi-starter)
- React + Chakra UI frontend structure in place
- AgentForge is complete and stable as a CLI + importable core

**1.2 TO CHANGE:**
- Remove unnecessary DB/user routes from starter template
- Replace placeholder logic with LLM/agent/cog interfaces

**1.3 TO CREATE:**
- Modular backend logic for agent/cog integration
- Frontend components for live prompt editing, memory visualization, and cog execution

---

## 2. Backend Development

**2.1 DONE:**
- FastAPI scaffold

**2.2 TO CHANGE:**
- Adjust API structure to match agent/cog/memory logic

**2.3 TO CREATE:**
- `agent_loader`: Load & cache agent YAML definitions
- `cog_runner`: Run cogs through API
- `prompt_editor`: Enable prompt modifications in memory (not file)
- `memory_viewer`: Access structured and filtered memory states

**Function:** Modular logic allows decoupling between frontend and the internal agent execution engine.

---

## 3. API Design

**3.1 TO CREATE:**
- `/api/agents/`: List available agents
- `/api/agents/{id}`: Return agent config
- `/api/agents/{id}/run`: Submit prompt and get response
- `/api/agents/{id}/memory`: View memory state
- `/api/agents/{id}/prompt`: Update working prompt
- `/api/cogs/execute`: Execute single cog logic
- `/api/status/llm`: Check LLM backend availability

**Function:** REST interface exposes internal logic of AgentForge through agentforge-web for UI integration.

---

## 4. Frontend Development

**4.1 DONE:**
- UI layout using Chakra UI and routing exists from starter template

**4.2 TO CHANGE:**
- Replace default pages with custom ones for LLM workflows

**4.3 TO CREATE:**
- `AgentListPage`: Select agent from list
- `AgentRunnerPage`: Submit prompt and see LLM results
- `PromptEditor`: UI for modifying base/system/user prompts
- `MemoryViewer`: UI for memory state, filtering, structure/raw toggling
- `CogExecutor`: UI to submit and visualize YAML cog workflows

**Function:** UI components support interactive agent design and testing for non-developers and prompt engineers.

---

## 5. Advanced Features

**5.1 TO CREATE:**
- Prompt versioning: Save prompt drafts and compare output
- Streaming outputs: Token-level LLM streaming via SSE
- Cog visual editor: Interactive GUI to build YAML-based cogs
- Benchmark dashboard: Track token use, response speed, model usage
- Agent inspector: Show memory schema, agent config, LLM backend in use

**Function:** Adds real-world engineering support tools to make agent testing scientific and transparent.

---

## 6. Deployment & DevOps

**6.1 DONE:**
- Dockerfile base image present from starter

**6.2 TO CHANGE:**
- Add multistage builds for frontend/backend separation
- CI should remove unused template actions

**6.3 TO CREATE:**
- Vercel/Render deploy hooks
- `.env.staging`, `.env.production` config files
- GitHub Actions for lint/test/build
- `/startup_healthcheck` route to test YAML, LLM, memory

**Function:** Ensures agentforge-web is deployable, maintainable, and scalable

---

## 7. Coding Progress Module (NEW)

**7.1 TO CREATE:**
- `coding_progress/` module in backend
  - `development_plan.md`: Read-only version of this plan
  - `tracker.py`: Auto-detect implemented features from file structure
  - `data_schema.py`: Track statuses as enums per feature
- `/api/progress/items`: Return dynamic implementation state
- `/api/progress/plan`: Return static markdown of plan
- `CodingProgress.tsx`: Frontend page to render plan + current progress

**Function:** Non-editable, transparent progress report tied to development plan. Tracks feature completion and exposes diagnostics without affecting core logic.

---

## 8. Testing & Diagnostics

**8.1 TO CREATE:**
- Backend self-test suite:
  - YAML parsing validation
  - LLM connectivity check
  - Agent runtime smoke test
- Frontend self-test components:
  - LLM ping indicator
  - Prompt validity (max length, format)

**Function:** Detect configuration errors early, ensure that all modules are testable and test-covered.

---

## Final Summary

| Area                   | Status     | Action                                     |
| ---------------------- | ---------- | ------------------------------------------ |
| Backend API structure  | 🟡 Partial | Replace default routes, add agent logic    |
| Frontend UI            | 🟡 Partial | Build custom pages from Chakra components  |
| AgentForge integration | 🔵 Stable  | Used as a read-only importable module      |
| Deployment             | 🟡 Partial | Docker setup present, needs full CI/CD     |
| Prompt engineering UX  | 🔴 Missing | Plan but no implementation yet             |
| Cog builder/streaming  | 🔴 Missing | Needs design & implementation              |
| Progress module        | 🔴 Missing | Build tracker, expose endpoints, lock plan |

---

This plan serves as both a milestone reference and implementation contract. All changes and new modules must conform to this logical structure and function documentation.
