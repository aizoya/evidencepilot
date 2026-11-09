# EvidencePilot — SURFACE-2 failure parity

October 28, 2026. Implemented and locally tested only; no Git checkout, branch, commit, merge, deployment or submission verified. OS 2.6 remains governing; no OS 2.7 adoption.

## Recovery and scope

Recovered the existing local EvidencePilot source and all 93 files in the request-mapping checkpoint matched its manifest. Reused FakeProvider(search_error), the existing bounded research pipeline, renderer, transport failures and no-tool-dispatch tests. Recovered the SURFACE-2 handoff from OS27_Missed_Training_Review_and_App_Handoffs_2026-10-28.md, Library ID libfile_a1c42b0603ac8191b0fa9ac128a75080, as task context, not policy approval. No provider, account, credential or external application changes.

## Before / after

| Check | Before | After |
|---|---|---|
| Failed-search pipeline | Existing tests establish insufficient evidence and no claims | Unchanged; reused fixture with three bounded failed queries, no synthesis/review |
| Card/plain parity | Missing, new regression fails | Both views use the same failure content and safe trace |
| User-facing status | Generic finished message for insufficient evidence | Explicit failed search and no verified answer |
| Next step | No shared failure guidance | Check availability and remaining quota before a separately initiated run; no automatic retry or external action |
| Export binding | Handler reads whichever report is current | Closure binds exact run ID, schema and serialized full result; stale record or changed same-ID content rejected |

Both views state: Search failed — no verified answer. No usable source material was retrieved. The answer remains unknown. Check provider availability and remaining quota before starting a new research run. No automatic retry or external action is authorized. Safe trace preserves event order, coarse action/result/outcome and research-only approval boundary, excluding raw questions, source payloads and search queries. The existing JSON export intentionally retains the full private report; it is not a redacted telemetry export.

## Evidence

- Historical same-checkpoint baseline: 60 local tests. Existing assertions/fixtures, core pipeline, web gates, calibration labels and approval controls unchanged.
- Full relevant regression after patch: 61/61 tests passed in after-tests-final.log; JavaScript syntax and narrow source guard passed.
- Additional export-byte/filename check passed in after-test-export-check.log. Only the targeted test was repeated after strengthening this test; production code unchanged.
- HTML balanced tags and unique IDs checked.
- Actual app.js executed locally in a Node VM using a DOM double. This is real local renderer execution with simulated DOM and synthetic provider output, not browser layout, real-device or live provider evidence.
- Checks cover exact shared failure text, safe trace parity, mode switching, private canary removal, rejected action-label injection, stale-record and changed-result rejection, bound JSON bytes/filename, and zero research/external-action requests. A stubbed /health response is not provider access. Python outbound connections blocked in the fixture test; no holdout answers accessed.
- Independent same-provider review found no material defect and independently passed the targeted test. It does not establish cross-family review or live semantic accuracy. The later export-bytes/filename assertions address its noted harness limitation.

## Preserved failures

1. before-test.log: new acceptance regression failed on missing evidence card.
2. after-test-initial.log: first patch allowed a changed action label to bypass the failure-specific sanitization path. Fixed by classifying insufficient-evidence/no-claims/no-sources reports using observed failed-event state rather than the mutable action label. The original failure log is retained.

## Action authority and remaining gaps

The only result-specific action is local JSON export. Its parameters (format, file name, snapshot) are fixed by the application closure; a stale callback cannot export a newer report. This is local snapshot binding, not an authoritative persisted record revision or server authorization mechanism. Research remains an explicit form submission under existing server gates. No effectful card/chat action or external write dispatcher exists. Any future write action still needs current server identity, tenant, version, scope and approval checks; UI text cannot authorize it.

Actual browser/mobile rendering, downloaded-file delivery, live provider execution, end-to-end semantic accuracy and authoritative server record/version checks remain unverified. Local DOM tests do not establish these. No live latency, billed cost or user timing measured. No provider calls, spending, deployment, new tools or submission occurred.

Disposition: GO for this bounded local SURFACE-2 patch; HOLD for browser/mobile acceptance and live/deployed claims. Next concrete step: test these two existing display modes in an authorized local browser with the same synthetic result, before making any usability claim.
