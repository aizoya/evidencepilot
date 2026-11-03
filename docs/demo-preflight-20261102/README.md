# Two-case demo preflight — November 2, 2026

Parent review branch: f409876a2a01a65d0bda1457da43f9d107479d38.
This increment changes test tooling and documentation only, not production behavior.

## Verified requirements and source checks

Primary event source: https://hackathon.odsc.ai/ and https://hackathon.odsc.ai/event
The direct reader returned no readable lines. A separate public search index
returned the primary page's requirements: Nebius Token Factory inference, Tavily
web research, public repository/README and short demo. It also returned the 30%
evidence and 25% end-to-end criteria, including inspecting citations and showing
real service calls plus a failure/insufficient-evidence case. Cross-check:
https://luma.com/rccjwcey specifies the November 20 submission date, repository,
README and short demo, with submission link emailed to registrants.

These are independent primary-source checks, not proof that EvidencePilot's Tavily
retrieval reached the governing page. Exact cutoff time/timezone, full legal rules
and demo duration remain unresolved. The 2:45 outline below is an editorial target.

Capability source checked November 2:
https://docs.tavily.com/documentation/api-reference/endpoint/search
The include_domains/include_domains_mode sections describe restriction versus
preference. The max_results section describes a ceiling, with accepted range 0–20.
These establish documented configuration support, not observed API behavior.
Only short paraphrases are retained here; no full page redistribution.

## Case A — live-success CANDIDATE, NOT yet executed

Copy candidate-question.txt into the app only after separate live authorization.

Intended user: a developer checking whether a proposed research API configuration
fits a bounded requirement. This question evaluates provider documentation. It
does not mean EvidencePilot itself sends searches with the proposed settings.

Human acceptance checklist (do not inject expected answers into the runtime):

- Actual Tavily and Token Factory calls recorded within the three-request and
  three-model-call limit; no alternative provider or silent fixture fallback.
- Answer resolves domain restriction and maximum count using retrieved official
  documentation. The documented configuration uses include_domains for the named
  domain, restrict mode, and max_results=5. Prefer mode is not a hard restriction.
- Five is an upper bound, never a promise of five relevant results.
- Two decisive findings have exact retained supporting passages and working
  source links; inspect surrounding scope and qualifiers manually.
- No claim that documentation proves SDK compatibility, live behavior or an
  executed configuration test. Dates/publication uncertainty stays visible.
- Export the actual run even on failure. Report tokens/credits separately from
  reserved amounts and unknown billed cost. Do not retry automatically.

No prompt tuning, retrieval changes or runtime model configuration changes were
made from this checklist. This is a public demo/development case, never a holdout.

## Case B — existing recorded partial/failure evidence

Use original run 13390016-ff9d-48c9-bfec-82e99529bcd6, audited in
docs/failure-diagnostics-20261102/third-live-audit.json. It records 13.39 seconds,
two searches, failed extraction, partial outcome and two reported Tavily credits
against three reserved. Actual billed USD remains unknown. Do not call the exact
extraction cause known; old diagnostics did not retain it.

Keep this run's original export unchanged. Show its incomplete requirements,
source-linked findings, explicit extraction warnings and retained execution events.
Label it RECORDED LIVE RUN; do not imply it is executing again. If the old screen
is still open, record it before refreshing. Otherwise inspect the saved JSON and
its source URLs, explicitly as an export inspection. No replay/import viewer or
historical screenshot has been verified; do not imply one exists.

The three supported participation findings do not make the whole answer complete.
The required-technologies claim lost its citation despite relevant retained text.
This is a known quality failure, not solely a graceful-outage showcase.

## Local rehearsal evidence

Baseline: all 95 previous tests passed. The existing SURFACE-2 Node harness was
extended with an explicit supported-fixture mode; original failure assertions
remain intact. A fictional endpoint and fixed synthetic reviewer judgments feed
the actual backend and renderer. No real provider documentation is impersonated
in the fixture: its URL is example.com and its model is test-only.

before-supported-render.log preserves the initial failure when the failure-only
harness was used for the supported fixture. after-tests.log records all 96 tests
passing. The new case checks two exact visible passages, source-registry links,
noopener/noreferrer, uncertainty wording, correct JSON export and zero research
network requests. Existing SURFACE-2 still checks card/text parity, stale-record
and changed-version rejection, redaction and no external actions.

This is a DOM double. Browser navigation, layout, physical iPhone usability and
live model behavior remain unverified. Test count is not evidence-accuracy proof.

## Modular recording outline (2:45 target)

| Segment | Show | Condition |
|---|---|---|
| 0:00–0:15 | Developer's bounded configuration question | Explain the decision being researched. |
| 0:15–1:00 | One actual Case A run and trace | Only after approval; preserve actual elapsed time if editing waits. |
| 1:00–1:40 | Inspect two decisive passages and source pages | Only call success after manual support checks. |
| 1:40–2:15 | Recorded Case B partial result and failure | Visible recorded-run label; acknowledge missing coverage. |
| 2:15–2:35 | Run IDs, actual usage, unknown USD and architecture | Distinguish observed results from simulations. |
| 2:35–2:45 | Repo/setup command and limitations | Video must match a pinned reviewed commit. |

## Readiness and next gate

GO for local rehearsal and preparation. HOLD for a verified-success recording,
deployment, merge, public release or submission. No new live run, spending, quota
change, credential or external communication occurred. The Mac checkout remains
older until Franklyn updates it. Preserve its existing quota database.

Next gate: authorize one live run of Case A with existing credits only, maximum
three Tavily requests/three model calls, no retry. First check current credit
availability and update the Mac to the verified branch. Do not raise/reset quota
until that specific run is authorized. Do not repeat the failed rules query as a
substitute for the success candidate.
