"""Actual rendering and offline voting for the registered graph case."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE=Path(__file__).resolve().parents[1]
CASE='openflights-red-aerea'


def main():
    folder=BASE/'output/v3'/CASE;output=BASE/'test-output/batch1a';output.mkdir(parents=True,exist_ok=True)
    figures=json.loads((folder/'visualization/figures.json').read_text())
    contracts=json.loads((folder/'research/contracts.json').read_text())
    allowed=[c['id'] for c in contracts if c['execution_status']=='EXECUTABLE']
    errors=[];remote=[];checks=[];screenshots=[]
    with sync_playwright() as p:
        browser=p.chromium.launch()
        for variant,viewport in [('projection',dict(width=1440,height=1000)),('mobile',dict(width=390,height=844))]:
            page=browser.new_page(viewport=viewport,reduced_motion='reduce')
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.on('request',lambda request:remote.append(request.url) if not request.url.startswith(('file:','data:','blob:')) else None)
            page.goto((folder/'student/index.html').as_uri())
            assert not page.locator('#evidence').is_visible()
            options=page.locator('option').evaluate_all('(items)=>items.map(i=>i.value).filter(Boolean)')
            assert options==allowed and 'D16-A' not in options
            assert page.locator('img:not([alt]),img[alt=""]').count()==0
            page.locator('#prediction').fill('Predigo que el grado no será una definición suficiente de importancia.')
            for question in allowed:
                page.locator('#question').select_option(question);page.get_by_role('button').click()
                cards=page.locator('article:visible');assert cards.count()>0
                for card in cards.all():assert card.locator('img').evaluate('(e)=>e.complete&&e.naturalWidth>0')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                checks.append(dict(question=question,variant=variant,visible_figures=cards.count(),overflow=False))
            for i,card in enumerate(page.locator('article').all()):
                card.evaluate('(e)=>e.hidden=false')
                expected=next(v['width'] for v in figures[i]['variants'] if v['variant']==variant)
                assert card.locator('img').evaluate('(e)=>e.naturalWidth')==expected
                file=output/f'{figures[i]["id"]}-{variant}-browser.png';card.screenshot(path=str(file));screenshots.append(str(file.relative_to(BASE)))
                link=card.locator('details a').get_attribute('href')
                assert (folder/'student'/link).is_file()
            page.close()
        browser.close()
    assert not errors,errors
    assert not remote,remote
    report=dict(status='PASS',browser='Chromium / pinned Playwright 1.56.0',route_viewport_checks=checks,
        screenshots=screenshots,js_errors=errors,remote_requests=remote,all_classroom_approvals=False,
        scope='Browser checks only; figures require separate observed inspection linked to hashes.')
    (output/'browser-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',route_viewport_checks=len(checks),screenshots=len(screenshots))))


if __name__=='__main__':main()
