/* Optional DOM regression checks. These do not replace a browser/pixel review. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {JSDOM,VirtualConsole}=require(process.env.JSDOM_MODULE_PATH||'jsdom');
const checked=[],errors=[];
const consoleBridge=new VirtualConsole();
consoleBridge.on('jsdomError',error=>errors.push(error.message));
let copied='',downloaded='',blobCreated=false;
const html=fs.readFileSync(path.join(__dirname,'demo.html'),'utf8');
const dom=new JSDOM(html,{runScripts:'dangerously',url:'https://classroom.example/bob-ross/',virtualConsole:consoleBridge,
 beforeParse(window){
  window.scrollTo=()=>{};
  Object.defineProperty(window.navigator,'clipboard',{value:{writeText:async text=>{copied=text;}}});
  window.URL.createObjectURL=()=>{blobCreated=true;return 'blob:local-test';};
  window.URL.revokeObjectURL=()=>{};
  window.HTMLAnchorElement.prototype.click=function(){downloaded=this.download;};
 }});
const w=dom.window,$=id=>w.document.getElementById(id),click=id=>$(id).click();
function check(name,fn){fn();checked.push(name);}
function select(id,value,event='change'){$(id).value=value;$(id).dispatchEvent(new w.Event(event,{bubbles:true}));}
async function main(){
 check('opening_hides_later_scenes',()=>{assert.equal($('scene-0').hidden,false);assert.equal($('scene-3').hidden,true);assert.equal($('previous').disabled,true);});
 click('next');
 check('six_real_cards_and_twelve_bits',()=>{assert.equal($('cards').children.length,6);assert.equal($('cards').querySelectorAll('.bit').length,72);assert.equal($('cards').querySelector('[data-card-title]').hidden,true);});
 const allocation=$('cards').querySelector('select');allocation.value='2';click('toggle-titles');
 check('title_reveal_preserves_manual_allocation',()=>{assert.equal(allocation.value,'2');assert.equal($('cards').querySelector('[data-card-title]').hidden,false);});
 click('clear-cards');check('clear_manual_allocation',()=>assert.equal(allocation.value,'0'));
 const before=$('distance').textContent;select('pair-b','0');
 check('distance_recalculates_from_real_profiles',()=>{assert.notEqual($('distance').textContent,before);assert.match($('distance').textContent,/0 de 12/);});
 $('criterion').value='Probamos similitud por motivos.';
 click('next');click('copy-prompt');await new Promise(resolve=>setImmediate(resolve));
 check('copy_agent_prompt',()=>{assert.match(copied,/No uses título, ID/);assert.match($('copy-status').textContent,/copiado/);});
 click('next');
 check('four_reference_episodes_and_embedded_chart',()=>{assert.equal($('gallery').children.length,4);assert.equal($('boundary').children.length,4);assert.match($('scene-3').querySelector('.chart').src,/^data:image\/svg\+xml;base64,/);});
 select('room-reader','2');check('centroid_denominator_changes',()=>assert.match($('centroid-reading').textContent,/96 \/ 100/));
 click('next');select('k-select','8','input');
 check('k_control_reads_computed_grid',()=>{assert.equal($('k-value').textContent,'8');assert.match($('k-reading').textContent,/0\.271/);assert.match($('k-reading').textContent,/28 episodios/);});
 check('trap_hidden_before_reveal',()=>assert.equal($('trap').hidden,true));click('reveal-trap');
 check('trap_reveal_and_numbers',()=>{assert.equal($('trap').hidden,false);assert.match($('trap-reading').textContent,/0\.571/);assert.match($('trap-reading').textContent,/0\.010/);});
 click('next');click('download');
 check('empty_decision_has_validation_message',()=>assert.match($('download-status').textContent,/Escribe primero/));
 $('decision').value='Proponemos cuatro salas por motivos; revisaremos las excepciones.';click('download');
 check('decision_download_dom_hook',()=>{assert.equal(downloaded,'decision-bob-ross.txt');assert.equal(blobCreated,true);});
 $('decision').focus();$('decision').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));
 check('arrow_keys_preserve_text_editing',()=>assert.equal($('scene-5').hidden,false));
 w.document.body.dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));
 check('arrow_navigation_works_outside_fields',()=>assert.equal($('scene-4').hidden,false));
 click('restart');
 check('restart_resets_all_exercise_state',()=>{assert.equal($('scene-0').hidden,false);assert.equal($('criterion').value,'');assert.equal($('decision').value,'');assert.equal($('k-select').value,'4');assert.equal($('trap').hidden,true);assert.equal($('room-reader').value,'0');assert.equal($('cards').querySelector('select').value,'0');assert.equal($('cards').querySelector('[data-card-title]').hidden,true);});
 check('no_embedded_javascript_exceptions',()=>assert.deepEqual(errors,[]));
 const result={status:'PASS',scope:'DOM and scripted-state checks in jsdom; no browser pixels, mobile layout, native clipboard or native file download verified.',checks:checked.length,passed:checked,html_sha256:crypto.createHash('sha256').update(html).digest('hex'),node_version:process.version,browser_visual_status:'NOT_TESTED_BY_THIS_DOM_HARNESS',checked_at_utc:new Date().toISOString()};
 const output=process.argv[2]||path.join(__dirname,'output/dom-validation.json');fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({status:result.status,checks:result.checks}));
}
main().catch(error=>{console.error(error.stack);process.exitCode=1;}).finally(()=>dom.window.close());
