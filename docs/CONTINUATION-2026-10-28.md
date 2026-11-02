# EvidencePilot recovery, gap checklist and decision — October 28, 2026 PT

## Decision
GO for local synthetic development and review. HOLD for live experiment, deployment, production or submission. OS 2.6 remains governing; no OS 2.7 approval inferred. Keynote notes are selected-slide hypotheses, not model benchmark facts or competition requirements.

## Recovered state and provenance
Recovered original EvidencePilot-prototype.zip from persistent saved artifact version 0; original archive SHA-256 5ca96378a21e5052e035a2dbd7daaa47d9503f5d3ef7210e9bc6368b5be51bb5. Source was restored, not regenerated. No Git metadata, branch or commit is contained in the archive; exact org:aizoya evidencepilot search returned no repositories today. This is not proof that no private repository exists elsewhere. No remote/branch was invented or initialized. The original archive and existing test logs remain unchanged. Package manifest from the baseline is historical and does not describe this patch; see continuation-manifest.json.

Prior observed account state (not freshly reauthenticated this turn): Nebius AIZOYA account showed $25 balance and dedicated EvidencePilot-Development key. Tavily showed 1,500 plan credits, zero usage, PAYG enabled without account cap, and dedicated development key capped at 100 credits/month. These are earlier observations, not current balance guarantees. Creating keys did not configure the application. Fresh environment presence checks: NEBIUS_API_KEY, TAVILY_API_KEY, NEBIUS_MODEL all absent. No provider calls attempted. No secrets read, transferred or changed.

Vercel project created earlier via browser: evidencepilot-development, project ID prj_tY1M0oK5ponbinnqGozwU0GlxXv2 under AIZOYA. No production deployment was observed then. Connector returned 403 on create and 404 on subsequent read even by exact ID. Browser creation and connector failures are distinct evidence. A Development-only Secret form was prepared but never saved. Do not retry credential transfer based on this directive.

## Existing versus missing coverage
| Area | Baseline | This patch / remaining gap |
|---|---|---|
| Supported claims | Exact quote plus same-model review; synthetic success test | Retained. Explained review required before support promotion. Semantic correctness unmeasured. |
| Missing evidence | Empty search and fabricated quote tests | Retained; snippet-only support now stays uncertain. |
| Conflicts | Two distinct exact opposing passages required | Retained. False conflicts caused by plan/date scope still need semantic evaluation. |
| Outdated evidence | Review prompt only | Added test that an uncertain dated-evidence judgment is respected. Actual stale-evidence detection NOT tested. |
| API failure | Search/review failures and reserved quota | Added result-bearing failed tool events. Real timeout/429 recovery unverified. |
| Hostile retrieved instructions | Prompt/data separation test | Added tool-call rejection and action-data/no-dispatch fixtures. Answer contamination remains possible. |
| Unauthorized actions | No action executor; auth/origin gates | Added attempted send_email tool rejection. No real external effects executed. |
| Trace | Query-bearing search trace, usage, run ID | Added allowlisted execution_events: R1, source IDs/hashes, proposed operation, configuration boundary, actual returned/failed state and final outcome. No raw question, quote, credential or exception body in these events. |
| Requirement coverage | No decomposition into user requirements | Still missing. R1 is only a whole-question reference; never claim per-requirement coverage. |
| Privacy | Full question/source text in private report/export | Legacy trace still includes queries; private report is not telemetry-safe. Only execution_events is intended for coarse audit. Do not publish raw run bundles. |
| Holdout | No authentic sealed set recovered | None created with expected answers by implementer. Requires independent custodian before final evaluation. |
| Reviewer evaluation | Same family, uncalibrated | Reference-set protocol added. No human labels or cross-family results fabricated. |
| Cost controls | Durable 10 runs/day default, 3 search + 3 model calls, no retry | Request/output caps are not dollar caps; monthly global ledger, aggregate input cap and deployed durability remain open. |

## Smallest useful patch
Implemented without infrastructure changes:
1. Reject model tool_calls at the provider adapter; never dispatch external actions.
2. Decline promotion on search excerpts alone or a missing reviewer explanation.
3. Add privacy-limited operation/result events and final evidence-status mapping to exported report.
4. Add seven missing development regressions; retain the existing suite.
Not implemented: framework migration, new providers, tenant database, additional autonomous loops, semantic scope classifier or billing.

Next patch only after reviewing these results: add explicit requested requirement IDs and unknown outcomes; retain source section/table context; test independent dated and scope-mismatch fixtures; expose safe execution_events in the trace UI (currently export-only). Evaluate whether those changes improve support rather than assume they do.

## Test evidence
Baseline: 22/22 passed in fresh local recovery. Patched: 29/29 passed, standard-library unittest; source syntax guard passed. Exact logs: baseline-recovery-tests.txt, failed-patch-experiment-01.txt, patch-tests.txt. The failed experiment produced 3 errors (uninitialized lookup); fixed by initializing the evidence lookup before review, then rerun. No test failure was deleted. Tests use fakes/patches and do not prove real service behavior or semantic security.

Automated regression pass rate: 29/29 on this run. Supported-claim accuracy, requirement coverage, appropriate abstention, serious violations missed, false-alarm rate, severity distribution and recoverability rate: NOT MEASURED on a human-labeled set. Test elapsed time is local fixture time, not application/provider latency. Actual Nebius/Tavily cost: NOT MEASURED; no calls this turn. Unknown cost is not zero-cost operation evidence.

## Reviewer evaluation and holdout boundary
Existing six public examples and all tests are development material. Have a human custodian assemble a small synthetic reference set with claim, full passage/context, date/scope, expected status, seriousness of error and annotation justification. A second human reviews disagreements. Mark labels pending until humans actually review them. Do not call model-authored labels human-reviewed.

Before tuning, have a separate custodian freeze held-out inputs and keep expected answers outside the implementation workspace, prompts, retrieval store and code repository visible to the agent. Record set version/hash and custody metadata only. Custodian runs final grading blind; report denominators and failed cases. If results are inspected and used for fixes, that set becomes a consumed test set; obtain a fresh holdout for new superiority claims. No claim of a sealed holdout is made today.

Compare reviewer predictions with adjudicated human labels: false support/false rejection, unsupported certainty, missed serious violations, false conflicts, appropriate abstention and precision/recall with zero-denominator metrics null. Severity: critical=unauthorized external effect or secret disclosure; high=unsupported decisive approval; medium=material omission/false conflict; low=presentation. Recoverability records whether a safe partial result, denial or human reconciliation remains possible. No global percent safety claim from a finite fixture set.

Cross-family reviewer comparison is deferred: no configured model, no approved added budget. If later authorized, use identical evidence and blinded labels, measure single-judge versus independent-family review, and include all attempts/costs. Keynote rankings cannot select a provider.

## Official rules recheck and demo
Today the dedicated official hackathon page was retrieved through indexed search; direct open rendered no body. It still states Nebius Token Factory inference, Tavily live search, public repository/README and short demo; weights 30% evidence, 25% end-to-end, 20% usefulness, 15% design, 10% integrations. Source: https://hackathon.odsc.ai/ . Pre-existing code/AI assistance permissions, exact cutoff timezone, full eligibility and demo-length limit remain unresolved. Preserve October 27 prototype provenance.

Demo target: one fresh successful research run, click decisive evidence; then one real conflicting-evidence or visible failed run. Show established/unknown distinctions, sanitized actual results and source links. Fixture demonstration must be labeled simulation. No real success is claimed today. Earlier HTTP smoke is historical; no new browser/mobile QA or deployment verification performed this turn.

## Approval ledger and risks
Prior approval: create dedicated provider keys; credit-only tests, no paid overage. Subsequent specific transfer of those keys into Vercel Development was requested but not approved before this directive. Current instruction explicitly stops for credentials, new access, spending, production or submission. No such action taken. Existing unlimited PAYG account setting means a 100-credit key limit alone does not prove no paid overage if other keys consume the allowance. Recheck balances and enforce global budget before any authorized live run.

HOLD reasons: runtime credentials missing, model unset, provider access untested, real reviewer calibration absent, no untouched heldout set, no per-requirement coverage implementation, privacy risk in full exports, security/dependency/container scans and primary-device tests outstanding, no verified public repo/branch/deployment/submission. GO scope is reversible local synthetic work only.
