# Request-link contract implementation
October 28, 2026 Pacific. Continues the 52-test transport-reliability checkpoint. Local implementation only; no Git metadata/branch/commit, merge, deployment or submission verified.

## Implemented
Canonical question is trimmed once before planning and reused for all calls/reporting. Existing planner response schema now requests exact user_spans; no new model call added. Pure request_links helper validates up to three records against that canonical string using Unicode code-point offsets, exact equality, integer/nonboolean indices and bounds. Quote-only records resolve only when unique. Repeated text without offsets is ambiguous; explicitly validated second occurrences are accepted. Whole-question spans are rejected for planner proposals to avoid blanket provenance laundering; explicit fallback remains unreviewed/missing.

Backend retains valid span records but aggregates all records: invalid outranks ambiguous, then missing, then matched. More than three spans rejects linkage without silent truncation. Declared/unresolved counts and limitation text are retained. Requirements remain visible even when linkage fails. Origin and interpretation_status are assigned by application code; a model cannot label its proposal human_confirmed.

Overall result becomes partial when any accepted requirement lacks matched linkage, fallback/unusable proposals occur, or the five-proposal cap is exceeded. Failed/insufficient results remain unchanged. Cap, withheld count and incomplete-coverage warning are visible through existing warnings. UI exposes Linked request text, planner-interpretation status, span counts and limitations. coverage_assurance remains not_verified even when every link matches. Exact spans establish location only, not faithful semantics or complete extraction. No action approval derives from a request span.

## Before/after and tests
Baseline 52/52 passed after correcting test-discovery working directory; original failed discovery log retained. New development cases cover unique and repeated spans, explicit second occurrence, mixed validity, invalid indices/bool, excess spans, Unicode codepoints, full-question misuse, model attempts to assign human authority, canonical whitespace and partial/cap behavior.

Initial expanded suite failed three tests: one whole-question rejection was not yet applied because the edit command used an incorrect relative path, plus two old success fixtures without spans. That record is retained in after-initial.log. Corrected paths applied the planned full-question guard and UI; before independent fixture correction, two old fixture tests still failed (after-before-review.log). No failures deleted.

Independent reviewer was authorized to update ONLY planner fixture records in test_core.py and test_report_completeness.py with quote 'plan limits', retaining existing requirement text and assertions. Reviewer ran 60/60 with outbound connections blocked and found cap disclosure missing from UI. Implementer then added count/limit warning and existing new-test assertion for it. Final local suite: 60/60 passed, source guard passed, JavaScript syntax passed. No claim of independent re-review of the last disclosure edit. New UI is not browser/mobile tested because browser remains stopped.

Three deterministic repetitions of four cases against original core and patched core, identical explicit fixtures/evidence:
- valid link: evidence_found -> evidence_found (3/3).
- missing link: evidence_found -> partial (3/3).
- invalid quote: evidence_found -> partial (3/3).
- six requirements: partial -> partial, with explicit five-item cap and withheld count now reported (3/3).
These are simulations. No real inference/search, semantic accuracy, service cost/latency or user-time improvement measured. Test runtime is not live latency. Expected development answers were visible; no heldout evaluated.

## Control integrity and limitations
Existing human calibration JSON, grading scorer, web approval gate and existing assertion criteria remain unchanged. Hash check confirms only the two independently authorized fixture files changed among frozen files. This is procedural independent review/change detection, not a sandbox against coordinator root access. No autonomous improvement agent is allowed to modify policy. Untouched independently custodied holdout is still absent; do not claim one.

Quotation anchoring can still be irrelevant, incomplete or misleading. A planner can omit an entire clause, overdecompose, choose the wrong occurrence despite valid offsets, or paraphrase negation incorrectly. requirement text is bounded and semantic review remains unmeasured. UI shows stored quotes rather than performing UTF-16 highlighting; actual iPhone display requires future QA. Whole-question rejection may increase abstention for atomic questions; measure false alarms before weakening this reviewed contract. Do not silently restore evidence_found to optimize scores.

## Boundaries and recommendation
No credentials read/transferred/created, provider changes, installs, external communications, spending, production or submission. Existing key transfer remains pending; runtime provider credentials/model remain unconfigured from last verified check. Browser remains stopped. OS 2.6 governs; no OS 2.7 approval inferred. PCC/PlateReach/LBK unchanged.

GO local patch review. HOLD live/production/submission. Next meaningful gate: verify real planner outputs and semantic fidelity against human development references only after secure runtime credentials, credit/overage checks and specific live-run authorization. No new architecture or additional reviewer provider is justified by these synthetic results.
