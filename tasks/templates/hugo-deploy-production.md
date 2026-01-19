---
# Metadata
task_id: {timestamp}-hugo-deploy-production
task_type: hugo-deploy-production
created_at: {ISO-8601-timestamp}
created_by: claude-code
status: pending
worker_type: deployer
priority: high
timeout_minutes: 15

# Context (audit trail)
context:
  user_request: "{description of what user requested}"
  branch: "{current-git-branch}"
  build_task_id: "{id of build task that preceded this}"
  staging_task_id: "{id of staging deploy, if applicable}"
  changes_summary: "{detailed summary of what's being deployed}"

# Task Parameters
params:
  public_dir: /Users/mark/PycharmProjects/{project}/klm-hugo-site/public
  bucket: s3://klminsurance.com
  cloudfront_id: "{production-cloudfront-id}"
  verify_url: https://www.klminsurance.com
  deployment_script: /Users/mark/PycharmProjects/klm-migrate/publish_to_production.py

# Expected Outputs (for CC verification)
expected_outputs:
  - deployment_success: boolean
  - uploaded_files: integer
  - invalidation_id: string
  - http_status: integer (200)
  - verification_url: string
  - duration_seconds: float
  - deployment_timestamp: string

# Approval (REQUIRED)
requires_approval: true
approval_type: explicit  # Must type "DEPLOY TO PRODUCTION"
approval_confirmation: "DEPLOY TO PRODUCTION"
approved_by: "{user-name}"
approved_at: "{ISO-8601-timestamp}"
---

## Task Description
⚠️ **PRODUCTION DEPLOYMENT** - Deploy to customer-facing site (www.klminsurance.com)

## Pre-Deployment Requirements
**MUST BE VERIFIED BEFORE APPROVAL:**
1. ✅ Staging deployment completed successfully
2. ✅ User reviewed staging site and approved
3. ✅ No errors in build or staging deploy
4. ✅ Changes are intentional and reviewed
5. ✅ User typed explicit confirmation: "DEPLOY TO PRODUCTION"

## Changes Being Deployed
{CC fills in detailed summary of changes}

## Success Criteria
- All files uploaded successfully to production S3
- CloudFront invalidation created
- Site accessible at www.klminsurance.com
- HTTP status 200 on homepage
- No broken links
- All pages render correctly

## Approval Process
CC MUST show user:
1. Summary of changes being deployed
2. Link to staging preview
3. Warning that this is production
4. Request explicit typed confirmation

User MUST type: "DEPLOY TO PRODUCTION"

## Rollback Plan
If deployment fails or critical issues found:
1. Worker reports error immediately
2. CC notifies user of failure
3. Previous version remains accessible
4. Manual rollback may be required

## Post-Deployment Verification
After deployment, worker will:
1. Check HTTP status of homepage
2. Verify key pages are accessible
3. Check CloudFront invalidation status
4. Report comprehensive results to CC

## Logging
All production deployments are logged with:
- Timestamp
- User who approved
- Changes deployed
- Build/deploy task IDs
- Verification results
