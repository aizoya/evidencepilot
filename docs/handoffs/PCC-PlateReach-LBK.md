# Separate handoff — PCC, PlateReach and LBK
Planning only. No application inspected, changed, connected or deployed from EvidencePilot. PCC expansion and app identity are unresolved; do not guess. This handoff does not approve OS 2.7 or authorize external communications.

For each application, its accountable owner should first identify exact repository, environment, tenants, supported actions, existing controls and approval records. Reuse existing mechanisms before adding infrastructure.

| Control | Required design/evidence | Synthetic acceptance cases |
|---|---|---|
| Approval enforcement | Bind authorization to actor, tenant, exact action/resource/parameters, expiry and one-use/idempotency scope; enforce before side effect in code | Missing, expired, revoked and changed-parameter approval all deny; model claiming approval does not count |
| Tenant isolation | Server-derived tenant identity; permission check on reads, writes, caches, attachments and worker jobs; RLS when applicable | Tenant A cannot enumerate/read/update/export Tenant B; revoked user loses cached and queued access |
| Duplicate prevention | Durable idempotency key scoped to tenant and operation; concurrency-safe transaction and dedup record | Concurrent replay creates one effect; legitimate distinct actions remain distinct |
| Safe external actions | Preview/validation then approved execution; destination resolution; tool result readback; unknown-write reconciliation | Timeout after send does not blindly resend; denied call creates no external effect; uncertain state escalates |
| Trace hygiene | Actor surrogate, tenant surrogate, source/evidence reference, approval ID, proposal, actual result and final verified state | Secret/PII canaries absent; failed events retained; agent assertion never marks completion |

PCC: verify exact identity and sensitive data categories before applying this plan. PlateReach: inspect outreach destination/consent, duplicate-contact/send protections and tenant-specific campaign data. LBK: inspect order/event changes, quote/invoice boundaries, duplicate requests and customer-facing sends. These are proposed inspection scopes, not claims about implemented features.

Use synthetic tenants and a fake external-effect sink first. Measure critical violations missed, false denials, duplicate effects, wrong-tenant exposure, recoverability and severity. No live email, SMS, payment, order alteration or customer-data use until separately authorized for the exact app/action. Deliver each app's own gap report and owner decision; never copy EvidencePilot credentials or customer data across products.
