# First live-run audit and bounded absence guard

## Verified baseline

Recovered source core.py matches GitHub blob 618cdd7f9acdc8791a63c493fb2c684939d22420
on build/checkpoint-20261101 at 7954ffd8f4cf47f433ae43093e5218fc47a180a8.
The existing 61 local tests passed. They use fixtures, including the SURFACE-2 DOM double.
No held-out answers were accessed and no grading or approval controls changed.

The user-supplied live export (run 198d00d0-87fb-4d8c-8f33-3c7a9d1f27a1) records
25.57 seconds, three Tavily credits, and three Nebius calls totaling 30,533 input
and 1,995 output tokens. These are exported usage records, not an independently
verified invoice. Dollar cost is unknown. The original export remains unchanged
in its uploaded artifact; saved-run-recheck.json records its SHA-256.

All seven stored source-content hashes and eight quote offsets matched locally.
That did not establish semantic support. The live answer was partial.

## Ranked failures and one scoped improvement

1. Unsupported absence conclusions accepted by the model reviewer: C4/C6/C8,
   plus the absence assertion in compound claim C5. Addressed conservatively.
2. Event dates overgeneralized as a submission period (C3). Still unresolved.
3. Search returned unrelated competitions and missed the governing main page.
   Still unresolved; this patch makes no retrieval changes.

The sole runtime change is an English wording guard on automatic promotion of
documentation-absence claims. Recognized claims remain uncertain even when the
model reviewer says supported. Positive findings and documented capability
restrictions are unaffected in the regression cases.

This is a heuristic safety brake, not semantic verification. It may over-abstain
on explicitly documented absence, and paraphrases outside its patterns may evade
it. Human scope review remains required. There is no UI override or new authority.

## Before and after evidence

- baseline-tests.log: 61 tests passed before changes.
- before-regression.log: four new test methods exposed six failures (including
  subtests) before the guard. No prior tests were weakened.
- after-tests.log: all 65 tests passed after the guard, including the existing
  SURFACE-2 parity, stale export binding and no-external-action checks.
- development-failure-fixture.json: short public-source excerpts from the failed
  live run; explicitly development data, never holdout.
- saved-run-recheck.json: deterministic offline application of the new guard to
  the saved model judgments. Four formerly supported claims become uncertain.
  C3 remains incorrectly supported; this failure is explicitly retained.
- saved-run-initial-failure.txt: initial audit assertion missed C5; preserved and
  corrected after inspecting the compound claim.

No provider requests, spending, new credentials, deployment, CI activation, merge,
or submission occurred in this patch. Offline changes do not demonstrate better
live-model accuracy, latency or cost. Existing export/action binding was unchanged.

## Decision and next step

GO for continued local development; HOLD for a verified-success demo or release.
Next: address C3's date/scope error with a separate development regression, then
evaluate retrieval coverage. A subsequent live run requires explicit authorization
within the existing usage boundary; do not reset the user's one-run quota.
