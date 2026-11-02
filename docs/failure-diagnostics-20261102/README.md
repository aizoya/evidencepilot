# Safe extraction and citation failure diagnostics

Parent: c338d01d1542fe34c311d5bb7745ddef789672eb on the existing review branch.

## Baseline and third live-run evidence

The user's Mac passed 84 tests and started the updated server. Uploaded run
13390016-ff9d-48c9-bfec-82e99529bcd6 recorded a partial result in 13.39 seconds:
two searches, one failed extraction, three model calls, 19,429 input tokens,
798 output tokens, two reported Tavily credits consumed versus three reserved.
Dollar cost remains unknown. All seven source hashes and three quote offsets match.

The extraction did not produce an accepted main-site source. The result was visible
and no retry occurred. S1 retained the required-provider wording, but C4 had no
accepted citation. Submission requirements remained unanswered. The eligibility
review reason still overstates open-to-everyone wording as unrestricted.

The exact extraction rejection category and rejected C4 evidence were not saved.
Neither failure cause can be reconstructed from the old export. It is not evidence
that the page is permanently inaccessible, or that a model switch is needed.
third-live-audit.json records this limitation and the original artifact SHA-256;
the original remains unchanged in the uploaded artifact.

## Scoped implementation: diagnostics only

Extraction ResearchErrors now carry fixed categories for request failure, malformed
structure, provider-reported URL failure, empty results, unexpected result count,
URL mismatch and empty content. Execution events expose only the application's
allowlisted categories. Provider messages, raw failure results and arbitrary error
codes are not copied into these diagnostics.

Each validated claim records counts of rejected evidence categories: missing/invalid
evidence list or record, unknown source, invalid/short quote, quote not in retained
source text. No rejected quote or source identifier is stored. Counts describe the
existing bounded validation path; they do not enumerate every possible error and
do not validate semantics. Existing three-evidence-item limits remain.

Acceptance criteria, citation matching, review rules, budgets, tools, permissions,
retry behavior, exports and UI action binding are unchanged. This patch improves
investigation of future failures; it does not repair retrieval or answer coverage.
Raw model responses are still not persisted. Claims remain unsupported when their
evidence is rejected, even if a model review approves them.

## Before and after

- baseline-tests.log: 84 existing tests passed.
- before-initial-harness.log: first test invocation accidentally collected seven
  imported TestCase methods again; retained. Only the import was corrected to use
  the existing fixture helper without duplicating its tests; assertions unchanged.
- before-regression.log: four new methods with subtests exposed 13 failures before
  implementation. No prior test or grading expectation was weakened.
- after-tests.log: all 88 tests pass, including existing SURFACE-2, action binding,
  interruption, no-retry and fail-closed claim checks. New cases cover raw-payload
  canaries, classification in actual pipeline events, unchanged request count and
  positive exact-evidence behavior. All calls use fixtures or patched transport;
  no holdout was read or tuned against. No live accuracy/cost/latency gains claimed.

## Next step and gates

GO for local investigation; HOLD for a successful-research demo or release. Before
another paid run, build an offline citation-attachment fixture with an explicitly
known failure cause; do not pretend it reproduces the unknown live C4 output.
Keep the main-page extraction outcome unresolved until new evidence exists.

No new provider calls, spending, credential changes, quota changes, persistent
access, CI activation, merge, deployment or submission occurred. The user's Mac
server is still the earlier version. Three live runs have already been performed;
this patch authorizes no fourth run and does not reset the quota.
