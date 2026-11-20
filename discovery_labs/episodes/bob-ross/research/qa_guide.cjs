/* Static proof only. Never reports browser, mobile or accessibility audit PASS. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const page=fs.readFileSync(path.join(root,'research_guide.html'),'utf8');
const ids=[...page.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
assert.equal(ids.length,new Set(ids).size,'duplicate ids');
assert.equal(page.match(/class="story-arc"/g).length,14);
assert.equal(page.match(/id="preguntas"/g).length,1);
let checkedLinks=0;
for(const [,target] of page.matchAll(/(?:href|src)="([^"]+)"/g)){
  if(target.startsWith('#'))assert.ok(ids.includes(target.slice(1)),target);
  else if(!target.match(/^https?:/))assert.ok(fs.existsSync(path.join(root,target)),target);
  checkedLinks++;
}
for(const [,attributes,code] of page.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)){
  if(!attributes.includes('application/json'))new vm.Script(code);
  else {const data=JSON.parse(code);assert.equal(data.length,381);assert.equal(new Set(data.map(x=>x.id)).size,381);}
}
console.log(JSON.stringify({status:'PASS_STATIC_ONLY',cards:14,local_links_and_anchors:checkedLinks,
  checks:['unique-dom-ids','local-links','one-canonical-index','inline-js-syntax','381-inspector-episodes'],
  browser:'NOT_VALIDATED',mobile:'NOT_VALIDATED',keyboard:'NOT_VALIDATED'},null,2));
