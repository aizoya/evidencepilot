# Execution record and release gates

Owner: AIZOYA. Product: EvidencePilot. Governing directive: supplied by Franklyn Rosario. Requested operating standard: AIZOYA OS 2.6 until approved replacement. The full authoritative OS 2.6 document was not available in the project or returned by the scoped searches; this package does not claim full OS 2.6 compliance. Available AIZOYA automation, connection and bootstrap skills informed implementation.

## Verified requirements and architecture decision

Checked October 27, 2026 Pacific Time:

- https://hackathon.odsc.ai/ — dedicated challenge and judging rubric.
- https://luma.com/rccjwcey — organizer listing corroborates the October 28–November 20 build window and email submission-link delivery.
- https://odsc.ai/west/nebius-hackathon/ — conflicting older one-day schedule; do not use for deadline assumptions.
- https://docs.tavily.com/documentation/api-reference/endpoint/search — current direct search endpoint and options.
- https://api.tokenfactory.nebius.com/docs — OpenAI-compatible chat completions endpoint.
- https://dev.nebius.com/cookbook/beam-reflection-token-factory — environment-managed API pattern; model selection still requires actual account verification.
- https://pypi.org/project/gunicorn/26.2.0/ — direct production-server pin. Not an audited transitive lock.

| Option | Advantages | Costs and limits | Decision |
|---|---|---|---|
| Single Python WSGI service, static UI, SQLite quota | Minimal local dependencies; one reproducible process; auditable bounds | Single instance only; no streaming or tenant accounts | Selected for competition prototype |
| React/Next frontend plus separate API/database | Rich UI, customer auth expansion | More deployment, dependency and timeout boundaries | Defer |
| Agent framework and distributed workers | Flexible long-running workflows | More orchestration and less predictable costs | Defer until evidence quality requires it |

The implementation deliberately uses bounded orchestration rather than an autonomous browsing agent. Relevant source selection and factual accuracy are still model-dependent; exact quotes and separate review are safeguards, not proof of truth.

## Current verification

- 22 automated standard-library tests passed locally; fixtures are explicitly test-only.
- JavaScript syntax check passed.
- Narrow source guard and Python syntax checks passed. These are not a full security scan.
- Local HTTP application started and returned health/static/unauthorized responses (see validation record).
- Independent code review identified query URL corruption, malformed provider-field handling, health/auth mismatch, contradiction-label validation and verification-client redirects. Corrections and regression coverage were applied.
- Responsive CSS was implemented. Browser-based mobile QA was attempted, but the runtime lacks the Chromium executable. No screenshot or actual mobile usability claim is supplied.
- Real Nebius/Tavily execution: NOT RUN; credentials absent and no approved provider budget established.
- Production image build, dependency/image scans and production deployment: NOT RUN.
- GitHub: connector read identity verified; exact product searches returned no repository under `bluehac` or `aizoya`. Repository creation tool and authenticated `gh` were unavailable. No remote repository was created or published.
- Product-name exclusivity: NOT established. Other public projects use EvidencePilot. Preserve the requested working name; complete name screening before commercial branding commitments.

## Milestones and acceptance

Dates below are targets, not background automations or completion claims.

| Target (Pacific dates) | Deliverable | Required acceptance evidence |
|---|---|---|
| Oct 28–30 | Authorized providers and real core path | Exact model ID, budget cap, real HTTP report, original-source checks, commit SHA |
| Oct 31–Nov 4 | Evidence-quality baseline | Live evaluation matrix, claim support/coverage, contradiction recall, failure cases |
| Nov 5–10 | Pilot usability and deployment candidate | Actual iPhone flow, auth/origin/limits, locked dependencies, clean scans, rollback plan |
| Nov 11–16 | Authorized deployment and demo | Exact deployed SHA, persisted quotas, health + live acceptance, captioned short recording |
| Nov 17–19 | Reproducibility and submission rehearsal | Fresh clone run, public repo review, README, demo links, organizer instructions rechecked |
| Nov 20 | Owner-authorized submission | Exact cutoff verified; submitted confirmation preserved |

Evidence and end-to-end operation receive priority because they account for 55% of the published rubric. No milestone passes solely on a polished interface or unit fixtures.

## Demo runbook (target 2–3 minutes; organizer length limit unconfirmed)

1. Identify a small-business user deciding which service or requirement applies.
2. Enter a fresh question; record the actual Nebius/Tavily execution on the approved deployed build.
3. Open an important claim's passage and original URL. Explain exact matching versus entailment.
4. Show an uncertainty or conflicting-source example, with dates and scope.
5. Show an actual safe failure/insufficient-evidence run. Label controlled fault injection explicitly.
6. Open trace/usage and repository setup instructions. Keep credentials, account details and private content out of the recording.

No demo video is included yet because recording fixtures as a working product would misrepresent live execution.

## Commercial validation

Initial wedge: repeatable vendor/market/requirements research for small consultancies and entrepreneurs. Test whether source verification reduces decision effort before adding billing. Use AIZOYA synthetic/public research tasks, then obtain consent for external pilots.

Record baseline research time, time to checked answer, material corrections, unsupported-claim rate, question coverage, report usefulness, latency and real provider cost. Evaluate 10–20 representative questions, including held-out failures and contradictory sources. A paid pilot is a hypothesis until customers agree to pay; do not assert willingness to pay or a market size without evidence.

Subscription architecture should later add per-tenant identity/quotas, private evidence storage, deletion/retention, invoice-backed unit costs and billing entitlements. Do not share company data across tenants. Pricing follows measured per-report cost and user value; no subscriptions or paid service commitments are created now.

## Smallest next owner actions

1. Make the authoritative OS 2.6 document available for a gap review.
2. Connect/provision Nebius Token Factory and Tavily credentials through a secret manager or trusted deployment environment, choose the model, and approve the exact development credit/dollar cap. Do not send keys in chat.
3. Enable repository creation for the intended AIZOYA owner, or provide the exact existing repository URL. The directive already requests a public competition repository; do not accidentally publish another project or private data.
4. After live validation and security checks, approve the exact hosting resource, costs, deployment SHA and environment before production deployment. Submission and external commitments remain separately gated.
