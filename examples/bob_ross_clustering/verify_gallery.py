#!/usr/bin/env python3
"""Optional online checks. Read four remote images; never redistribute them."""
import argparse
import csv
import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

HERE=Path(__file__).resolve().parent
PIN='f8741b2ba36d7b7a6e3fc87cb757ea73c9da6e1f'
SOURCE=f'https://raw.githubusercontent.com/jwilber/Bob_Ross_Paintings/{PIN}/data/bob_ross_paintings.csv'


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'DataCollectionMov-class-demo/1.0 (+https://github.com/jcval94/DataCollectionMov)'}),timeout=20) as response:
        data=response.read(1048577)
        if len(data)>1048576:raise ValueError('Respuesta supera 1 MiB; no se valida un prefijo como archivo completo.')
        meta=dict(requested_url=url,final_url=response.url,http_status=response.status,
                  content_type=response.headers.get('Content-Type'),bytes=len(data),
                  checked_at_utc=datetime.now(timezone.utc).isoformat(timespec='seconds'),
                  sha256=hashlib.sha256(data).hexdigest(),hash_scope='complete_response')
    return data,meta


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'output/gallery.json')
    args=parser.parse_args()
    from PIL import Image
    report=json.loads((HERE/'reference/report.json').read_text())
    data,source_meta=fetch(SOURCE)
    records=list(csv.DictReader(io.StringIO(data.decode('utf-8-sig'))))
    gallery=[]
    for room in report['rooms']:
        medoid=room['medoid'];episode=medoid['episode']
        season,number=int(episode[1:3]),int(episode[4:6])
        matches=[r for r in records if int(r['season'])==season and int(r['episode'])==number]
        if len(matches)!=1:raise ValueError('Cruce no unívoco para '+episode)
        match=matches[0];image_bytes,image_meta=fetch(match['img_src'])
        with Image.open(io.BytesIO(image_bytes)) as image:
            image.load();image_meta.update(status='IMAGE_DECODED',format=image.format,width=image.width,height=image.height)
        gallery.append(dict(room=room['room'],episode=episode,elements_title=medoid['title'],
            palette_title=match['painting_title'],image_url=match['img_src'],
            join_key='season + episode; exactly one palette row for this element episode',
            title_note='Titles preserved independently; Dawn/Down and singular/plural differences are not silently corrected.',
            attribution='Bob Ross; image hosted by Two Inch Brush, linked by jwilber/Bob_Ross_Paintings.',
            rights='Rights of their holders; no open image licence confirmed. Remote link only; image bytes are not saved in this repository.',
            test=image_meta))
    payload=dict(source=source_meta,source_commit=PIN,source_dataset_id='bob-ross-paletas',
                 model_dataset_id='bob-ross-elementos',scope='Illustration of actual representative episodes; images and palettes did not enter the model. No vision verification of every motif.',gallery=gallery)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print('PASS: four unique episode joins and four complete IMAGE_DECODED checks. No image files copied.')


if __name__=='__main__':main()
