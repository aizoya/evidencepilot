# Bounded linked-site discovery

Parent: 8813c6c70a7bf000cf5800480ec7ee39f1b51ded, existing review branch.
This increment addresses a retrieval gap, not the separate semantic-review gaps.

## Baseline and failure

All 71 previous local tests pass. The first saved live run retrieved an event
listing with a main-website link, but none of its seven registered sources came
from the main rules domain. Its third search repeated the broad question with
contrary-evidence wording and returned unrelated competitions.

Two new development regression cases failed before implementation: selecting the
linked domain and making a missed linked domain visible. See before-regression.log.
Four other methods cover fallback, unsafe links, hostile text and targeted failure.
All cases are local fixtures; no held-out expected answers were accessed.

## One scoped change

Reuse the existing final search for a domain-constrained query when prior extracted
source text contains a Markdown link explicitly labelled main/official website/site.
Safe-URL checks and hostname syntax checks apply. Only the hostname enters the
query; paths, tracking parameters, fragments and surrounding source instructions
are discarded. The user's question and contrary-evidence intent remain included.

No direct URL fetching or new action dispatcher is introduced. No extra search,
model call, retry, credential, permission or quota is added. Without a usable link,
the previous contrary search remains unchanged. The trace calls the selected link
an unverified hint. No source is automatically labelled authoritative.

If no extracted page from the hinted domain is retained, a warning prevents a
silent claim of complete research. A domain match alone does not prove the right
page or governing rules were retrieved.

## Verification

- baseline-tests.log: 71 existing tests passed.
- before-regression.log: five initial methods, two failures before implementation.
- after-tests.log: 77 tests passed after implementation and the targeted-timeout
  regression was added. SURFACE-2 export binding and no-action checks still pass.
- saved-run-query-check.json: offline selection from the saved live run's first
  five sources chooses site:hackathon.odsc.ai within the 300-character query cap.
  The original export is unchanged and identified by SHA-256.

Tests forbid socket connections. Hostile instructions cannot expand the fixed
tool sequence; a failed final search remains recorded with no retry. No live API
requests, spending, CI activation, deployment, merge or submission occurred.

## Remaining risks and next gate

This heuristic does not authenticate publishers or validate event identity. An
untrusted listing can point to the wrong public domain; the bounded final search
may then be less useful. Only the first usable hint is selected. Markdown links
are supported; HTML-only navigation is not. Dynamic or inaccessible pages may
still yield no evidence, and extracted content may be incomplete.

GO for local development; HOLD for a verified-success demo or release. The prior
absence and submission-date guards remain intact. Live retrieval quality, accuracy,
latency and cost after this change are not measured.

Next gate: obtain specific authorization for one additional live run within the
unchanged three-search/three-model-call limit, with existing credits only. Do not
reset the user's one-run quota, spend, or silently rerun failed research. The Mac
checkout and running server have not been updated by this remote branch commit.
