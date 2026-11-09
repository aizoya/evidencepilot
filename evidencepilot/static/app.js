'use strict';
let currentReport;
const $ = id => document.getElementById(id);
function el(tag, content, cls) { const n = document.createElement(tag); if (content !== undefined) n.textContent = content; if (cls) n.className = cls; return n; }
function failedSearchSurface(r) {
  if (r.status !== 'insufficient_evidence' || r.claims.length || r.sources.length || !(r.execution_events || []).some(e => e.actual_tool_result === 'failed')) return null;
  const actions = ['plan', 'search', 'synthesis', 'evidence_review', 'render_report'];
  const results = ['returned', 'failed', 'insufficient_evidence', 'partial'];
  const outcomes = ['received; downstream validation required', 'no result accepted; no retry', 'insufficient_evidence', 'failed', 'partial'];
  const safeTrace = {execution_events:(r.execution_events || []).map((e, index) => ({
    sequence:index + 1,
    proposed_action:actions.includes(e.proposed_action) ? e.proposed_action : 'unrecognized',
    applicable_approval:'Research-only gate; no external writes authorized.',
    actual_tool_result:results.includes(e.actual_tool_result) ? e.actual_tool_result : 'unknown',
    final_outcome:outcomes.includes(e.final_outcome) ? e.final_outcome : 'unknown'
  }))};
  return {title:'Search failed — no verified answer', error:'No usable source material was retrieved.',
    uncertainty:'The answer remains unknown.',
    nextStep:'Check provider availability and remaining quota before starting a new research run. No automatic retry or external action is authorized.',
    trace:safeTrace};
}
function selectReportMode() {
  const plain = !$('failure-presentation').hidden && $('report-mode').value === 'plain';
  $('rich-report').hidden = plain; $('plain-report').hidden = !plain;
}
function exportBoundReport(r) {
  // Exact local result snapshot + fixed JSON action parameters; never server authority.
  const snapshot = JSON.stringify(r), record = r.run_id, schema = r.schema_version;
  return () => {
    if (!currentReport || currentReport.run_id !== record || currentReport.schema_version !== schema || JSON.stringify(currentReport) !== snapshot) {
      $('status').textContent = 'This result changed. Refresh the report before exporting.'; return false;
    }
    const blob = new Blob([snapshot], {type:'application/json'}); const url = URL.createObjectURL(blob);
    const a = el('a'); a.href = url; a.download = `evidencepilot-${record}.json`; a.click(); URL.revokeObjectURL(url);
    return true;
  };
}
function passage(e, parent, sources) {
  parent.append(el('blockquote', e.quote));
  if (e.context) {const d = el('details'); d.append(el('summary', 'Inspect source context'), el('p', e.section_heading || 'Section heading unavailable', 'fine')); if (e.table_header && e.table_header.length) d.append(el('pre', e.table_header.join('\n'))); d.append(el('pre', e.context), el('p', e.context_basis, 'fine')); parent.append(d);}
  const s = sources.find(s => s.id === e.source_id);
  if (s) { const a = el('a', `${s.id} · ${s.title || s.url}`); a.href = s.url; a.target = '_blank'; a.rel = 'noopener noreferrer'; parent.append(a); }
}
function render(r) {
  currentReport = JSON.parse(JSON.stringify(r)); r = currentReport;
  $('download').onclick = exportBoundReport(r);
  $('report').hidden = false; $('report-title').textContent = r.question;
  const count = r.claims.filter(c => c.status === 'supported').length;
  $('overview').textContent = `${r.status.replaceAll('_', ' ')} · ${count} of ${r.claims.length} claims passed evidence checks · ${r.sources.length} sources · ${r.elapsed_seconds}s`;
  for (const id of ['warnings', 'claims', 'conflicts', 'sources', 'requirements']) $(id).replaceChildren();
  (r.requirement_outcomes || []).forEach(item => {const box = el('article', undefined, 'claim'); box.append(el('span', item.state.replaceAll('_', ' '), 'badge'), el('h4', `${item.id} · ${item.text}`), el('p', item.claim_ids.length ? `Related findings: ${item.claim_ids.join(', ')}` : 'No mapped supporting findings. More evidence is needed.', 'reason')); const linked = el('details'); linked.append(el('summary', 'Linked request text'), el('p', `Planner interpretation · ${item.text_link_status || 'missing'} · interpretation not reviewed`, 'fine')); (item.user_spans || []).forEach(span => linked.append(el('blockquote', span.quote))); if (item.declared_span_count) linked.append(el('p', `${item.unresolved_span_count} of ${item.declared_span_count} supplied request spans unresolved`, 'fine')); if (item.limitation) linked.append(el('p', item.limitation, 'fine')); box.append(linked); $('requirements').append(box);});
  r.warnings.forEach(w => $('warnings').append(el('p', w, 'warning')));
  r.claims.forEach(c => {const box = el('article', undefined, 'claim'); box.append(el('span', c.status, `badge ${c.status}`), el('h4', c.text), el('p', c.reason, 'reason')); c.evidence.forEach(e => passage(e, box, r.sources)); $('claims').append(box);});
  if (!r.claims.length) $('claims').append(el('p', 'No factual findings are available.'));
  if (!r.contradictions.length) $('conflicts').append(el('p', 'No validated opposing passage pair was identified. This does not prove the sources agree.'));
  r.contradictions.forEach(c => {const box = el('article', undefined, 'conflict'); box.append(el('p', c.description)); c.passages.forEach(e => passage(e, box, r.sources)); $('conflicts').append(box);});
  r.sources.forEach(s => {const box = el('article', undefined, 'source'); const a = el('a', `${s.id} · ${s.title || s.url}`); a.href = s.url; a.target = '_blank'; a.rel = 'noopener noreferrer'; box.append(a, el('p', `${s.content_type} · Retrieved ${s.retrieved_at} · Published ${s.published_at || 'unknown'}`, 'fine'), el('p', s.credibility, 'fine')); const d = el('details'); d.append(el('summary', 'Inspect retained source text'), el('pre', s.content)); box.append(d); $('sources').append(box);});
  $('trace').textContent = JSON.stringify({run_id:r.run_id, model:r.model, trace:r.trace, execution_events:r.execution_events, usage:r.usage, cost:r.cost, limits:r.limits, verification:r.verification}, null, 2);
  const failure = failedSearchSurface(r);
  $('failure-presentation').hidden = !failure; $('failure-card').hidden = !failure;
  $('failure-card').replaceChildren(); $('plain-report').textContent = '';
  if (failure) {
    $('overview').textContent = failure.title;
    $('failure-card').append(el('h3', failure.title), el('p', failure.error), el('p', failure.uncertainty), el('p', failure.nextStep));
    $('trace').textContent = JSON.stringify(failure.trace, null, 2);
    $('plain-report').textContent = [failure.title, failure.error, failure.uncertainty, failure.nextStep, 'Safe execution trace:', $('trace').textContent].join('\n\n');
  }
  selectReportMode();
}
$('report-mode').addEventListener('change', selectReportMode);
$('research').addEventListener('submit', async event => {
  event.preventDefault(); $('submit').disabled = true; $('report').hidden = true; currentReport = null;
  $('status').textContent = 'Planning searches, retrieving sources, and checking evidence. This may take several minutes.';
  try {const response = await fetch('/api/research', {method:'POST', headers:{'Content-Type':'application/json', 'Authorization':`Bearer ${$('access').value}`}, body:JSON.stringify({question:$('question').value})}); const data = await response.json(); if (!response.ok) throw new Error(data.error || 'Research failed.'); render(data); $('status').textContent = failedSearchSurface(data) ? 'Search failed. No verified answer is available. Review the failure details below.' : data.status === 'failed' ? 'Research did not finish. Review the failure details below.' : 'Research finished. Review the evidence and uncertainty below.';
  } catch (error) {$('status').textContent = error.message || 'Connection failed. No report is available. Please check before retrying; a disconnected request may still consume quota.';} finally {$('submit').disabled = false;}
});
fetch('/health').then(r=>r.json()).then(h=>{$('status').textContent = h.research_ready ? 'Research is available. Enter your question to begin.' : 'Research is not enabled. The administrator must configure providers and authorize usage.';}).catch(()=>{$('status').textContent='Unable to check research availability.';});
