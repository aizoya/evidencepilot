# Submission-date scope regression

Parent review-branch commit: 2c99b2d417c459cccb14cdae715706818a3b3a52.
This is a separate increment after the documentation-absence guard. Prior failures,
artifacts and test expectations remain intact; no holdout was accessed.

## Failure and bounded fix

The first uploaded live report's C3 called an event date range a submission period.
The cited passage gave kickoff/build dates, not submission timing. The previous
audit explicitly retained this error.

One runtime guard now holds recognized submission-timing claims uncertain when
none of their exact cited passages explicitly identifies submission scope. It
does not use arbitrary surrounding page text or source headings to rescue the
claim. It adds no provider calls, retries, actions or permissions.

This is a conservative English lexical necessary-condition check, not a general
date verifier. It can over-abstain if a page relies on headings or uses different
terminology. A passage mentioning submissions can still contain the wrong date,
wrong event, negation or qualifier. The model reviewer and human assessment remain
necessary; this patch does not establish semantic accuracy on unseen questions.

## Evidence

- baseline-tests.log: existing 65 tests pass.
- before-regression.log: six new test methods, four failures before runtime change.
- after-tests.log: all 71 tests pass after change, including existing SURFACE-2
  card/text parity, stale export binding and no-external-action checks.
- development-case.json: minimal C3 development fixture with public-source quote,
  source URL and original artifact hash. Not holdout data.
- saved-run-recheck.json: deterministic offline recheck of saved live judgments.
  C3 changes from supported to uncertain; together with the prior guard, only C1
  and C2 remain supported. This is not a new live run or an accuracy benchmark.

The original live export remains unchanged. No expected answers, grading rules,
approval controls, provider configuration, quota or UI action binding changed.
No new provider requests, spending, deployment, merge or submission occurred.

## Remaining blockers and decision

GO for local development. HOLD for verified-success demo or release.

The search still missed the main rules page and returned unrelated competitions.
No new official-rules verification or independent evaluation is claimed here.
Next scoped task: inspect source selection and retrieve governing pages within
existing budgets, using fixtures first. Do not raise/reset the user's one-run
quota or initiate another live research run without explicit authorization.
