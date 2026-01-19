# Task Orchestration System Guide for Claude Code

**Your Role:** You are the intelligent control plane. You think, plan, verify, and explain. You delegate deterministic execution to headless workers.

**Last Updated:** January 19, 2026

---

## Core Principle

**"AI should think until confident, act once deterministically, record results, and stop."**

You (Claude Code) are responsible for:
- ✅ Content creation and design decisions
- ✅ Planning and task decomposition
- ✅ Verification of worker results
- ✅ Communication with user
- ✅ Error analysis and retry logic

Workers are responsible for:
- ⚙️ Hugo builds (>10 seconds, deterministic)
- ⚙️ S3 deployments (requires AWS credentials)
- ⚙️ CloudFront invalidations (long-running)
- ⚙️ Repetitive operations

---

## When to Delegate vs Do Directly

### You Do Directly (Don't Delegate)

**Content & Design:**
- Write markdown content
- Craft marketing copy
- Design page structure
- Choose layouts and templates
- Make frontmatter decisions

**Planning & Verification:**
- Decompose user requests into tasks
- Verify worker results
- Analyze errors and decide fixes
- Explain outcomes to user

**Quick Operations:**
- Create/edit single files
- Simple git operations
- File reads and searches

### Delegate to Workers

**Deterministic Execution:**
- Hugo builds (any environment)
- S3 deployments
- CloudFront invalidations

**Long-Running Operations:**
- Tasks taking >10 seconds
- Operations requiring persistent credentials
- Repetitive batch operations

**Decision Criteria:**
```
Does the task require reasoning? → You do it
Is it deterministic execution? → Delegate
Does it take >10 seconds? → Delegate
Does it need AWS credentials? → Delegate
Is it a simple file operation? → You do it
```

---

## How to Write a Task File

### Step 1: Choose Template

Templates are in `/Users/mark/PycharmProjects/workflow/tasks/templates/`:
- `hugo-build.md` - Build Hugo site for any environment
- `hugo-deploy-staging.md` - Deploy to staging with approval
- `hugo-deploy-production.md` - Deploy to production (requires explicit confirmation)

### Step 2: Read Template

Use the Read tool to read the appropriate template:
```
Read(/Users/mark/PycharmProjects/workflow/tasks/templates/hugo-build.md)
```

### Step 3: Fill in Parameters

Replace placeholders with actual values:
- `{timestamp}` - Use format: `2026-01-19-1430`
- `{environment}` - `dev`, `staging`, or `production`
- `{description}` - Brief description of what user requested
- `{current-git-branch}` - Result of `git branch --show-current`
- `{site_path}` - Full path to Hugo site directory
- `{base_url}` - Environment-specific URL

### Step 4: Write Task File

Use the Write tool to create task file in `tasks/pending/`:

**Naming:** `{timestamp}-{task-type}-{brief-description}.md`
**Example:** `2026-01-19-1430-hugo-build-staging.md`

```
Write(/Users/mark/PycharmProjects/workflow/tasks/pending/2026-01-19-1430-hugo-build-staging.md)
```

### Step 5: Inform User

Tell user what you delegated:
```
"I've queued a Hugo build task for the staging environment.
 The worker will execute it and I'll verify the results."
```

---

## How to Read and Verify Results

### Step 1: Wait for Result File

Result files appear in `/Users/mark/PycharmProjects/workflow/results/YYYY-MM-DD/`

**Naming:** `{task-id}.result.md`

In manual testing (Phase 1), you'll need to check for the result file after the worker completes.

### Step 2: Read Result File

```
Read(/Users/mark/PycharmProjects/workflow/results/2026-01-19/2026-01-19-1430-hugo-build-staging.result.md)
```

### Step 3: Verify Outputs

Check the YAML frontmatter for:
- `status: success` or `failed`
- All `expected_outputs` are present
- Values match success criteria

**Success Criteria from Templates:**

**Hugo Build:**
- `build_success: true`
- `errors: []` (empty array)
- `file_count > 100`
- `duration_seconds < 60`

**Deployment:**
- `deployment_success: true`
- `http_status: 200`
- `uploaded_files > 0`
- `invalidation_id` present

### Step 4: Decide Next Action

**If Success:**
- Proceed to next step in workflow
- Report success to user with details

**If Failed:**
- Read error logs
- Analyze error type
- Decide: auto-fix and retry OR escalate to user

---

## Complete Workflow Examples

### Example 1: Create Landing Page

**User Request:** "Create a summer auto insurance promo landing page"

**Your Process:**

1. **Design** (You do directly)
   - Decide slug: `/summer-auto-promo-2026/`
   - Choose layout: `landing`
   - Define form tracking: `summer-auto-2026`

2. **Write Content** (You do directly)
   - Craft hero headline
   - Write promo copy
   - Show draft to user for approval

3. **Create File** (You do directly)
   - Write markdown with frontmatter
   - Use Write tool

4. **Build Site** (DELEGATE)
   - Read template: `hugo-build.md`
   - Fill in params for dev environment
   - Write task file to `tasks/pending/`
   - Wait for worker to complete
   - Read result from `results/YYYY-MM-DD/`
   - Verify: `build_success=true`, `errors=[]`

5. **Commit to Git** (You do directly)
   - Git add, commit, push
   - GitHub Actions auto-deploys to dev

6. **User Preview** (Checkpoint)
   - Report dev URL to user
   - Wait for user approval

7. **Deploy to Staging** (DELEGATE)
   - Ask user: "Ready to deploy to staging?"
   - If yes, read template: `hugo-deploy-staging.md`
   - Fill in params
   - Write task file to `tasks/pending/`
   - Wait for worker
   - Read and verify result
   - Report staging URL to user

**User Experience:** 3 messages, 1 content approval, 0 permission prompts, 0 device switches

### Example 2: Update Existing Page

**User Request:** "Update the homepage hero text"

**Your Process:**

1. **Read Current Content** (You do directly)
   - Read the current homepage file
   - Show current text to user

2. **Write New Content** (You do directly)
   - Update hero text
   - Show to user for approval

3. **Edit File** (You do directly)
   - Use Edit tool to update content

4. **Build & Deploy** (DELEGATE)
   - Write hugo-build task for dev
   - Verify build success
   - Commit to git (auto-deploy to dev)
   - User previews
   - Write hugo-deploy-staging task
   - Verify deployment
   - Report success

---

## Error Handling Strategy

### Auto-Fix and Retry

**These errors you fix automatically:**
- Template not found → Create template, write retry task
- Missing frontmatter → Add frontmatter, write retry task
- Broken internal link → Fix link, write retry task
- Syntax errors in markdown → Fix syntax, write retry task

**Process:**
1. Read error from result file
2. Analyze root cause
3. Fix the issue (edit file, create template, etc.)
4. Write new task file with same params
5. Inform user: "Build failed due to [error], I fixed it and retrying"

### Escalate to User

**These errors you cannot fix:**
- AWS credential errors → "Please check AWS credentials on laptop"
- CloudFront configuration errors → "Manual intervention needed: [details]"
- Git merge conflicts → "Merge conflict detected, please resolve: [files]"
- Unknown/complex errors → "Build failed with unexpected error: [summary]. How would you like to proceed?"

**Process:**
1. Read error from result file
2. Summarize in plain language
3. Explain what you tried (if anything)
4. Ask user for guidance
5. Wait for user response before proceeding

---

## Approval Requirements

### Dev Environment
- **Build:** No approval needed
- **Deploy:** Auto-deployed via GitHub Actions (no task needed)

### Staging Environment
- **Build:** No approval needed
- **Deploy:** Conditional approval
  - If minor changes → No approval, just inform user
  - If significant changes → Ask: "Ready to deploy to staging?"

### Production Environment
- **Build:** No approval needed (if for production deploy)
- **Deploy:** ALWAYS require explicit approval
  - Show summary of changes
  - Show staging preview URL
  - Request typed confirmation: "DEPLOY TO PRODUCTION"
  - Only proceed after exact match

**Production Approval Message Template:**
```
⚠️ PRODUCTION DEPLOYMENT WARNING

Changes being deployed:
- {summary of changes}

Staging preview: {staging-url}

This will update the customer-facing site at {production-url}

Type 'DEPLOY TO PRODUCTION' to confirm:
```

---

## File Locations Reference

### Task Files
- **Templates:** `/Users/mark/PycharmProjects/workflow/tasks/templates/`
- **Pending:** `/Users/mark/PycharmProjects/workflow/tasks/pending/`
- **In Progress:** `/Users/mark/PycharmProjects/workflow/tasks/in-progress/`
- **Completed:** `/Users/mark/PycharmProjects/workflow/tasks/completed/`
- **Failed:** `/Users/mark/PycharmProjects/workflow/tasks/failed/`

### Result Files
- **Results:** `/Users/mark/PycharmProjects/workflow/results/YYYY-MM-DD/`
- **Latest:** `/Users/mark/PycharmProjects/workflow/results/latest/` (symlinks)

### Hugo Projects
- **klm-migrate:** `/Users/mark/PycharmProjects/klm-migrate/klm-hugo-site/`
- **klm-plan:** `/Users/mark/PycharmProjects/klm-plan/`

### Deployment Scripts (existing)
- **Staging:** `/Users/mark/PycharmProjects/klm-migrate/publish_to_staging.py`
- **Production:** `/Users/mark/PycharmProjects/klm-migrate/publish_to_production.py`

---

## Current Implementation Status

**Phase 1 (Foundation):** In Progress
- ✅ Directory structure created
- ✅ Task templates created
- ✅ .gitignore configured
- ✅ This guide created
- ⏳ Workers implementation pending
- ⏳ Manual testing pending

**Worker Status:**
- ⏳ hugo_builder.py - Not yet implemented
- ⏳ deployer.py - Not yet implemented
- ⏳ content_editor.py - Not yet implemented

**Phase 1 Testing:**
In Phase 1, you'll manually trigger workers:
1. Write task file to pending/
2. Manually run: `python3 workers/hugo_builder.py` (when implemented)
3. Read result file
4. Verify outputs

**Future Phases:**
- Phase 2: Workers auto-watch pending/ directory
- Phase 3: Full CC integration with auto-verification
- Phase 4: Production deployment with all safety gates

---

## Quick Reference Commands

### Check for Result Files
```bash
ls -lt /Users/mark/PycharmProjects/workflow/results/$(date +%Y-%m-%d)/
```

### View Recent Tasks
```bash
ls -lt /Users/mark/PycharmProjects/workflow/tasks/completed/ | head -5
```

### Check Worker Status
```bash
ps aux | grep python3 | grep workers
```

---

## Tips for Efficient Operation

1. **Always read templates before writing tasks** - Don't guess the format
2. **Verify result files exist before reading** - Use ls first
3. **Include context in task files** - Future you will thank present you
4. **Inform user about delegation** - Transparency builds trust
5. **Verify before proceeding** - Don't assume success, check the result
6. **Commit task files to git** - Audit trail is important
7. **Use consistent timestamps** - Format: `YYYY-MM-DD-HHMM`

---

## Integration with Existing Workflows

This task system **coexists** with existing workflows:

**Git Workflow:** Unchanged
- Still commit to `main` or `claude/*` branches
- GitHub Actions still auto-deploy to dev
- Task system is for builds and staging/prod deploys

**Dev Deploys:** Use existing auto-deploy
- Commit to `main` or `claude/*`
- GitHub Actions deploys automatically
- No task file needed for dev deploys

**Staging/Prod Deploys:** Use task system
- Write task file instead of running deploy script manually
- Worker executes deploy script
- You verify results and report to user

---

**Remember:** You are the brain, workers are the hands. Think deeply, delegate deterministically, verify thoroughly, explain clearly.
