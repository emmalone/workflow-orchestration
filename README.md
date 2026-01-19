# Workflow Orchestration System

**Transform Claude Code into an AI Control Plane**

A CC-centric orchestration system that keeps Claude Code focused on high-value reasoning (planning, verification, communication) while delegating repetitive execution to headless workers.

---

## What is This?

This project implements a file-based task orchestration architecture where:

- **Claude Code** acts as the intelligent control plane
- **Workers** execute deterministic tasks (builds, deployments)
- **Task files** serve as the contract between CC and workers
- **Result files** provide structured feedback for verification

**Core Principle:** *"AI should think until confident, act once deterministically, record results, and stop."*

---

## Why?

### Problems Solved

❌ **Before:** 4-6 permission prompts per workflow
✅ **After:** 0-1 approval (content only)

❌ **Before:** 10 minutes to staging, switching devices
✅ **After:** 2 minutes, iPhone only

❌ **Before:** Manual deployment commands
✅ **After:** Natural language conversation

### Benefits

- 🎯 **Mobile-First** - Seamless iPhone workflow
- 🤖 **Intelligent Delegation** - CC decides what to delegate
- 📝 **Auditable** - All tasks and results tracked in files
- 🔒 **Safe** - Approval gates for critical operations
- 🔄 **Iterative** - Start simple, evolve as needed

---

## Architecture

```
┌─────────────────────┐
│  You (iPhone/Mac)   │
│  Natural language   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  CLAUDE CODE        │
│  Control Plane      │
│  • Plans            │
│  • Writes tasks     │
│  • Verifies results │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  TASK FILES         │
│  /tasks/pending/    │
│  File-based queue   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  WORKERS            │
│  • Hugo Builder     │
│  • Deployer         │
│  • Content Editor   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  RESULT FILES       │
│  /results/date/     │
│  Structured output  │
└─────────────────────┘
```

---

## Quick Start

### 1. Review Planning Documents

```bash
# Read the complete implementation plan
cat PLAN.md

# Review architecture philosophy
cat "HL AI Orchastration.md"

# Check project context
cat claude.md
```

### 2. Implementation Phases

- **Phase 1 (Week 1-2):** Directory structure, task/result schemas, templates
- **Phase 2 (Week 2-3):** Worker implementations (Hugo builder, deployer)
- **Phase 3 (Week 3-4):** CC integration, verification logic, error handling
- **Phase 4 (Week 4):** Integration with existing Hugo workflows

### 3. First Milestone

CC can delegate a Hugo build task → Worker executes it → CC verifies the result

---

## Project Structure

```
workflow/
├── README.md                  # This file
├── PLAN.md                    # Complete implementation plan ⭐
├── claude.md                  # CC's project instructions
├── project.md                 # Architecture mandate
├── HL AI Orchastration.md     # Design philosophy
├── Claude Code Instructions.md # CC role definition
├── chat_conv.md               # Historical context
│
├── tasks/                     # (To be created)
│   ├── pending/               # CC writes tasks here
│   ├── in-progress/           # Workers process
│   ├── completed/             # Audit trail
│   └── templates/             # Task templates
│
├── results/                   # (To be created)
│   └── YYYY-MM-DD/            # Results by date
│
└── workers/                   # (To be created)
    ├── hugo_builder.py        # Builds Hugo sites
    ├── deployer.py            # Deploys to S3/CloudFront
    └── content_editor.py      # Creates/edits content
```

---

## Primary Use Case: Hugo Website Development

This orchestration system initially serves:

1. **klm-migrate** - Insurance website (www.klminsurance.com)
2. **klm-plan** - Business documentation site

### Workflow Example

**User (on iPhone):** "Create a new landing page for summer auto insurance promo"

**CC Process:**
1. Designs page structure (direct)
2. Writes marketing content (direct, shows draft)
3. Creates markdown file (direct)
4. Writes build task → Worker builds → CC verifies
5. Commits to git → Auto-deploy to dev
6. User previews, approves
7. Writes staging deploy task → Worker deploys → CC verifies
8. Reports success with URL

**User Experience:** 3 messages, 1 content approval, zero permission prompts, zero device switching

---

## Key Documents

### Start Here
- **PLAN.md** - Complete implementation roadmap, schemas, and patterns

### Architecture & Philosophy
- **HL AI Orchastration.md** - Why CC as control plane, task exchange design
- **project.md** - System principles, planning mandate, success criteria
- **Claude Code Instructions.md** - CC's role and responsibilities

### For Claude Code
- **claude.md** - Project context, workflow instructions, task formats

### Historical Context
- **chat_conv.md** - Prior AI conversations and decision rationale

---

## Task File Format (Example)

CC delegates work by writing task files:

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
Build Hugo site for staging environment after homepage updates.

## Success Criteria
- Build completes without errors
- File count > 100
- Duration < 60 seconds
```

Worker writes result to `results/2026-01-19/{task-id}.result.md`

---

## Success Metrics

### Quantitative Goals
| Metric | Before | Target |
|--------|--------|--------|
| Permission prompts | 4-6 | 0-1 |
| Time to staging | 10 min | 2 min |
| Device switches | 1-2 | 0 |
| Manual commands | 2-3 | 0 |

### Qualitative Goals
- ✅ Conversational experience (not command-driven)
- ✅ Mobile-first (works seamlessly from iPhone)
- ✅ Graceful error handling
- ✅ Context maintained across tasks
- ✅ User confidence in outcomes

---

## Integration with Existing Workflows

### Preserves
- ✅ Git branching strategy (`main`, `claude/*`)
- ✅ GitHub Actions auto-deploy to dev
- ✅ Existing deployment scripts (`publish_to_*.py`)
- ✅ Safety checks and approval gates

### Enhances
- 🎯 Eliminates permission prompts
- 🎯 Enables iPhone-only workflow
- 🎯 Provides audit trail
- 🎯 Structured verification

---

## Current Status

**Planning:** ✅ Complete
**Implementation:** ⏳ Pending

**Next Step:** Implement Phase 1.1 (Directory Structure Setup)

**Time Estimate:** 2-4 weeks to Phase 1, 1-2 months to full mobile-first workflow

---

## For Developers

### Prerequisites
- Python 3.x
- Hugo (extended version)
- AWS CLI (configured)
- Git

### Testing
```bash
# Phase 1: Manual workflow
# 1. CC writes task file to tasks/pending/
# 2. Run worker: python3 workers/hugo_builder.py
# 3. CC reads result from results/
# 4. CC verifies outcome
```

See **PLAN.md** for complete implementation details.

---

## Philosophy

This system applies proven software architecture patterns to AI:

- **Control plane** - CC thinks, plans, verifies
- **Workers** - Execute deterministically, report results
- **File contracts** - Human-readable, auditable, versionable
- **Stateless execution** - Workers exit after completion

**Not just automation - intelligent orchestration.**

---

## Contributing

This is a personal project for Mark's Hugo website development workflow.

For questions or suggestions:
- Developer: Mark (mark@emm-associates.com)
- Project: Workflow Orchestration System
- Location: `/Users/mark/PycharmProjects/workflow`

---

**Last Updated:** January 19, 2026
**Status:** Planning Complete, Ready for Implementation

*Transform Claude Code from intern to chief of staff.*
