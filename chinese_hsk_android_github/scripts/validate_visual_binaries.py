#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[1]
ASSETS=ROOT/'app'/'src'/'main'/'assets'
MEDIA=ASSETS/'chinese_course'/'media'
q=json.loads((MEDIA/'visual_asset_queue.json').read_text(encoding='utf-8'))
errors=[]; present=0
seen=set()
for e in q['entries']:
    if e['assetId'] in seen: errors.append('duplicate queue assetId '+e['assetId'])
    seen.add(e['assetId'])
    dst=ASSETS/e['target']
    if not dst.exists(): continue
    present+=1
    try:
        with Image.open(dst) as im:
            if im.format!='WEBP': errors.append(f"{e['assetId']}: not WEBP")
            if (im.width,im.height)!=(e['width'],e['height']): errors.append(f"{e['assetId']}: {im.width}x{im.height}, expected {e['width']}x{e['height']}")
            if e['kind']=='character' and 'A' not in im.getbands(): errors.append(f"{e['assetId']}: character missing alpha channel")
    except Exception as ex: errors.append(f"{e['assetId']}: unreadable image: {ex}")
print(f'Visual binary validation: present={present}/{len(q["entries"])}, errors={len(errors)}')
for x in errors[:50]: print('ERROR:',x)
if errors: sys.exit(1)
