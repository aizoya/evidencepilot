# EvidencePilot PED — one scoped reliability improvement
October 28, 2026 Pacific. This report supersedes status counts in older checkpoint notes, while preserving their evidence.

## Verified recovery and baseline
Recovered latest saved EvidencePilot-reviewer-scorer.zip version 0; SHA256 06a895654a7ae3eaeef2a38987edb976d7b5f7083be80e549a80c449237d223c. Original retained intact. No newer local files existed after workspace maintenance. No Git metadata/branch recovered. A current org:aizoya evidencepilot repository search returned no match; remote/commit remain unverified. No repository, branch, credentials or project recreated.

Baseline: 44/44 local tests passed. Synthetic question -> planner -> three search fixtures -> source registry -> claim construction -> separate review fixture -> report works. This is a mocked workflow, not actual Nebius/Tavily. Baseline demonstrated a report-level inconsistency: evidence_found despite a not_established requirement and unmapped C1. Before bundle retained, not rewritten after fixture correction.

Current environment presence check: NEBIUS_API_KEY, TAVILY_API_KEY, NEBIUS_MODEL absent. Prior browser observations remain historical: Nebius $25 balance, dedicated EvidencePilot key; Tavily 1,500 plan credits, key capped to 100 credits/month, account PAYG enabled without cap; Vercel development project created, no deployment then, connector access failed. No current balance or UI state claimed. Credential transfer was specifically requested but not approved; latest directives stop at credentials and forbid browser access. Browser was not used. Existing credit-only approval is not permission for paid overage or additional access. OS 2.6 remains governing; OS 2.7 not approved.

## Ranked failure categories
Ranking is engineering severity/prioritization, not measured incidence.
1. HIGH, open: semantic false support, stale/scope-mismatched evidence and omitted requirements. Exact quotes/context help inspection but do not prove meaning. Human-reviewed calibration has only three development examples; no real judge predictions or unseen holdout exists.
2. MEDIUM-HIGH, fixed here: report indicated full evidence success despite known incomplete mapping/coverage. Evidence: before.json and new completeness tests.
3. HIGH, open for live release: missing runtime credentials, unknown current balances, PAYG exposure and no verified live integration or deployment. Application daily quota is a request cap, not an invoice guarantee.
4. MEDIUM, open: API timeouts/429s and malformed provider responses beyond current fixtures. Three search/three model bounds prevent repeated loops; zero automatic retries remain intentional. Per-request 40-second timeout is not an aggregate end-to-end deadline. Consequential actions have no dispatcher and are never retried.
5. HIGH-impact if introduced, bounded structurally: hostile retrieved instructions. Existing adapter rejects model tool_calls; arbitrary action fields have no executor; data/instruction separation and auth tests pass. Semantic answer contamination remains unmeasured. No new external-effect tool added.
6. MEDIUM, partially bounded: oversized input and response content. Question 10–1,200 characters, request 8,192 bytes, provider response 2MB, four results/search, 6,000 characters/source, 2,200 output tokens/model. Aggregate input-token and monetary budgets remain open. Existing checks inspected; no duplicate tests added for already covered behavior.

## One implementation change
In core.research finalization only: downgrade evidence_found to partial if any claims are unmapped, outcomes are absent, or any requirement state differs from supported_findings. Add a clear warning. Never overwrite failed or insufficient_evidence. Emit final outcome after this decision so trace and report agree. Diff: implementation.diff. No provider/framework switch, retries, prompt tuning or architecture expansion.

This prevents a misleading overall state; it does not establish completeness of the planner's proposed requirement list. A wrong mapping could still look complete. Supported findings still do not mean deployment approval or contractual compliance.

## Before/after evidence and process
Four synthetic cases, three deterministic repetitions each (not stochastic model eval):
- mapped_success: evidence_found before and after, 3/3 each.
- unmapped_success: evidence_found before -> partial after, 3/3 each.
- safe_search_failure: insufficient_evidence before/after; no synthesis; 3/3 each.
- review_failure: failed before/after; no supported claim promotion; 3/3 each.
Every reported evidence reference in these fixtures resolves to retained synthetic source text with an exact quotation. Empty reports have zero claims; vacuous quote-check success is not evidence support. No external URL was opened or fetched. No source-semantic quality or human-time improvement inferred. FakeProvider call lists confirm only plan/search/synthesis/review operations, with real provider transport patched to reject unexpected calls. A full final regression also passed with outbound socket.connect blocked.

Added four nonduplicative completeness regressions. Initial after run: 47/48 passed, one stale baseline success-fixture expectation failed. Saved as failed-regression-initial.log. Independent reviewer found fixture correction justified, and changed only plan.requirements and synthesis.requirement_ids in FakeProvider. Assertions/grading were unchanged. New unmapped fixture explicitly removes the mapping to preserve the negative test; synthetic harness does likewise. Original before/after bundles retained plus final after-final.json. Final: 48/48 tests pass; independent baseline/core subset 22/22 passes with outbound connections blocked. No interrupted live run occurred.

## Evaluation and control separation
Improvement edit scope: core.py and newly added completeness tests only. Frozen hashes captured for existing tests, eval JSON, reviewer scorer and web approval gate in a separate controls directory before implementation. Hash verification before independent fixture review showed no changes; after review, only tests/test_core.py changed. Its exact diff is recorded as independent-fixture.diff. Existing grading assertions, human labels and web approval gate unchanged.

This is procedural independent-review separation plus change detection, NOT a root-proof security boundary: the coordinating process owns the filesystem. No autonomous self-improvement agent is deployed or allowed to rewrite policy. Strong external repository protections and independent final grading remain required before enabling autonomous improvement. No expected holdout answers accessed or generated. Three earlier human-confirmed examples are development material and never called holdout. No criteria weakened to force a pass.

Measured: local test pass counts, observed report states, source-reference consistency, and local fixture durations in bundles. Not measured: real model support precision, omitted-user-requirement rate, reviewer false alarms, missed serious safety violations, live recoverability, actual provider charges or live latency. Billed cost remains null rather than reported zero. No external effects attempted beyond read-only official web/repository checks.

## Demo preparation and official rules
DEMO-RUNBOOK.md prepares a successful mapped case and honest search/reviewer-failure case. Current prepared run bundles are simulations only; live Nebius/Tavily demo remains HOLD. The existing live verification script is not executed. Original source URL checks and human quote/meaning audits remain required for real demo acceptance.

Dedicated official site rechecked via indexed official-page retrieval: https://hackathon.odsc.ai/ . It retains Nebius Token Factory, Tavily live search, public repository/README, short demo; judging weights 30% evidence, 25% end-to-end, 20% usefulness, 15% design, 10% integrations. No rules inferred from unrelated NVIDIA event. Exact cutoff/timezone, assistance/pre-existing-code policy, full eligibility and demo limit unresolved. Preserve October 27 source provenance. Keynote notes are hypotheses only.

## Recommendation and next concrete step
GO: this local reversible patch is ready for review. HOLD: live reviewer quality measurement, deployment, production, public submission and cross-family experiments.

Next: Franklyn must configure the existing dedicated provider credentials in an authorized development runtime without sending them in chat; verify actual runtime presence and current remaining credits/overage safeguards before authorizing a bounded real run. Browser remains stopped until separately authorized; do not re-open it on this report. No new secrets, paid usage, deploy or submission commitment is approved here. After a permitted live run, retain actual outputs and grade against the development reference, then obtain a genuinely untouched independently held holdout.

State: local modified source + saved checkpoint only. Not Git-committed, merged, deployed or submitted. Other apps untouched; previous separate PCC/PlateReach/LBK handoff retained.
