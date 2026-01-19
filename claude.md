# Workflow Orchestration System Project

**CC-Centric Task Orchestration Architecture**

---

## 📋 Quick Reference

**Project Location:** `/Users/mark/PycharmProjects/workflow`
**Purpose:** Design and implement a CC-centric orchestration system where Claude Code acts as the control plane
**Developer:** Mark (mark@emm-associates.com)
**Status:** Planning Complete, Implementation Pending
**Last Updated:** January 19, 2026

---

## 🎯 Project Overview

This project contains the design and implementation of a **Claude Code-centric orchestration system** that transforms CC from a direct executor into an intelligent control plane. CC delegates repetitive execution tasks to headless workers while maintaining oversight, verification, and decision-making authority.

**Core Principle:** *"AI should think until confident, act once deterministically, record results, and stop."*

### Primary Use Case
Hugo website development workflow (klm-migrate, klm-plan projects)

### Architecture
```
YOU → CLAUDE CODE (Control Plane) → TASK FILES → WORKERS → RESULTS → CC Verifies
```

---

## 📂 Key Documents

### Planning & Architecture (Read These First)

1. **PLAN.md** - Complete implementation plan
   - Phase-by-phase roadmap
   - File structures and schemas
   - Worker implementations
   - Success metrics and testing

2. **project.md** - Architecture mandate (excerpt from larger doc)
   - System philosophy
   - Planning mandate for Claude Code
   - Success criteria
   - Non-goals

3. **HL AI Orchastration.md** - CC-centric architecture philosophy
   - Why CC as control plane
   - Task exchange layer design
   - Worker patterns
   - Cost and risk management

4. **Claude Code Instructions.md** - CC role and responsibilities
   - What CC should/shouldn't do
   - Workflow rules
   - Safety guidelines

5. **chat_conv.md** - Historical context from prior AI conversations
   - Design discussions
   - Decision rationale

---

## 🏗️ Implementation Status

### Completed
✅ Architecture design
✅ Task/result file format specification
✅ Worker pattern design
✅ CC integration workflows
✅ Planning documentation

### In Progress
🔄 Phase 1: Foundation (not started)
- Directory structure setup
- Task templates
- Worker implementations

### Pending
⏳ Phase 2: Worker Implementation
⏳ Phase 3: CC Integration
⏳ Phase 4: Process Integration

---

## 🎨 System Components

### Task Exchange Layer
**Location:** `tasks/` folder (to be created)

File-based contracts between CC and workers:
- `tasks/pending/` - CC writes task files here
- `tasks/in-progress/` - Workers move tasks here during execution
- `tasks/completed/` - Completed tasks (audit trail)
- `tasks/failed/` - Failed tasks for review
- `tasks/templates/` - Reusable templates

### Results Layer
**Location:** `results/` folder (to be created)

Workers write execution results:
- `results/YYYY-MM-DD/` - Results organized by date
- Structured YAML frontmatter + markdown body
- Includes logs, metrics, errors

### Workers
**Location:** `workers/` folder (to be created)

Headless execution agents:
- `hugo_builder.py` - Builds Hugo sites
- `deployer.py` - Deploys to S3/CloudFront (wraps existing scripts)
- `content_editor.py` - Creates/edits markdown content
- Additional workers as needed

---

## 🔧 Claude Code Workflow

### When Working on This Project

**CC's Role:**
1. **Design & Planning** - Think through requirements, decompose tasks
2. **Write Task Files** - Delegate execution to workers
3. **Verify Results** - Read worker outputs, validate correctness
4. **Explain Outcomes** - Communicate results to user

**CC Does Directly:**
- Content writing and design decisions
- Task decomposition and planning
- Verification and quality checks
- Communication with user

**CC Delegates to Workers:**
- Hugo builds (>10 seconds, deterministic)
- S3 deployments (requires AWS credentials)
- CloudFront invalidations (long-running)

### Decision Criteria
```
Task requires reasoning/creativity? → CC does it directly
Task is deterministic execution? → Delegate to worker
Task takes >10 seconds? → Delegate to worker
Task needs persistent credentials? → Delegate to worker
```

---

## 📝 Task File Format

When CC needs to delegate work, write a task file to `tasks/pending/`:

**Naming:** `{timestamp}-{task-type}-{description}.md`

**Example:**
```yaml
---
task_id: 2026-01-19-1430-hugo-build-staging
task_type: hugo-build
created_by: claude-code
params:
  site_path: /Users/mark/PycharmProjects/klm-migrate/klm-hugo-site
  environment: staging
  base_url: https://www.klmcrm.com
  minify: true
expected_outputs:
  - build_success
  - file_count
  - errors
---

## Task Description
Build Hugo site for staging environment.
```

Then read result from `results/YYYY-MM-DD/{task-id}.result.md`

---

## 🚀 Common Tasks

### Reviewing the Plan
```bash
# Read the complete implementation plan
cat PLAN.md

# Review specific phase
# Phase 1: Foundation (Week 1-2)
# Phase 2: Worker Implementation (Week 2-3)
# Phase 3: CC Integration (Week 3-4)
# Phase 4: Process Integration (Week 4)
```

### Implementing Phase 1
```bash
# Create directory structure
mkdir -p tasks/{pending,in-progress,completed,failed,templates}
mkdir -p results
mkdir -p workers
mkdir -p archive
mkdir -p .claude

# See PLAN.md Phase 1.1 for detailed structure
```

### Testing Task System
```bash
# Manual test workflow:
# 1. CC writes task file to tasks/pending/
# 2. Run worker: python3 workers/hugo_builder.py
# 3. CC reads result from results/
# 4. CC verifies outcome
```

---

## 🔗 Related Projects

This orchestration system will initially serve:

1. **klm-migrate** (`/Users/mark/PycharmProjects/klm-migrate`)
   - Hugo insurance website
   - Existing deployment scripts: `publish_to_staging.py`, `publish_to_production.py`
   - Deployment workers will wrap these scripts

2. **klm-plan** (`/Users/mark/PycharmProjects/klm-plan`)
   - Hugo business documentation site
   - Similar workflow patterns

---

## ⚙️ Integration with Existing Workflows

### Git Workflow (No Changes)
- Keep existing `main` and `claude/*` branch strategy
- Auto-deploy to dev continues via GitHub Actions
- Task system runs in parallel (not replacement)

### Deployment Scripts (Wrapped)
- `publish_to_staging.py` - Wrapped by deployer worker
- `publish_to_production.py` - Wrapped by deployer worker
- Preserves existing safety checks and logic

### Approval Requirements
- **Dev builds:** No approval needed
- **Staging deploys:** Conditional (CC asks user)
- **Production deploys:** Explicit "DEPLOY TO PRODUCTION" confirmation required

---

## 🎯 Success Metrics

### Quantitative Goals
- Permission prompts per workflow: 4-6 → 0-1
- Time to staging deployment: 10 min → 2 min
- Device switches required: 1-2 → 0
- Manual commands required: 2-3 → 0

### Qualitative Goals
- Conversational experience (not command-driven)
- Mobile-first (works seamlessly from iPhone)
- Error handling is graceful
- CC maintains context across tasks
- User confidence in outcomes

---

## 📞 For Claude Code Sessions

**When starting work on this project:**

1. Read **PLAN.md** first - complete implementation roadmap
2. Check **Implementation Status** section above
3. Review relevant phase in PLAN.md
4. Follow established patterns and schemas
5. Update this file when major milestones complete

**When user asks to implement:**
- Start with Phase 1.1 (directory structure)
- Follow PLAN.md sequentially
- Test each phase before moving to next
- Update Implementation Status in this file

**When delegating work:**
- Write task files per PLAN.md section 1.2
- Workers will be created in Phase 2
- Until then, manual execution is expected

---

## 🔍 Critical Files to Reference

### Existing Files (Study These)
1. `/Users/mark/PycharmProjects/klm-migrate/publish_to_staging.py` - Deployment pattern
2. `/Users/mark/PycharmProjects/klm-migrate/publish_to_production.py` - Safety checks
3. `/Users/mark/PycharmProjects/klm-migrate/klm-hugo-site/.github/workflows/deploy-dev.yml` - Auto-deploy workflow

### Files to Create (Per PLAN.md)
1. `tasks/templates/hugo-build.md` - Task template
2. `tasks/templates/hugo-deploy-staging.md` - Staging deploy template
3. `workers/hugo_builder.py` - Hugo build worker
4. `workers/deployer.py` - Deployment worker
5. `.claude/task-system-guide.md` - CC's task system guide

---

## ⚠️ Important Reminders

- **Don't overengineer** - Start simple, evolve as needed
- **File-based first** - Only move to database when >100 tasks/day
- **Preserve existing workflows** - Wrap, don't replace
- **Safety first** - Production requires explicit confirmation
- **Mobile-first** - iPhone experience is primary design goal

---

**Project Status:** Planning Complete, Ready for Implementation
**Next Step:** Implement Phase 1.1 (Directory Structure Setup)
**Time Estimate:** 2-4 weeks to Phase 1 completion, 1-2 months to full workflow

---

*This orchestration system will transform CC from a direct executor into an intelligent control plane, eliminating permission fatigue while maintaining safety and oversight.*
