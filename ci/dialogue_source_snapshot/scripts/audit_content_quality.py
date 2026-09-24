#!/usr/bin/env python3
import json, pathlib, statistics
ROOT=pathlib.Path(__file__).resolve().parents[1]
CONTENT=ROOT/'app'/'src'/'main'/'assets'/'chinese_course'

def load(p): return json.loads(p.read_text(encoding='utf-8'))

def main():
    rows=[]; errors=[]
    for level_no in range(1,7):
        level=f'HSK{level_no}'
        idx=load(CONTENT/'levels'/level/'index.json')
        for meta in idx['scenes']:
            s=load(CONTENT/'levels'/level/'scenes'/(meta['id']+'.json'))
            if not s.get('complete'): continue
            ds=s.get('dialogues',[])
            unique=len({d.get('zh','') for d in ds})
            cards=len((s.get('learning') or {}).get('vocabularyCards') or [])
            rows.append((s['id'],len(ds),unique,cards,s.get('editorialStatus','')))
            if unique < 35: errors.append(f"{s['id']}: very low dialogue diversity ({unique}/100 unique)")
            if cards < 6: errors.append(f"{s['id']}: fewer than 6 vocabulary cards")
    print('Quality audit (complete scenes only)')
    print('Scenes:',len(rows))
    if rows:
        print('Dialogues:',sum(r[1] for r in rows))
        print('Unique-ZH per scene: min=%d avg=%.1f max=%d' % (min(r[2] for r in rows),statistics.mean(r[2] for r in rows),max(r[2] for r in rows)))
        print('Vocabulary cards:',sum(r[3] for r in rows))
        print('Native/editorial review flagged:',sum('requires_native_review' in r[4] for r in rows))
    if errors:
        print('\nAUDIT WARNINGS:')
        for e in errors: print(' -',e)
        return 1
    print('Audit thresholds passed. Editorial/native review flags remain intentionally visible.')
    return 0
if __name__=='__main__': raise SystemExit(main())
