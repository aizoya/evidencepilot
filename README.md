# AIZOYA EvidencePilot

EvidencePilot researches business questions through Nebius Token Factory and Tavily, then presents claim-level passages, uncertainty, conflicting evidence and an inspectable research trace.

**Status: research prototype.** [Browse the exact source, tests, and setup](https://github.com/aizoya/evidencepilot/tree/efe375b79411273571062604e587f5b4afd5ab0e). The default branch contains this overview; use the pinned source above to run the app.

**November 20, 2026 (Pacific) live test:** EvidencePilot made three Tavily searches and three Nebius Token Factory calls on the pinned source. The result was **Partial**. It found documentation for hard domain filtering but did not adequately cite the five-result limit or support its wildcard claim. The run researched documented behavior; it did not test the domain filter itself. All 96 offline tests passed separately.

**Demo:** [Watch the archival recap](https://youtu.be/Q9jBLcrc28Q) of three earlier partial runs. It does not show the November 20 run. A complete live success and ODSC starter-template provenance remain unverified; no contest submission is claimed.

Unit fixtures never serve application answers. No default model or credentials are assumed.

## Run locally

Start from the pinned source link above, not the default branch. Requires Python 3.12+. The local app and tests use only the standard library.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_source.py
python3 -m evidencepilot.web
```

Open http://127.0.0.1:8000. The interface loads without keys; research returns an explicit unavailable state. The development server listens only on localhost and is not a production server.

Inject `NEBIUS_API_KEY`, `TAVILY_API_KEY`, `NEBIUS_MODEL`, and a cryptographically random `APP_ACCESS_TOKEN` of at least 24 characters through a secret manager or your shell environment. `.env.example` lists settings; this application does **not** automatically load `.env`. Never paste credentials into chat, source, reports or Git. Choose a JSON-capable text model available in your Nebius account, record its exact ID, and evaluate it before release.

Set `ENABLE_LIVE_RESEARCH=true` only after the owner approves the exact provider accounts, credit/dollar budget and environment. Defaults: 10 runs per UTC day, 3 basic Tavily searches and 3 model calls per run; 2,200 output tokens per model call. No automatic retries. Failed or disconnected runs keep their quota reservation. Returned usage may be missing and is never treated as zero cost. This caps requests, **not dollar spend**; use provider hard spend/credit caps before enabling usage. No inference call is made on `/health`.

For the local browser, `APP_ORIGIN=http://127.0.0.1:8000`. Enter the research access code in the interface; it is kept only in the current page's memory. Do not enter provider API keys in the UI. For remote access require HTTPS and the exact deployed origin.

## Research design

1. Nebius plans at most two complementary searches.
2. Tavily retrieves up to four results per query. A third bounded search looks for contrary evidence and limitations.
3. Code rejects unsafe link schemes and local IP links, deduplicates exact URLs and identical retained text, and bounds source content to 6,000 characters per source.
4. Nebius proposes up to eight claims with exact supporting passages.
5. Code requires a real source ID and an exact quote match. Invented citations cannot pass.
6. A separate Nebius review call checks entailment, dates, scope, credibility and contradictions. It sees all retained evidence, not only the proposed quote.
7. The UI labels supported, uncertain, unsupported and contradicted claims separately. Contradictions need exact passages from two distinct sources. Empty results never become an answer.

The reviewer is a separate pass using the same model/provider, not a guarantee of independence or truth. Deterministic quote presence does not prove entailment. Source independence, authority, freshness and contradiction recall remain evaluation tasks. Tavily excerpts are labeled separately from extracted page text. A truncated excerpt may omit decisive context. No arbitrary source URL is fetched by the server; source links open in the user's browser.

No model output can execute code, choose arbitrary network destinations, write files, access credentials or invoke additional tools. Source and question content stay inside an untrusted JSON field; system instructions are separate. These boundaries reduce prompt-injection impact, but semantic manipulation remains possible and needs live adversarial evaluation.

## Inspect and preserve evidence

Every report includes source URLs, retrieval/publication timestamps (unknown when absent), retained text SHA-256, model ID, bounded search trace, usage and uncertainty. Export evidence JSON from the interface; it may contain research content and should be handled privately.

For the authorized synthetic acceptance question:

```bash
python3 scripts/verify_live.py
```

Start the server first and provide the same access-token environment to this script. It calls the real HTTP endpoint, saves the report and hash manifest under ignored `evidence/private/`, and exits nonzero if both providers and supported findings are absent. A real failed run is preserved as failed evidence. Inspect original citations manually and retain the exact code commit SHA. This script has **not** been run successfully here because credentials and usage authorization are absent.

Run the cases in `docs/evaluations.json`; record actual results without rewriting expected outcomes as observed evidence.

## Deploy preparation

A non-root Dockerfile and Gunicorn config are provided. Do not deploy yet. `requirements-production.txt` pins the direct server package, but transitive dependencies and base-image digest are not locked. Before deployment, resolve/hash all dependencies, pin the image digest, generate an SBOM, run secret/history, static, dependency and image scans, build the image, and fix findings.

Use one service instance and one Gunicorn worker with the persistent SQLite volume at `/data`. The concurrency lock is process-local. Multiple workers/replicas or ephemeral quota storage invalidate the controls. Add a reverse proxy with HTTPS, request/header/body timeouts and request-rate limits; disable request-body/header capture and sensitive tracing. Set platform request timeouts to at least 300 seconds; no automatic POST retry. Distributed public scale requires a central quota service and real tenant authentication.

Verify `/health`, missing/invalid access, origin checks, successful real research, provider failure, empty evidence, citation links, quota exhaustion, persistent quota across restart and mobile navigation on the exact deployment SHA. Keep rollback instructions and proof. No production deployment or hosting costs are authorized by this package.

## Competition

Official dedicated page: https://hackathon.odsc.ai/ (checked October 27, 2026 PT). Kickoff October 28; submissions close November 20, 2026. See the [official submission form](https://hackathon.odsc.ai/submit) for the stated 8:59 p.m. Pacific cutoff and repository instructions. Older ODSC pages conflict with the dedicated page; recheck organizer announcements before submission.

Required: real Nebius Token Factory inference, Tavily live search, public repository with README, short demo. Judging weights: sourced/verifiable 30%, end-to-end 25%, usefulness 20%, agent design 15%, integrations 10%. These are planning inputs, not a claim of eligibility, registration or submission. See `docs/EXECUTION.md` for the evidence and release gates.

## Data and commercial scope

Initial target: entrepreneurs and small consultancies checking vendor claims, market options and business requirements. AIZOYA is the initial evaluator; no company data or special internal dependency is required. No accounts, payments or subscription entitlements are implemented. Do not market this prototype as a multi-tenant subscription service. Add tenant isolation, secure auth, retention/deletion controls, abuse limits and billing only after the research-quality baseline is measured.

The server retains quota counts only. Questions and source content go to Nebius and Tavily; reports remain in browser memory until exported. Provider retention/terms need review before customer use. No analytics or session replay is enabled. Operational traces remain in returned report data, not telemetry.
