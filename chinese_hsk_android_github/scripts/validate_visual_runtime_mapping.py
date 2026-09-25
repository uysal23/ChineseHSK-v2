#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
CONTENT=ROOT/'app'/'src'/'main'/'assets'/'chinese_course'
chars=json.loads((CONTENT/'characters.json').read_text(encoding='utf-8'))['characters']
bible=json.loads((CONTENT/'media'/'visual_bible.json').read_text(encoding='utf-8'))
core={x['characterId']:x for x in bible['coreCharacters']}
errors=[]
for c in chars:
    if c['id'] not in core: continue
    if not c.get('visualIdentityLocked'): errors.append(c['id']+': visualIdentityLocked missing')
    by=c.get('portraitByLevel',{})
    if set(by) != {'HSK1','HSK2','HSK3','HSK4','HSK5','HSK6'}: errors.append(c['id']+': portraitByLevel incomplete')
    valid=set(c.get('portraitVariants',{}).values())|{c.get('portraitAsset','')}
    for level,path in by.items():
        if path not in valid: errors.append(f'{c["id"]}: {level} maps to unknown asset {path}')
print(f'Visual runtime mapping: {len(core)} core characters, errors={len(errors)}')
for x in errors: print('ERROR:',x)
if errors: sys.exit(1)
