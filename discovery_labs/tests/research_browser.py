"""Observe actual offline galleries in Chromium at projection and mobile sizes."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parents[1]


def main():
    output = BASE/'test-output/v3'; output.mkdir(parents=True, exist_ok=True)
    contracts = json.loads((BASE/'contracts/batch0.json').read_text())
    errors = []; remote = []; checks = []; screenshots = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for case in ['uci-retail','nba-elo','bob-ross-elementos']:
            allowed = [c['id'] for c in contracts if c['source_id']==case and c['execution_status']=='EXECUTABLE']
            blocked = [c['id'] for c in contracts if c['source_id']==case and c['execution_status']=='BLOCKED']
            for variant, viewport in [('projection',dict(width=1440,height=1000)), ('mobile',dict(width=390,height=844))]:
                page = browser.new_page(viewport=viewport, reduced_motion='reduce')
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('request', lambda r: remote.append(r.url) if not r.url.startswith(('file:','data:','blob:')) else None)
                page.goto((BASE/'output/v3'/case/'student/index.html').as_uri())
                assert not page.locator('#evidence').is_visible()
                options = page.locator('option').evaluate_all('(xs)=>xs.map(x=>x.value).filter(Boolean)')
                assert options == allowed
                assert not set(options) & set(blocked)
                assert page.locator('img:not([alt]),img[alt=""]').count()==0
                page.locator('#prediction').fill('Predigo que cambiará la comparación al revisar el denominador.')
                for question in allowed:
                    page.locator('#question').select_option(question)
                    page.get_by_role('button').click()
                    visible = page.locator('article:visible'); assert visible.count()>0
                    for card in visible.all():
                        assert card.locator('img').evaluate('(e)=>e.complete&&e.naturalWidth>0')
                        assert card.locator('img').evaluate('(e)=>e.naturalWidth') == (777 if variant=='mobile' else 1584)
                        assert card.locator('details a').count()==1
                    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                    checks.append(dict(case=case, question=question, variant=variant, decoded_figures=visible.count(), horizontal_overflow=False))
                # Every figure is captured once in each viewport; repeated questions need no duplicate screenshot.
                for card in page.locator('article').all():
                    card.evaluate('(e)=>e.hidden=false')
                for i, card in enumerate(page.locator('article').all()):
                    file=output/f'{case}-{i}-{variant}.png'; card.screenshot(path=str(file)); screenshots.append(str(file.relative_to(BASE)))
                page.close()
        browser.close()
    assert not errors, errors
    assert not remote, remote
    report = dict(status='PASS', browser='Chromium / Playwright 1.56.0', route_viewport_checks=checks,
                  screenshots=screenshots, js_errors=errors, remote_requests=remote,
                  human_class_rehearsal='NOT_OBSERVED', visual_inspection='Screenshots require separate observed review.')
    (output/'browser-qa.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', checks=len(checks), screenshots=len(screenshots))))


if __name__=='__main__':main()
