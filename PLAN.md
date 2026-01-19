# CC-Centric Orchestration System Implementation Plan

## Executive Summary

Transform Claude Code from a direct executor into an intelligent **AI Control Plane** that orchestrates deterministic workers through file-based contracts. This design keeps CC focused on high-value reasoning (planning, verification, communication) while delegating repetitive execution (builds, deployments) to headless workers.

**Primary Use Case:** Hugo website development workflow (klm-migrate, klm-plan projects)

**Core Principle:** *"AI should think until confident, act once deterministically, record results, and stop."*

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│   YOU (Desktop / iPhone)            │
│   Natural language requests         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   CLAUDE CODE (Control Plane)       │
│   • Thinks & Plans                  │
│   • Writes task files               │
│   • Verifies results                │
│   • Explains outcomes               │
└────────────┬────────────────────────┘
             │ writes/reads
             ▼
┌─────────────────────────────────────┐
│   TASK EXCHANGE LAYER               │
│   File-based contracts              │
│   • /tasks/pending/                 │
│   • /tasks/in-progress/             │
│   • /tasks/completed/               │
│   • /results/YYYY-MM-DD/            │
└────────────┬────────────────────────┘
             │ consumed by
             ▼
┌─────────────────────────────────────┐
│   EXECUTION WORKERS (Headless)      │
│   • Hugo Builder                    │
│   • Deployer (S3 + CloudFront)      │
│   • Content Editor                  │
│   • Form Manager (JotForm)          │
│   • Validator (links, SEO)          │
└─────────────────────────────────────┘
```

---

## Phase 1: Foundation (Week 1-2)

### 1.1 Directory Structure Setup

Create the orchestration system structure:

```
/Users/mark/PycharmProjects/workflow/
├── tasks/
│   ├── pending/              # CC writes tasks here
│   ├── in-progress/          # Workers move tasks here while executing
│   ├── completed/            # Completed tasks (audit trail)
│   ├── failed/               # Failed tasks for review
│   └── templates/            # Reusable task templates
│       ├── hugo-build.md
│       ├── hugo-deploy-staging.md
│       └── hugo-deploy-production.md
│
├── results/
│   ├── 2026-01-19/          # Results organized by date
│   │   ├── task-{id}.result.md
│   │   └── task-{id}.logs/
│   └── latest/              # Symlinks to most recent
│
├── workers/
│   ├── hugo_builder.py      # Hugo build worker
│   ├── deployer.py          # Deployment worker (wraps publish_to_*.py)
│   ├── content_editor.py    # Content creation/editing worker
│   └── README.md            # Worker documentation
│
├── archive/
│   └── 2026-01/             # Monthly archives
│       ├── tasks/
│       └── results/
│
└── .claude/
    └── task-system-guide.md # CC's instructions for using task system
```

**Files to create:**
- `.gitignore` - Add `results/`, `tasks/in-progress/`, `workers/*.log`
- Keep tasks/templates/ and completed tasks in git for audit trail

### 1.2 Task File Format (Standard Schema)

**Naming Convention:** `{timestamp}-{task-type}-{brief-description}.md`
**Example:** `2026-01-19-1430-hugo-build-staging.md`

**Template Structure:**
```yaml
---
# Metadata
task_id: 2026-01-19-1430-hugo-build-staging
task_type: hugo-build
created_at: 2026-01-19T14:30:00Z
created_by: claude-code
status: pending
worker_type: hugo-builder
priority: normal
timeout_minutes: 10

# Context (audit trail)
context:
  user_request: "Deploy updated homepage to staging"
  branch: claude/update-homepage-xyz
  files_changed:
    - content/_index.md

# Task Parameters
params:
  site_path: /Users/mark/PycharmProjects/klm-migrate/klm-hugo-site
  environment: staging
  base_url: https://www.klmcrm.com
  minify: true
  clean: true

# Expected Outputs (for CC verification)
expected_outputs:
  - build_success: boolean
  - file_count: integer (>100)
  - errors: array (empty)
  - duration_seconds: float (<60)

# Approval (if needed)
requires_approval: false
---

## Task Description
Build Hugo site for staging environment after homepage updates.

## Success Criteria
- Build completes without errors
- File count > 100
- Duration < 60 seconds

## Rollback Plan
If build fails, restore previous public/ directory and report errors.
```

### 1.3 Result File Format (Standard Schema)

**Naming Convention:** `{task-id}.result.md`
**Example:** `2026-01-19-1430-hugo-build-staging.result.md`

**Template Structure:**
```yaml
---
# Result Metadata
task_id: 2026-01-19-1430-hugo-build-staging
task_type: hugo-build
status: success  # or failed
completed_at: 2026-01-19T14:30:45Z
duration_seconds: 12.3
worker_id: hugo-builder-laptop

# Outputs (match expected_outputs in task)
outputs:
  build_success: true
  file_count: 247
  errors: []
  warnings: []
  hugo_version: "0.122.0+extended"
  pages_generated: 24

# Full logs
logs: |
  Building sites …
  hugo v0.122.0+extended
  Total in 12345 ms
---

## Build Summary
Build completed successfully for staging environment.

## Statistics
- Pages: 24
- Assets: 223
- Total files: 247
- Duration: 12.3 seconds

## Next Steps
Ready for deployment to S3.
```

### 1.4 Task Templates for Hugo Workflow

Create templates in `tasks/templates/`:

#### Template 1: `hugo-build.md`
```yaml
---
task_type: hugo-build
worker_type: hugo-builder
params:
  site_path: /Users/mark/PycharmProjects/klm-migrate/klm-hugo-site
  environment: dev | staging | production
  base_url: <environment-specific-url>
  minify: true
  clean: true
expected_outputs:
  - build_success
  - file_count
  - errors
  - warnings
---
Build Hugo site for specified environment.
```

#### Template 2: `hugo-deploy-staging.md`
```yaml
---
task_type: hugo-deploy-staging
worker_type: deployer
requires_approval: true
params:
  public_dir: /Users/mark/PycharmProjects/klm-migrate/klm-hugo-site/public
  bucket: s3://klmcrm.com
  cloudfront_id: E3HA8770RGET6T
  verify_url: https://www.klmcrm.com
expected_outputs:
  - uploaded_files
  - invalidation_id
  - http_status
---
Deploy built site to staging S3 bucket with CloudFront invalidation.
```

#### Template 3: `hugo-deploy-production.md`
```yaml
---
task_type: hugo-deploy-production
worker_type: deployer
requires_approval: true
approval_confirmation: "DEPLOY TO PRODUCTION"
params:
  public_dir: /Users/mark/PycharmProjects/klm-migrate/klm-hugo-site/public
  bucket: s3://klminsurance.com
  verify_url: https://www.klminsurance.com
expected_outputs:
  - uploaded_files
  - deployment_id
  - http_status
---
Deploy to PRODUCTION (customer-facing site). Requires explicit approval.
```

---

## Phase 2: Worker Implementation (Week 2-3)

### 2.1 Hugo Builder Worker

**File:** `/Users/mark/PycharmProjects/workflow/workers/hugo_builder.py`

**Responsibilities:**
- Watch `tasks/pending/` for `hugo-build` tasks
- Execute `hugo build` with environment-specific parameters
- Validate build output
- Write structured results
- Move task files between states

**Implementation Pattern:**
```python
#!/usr/bin/env python3
"""Hugo Builder Worker - Executes Hugo builds"""

import subprocess
import yaml
import time
from pathlib import Path
from datetime import datetime

TASKS_DIR = Path("/Users/mark/PycharmProjects/workflow/tasks")
RESULTS_DIR = Path("/Users/mark/PycharmProjects/workflow/results")

def watch_for_tasks():
    """Poll for new hugo-build tasks"""
    while True:
        for task_file in (TASKS_DIR / "pending").glob("*hugo-build*.md"):
            process_task(task_file)
        time.sleep(2)

def process_task(task_file):
    """Execute hugo build task"""
    # Move to in-progress
    in_progress = TASKS_DIR / "in-progress" / task_file.name
    task_file.rename(in_progress)

    # Parse task
    task = parse_yaml_frontmatter(in_progress)

    # Execute hugo build
    result = execute_hugo_build(task['params'])

    # Write result file
    write_result(task['task_id'], result)

    # Move to completed
    completed = TASKS_DIR / "completed" / task_file.name
    in_progress.rename(completed)

def execute_hugo_build(params):
    """Run hugo build command"""
    cmd = [
        "hugo",
        "--baseURL", params['base_url'],
        "--environment", params['environment']
    ]
    if params.get('minify'):
        cmd.append("--minify")
    if params.get('clean'):
        cmd.append("--cleanDestinationDir")

    result = subprocess.run(
        cmd,
        cwd=params['site_path'],
        capture_output=True,
        text=True
    )

    return {
        "status": "success" if result.returncode == 0 else "failed",
        "build_log": result.stdout,
        "errors": parse_errors(result.stderr),
        "file_count": count_files(f"{params['site_path']}/public")
    }
```

**Start worker:** `python3 workers/hugo_builder.py` (runs continuously)

### 2.2 Deployment Worker

**File:** `/Users/mark/PycharmProjects/workflow/workers/deployer.py`

**Strategy:** Wrap existing `publish_to_staging.py` and `publish_to_production.py` scripts

**Implementation:**
```python
#!/usr/bin/env python3
"""Deployment Worker - Wraps existing deployment scripts"""

import subprocess
from pathlib import Path

def execute_staging_deploy(task):
    """Execute staging deployment via existing script"""
    result = subprocess.run(
        ["python3", "publish_to_staging.py"],
        cwd="/Users/mark/PycharmProjects/klm-migrate",
        capture_output=True,
        text=True
    )

    return {
        "status": "success" if result.returncode == 0 else "failed",
        "deployment_log": result.stdout,
        "site_url": "https://www.klmcrm.com",
        "http_status": verify_site_accessible("https://www.klmcrm.com")
    }
```

**Benefits:**
- Reuses proven deployment logic
- No need to rewrite S3/CloudFront code
- Maintains existing safety checks
- Easy migration path

### 2.3 Content Editor Worker

**File:** `/Users/mark/PycharmProjects/workflow/workers/content_editor.py`

**Responsibilities:**
- Create new markdown content files
- Edit existing content with frontmatter
- Validate YAML frontmatter
- Verify markdown syntax

**Implementation:**
```python
import frontmatter

def create_content(params):
    """Create new Hugo content file"""
    content = frontmatter.Post(
        params['body'],
        **params['frontmatter']
    )

    file_path = Path(params['site_path']) / params['content_path']
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w') as f:
        f.write(frontmatter.dumps(content))

    return {
        "status": "success",
        "file_path": str(file_path),
        "word_count": len(params['body'].split())
    }
```

---

## Phase 3: CC Integration (Week 3-4)

### 3.1 CC Decision Logic: Delegate vs Direct

**CC Does Directly:**
- Content writing (intelligence required)
- Design decisions (choosing layouts, structure)
- Planning & task decomposition
- Verification & quality checks
- Communication with user

**CC Delegates to Workers:**
- Hugo builds (deterministic, >10 seconds)
- S3 deployments (requires AWS credentials)
- CloudFront invalidations (long-running)
- Repetitive git operations

**Decision Criteria:**
```
Task requires reasoning/creativity? → CC does it
Task is deterministic execution? → Delegate to worker
Task takes >10 seconds? → Delegate to worker
Task needs persistent credentials? → Delegate to worker
```

### 3.2 CC Task Workflow: Landing Page Creation

**User Request (iPhone):**
> "Create a new landing page for summer auto insurance promo"

**CC Process:**

1. **Design & Plan (CC Direct)**
   - Decide page slug: `/summer-auto-promo-2026/`
   - Choose layout: `landing`
   - Define form tracking: `summer-auto-2026`

2. **Write Content (CC Direct)**
   - Craft hero headline
   - Write promo copy
   - Show draft to user for approval

3. **Create File (CC Direct)**
   - Write markdown with frontmatter
   - Use Write tool directly

4. **Build Site (DELEGATED)**
   - CC writes task file: `tasks/pending/2026-01-19-1430-hugo-build-dev.md`
   - Worker picks up, executes, writes result
   - CC reads result: `results/2026-01-19/2026-01-19-1430-hugo-build-dev.result.md`
   - CC verifies: build_success=true, errors=[]

5. **Deploy to Dev (EXISTING AUTO-DEPLOY)**
   - CC commits to `claude/*` branch
   - GitHub Actions auto-deploys
   - No task file needed (existing workflow)

6. **User Preview (CHECKPOINT)**
   - CC: "Preview at http://dev-klmhugoweb..."
   - User reviews on iPhone
   - User: "Deploy to staging"

7. **Deploy to Staging (DELEGATED)**
   - CC asks: "Ready to deploy to staging?"
   - User confirms
   - CC writes task file: `tasks/pending/2026-01-19-1500-hugo-deploy-staging.md`
   - Worker executes `publish_to_staging.py`
   - CC verifies deployment success

**Total User Interaction:** 3 messages, 1 approval, zero permission prompts

### 3.3 CC Verification Logic

**After Build:**
```python
# CC reads result file and verifies
result = read_task_result(task_id)

if result['status'] == 'success':
    if result['outputs']['errors'] == []:
        if result['outputs']['file_count'] > 100:
            # PASS: Build successful, proceed to deploy
            return "proceed_to_deploy"
    else:
        # WARNING: Build succeeded with errors
        return "warn_user_about_errors"
else:
    # FAIL: Analyze error and decide action
    return analyze_build_failure(result)
```

**After Deployment:**
```python
# CC verifies deployment
result = read_task_result(task_id)

if result['status'] == 'success':
    if result['outputs']['http_status'] == 200:
        # PASS: Site accessible
        return f"Deployed successfully to {result['outputs']['site_url']}"
    else:
        # FAIL: Deployment succeeded but site not accessible
        return "deployment_verification_failed"
```

### 3.4 Error Handling Strategy

**Auto-Retry (CC fixes and retries):**
- Template not found → CC creates template, retries
- Missing frontmatter → CC adds frontmatter, retries
- Broken internal link → CC fixes link, retries

**Escalate to User:**
- AWS credential errors → User must fix on laptop
- CloudFront configuration errors → Requires manual intervention
- Git merge conflicts → User decides resolution
- Unknown errors → CC explains and asks for guidance

### 3.5 Update CC's Knowledge Base

**File:** `/Users/mark/PycharmProjects/workflow/.claude/task-system-guide.md`

Create comprehensive guide for CC:

```markdown
# Task Orchestration System Guide for Claude Code

## Overview
You (Claude Code) are the control plane for an orchestration system.
You write task files, workers execute them, you verify results.

## When to Delegate vs Do Directly

### You Do Directly:
- Write content (markdown, copy)
- Design decisions (layouts, structure)
- Plan and decompose user requests
- Verify worker results
- Communicate with user

### Delegate to Workers:
- Hugo builds (>10 seconds)
- S3 deployments (requires AWS credentials)
- CloudFront invalidations (long-running)

## How to Write a Task File

Use the Write tool to create a task file in tasks/pending/:

```yaml
---
task_id: 2026-01-19-1430-hugo-build-dev
task_type: hugo-build
params:
  environment: dev
  base_url: http://dev-klmhugoweb.s3-website-us-east-1.amazonaws.com/
  minify: true
---
```

## How to Read Results

Use the Read tool to check results/:

```bash
results/2026-01-19/2026-01-19-1430-hugo-build-dev.result.md
```

Check status: success or failed
Verify outputs match expectations

## Workflow Examples

[Include 3-4 complete examples of common workflows]
```

**Also update:** `/Users/mark/PycharmProjects/klm-migrate/klm-hugo-site/claude.md`

Add new section:
```markdown
## Task Orchestration System

CC can delegate work to headless workers via task files.

### Task Types Available:
- hugo-build: Build Hugo site for environment
- hugo-deploy-staging: Deploy to staging (requires approval)
- hugo-deploy-production: Deploy to production (requires explicit confirmation)

### Workflow:
1. CC writes task file to tasks/pending/
2. Worker executes task
3. Worker writes result to results/
4. CC reads result and verifies
5. CC explains outcome to user

### Approval Requirements:
- Dev builds: No approval needed
- Staging deploys: Conditional (CC asks user)
- Production deploys: Explicit "DEPLOY TO PRODUCTION" confirmation required
```

---

## Phase 4: Integration with Existing Processes (Week 4)

### 4.1 Git Workflow (No Changes)

**Keep existing:**
- `main` branch for desktop work
- `claude/*` branches for iPhone work
- Auto-deploy to dev on push

**Add to git:**
- `tasks/templates/` (task templates)
- `tasks/completed/` (audit trail)
- `.workflow/.gitignore` (exclude results/, in-progress/)

### 4.2 Dev Auto-Deploy (No Changes)

**Keep existing:** `.github/workflows/deploy-dev.yml`

**How it fits:**
- CC still commits to `claude/*` branches
- GitHub Actions still auto-deploys to dev
- Task system is parallel option (not replacement)
- CC can use either: git push (auto-deploy) OR task file (manual trigger)

### 4.3 Staging Deploy (Migrate to Task-Based)

**Current:** Manual execution of `publish_to_staging.py`

**Phase 1 (Week 4):** Wrap script in worker
- Worker executes existing script
- CC writes task file instead of reminding user to run script
- Preserves all existing logic

**Phase 2 (Month 2):** Native task execution
- Reimplement as standalone worker
- Or GitHub Actions with manual trigger

### 4.4 Production Deploy (Enhanced Safety)

**Current:** Manual execution with confirmation prompt

**Enhanced:**
```
User: "Deploy to production"

CC: "⚠️ PRODUCTION DEPLOYMENT WARNING

     Changes being deployed:
     - Updated homepage hero
     - New summer promo landing page

     Staging preview: https://www.klmcrm.com

     Type 'DEPLOY TO PRODUCTION' to confirm:"

User: "DEPLOY TO PRODUCTION"

CC: [Writes production deploy task with approval_confirmed: true]
    [Worker executes publish_to_production.py]
    [CC verifies and reports success]
```

---

## Verification & Testing

### End-to-End Test: Landing Page Creation

**Test Scenario:** Create summer auto insurance landing page from iPhone

**Steps:**
1. User: "Create summer auto landing page"
2. CC: Writes content, shows draft
3. User: "Looks good"
4. CC: Creates file, writes build task
5. Worker: Executes build, writes result
6. CC: Reads result, verifies success
7. CC: Commits to `claude/*` branch
8. GitHub Actions: Auto-deploys to dev
9. CC: "Preview at http://dev-klmhugoweb..."
10. User: "Deploy to staging"
11. CC: Writes staging deploy task
12. Worker: Executes `publish_to_staging.py`
13. CC: Verifies deployment, reports success

**Success Criteria:**
- Zero permission prompts (except content approval)
- No device switching required
- Build completes in <60 seconds
- Staging deploys successfully
- CC verifies all outputs correctly
- User experience feels conversational

### Unit Tests

**Test 1: Task File Creation**
- CC writes valid YAML task file
- Task file passes schema validation
- All required fields present

**Test 2: Worker Execution**
- Worker picks up task file
- Executes build successfully
- Writes valid result file
- Moves task to completed/

**Test 3: CC Result Verification**
- CC reads result file correctly
- CC interprets success/failure correctly
- CC makes correct next-step decision

**Test 4: Error Handling**
- Build fails with template error
- CC analyzes error correctly
- CC fixes template and retries
- Retry succeeds

---

## Critical Files

### Files to Study (Existing)

1. **klm-migrate/publish_to_staging.py**
   - Existing staging deployment script
   - Deployment worker will wrap this
   - Contains proven S3 sync + CloudFront logic

2. **klm-migrate/publish_to_production.py**
   - Existing production deployment script
   - Contains safety confirmation logic
   - Deployment worker will wrap this

3. **klm-migrate/klm-hugo-site/.github/workflows/deploy-dev.yml**
   - Auto-deploy workflow for dev
   - Must coexist with task system
   - Study integration points

4. **klm-migrate/klm-hugo-site/hugo.toml**
   - Hugo configuration
   - Understand baseURL patterns
   - Environment-specific settings

5. **klm-migrate/klm-hugo-site/claude.md**
   - CC's project instructions
   - Must be updated with task system info

### Files to Create (New)

1. **/Users/mark/PycharmProjects/workflow/tasks/templates/hugo-build.md**
   - Task template for Hugo builds
   - CC references this when writing tasks

2. **/Users/mark/PycharmProjects/workflow/tasks/templates/hugo-deploy-staging.md**
   - Task template for staging deploys
   - Includes approval requirements

3. **/Users/mark/PycharmProjects/workflow/workers/hugo_builder.py**
   - Hugo build worker implementation
   - Watches for build tasks, executes, writes results

4. **/Users/mark/PycharmProjects/workflow/workers/deployer.py**
   - Deployment worker implementation
   - Wraps publish_to_*.py scripts

5. **/Users/mark/PycharmProjects/workflow/.claude/task-system-guide.md**
   - CC's guide to using task system
   - How to write tasks, read results, verify

6. **/Users/mark/PycharmProjects/workflow/.gitignore**
   - Exclude results/ (ephemeral)
   - Exclude tasks/in-progress/ (temporary)
   - Include tasks/templates/ and completed/ (audit trail)

---

## Risks & Mitigation

### Risk 1: Worker Reliability
**Risk:** Worker crashes, task stuck in in-progress
**Mitigation:**
- Implement timeout on tasks
- Worker writes heartbeat file
- CC can detect stale tasks and restart

### Risk 2: Result File Corruption
**Risk:** Worker writes malformed YAML
**Mitigation:**
- Schema validation in worker
- CC validates result file before parsing
- Fallback to log file if YAML fails

### Risk 3: Permission Accumulation
**Risk:** Workers need AWS credentials, git access, etc.
**Mitigation:**
- Use existing .claude/settings.json permissions
- Workers inherit user's credentials
- No new permission model needed

### Risk 4: Mobile Connectivity
**Risk:** iPhone loses connection mid-task
**Mitigation:**
- Tasks execute asynchronously
- CC can check status when reconnected
- Results persist in files

---

## Success Metrics

### Quantitative
- Permission prompts per workflow: 4-6 → 0-1
- Time to staging deployment: 10 min → 2 min
- Device switches required: 1-2 → 0
- Manual commands required: 2-3 → 0

### Qualitative
- Conversational experience (not command-driven)
- Mobile-first (works seamlessly from iPhone)
- Error handling is graceful
- CC maintains context across tasks
- User confidence in outcomes

---

## Open Questions

1. **Worker Hosting:** Run workers on laptop or GitHub Actions?
   - **Recommendation:** Start on laptop, migrate to GitHub Actions in Phase 2

2. **Database Migration:** When to move from files to SQLite?
   - **Recommendation:** Only when >100 tasks/day or >3 concurrent workers

3. **Task Chaining:** Should CC chain tasks automatically or ask user?
   - **Recommendation:** Auto-chain dev builds+deploys, ask for staging/prod

4. **Approval Granularity:** What level of approval for staging?
   - **Recommendation:** Conditional - CC asks if changes are significant

---

## Next Steps (Immediate)

1. Create directory structure in `/Users/mark/PycharmProjects/workflow/`
2. Write task/result templates
3. Implement hugo_builder.py worker (basic version)
4. Test manual workflow: CC writes task → run worker → CC reads result
5. Create task-system-guide.md for CC
6. Update klm-migrate/klm-hugo-site/claude.md with task system info

**First Milestone:** CC can delegate a Hugo build, worker executes it, CC verifies the result.

**Time Estimate:** 2-4 weeks to Phase 1 completion, 1-2 months to full mobile-first workflow.
