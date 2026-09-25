#!/usr/bin/env python3
from __future__ import annotations
import json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
CONTENT=ROOT/'app'/'src'/'main'/'assets'/'chinese_course'
MEDIA=CONTENT/'media'
errors=[]; warnings=[]
def load(p): return json.loads(p.read_text(encoding='utf-8'))
b=load(MEDIA/'visual_bible.json')
vm=load(MEDIA/'visual_manifest.json')
seen=set()
for c in b['coreCharacters']:
    if c['characterId'] in seen: errors.append('duplicate visual character '+c['characterId'])
    seen.add(c['characterId'])
    pf=CONTENT/c['promptFile'].replace('chinese_course/','')
    if not pf.exists(): errors.append('missing prompt '+str(pf))
    asset=CONTENT/c['baseAsset'].replace('chinese_course/','')
    if not asset.exists(): warnings.append('binary missing '+c['baseAsset'])
for l in b['coreLocations']:
    if l['locationId'] in seen: errors.append('duplicate visual id '+l['locationId'])
    seen.add(l['locationId'])
    pf=CONTENT/l['promptFile'].replace('chinese_course/','')
    if not pf.exists(): errors.append('missing prompt '+str(pf))
    asset=CONTENT/l['baseAsset'].replace('chinese_course/','')
    if not asset.exists(): warnings.append('binary missing '+l['baseAsset'])
print(f"Visual asset validation: {len(b['coreCharacters'])} core characters, {len(b['coreLocations'])} core locations")
print(f"Binary media missing (expected until generated): {len(warnings)}")
if errors:
    print('\n'.join('ERROR: '+x for x in errors)); sys.exit(1)
