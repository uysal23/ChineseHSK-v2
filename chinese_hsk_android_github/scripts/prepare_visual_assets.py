#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib
from PIL import Image, ImageOps

ROOT=pathlib.Path(__file__).resolve().parents[1]
ASSETS=ROOT/'app'/'src'/'main'/'assets'
MEDIA=ASSETS/'chinese_course'/'media'
QUEUE=MEDIA/'visual_asset_queue.json'

def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def process_character(im,w,h):
    im=im.convert('RGBA')
    contained=ImageOps.contain(im,(w,h),method=Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(w,h),(0,0,0,0))
    x=(w-contained.width)//2; y=h-contained.height
    canvas.alpha_composite(contained,(x,y))
    return canvas

def process_background(im,w,h):
    im=im.convert('RGB')
    return ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=(0.5,0.5))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--strict-sources',action='store_true',help='fail when queue entries have no source or target')
    args=ap.parse_args()
    q=json.loads(QUEUE.read_text(encoding='utf-8'))
    inventory=[]; missing=[]; built=0; reused=0
    for e in q['entries']:
        src=ROOT/e['source']; dst=ASSETS/e['target']
        if src.exists():
            dst.parent.mkdir(parents=True,exist_ok=True)
            with Image.open(src) as im:
                out=process_character(im,e['width'],e['height']) if e['kind']=='character' else process_background(im,e['width'],e['height'])
                out.save(dst,'WEBP',quality=84,method=6,lossless=False)
            built+=1
        elif dst.exists():
            reused+=1
        else:
            missing.append(e['assetId']); continue
        with Image.open(dst) as im:
            inventory.append({'assetId':e['assetId'],'target':e['target'],'kind':e['kind'],'variant':e['variant'],
                              'width':im.width,'height':im.height,'mode':im.mode,'bytes':dst.stat().st_size,'sha256':sha256(dst)})
    payload={'schemaVersion':1,'builtFromSources':built,'reusedExisting':reused,'missing':missing,'assets':inventory}
    (MEDIA/'visual_binary_inventory.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Prepared visual assets: built={built}, reused={reused}, missing={len(missing)}')
    if args.strict_sources and missing: raise SystemExit('Missing visual assets: '+', '.join(missing[:12]))

if __name__=='__main__': main()
