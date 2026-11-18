"""Real offline gallery checks, independent of scientific/visual approval."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE=Path(__file__).resolve().parents[1]


def main(case):
    folder=BASE/'output/v3'/case;output=BASE/'test-output/fieldlab'/case;output.mkdir(parents=True,exist_ok=True)
    figures=json.loads((folder/'visualization/figures.json').read_text());contracts=json.loads((folder/'research/contracts.json').read_text())
    allowed=[c['id'] for c in contracts if c['execution_status']=='EXECUTABLE'];errors=[];remote=[];checks=[];screenshots=[]
    with sync_playwright() as p:
        browser=p.chromium.launch()
        for variant,viewport in [('projection',dict(width=1440,height=1000)),('mobile',dict(width=390,height=844))]:
            page=browser.new_page(viewport=viewport,reduced_motion='reduce')
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.on('request',lambda r:remote.append(r.url) if not r.url.startswith(('file:','data:','blob:')) else None)
            page.goto((folder/'student/index.html').as_uri());assert not page.locator('#evidence').is_visible()
            assert page.locator('option').evaluate_all('(xs)=>xs.map(x=>x.value).filter(Boolean)')==allowed
            assert page.locator('img:not([alt]),img[alt=""]').count()==0
            page.locator('#prediction').fill('Predigo una diferencia; comprobaré el denominador y la selección.')
            for question in allowed:
                page.locator('#question').select_option(question);page.get_by_role('button').click()
                cards=page.locator('article:visible');assert cards.count()>0
                assert cards.count()==sum(question in f['question_ids'] for f in figures)
                for card in cards.all():assert card.locator('img').evaluate('(e)=>e.complete&&e.naturalWidth>0')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                checks.append(dict(question=question,variant=variant,visible_figures=cards.count(),overflow=False))
            for i,card in enumerate(page.locator('article').all()):
                card.evaluate('(e)=>e.hidden=false');expected=next(v['width'] for v in figures[i]['variants'] if v['variant']==variant)
                assert card.locator('img').evaluate('(e)=>e.naturalWidth')==expected
                path=output/f'{figures[i]["id"]}-{variant}-browser.png';card.screenshot(path=str(path));screenshots.append(str(path.relative_to(BASE)))
                assert (folder/'student'/card.locator('details a').get_attribute('href')).is_file()
            page.close()
        browser.close()
    assert not errors,errors
    assert not remote,remote
    report=dict(status='PASS',case=case,browser='Chromium / Playwright 1.56.0',route_viewport_checks=checks,screenshots=screenshots,
        js_errors=errors,remote_requests=remote,scope='Browser checks only; visual inspection and human teaching review are separate.')
    (output/'browser-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(case=case,status='PASS',route_viewport_checks=len(checks),screenshots=len(screenshots))))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--case',required=True,choices=['nasa-exoplanetas','nyc-ratas']);main(p.parse_args().case)
