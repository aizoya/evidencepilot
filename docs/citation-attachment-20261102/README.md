# Controlled whitespace-only citation attachment experiment

Parent: 42f29c92c7fcb698330f1297ee51aeb3b48aaa3c, existing review branch.
Scratch maintenance removed the earlier local checkout. Recovered 23 necessary
source/test/helper files from that pinned GitHub commit and verified every Git blob
identity. No repository AGENTS.md was present in the remote tree. No holdout dataset
or expected holdout answers were retrieved. Existing scoring code was read for test
execution only and remains unchanged.

## Baseline and hypothesis

All 88 recovered tests passed. The third live run's C4 had no accepted citation,
despite relevant retained source text. Its rejected model output is unavailable;
the actual cause remains UNKNOWN. This experiment does not reconstruct that output.

Synthetic hypothesis: a draft quote that differs solely in whitespace can fail
attachment while its wording is present. Test sources and reviewer judgments are
fictional development fixtures, not primary-source research or observed API behavior.

## One bounded implementation change

Try exact matching first. If it fails, allow only equivalence of whitespace runs.
Preserve every non-whitespace character: words, punctuation, negation, numbers,
case and Markdown remain unchanged. Reconstruct the exact original source substring,
store its original offsets/context and mark quote_match as whitespace_only.
Do not store a cleaned quote as if it appeared verbatim on the page.

Recovered source passages remain capped at 600 quote characters. Count overlapping
matches as well as separate occurrences on this fallback path. Multiple matches
remain subject to the existing ambiguity gate and cannot be promoted as supported
by a positive model review alone. Successful attachment still requires semantic
review; this change does not grant factual support automatically.

No fuzzy similarity, synonym replacement, Markdown stripping, additional provider
call, retry, spending, provider switch, quota or approval change was introduced.

## Verification evidence

- baseline-tests.log: all 88 pre-existing tests passed after verified recovery.
- before-regression.log: six initial methods exposed four failures before change.
- overlap-before.log: an additional overlapping-match case exposed one ambiguity
  failure in the first implementation. Preserved; no test expectation weakened.
- after-tests.log: all 95 tests pass, including the 88 existing regressions.
  New cases cover exact source offsets, invented-word/negation rejection, punctuation
  mismatch, duplicate and overlapping ambiguity, scope rejection and full pipeline
  attachment with unchanged call count. The pipeline fixture forbids network use.

No new live API calls or measured model-accuracy, billed-cost, or latency gains.
The old live export remains unchanged. A future categorized failure may identify
the real C4 issue; this experiment alone cannot.

## Demo and next step

Keep the three rules-query runs as honest incomplete-research evidence. Do not keep
repeating that same live task without a specific diagnostic hypothesis and approval.
For the successful demo, prepare a narrow documented-capability task, such as asking
whether Tavily Search supports domain restriction and a maximum result count. This
is a candidate, not an executed or verified-success example. Require actual source
retrieval, clickable supporting passages and clear separation of documented
capability from tested API behavior before calling the demo successful.

GO for continued local development; HOLD for verified-success demo or release.
Main-site extraction, complete deliverable coverage, independent human review and
the actual cause of live C4 remain unresolved. The Mac checkout/server is unchanged.
No fourth run, credentials, persistent access, CI activation, merge, deployment,
public release or submission is authorized or performed by this patch.
