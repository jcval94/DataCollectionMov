"""Browser checks for the generated offline dashboard; no external page or session."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
def main():
    errors=[];requests=[];output=ROOT/'test-output';output.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch();page=browser.new_page(viewport={'width':1440,'height':1000})
        page.on('pageerror',lambda error:errors.append(str(error)))
        page.on('request',lambda request:requests.append(request.url))
        page.goto((ROOT/'dashboard/index.html').as_uri());page.wait_for_selector('.card')
        assert '86 fuentes' in page.locator('#count').inner_text()
        page.locator('#viability').select_option('pilot');assert '3 fuentes' in page.locator('#count').inner_text()
        page.screenshot(path=str(output/'dashboard-desktop.png'))
        page.locator('#viability').select_option('ready');assert '0 fuentes' in page.locator('#count').inner_text();assert page.locator('.empty').is_visible()
        page.locator('#viability').select_option('');page.locator('#search').fill('bts');assert '2 fuentes' in page.locator('#count').inner_text()
        page.locator('#search').fill('');page.locator('#category').select_option('Sociedad, desigualdad y demografía');assert '7 fuentes' in page.locator('#count').inner_text()
        page.locator('#category').select_option('');page.locator('#technique').select_option('Redes');assert not page.locator('#count').inner_text().startswith('0 ')
        page.locator('#technique').select_option('');page.locator('#difficulty').select_option('Inicial guiado');assert not page.locator('#count').inner_text().startswith('0 ')
        page.locator('#difficulty').select_option('')
        with page.expect_download() as info:page.locator('#download').click()
        downloaded=info.value;downloaded.save_as(output/'filtered.json');assert len(json.loads((output/'filtered.json').read_text()))==516
        page.get_by_role('button',name='Priorizar producción').click();assert page.locator('#top10 tr').count()==10;assert page.locator('#categorytops tr').count()==13
        page.get_by_role('button',name='Probar los pilotos').click();assert page.locator('#pilotcards article').count()==3
        page.locator('#pilotcards summary').first.click();assert page.locator('#pilotcards img').first.is_visible()
        for image in page.locator('#pilotcards img').all():assert image.evaluate('(el)=>el.complete&&el.naturalWidth>0')
        page.get_by_role('button',name='Explorar fuentes').click();page.set_viewport_size({'width':390,'height':844})
        page.screenshot(path=str(output/'dashboard-mobile.png'));assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert not errors,errors;assert all(url.startswith(('file:','data:','blob:')) for url in requests),requests
        browser.close()
    report={'status':'PASS','scope':'Navegador real Chromium mediante Playwright 1.56.0 en CI; escritorio y móvil.','checks':['86_sources','3_technical_pilots','0_ready_empty_state','BTS_disambiguation','category_filter','technique_filter','difficulty_filter','filtered_export_516','top10','13_category_tops','3_pilot_images_decoded','mobile_no_horizontal_overflow','zero_js_errors','no_remote_requests'],'js_errors':errors,'desktop':'1440x1000','mobile':'390x844','human_45min_rehearsal':'PENDIENTE'}
    (output/'browser-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
