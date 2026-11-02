# Replace index search with bounded extraction of a known linked page

Parent: 4ae78c5dbdc740631ebcd3eb23cee5a79cc4ee5a on the existing review branch.
No OS promotion, provider switch, quota change, deployment or submission.

## Verified baseline and observed gap

The user's Mac fast-forwarded to 4ae78c5 and passed 77 tests. Its second live run,
12c33e89-48c1-4cf4-880d-405e46129d76, recorded 23.64 seconds, three Tavily credits,
and three Nebius calls (23,324 input / 1,491 output tokens). These are export
records, not a checked invoice. Dollar cost remains unknown.

The third search targeted hackathon.odsc.ai and returned zero results. The warning
and partial outcome remained visible; C8 stayed uncertain under the absence guard.
All seven retained source hashes and nine quote offsets matched. Governing-page
access was not established. R3 findings did not prove complete deliverable coverage;
the review reason for C1 overstated open-to-everyone wording as unrestricted.
See second-live-audit.json. Original uploaded files remain unchanged.

## Diagnosis versus hypothesis

Known: search returned no result despite a source containing a main-site URL.
Unknown: indexing, query specificity, blocking, rendering or another cause.
Hypothesis: basic extraction of the exact known URL may reach content that search
did not return. No live extraction or measured accuracy improvement is claimed.

Primary reference checked: https://docs.tavily.com/documentation/api-reference/endpoint/extract
documents POST /extract, successful results and per-URL failures even under HTTP 200.
https://docs.tavily.com/documentation/api-credits documents basic-extraction credit
consumption and failed-extraction treatment. The integration uses the existing
stdlib HTTP transport, credentials and provider, with no SDK installation.

## Scoped implementation

- For a safely parsed, explicitly labelled main/official website link, replace the
  final Tavily search with one basic extraction of one URL. Do not add a call.
- Preserve the exact path/query identity after existing safe-URL normalization.
- Explicit basic depth, provider timeout 10 seconds, no images or favicon, usage
  reporting enabled. Existing transport timeout/size bounds remain.
- Reserve one credit for the extraction attempt, including uncertain transport
  failure. Returned usage stays separate from reservation; missing usage is unknown.
- Require one nonempty result for the requested URL. Reject per-URL failures,
  malformed results, empty content and changed URLs without exposing provider error
  payloads. No advanced fallback, alternate URL, automatic retry or fourth request.
- Runs remain bounded to three total Tavily requests and three model calls.
  Without a usable link, normal search behavior remains. Search-only test providers
  retain the prior domain-query path. The real provider has an extraction adapter.
- Trace records extract returned/failed separately. UI describes Tavily requests
  rather than claiming all calls are searches. Source credibility stays unrated.

## Test evidence

baseline-tests.log: all 77 existing tests passed.
before-regression.log: seven new development methods exposed absent adapter and
workflow behavior (two failures and seven subcase errors); retained unchanged.
after-tests.log: all 84 tests passed, including the existing SURFACE-2 parity,
stale export binding, no-action and transport regressions. Fixtures cover endpoint
payload/usage, exact URL identity, request count, empty/HTTP-200 failures, unexpected
URLs, unsafe targets and transport failures without retries. Socket use is forbidden
in the synthetic end-to-end cases. No holdout expected answers or grading/approval
controls were changed.

offline-target-check.json selects the saved run's linked URL without making a
request. This is query/target inspection, not a new live run or measured benchmark.

## Risks, decision and next gate

GO for local development; HOLD for live-success demonstration or release.

Basic extraction can still fail on dynamic/blocked pages. Existing retained-content
limits can truncate relevant information. Exact response-URL matching can reject
legitimate redirects/canonicalization; this intentionally remains a visible failure.
An untrusted link is not proof of publisher authority, event identity or approval.
Application URL checks do not prove Tavily-side DNS/redirect/SSRF behavior. Content
remains untrusted, with no external-write dispatcher. General entailment, complete
requirement coverage and eligibility interpretation remain unresolved risks.

No API calls, purchases, credentials, persistent access, CI activation, merge,
deployment or submission were made by this patch. Your running Mac server is still
the previous version. Its two-run quota is unchanged. Any third live run needs
specific authorization and a current credit check; do not reset or silently raise
the quota. Preserve all failed runs regardless of the next outcome.
