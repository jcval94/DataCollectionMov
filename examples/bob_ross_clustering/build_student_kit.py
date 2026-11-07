#!/usr/bin/env python3
"""Export a small student package without the teacher guide or model answers."""
import argparse
from pathlib import Path
import shutil
import tempfile
import zipfile

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'output')
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    archive=args.output/'bob-ross-alumnos.zip'
    allowed=['ALUMNO.md','ATRIBUCION.md','data/elements-by-episode.csv','data/manifest.json']
    # Fresh temporary staging: never delete an existing user-owned export folder.
    with tempfile.TemporaryDirectory(prefix='bob-ross-student-kit-') as temporary:
        target=Path(temporary);(target/'data').mkdir()
        shutil.copyfile(HERE/'ALUMNO.md',target/'ALUMNO.md')
        for name in ['elements-by-episode.csv','manifest.json']:
            shutil.copyfile(HERE/'data'/name,target/'data'/name)
        (target/'ATRIBUCION.md').write_text('Datos: FiveThirtyEight, trabajo sobre Bob Ross de Walt Hickey. CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ .\nFuente y edición: ver data/manifest.json. CSV sin modificaciones; selección de motivos y filtros propuestos en ALUMNO.md. La licencia de datos no cubre pinturas ni vídeos. El Museo Imaginario es un encargo ficticio.\n')
        assert sorted(str(p.relative_to(target)) for p in target.rglob('*') if p.is_file())==sorted(allowed)
        with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as out:
            for name in allowed:out.write(target/name,'bob-ross-alumnos/'+name)
    print(f'Paquete de alumnos: {archive} · cuatro archivos, sin soluciones ni guía docente.')


if __name__=='__main__':main()
