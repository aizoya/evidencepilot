# Offline reviewer scorer

Continues context patch and three explicitly human-confirmed development labels. No live reviewer predictions exist. score_reviewer.py accepts a reference JSON plus a prediction JSON with predictions [{id,status}] and optional execution_class. It does not call providers. Expected labels must not be sent to the model producing predictions.

It reports coverage of submitted cases, missing IDs, accuracy among answered cases separately from all-case correctness, false support, missed support and appropriate abstention. Zero-denominator precision/accuracy remain null. Unknown/duplicate IDs are rejected. Caller execution_class is unverified metadata, not proof of a live run. It does not compute safety-action metrics from a claim-label dataset; serious violations, false action alarms and recoverability remain null. Cost and live latency remain null rather than invented.

Verification: 44/44 synthetic local tests passed, including deliberate wrong approval/rejection, missing predictions and duplicate/unknown IDs. Exact output scorer-patch-tests.txt. These validate scorer behavior, not reviewer accuracy. No new human annotations or hidden test answers generated. First file-write invocation used duplicated relative paths; it failed before applying files and ran unchanged 41-test suite. Paths corrected and full 44-test suite rerun. That initial result is not evidence for this patch.

Usage (after a separately authorized prediction run):
python3 scripts/score_reviewer.py evals/development-calibration-v1.json PATH_TO_PREDICTIONS_JSON

No actual prediction file supplied or created from expected labels. No provider calls, credential reads/transfers, new persistent access, spending, deployment or submission. GO local development; HOLD live reviewer measurement until configured access and applicable approvals. Larger blind independent reference/holdout evaluation remains necessary; these three development cases do not establish reliability.
