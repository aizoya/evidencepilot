'use strict';
// A DOM double, not a browser/layout/user test. External effects throw.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const report = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const nodes = new Map(), downloads = [], requests = [], blobs = [];
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.listeners = {}; this.value = ''; this.hidden = false; this._text = ''; }
  set textContent(t) { this._text = String(t); this.children = []; }
  get textContent() { return this._text + this.children.map(x => x.textContent).join('\n'); }
  append(...xs) { this.children.push(...xs); }
  replaceChildren(...xs) { this._text = ''; this.children = xs; }
  addEventListener(name, fn) { this.listeners[name] = fn; }
  click() { if (this.tag === 'a') downloads.push({name:this.download, href:this.href}); else if (this.onclick) return this.onclick(); }
}
const context = vm.createContext({console, Blob, URL:{createObjectURL:blob=>{blobs.push(blob);return 'blob:local-test';}, revokeObjectURL:()=>{}},
  document:{getElementById:id=>{if (!nodes.has(id)) nodes.set(id,new Element('div')); return nodes.get(id);}, createElement:t=>new Element(t)},
  fetch:(url)=>{requests.push(url); if(url!=='/health') throw Error('Unexpected external/research action'); return Promise.resolve({json:async()=>({research_ready:false})});}});
vm.runInContext(fs.readFileSync('evidencepilot/static/app.js','utf8'),context);
context.input = report;
vm.runInContext('render(input)',context);
if (process.argv[3] === 'supported') {
  // Same actual renderer and DOM double; not browser navigation or layout proof.
  assert.equal(report.model, 'test-only');
  assert.equal(report.status, 'evidence_found');
  assert.equal(nodes.get('failure-card').hidden, true);
  assert.equal(nodes.get('failure-presentation').hidden, true);
  assert.equal(nodes.get('rich-report').hidden, false);
  assert.ok(nodes.get('conflicts').textContent.includes('This does not prove the sources agree.'));
  const descendants = node => [node, ...node.children.flatMap(descendants)];
  const rendered = descendants(nodes.get('claims'));
  const links = rendered.filter(n => n.tag === 'a');
  const quotes = rendered.filter(n => n.tag === 'blockquote');
  const evidence = report.claims.flatMap(c => c.evidence);
  assert.equal(quotes.length, evidence.length);
  assert.equal(links.length, evidence.length);
  report.claims.forEach(c => assert.ok(nodes.get('claims').textContent.includes(c.text)));
  evidence.forEach((e, i) => {
    assert.equal(quotes[i].textContent, e.quote);
    assert.equal(links[i].href, report.sources.find(s => s.id === e.source_id).url);
    assert.equal(links[i].target, '_blank');
    assert.equal(links[i].rel, 'noopener noreferrer');
  });
  nodes.get('download').onclick();
  assert.equal(downloads.length, 1);
  assert.equal(downloads[0].name, `evidencepilot-${report.run_id}.json`);
  blobs[0].text().then(raw => {
    assert.deepEqual(JSON.parse(raw), report);
    assert.equal(requests.filter(url => url !== '/health').length, 0);
    console.log('SUPPORTED FIXTURE: exact quotes, resolved source links, uncertainty language and bound export passed; DOM double only, no live providers or navigation.');
  }).catch(error => {console.error(error); process.exitCode = 1;});
} else {
assert.ok(nodes.get('failure-card'), 'Missing failed-search evidence card');
assert.ok(nodes.get('plain-report'), 'Missing plain-text failure mode');
const card = nodes.get('failure-card').textContent;
const text = nodes.get('plain-report').textContent;
for (const value of ['Search failed — no verified answer', 'No usable source material was retrieved.',
  'The answer remains unknown.', 'Check provider availability and remaining quota before starting a new research run.',
  'No automatic retry or external action is authorized.']) {
  assert.ok(card.includes(value), 'Card missing: '+value);
  assert.ok(text.includes(value), 'Text missing: '+value);
}
assert.equal(nodes.get('failure-card').hidden,false);
nodes.get('report-mode').value='plain'; nodes.get('report-mode').listeners.change();
assert.equal(nodes.get('rich-report').hidden,true);
assert.equal(nodes.get('plain-report').hidden,false);
nodes.get('report-mode').value='cards'; nodes.get('report-mode').listeners.change();
assert.equal(nodes.get('rich-report').hidden,false);
const safe = JSON.parse(nodes.get('trace').textContent);
assert.equal(safe.execution_events.filter(e=>e.actual_tool_result==='failed').length,3);
assert.ok(text.includes(JSON.stringify(safe,null,2)), 'Both modes must retain the same safe trace');
assert.ok(!text.includes(report.question));
assert.ok(!text.includes('official pricing'));
const exportOld = nodes.get('download').onclick;
exportOld(); assert.equal(downloads.length,1);
context.changed = {...report, run_id:'different-record'};
vm.runInContext('render(changed)',context);
exportOld(); assert.equal(downloads.length,1,'Stale record action must be rejected');
context.changed = {...report, warnings:[...report.warnings,'changed result under same ID']};
vm.runInContext('render(changed)',context);
exportOld(); assert.equal(downloads.length,1,'Changed result version must be rejected');
context.changed = {...report, question:'PRIVATE-CANARY', trace:[{query:'PRIVATE-CANARY'}],
  execution_events:report.execution_events.map(e=>({...e, query:'PRIVATE-CANARY', proposed_action:'send_email', final_outcome:'PRIVATE-CANARY'}))};
vm.runInContext('render(changed)',context);
assert.ok(!nodes.get('plain-report').textContent.includes('PRIVATE-CANARY'));
assert.ok(!nodes.get('trace').textContent.includes('send_email'));
assert.equal(requests.filter(x=>x!=='/health').length,0);
assert.equal(downloads.length,1);
blobs[0].text().then(raw => {
assert.deepEqual(JSON.parse(raw), report, 'Export bytes must match the bound original report');
assert.equal(blobs[0].type,'application/json');
assert.equal(downloads[0].name,`evidencepilot-${report.run_id}.json`);
if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify({
  classification:'Local execution of actual renderer with a DOM double; synthetic provider fixture, not live API or browser layout evidence',
  card_text:card, plain_text:text, safe_trace:safe,
  permitted_action:'Inspect failure details; check availability/quota before a separately initiated run. Export this local result only.',
  successful_local_exports:downloads.length, unexpected_network_requests:requests.filter(x=>x!=='/health').length,
  stale_record_export:'rejected', changed_result_version_export:'rejected', export_bytes_and_filename:'matched bound original record'
},null,2));
console.log('SURFACE-2: parity, safe trace, no answer, same next step, mode switching, stale-record/version rejection, redaction, and zero external actions passed (DOM double).');
}).catch(error=>{console.error(error);process.exitCode=1;});
}
