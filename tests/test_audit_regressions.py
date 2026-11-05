import importlib.util
import json
from datetime import date
from pathlib import Path
from unittest.mock import Mock
import pandas as pd
import pytest
from historico_api import storage
from historico_api.runner import _is_due
from historico_api.sources import google_routes, ecobici, denue

@pytest.fixture
def isolated(tmp_path,monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path

def test_snapshots_hash_metadata_and_no_overwrite(isolated):
    row=storage.save_table(name='x',frame=pd.DataFrame({'route_id':['001'],'_snapshot_id':['stale']}),source='test',snapshot_date=date(2026,11,5),snapshot_id='one',cadence='daily')
    import hashlib
    before=Path(row['current_path']).read_bytes()
    assert row['hash_sha256']==hashlib.sha256(Path(row['snapshot_path']).read_bytes()).hexdigest()
    loaded=storage.read_current_table('x')
    assert loaded['route_id'].iloc[0]=='001' and loaded['_snapshot_id'].iloc[0]=='one'
    with pytest.raises(FileExistsError):storage.save_table(name='x',frame=pd.DataFrame({'x':[99]}),source='test',snapshot_date=date(2026,11,5),snapshot_id='one',cadence='daily')
    assert Path(row['current_path']).read_bytes()==before

def test_artifacts_append_and_update(isolated):
    for name in ['a','b','a']:
        storage.save_artifact(name=name,suffix='txt',content='example',source='test',run_date='2026-11-05',snapshot_id='one')
    obj=json.loads(Path('data/manifests/one_test_artifacts.json').read_text())
    assert sorted(x['artifact'] for x in obj['artifacts'])==['a','b']

@pytest.mark.parametrize('cadence',['hourly_weekdays','every_2_hours_weekdays','daily_weekdays'])
def test_weekdays(cadence):
    assert not _is_due(cadence,date(2026,11,8),{})
    assert _is_due(cadence,date(2026,11,9),{})
    assert _is_due('daily',date(2026,11,8),{})

def test_google_key_empty_fallback(monkeypatch):
    monkeypatch.setenv('MAPS','');monkeypatch.setenv('GOOGLE_MAPS_API_KEY','test-placeholder')
    fake=Mock(side_effect=RuntimeError('stop before request'))
    monkeypatch.setattr(google_routes,'RoutesClient',fake)
    with pytest.raises(RuntimeError):google_routes.run_google_routes('unused')
    fake.assert_called_once_with('test-placeholder')

def test_missing_route_never_low_and_invalid_excluded_from_scale():
    result=google_routes.build_accessibility_score(pd.DataFrame({'duration_minutes':[10,20,99999,None],'delay_minutes':[0,0,0,None],'traffic_delay_pct':[0,0,0,None],'condition':['ROUTE_EXISTS','ROUTE_EXISTS','ROUTE_NOT_FOUND','ROUTE_NOT_FOUND']}))
    assert result.loc[2:,'criticality_score_0_100'].isna().all()
    assert result.loc[2:,'criticality_level'].isna().all()
    assert result.loc[1,'duration_score']==1

@pytest.mark.parametrize('start,end',[('2026-13',None),('2026-1',None),('bad',None),('2026-11','2026-01')])
def test_invalid_months_before_network(monkeypatch,start,end):
    call=Mock();monkeypatch.setattr(ecobici,'discover_historical_csv_links',call)
    with pytest.raises(ValueError):ecobici.run_ecobici_historical('unused',start_month=start,end_month=end)
    call.assert_not_called()

def test_denue_error_does_not_leak_url(monkeypatch):
    import requests
    monkeypatch.setattr(denue.requests,'get',Mock(side_effect=requests.HTTPError('https://example.test/token-placeholder')))
    with pytest.raises(RuntimeError) as exc:denue.denue_get_json('https://example.test/token-placeholder',retries=1)
    assert 'token-placeholder' not in str(exc.value)

def test_existing_discovery_contracts():
    base=Path(__file__).resolve().parents[1]
    spec=importlib.util.spec_from_file_location('retail',base/'scripts/run_discovery.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    assert len(m.self_check())==8
