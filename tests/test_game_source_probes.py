"""Synthetic notation fixtures test parsers; live examples live in source_tests/."""
import hashlib
import importlib.util
import io
from pathlib import Path
from types import SimpleNamespace
import zipfile

import pytest

spec=importlib.util.spec_from_file_location('game_probes',Path(__file__).resolve().parents[1]/'scripts/probe_catalog_sources.py')
probes=importlib.util.module_from_spec(spec)
spec.loader.exec_module(probes)

PGN='[Event "Synthetic test"]\n[Date "2021.01.01"]\n[White "A"]\n[Black "B"]\n[Result "1-0"]\n\n1.e4 e5 2.Nf3 1-0\n\n'
GCG='#player1 A Player A\r\n#player2 B Player B\r\n>A: ABC H8 ABC +10 10\r\n#note This is a synthetic comment, not a scored turn.\r\n>B: DEF 9G DEF +12 12\r\n'

def test_pgn_samples_separate_games_and_preserve_notation():
    rows=probes.pgn_samples(PGN+PGN.replace('[White "A"]','[White "C"]'))
    assert [r['White'] for r in rows]==['A','C']
    assert rows[0]['Result']=='1-0' and '1.e4 e5' in rows[0]['moves_excerpt']

@pytest.mark.parametrize('text',[PGN.replace('[White "A"]',''),PGN.replace('"1-0"','"win"'),PGN.split('\n\n')[0],'<html>Not a game</html>'])
def test_invalid_pgn_is_rejected(text):
    with pytest.raises(ValueError):probes.pgn_samples(text)

def test_gcg_crlf_names_turn_scores_and_annotations():
    rows=probes.gcg_samples(GCG)
    assert rows==[dict(player='Player A',action='ABC H8 ABC',points=10,total=10),dict(player='Player B',action='DEF 9G DEF',points=12,total=12)]

@pytest.mark.parametrize('text',[GCG.replace('#player2 B Player B',''),GCG.replace('>A:', '>C:'),'#player1 A Player A\n#player2 B Player B\n#note No scored turns'])
def test_invalid_gcg_is_rejected(text):
    with pytest.raises(ValueError):probes.gcg_samples(text)

def fake_fetch(monkeypatch,data,content_type):
    monkeypatch.setattr(probes,'fetch',lambda *args: (data,dict(http_status=200,truncated=False,bytes_read=len(data),sha256=hashlib.sha256(data).hexdigest(),hash_scope='complete_response',content_type=content_type)))

def test_html_with_status_200_never_counts_as_game(monkeypatch):
    fake_fetch(monkeypatch,b'<!doctype html><html><title>Portal</title></html>','text/html')
    result=probes.run_check(dict(url='https://example.org/game.gcg',kind='gcg'),SimpleNamespace(timeout=1,max_bytes=8388608))
    assert result['status']=='PARSE_ERROR' and result['sample']==[]

def test_zip_member_is_read_with_a_bounded_prefix(monkeypatch):
    content=(PGN*2+' '*200000).encode()
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('../never-extracted.pgn',content)
    fake_fetch(monkeypatch,stream.getvalue(),'application/zip')
    result=probes.run_check(dict(url='https://example.org/games.zip',kind='pgn_zip'),SimpleNamespace(timeout=1,max_bytes=8388608))
    assert result['status']=='DATA_SAMPLE' and len(result['sample'])==2
    assert result['archive_member']['bytes_read']==65536
    assert result['archive_member']['hash_scope']=='member_prefix'
    assert result['archive_member']['sha256']==hashlib.sha256(content[:65536]).hexdigest()
