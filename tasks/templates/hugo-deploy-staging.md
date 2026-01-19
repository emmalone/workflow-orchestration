---
# Metadata
task_id: {timestamp}-hugo-deploy-staging
task_type: hugo-deploy-staging
created_at: {ISO-8601-timestamp}
created_by: claude-code
status: pending
worker_type: deployer
priority: normal
timeout_minutes: 15

# Context (audit trail)
context:
  user_request: "{description of what user requested}"
  branch: "{current-git-branch}"
  build_task_id: "{id of build task that preceded this}"
  changes_summary: "{brief summary of what's being deployed}"

# Task Parameters
params:
  public_dir: /Users/mark/PycharmProjects/{project}/klm-hugo-site/public
  bucket: s3://klmcrm.com
  cloudfront_id: E3HA8770RGET6T
  verify_url: https://www.klmcrm.com
  deployment_script: /Users/mark/PycharmProjects/klm-migrate/publish_to_staging.py

# Expected Outputs (for CC verification)
expected_outputs:
  - deployment_success: boolean
  - uploaded_files: integer
  - invalidation_id: string
  - http_status: integer (200)
  - verification_url: string
  - duration_seconds: float

# Approval
requires_approval: true
approval_type: conditional  # CC asks if changes are significant
---

## Task Description
Deploy built Hugo site to staging S3 bucket with CloudFront invalidation.

## Success Criteria
- All files uploaded successfully to S3
- CloudFront invalidation created
- Site accessible at verification URL
- HTTP status 200 on homepage
- No broken links

## Pre-Deployment Checklist
- [ ] Build completed successfully
- [ ] File count is reasonable (>100, <500)
- [ ] No errors in build log
- [ ] Changes reviewed by user

## Rollback Plan
If deployment fails or site is inaccessible:
1. Report error to CC
2. CC can trigger rollback task if needed
3. Previous version remains accessible

## Verification Steps
After deployment, worker will:
1. Check HTTP status of homepage
2. Verify CloudFront invalidation is in progress
3. Report success/failure with details
