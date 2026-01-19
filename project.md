
Claude Code:
- Writes task files
- Reads result files
- Explains outcomes

---

### 8.2 Database-Backed Tasks (Future)
When concurrency or volume increases:
- SQLite or Postgres
- Explicit task states
- Strong auditability

---

## 9. Deployment Philosophy

### 9.1 Environments
- Local (developer)
- Dev
- Staging
- Production

Claude Code must never deploy to production without explicit approval.

---

### 9.2 AWS Integration (Future)
- CI runners for builds
- S3 / CloudFront for Hugo
- Secrets managed via AWS tooling
- No secrets embedded in AI prompts

---

## 10. Cost & Risk Management

- Claude Code used for high-leverage thinking
- Execution offloaded to cheaper systems
- Local models used where appropriate
- No proxy services required
- No vendor-specific APIs baked into core logic

---

## 11. Success Criteria

The system is successful when:
- Routine work runs without CC intervention
- CC focuses on design and oversight
- Virtual employees are predictable
- Costs are controllable
- Model changes do not require rewrites
- Human trust increases, not decreases

---

## 12. Planning Mandate for Claude Code

Upon reading this document, Claude Code must:

1. Summarize the intended architecture in its own words
2. Identify missing details or ambiguities
3. Propose a **phased implementation plan**
4. Recommend:
   - Tool versions
   - Folder structure
   - Initial workflows
5. Ask clarifying questions **before** implementing anything

---

## 13. Explicit Non-Goals

- Fully autonomous AI without human checkpoints
- Single “god agent”
- Hidden state or long-running AI memory
- UI-driven automation
- Tight coupling to any single model provider

---

## 14. Final Principle

> **AI should think until confident, act once deterministically, record results, and stop.**

Anything else introduces risk, cost, and fragility.

---

## End of Document
