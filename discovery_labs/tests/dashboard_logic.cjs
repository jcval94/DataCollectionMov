/* Tests the real embedded JavaScript with a minimal document adapter.
   This checks filter logic and generated markup, not browser layout or rendering. */
const fs=require('node:fs');const vm=require('node:vm');const path=require('node:path');const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');const html=fs.readFileSync(path.join(root,'dashboard/index.html'),'utf8');
const data=html.match(/<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const script=html.match(/<\/script><script>([\s\S]*?)<\/script>/)[1];
class Element{constructor(){this.value='';this.textContent='';this.innerHTML='';this.hidden=false;this.disabled=false;this.options=[];this.handlers={};this.attrs={}}add(o){this.options.push(o)}addEventListener(n,f){this.handlers[n]=f}setAttribute(k,v){this.attrs[k]=v}click(){if(this.onclick)this.onclick()}}
const ids={};const get=id=>ids[id]??(ids[id]=new Element());get('catalog-data').textContent=data;
const buttons=['library','ranking','pilots','audit'].map(view=>{const b=new Element();b.dataset={view};return b});
const document={getElementById:get,querySelectorAll:()=>buttons,createElement:()=>new Element()};
const context=vm.createContext({document,URL,Blob,Option:class{constructor(text,value){this.text=text;this.value=value}},setTimeout:f=>f()});vm.runInContext(script,context,{timeout:10000});
function input(id,value){get(id).value=value;get(id).handlers[id==='search'?'input':'change']()}
const checks=[];function ok(name,f){f();checks.push(name)}
ok('86_sources_516_questions',()=>assert.match(get('count').textContent,/86 fuentes · 516 preguntas/));
ok('13_categories',()=>assert.equal(get('category').options.length,13));
ok('12_cards_first_page',()=>assert.equal((get('cards').innerHTML.match(/<article class="card">/g)||[]).length,12));
input('viability','pilot');ok('3_technical_pilots_18_designs',()=>assert.match(get('count').textContent,/3 fuentes · 18 preguntas/));
input('viability','ready');ok('0_ready_has_empty_state',()=>{assert.match(get('count').textContent,/0 fuentes/);assert.match(get('cards').innerHTML,/No hay fuentes/)});
input('viability','');input('search','bts');ok('BTS_disambiguated',()=>{assert.match(get('count').textContent,/2 fuentes/);assert.match(get('cards').innerHTML,/bts-kpop-musica/);assert.match(get('cards').innerHTML,/bts-puntualidad-vuelos/)});
input('search','');input('category','Sociedad, desigualdad y demografía');ok('category_filter',()=>assert.match(get('count').textContent,/7 fuentes/));
input('category','');input('technique','Redes');ok('technique_filter',()=>assert(!get('count').textContent.startsWith('0 ')));input('technique','');input('difficulty','Inicial guiado');ok('difficulty_filter',()=>assert(!get('count').textContent.startsWith('0 ')));input('difficulty','');
buttons[1].click();ok('navigation_ranking',()=>{assert.equal(get('ranking').hidden,false);assert.equal(get('library').hidden,true)});
ok('top10_and_13_category_tops',()=>{assert.equal((get('top10').innerHTML.match(/<tr>/g)||[]).length,10);assert.equal((get('categorytops').innerHTML.match(/<tr>/g)||[]).length,13)});
ok('3_embedded_pilot_images',()=>assert.equal((get('pilotcards').innerHTML.match(/data:image\/png;base64,/g)||[]).length,3));
ok('no_remote_scripts_css_images',()=>assert(!/<(?:script|link|img)\b[^>]*(?:src|href)=["']https?:/i.test(html)));
ok('escaped_dataset_payload',()=>assert(!data.includes('</script>')));
const report={status:'PASS',checks,scope:'Lógica JavaScript y marcado con adaptador de documento; NO validación visual ni smoke en navegador.',browser_verification:'Prueba de navegador independiente en tests/dashboard_browser.py; consultar su evidencia de CI.',responsive_css:'Presente; este test no valida renderizado.'};
fs.writeFileSync(path.join(root,'evidence/dashboard_qa.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
