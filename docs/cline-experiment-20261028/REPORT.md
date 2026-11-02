# EvidencePilot — tool/workflow experiment inspired by the Cline talk
October 28, 2026 Pacific. Selected-slide notes motivate hypotheses only; no speaker benchmark is claimed for this application. Scope: EvidencePilot exclusively.

## Recovery and authority
Continued the PED source already present, backed by EvidencePilot-PED-20261028.zip. No newer source overwritten or regenerated. Prior patch and failed regression logs retained. Source has no Git metadata; branch/remote/commit remain unverified. Work is local and saved, not committed, merged, deployed or production verified.

Fresh presence-only environment checks: NEBIUS_API_KEY, TAVILY_API_KEY, NEBIUS_MODEL absent. Earlier provider balances and Vercel UI access remain historical, not newly confirmed. Approved dedicated keys were created earlier, with Tavily key cap 100 credits/month. Account PAYG was unlimited and available balance is not freshly verified. Development-secret transfer remains pending. No browser access, credentials, signatures, attestations, installs, provider switches, purchases, deployment or communications performed. OS 2.6 governs; no OS 2.7 approval inferred.

## Baseline evidence
48/48 existing local tests passed before edits (baseline-corrected.log). First test command used the workspace root and failed discovery; baseline.log retained and not counted as a test result. Corrected working directory without changing code or criteria.

Isolated transport harness ran three cases three times each: actual application research pipeline and actual provider adapter, with simulated HTTP read errors and fixtures for inference/search. Outbound socket connections blocked. Normal synthetic case completed. Interrupted search response and interrupted review response each raised an uncaught IncompleteRead in all 3 baseline trials. before.json preserves these failures. No live HTTP/API requests occurred.

## Ranked failure categories
Ranking is engineering judgment, not measured incidence.
| Priority | Cause | State |
|---|---|---|
| 1 | Tool/transport error: incomplete HTTP read or reset connection bypasses structured result | Selected and fixed in this experiment |
| 2 | Incorrect reasoning: quote can match while claim scope/negation is wrong | Open; model semantic accuracy unmeasured, human development labels only |
| 3 | Missing context: source truncation, linked exceptions, heuristic headings/tables | Partially addressed previously; still open |
| 4 | Timeouts: per-call 40s guard but no aggregate deadline; slow partial reads | Existing timeout fixtures; total-duration risk remains open |
| 5 | Oversized inputs: bounded request/response/source text but no aggregate tokenizer budget | Existing bounds retained; monetary limits not established by bytes alone |
| 6 | Task drift/omissions: planner proposals can omit user requirements | Partial-result guard retained; actual completeness unmeasured |
| 7 | Repeated loops | Fixed pipeline max three searches/three model calls; zero automatic retries; no consequential action dispatcher |

## One scoped improvement
Only application delta: import http.client.HTTPException and translate HTTPException/ConnectionError through the existing redacted ResearchError handler in post_json. Exact diff in implementation.diff. This covers IncompleteRead, RemoteDisconnected and reset/broken connection errors. No general catch-all, provider swap, prompt tuning, automatic retry, fallback model, new transport library or higher limit.

Search failures remain visible; the three separately planned queries may still be attempted, each once. This is not three retries of one request. If evidence remains absent, result is insufficient_evidence with zero answer claims. A broken review yields failed; draft claims are never promoted. Failed run quota remains reserved. Unknown upstream token/credit use remains unknown, not zero. A provider might charge before the connection breaks.

## Before/after and resulting behavior
| Case | Baseline (3 repeats) | Patched (3 repeats) |
|---|---|---|
| Incomplete search response | 3 uncaught exceptions | 3 structured insufficient_evidence reports |
| Incomplete review response | 3 uncaught exceptions | 3 structured failed reports; no supported drafts |
| Normal fixture | 3 successful reports | 3 successful reports |

The runtime path was also exercised through the in-process WSGI application route, including its auth/configuration gates under synthetic test settings: success returned 200 with evidence_found; interrupted search returned 200 with insufficient_evidence; interrupted review returned 200 with failed. HTTP 200 indicates a readable report, NOT research success. No browser or deployed endpoint was used. WSGI failure-event counts include the terminal render event where applicable; they are not provider-call counts.

Final full regression: 52/52 passed. Added four focused tests: redacted/no-retry interrupted transport (three exception subcases), search failure + quota reservation, reviewer failure, and unrelated programming errors remaining visible. Also passed all 52 tests with outbound connections blocked. Independent read-only reviewer repeated the network-blocked suite and found no material issue. No old assertions, fixtures, grading labels, approval controls or provider permissions changed in this experiment.

Synthetic reports retain requirement outcomes, citation registry, exact quotes, section/window context, uncertainty and tool results from previous patches. Normal synthetic quote support is stipulated by its fixture and prior tests; this experiment does not measure model entailment or actual external source resolution. It validates failure recoverability. Partial response-body canaries are absent from public error strings. No prohibited action tool exists or was executed. No secret value read or exposed.

Actual model task accuracy, supported-claim precision, external citation availability, real provider latency and billed cost remain NOT MEASURED. Local fixture durations are recorded in JSON; they are not service performance. Three repetitions are deterministic stability checks, not noisy model evaluation or a statistically meaningful gain.

## Evaluation independence and holdout
Captured control hashes before edit, including existing tests, eval references, reviewer scorer and web approval gate; after edit all hashes matched. New regression tests verify transport behavior only. Control-check and hashes saved alongside evidence. Independent reviewer had read-only scope and did not modify grades. This is procedural scope separation/change detection, not an OS-level security sandbox against a root-owning coordinator. No self-improvement agent has permission to rewrite these controls. A stronger external enforcement boundary remains necessary before unattended iterative improvement.

The three human-confirmed examples are development-only and unchanged. No true independently custodied holdout is available; no expected holdout answers were accessed, generated, tuned against or graded. Do not advertise a heldout pass rate. No cross-family model evaluation performed.

## Demo and next gate
Prepared cases remain the synthetic successful research and honest failure cases. They can demonstrate local behavior only. Live demonstration must use actual Nebius Token Factory and Tavily, clickable original-source support and clear uncertainty. No new competition claim or rule is inferred from the talk.

GO: scoped local patch is tested and independently reviewed. HOLD: live provider validation, production and submission. Next concrete gate is secure configuration of existing development credentials plus verification of remaining credits and no-overage controls, followed by specific authorization for a bounded live experiment. Do not reopen stopped browser access from this report. Franklyn handles passwords/codes and attestations. No missing approval is treated as granted by a local test result.
