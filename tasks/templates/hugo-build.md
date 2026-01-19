---
# Metadata
task_id: {timestamp}-hugo-build-{environment}
task_type: hugo-build
created_at: {ISO-8601-timestamp}
created_by: claude-code
status: pending
worker_type: hugo-builder
priority: normal
timeout_minutes: 10

# Context (audit trail)
context:
  user_request: "{description of what user requested}"
  branch: "{current-git-branch}"
  files_changed:
    - "{list of files modified}"

# Task Parameters
params:
  site_path: /Users/mark/PycharmProjects/{project}/klm-hugo-site
  environment: dev | staging | production
  base_url: "{environment-specific-url}"
  minify: true
  clean: true

# Expected Outputs (for CC verification)
expected_outputs:
  - build_success: boolean
  - file_count: integer (>100)
  - errors: array (empty)
  - warnings: array
  - duration_seconds: float (<60)
  - hugo_version: string

# Approval (if needed)
requires_approval: false
---

## Task Description
Build Hugo site for {environment} environment.

## Success Criteria
- Build completes without errors
- File count > 100
- Duration < 60 seconds
- All pages render correctly

## Rollback Plan
If build fails, restore previous public/ directory and report errors to CC.

## Environment-Specific URLs
- dev: http://dev-klmhugoweb.s3-website-us-east-1.amazonaws.com/
- staging: https://www.klmcrm.com
- production: https://www.klminsurance.com
