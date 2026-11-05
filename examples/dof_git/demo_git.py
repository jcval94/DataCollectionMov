#!/usr/bin/env python3
"""Run two real local Git commits in a disposable repository; no remotes."""
import argparse
import json
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path,help='Save the actual execution output as Markdown')
    args=parser.parse_args()
    before=json.loads((HERE/'antes.json').read_text())
    after=json.loads((HERE/'despues.json').read_text())
    assert before['minimo_anual_dias_laborables']==6 and after['minimo_anual_dias_laborables']==12
    assert {k for k in before if before[k]!=after[k]}=={'minimo_anual_dias_laborables'}
    output=[]
    with tempfile.TemporaryDirectory(prefix='dof-git-demo-') as folder:
        def git(*cmd):
            result=subprocess.run(['git','-c','user.name=Demo didáctica','-c','user.email=demo@example.invalid','-c','commit.gpgsign=false',*cmd],cwd=folder,text=True,capture_output=True,check=True)
            return result.stdout.strip()
        git('init','--quiet','--initial-branch=main')
        target=Path(folder)/'articulo_76.json'
        target.write_text((HERE/'antes.json').read_text())
        git('add','articulo_76.json')
        git('commit','--quiet','-m','Representar el mínimo anterior a la reforma de vacaciones')
        target.write_text((HERE/'despues.json').read_text())
        git('add','articulo_76.json')
        git('commit','--quiet','-m','Representar el cambio publicado en DOF el 27-12-2022')
        for cmd in [('log','--oneline','--reverse'),('diff','HEAD~1','HEAD','--','articulo_76.json'),('blame','-L','5,5','--','articulo_76.json')]:
            output += ['$ git '+' '.join(cmd),git(*cmd),'']
        assert git('rev-list','--count','HEAD')=='2'
        assert git('status','--porcelain')==''
        output+=['Comprobación: 2 commits, un único dato modificado y árbol de trabajo limpio.']
    result='\n'.join(output)
    print(result)
    if args.report:
        args.report.write_text('# Ejecución real de la demostración Git\n\nUTC: '+datetime.now(timezone.utc).isoformat(timespec='seconds')+'\n\nRepositorio temporal, eliminado al terminar. Los hashes pertenecen a esta ejecución local.\n\n```text\n'+result+'\n```\n')

if __name__=='__main__':main()
