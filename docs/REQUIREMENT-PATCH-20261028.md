# Requirement mapping patch — October 28, 2026 PT

Continues the recovered source and previous checkpoint. No repository recreated, infrastructure changed, or provider called.

Implemented: planner may propose up to five requirements; backend assigns R1–R5 rather than accepting model IDs. Missing/malformed requirement list falls back to the whole question with an explicit fallback label. Synthesis receives these IDs; code rejects unknown/malformed mappings. Final reports preserve every accepted requirement and associate mapped claim IDs. States are supported_findings, partial_findings, conflicting_findings, or not_established. These describe findings, NOT full requirement satisfaction. Unmapped claims remain listed in JSON. Failed and empty runs retain unknown requirements. UI displays requirement rows and execution events.

Development tests: 35/35 passed (previous 29 plus six new tests). Python source guard and JavaScript syntax checks passed. See requirement-patch-tests.txt. Earlier failed patch experiment and previous logs retained. Browser/mobile rendering NOT tested this turn; no live model test, latency/cost measurement, human calibration or held-out evaluation performed.

Limitations: planner may omit requested requirements or invent extra ones; maximum five truncates additional planner proposals. No coverage percentage should be claimed. A model can assign a fact to the wrong requirement. Supported findings do not show every facet was addressed. Section/table scope preservation is still a next patch; no semantic-scope guarantee. Legacy trace contains queries and full reports include user/source content; treat them as private, not public telemetry. Execution events retain R1 as whole-question operation reference; final evidence events include validated claim requirement IDs. Source metadata is not copied into operational event text.

Next smallest work: include source section and surrounding context with each evidence passage, preserving original text; add synthetic scope/negation tests, then independent human reference labels. Do not tune on held-out answers. No cross-family judge trial without configured access and authorized budget.

Approval boundaries unchanged: Vercel key transfer remains pending; no persistent access created, credential exposed, paid overage enabled, production deployment or submission performed. GO local development; HOLD live/production/submission until prerequisites and approvals are verified. OS 2.7 remains unapproved.
