#!/usr/bin/env python3
from __future__ import annotations
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT/'app'/'src'/'main'/'assets'/'chinese_course'
MEDIA = CONTENT/'media'
SOURCES = ROOT/'visual_sources'

def dump(path,obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def rel_source_for(target: str) -> str:
    name=pathlib.Path(target).with_suffix('.png').name
    if '/characters/' in target:
        parts=pathlib.PurePosixPath(target).parts
        cid=parts[-2]
        return f'visual_sources/characters/{cid}/{name}'
    return f'visual_sources/backgrounds/{name}'

def main():
    bible=json.loads((MEDIA/'visual_bible.json').read_text(encoding='utf-8'))
    entries=[]
    for ch in bible.get('coreCharacters',[]):
        assets=[('BASE',ch['baseAsset'])]
        assets += [(k,v) for k,v in ch.get('variantMap',{}).items()]
        for variant,target in assets:
            source=rel_source_for(target)
            target_path=ROOT/'app'/'src'/'main'/'assets'/target
            source_path=ROOT/source
            entries.append({
                'assetId': f"{ch['characterId']}__{variant}",
                'kind':'character', 'ownerId':ch['characterId'], 'variant':variant,
                'priority':1 if variant=='BASE' else 2,
                'source':source, 'target':target,
                'promptFile':ch['promptFile'],
                'variantDirective': ('canonical identity master; neutral adult/age-start appearance' if variant=='BASE' else f'preserve the exact canonical face and silhouette; create age-stage variant {variant}; age gradually and naturally, never replace identity'),
                'width':768, 'height':1152,
                'transparent':True,
                'status':'ready' if target_path.exists() else ('source_ready' if source_path.exists() else 'waiting_for_source')
            })
    for loc in bible.get('coreLocations',[]):
        assets=[('DAY',loc['baseAsset'])]
        assets += [(k,v) for k,v in loc.get('variantAssets',{}).items()]
        for variant,target in assets:
            source=rel_source_for(target)
            target_path=ROOT/'app'/'src'/'main'/'assets'/target
            source_path=ROOT/source
            entries.append({
                'assetId': f"{loc['locationId']}__{variant}",
                'kind':'background', 'ownerId':loc['locationId'], 'variant':variant,
                'priority':1 if variant=='DAY' else 3,
                'source':source, 'target':target,
                'promptFile':loc['promptFile'],
                'variantDirective': ({'DAY':'canonical daylight master; lock architecture and camera','NIGHT':'same exact architecture/camera; nighttime practical lighting only','RAIN':'same exact architecture/camera; rainy weather and wet surfaces only','HOLIDAY':'same exact architecture/camera; modest festive/holiday decor only'}[variant]),
                'width':1280, 'height':720,
                'transparent':False,
                'status':'ready' if target_path.exists() else ('source_ready' if source_path.exists() else 'waiting_for_source')
            })
    entries.sort(key=lambda x:(x['priority'],x['kind'],x['ownerId'],x['variant']))
    payload={'schemaVersion':1,'policy':'source_image -> deterministic optimized WebP -> Android assets',
             'sourceRoot':'visual_sources','entries':entries,
             'summary':{
                 'total':len(entries),
                 'ready':sum(x['status']=='ready' for x in entries),
                 'sourceReady':sum(x['status']=='source_ready' for x in entries),
                 'waitingForSource':sum(x['status']=='waiting_for_source' for x in entries),
             }}
    dump(MEDIA/'visual_asset_queue.json',payload)
    status_path=CONTENT/'content_status.json'
    if status_path.exists():
        status=json.loads(status_path.read_text(encoding='utf-8'))
        vp=status.setdefault('visualProduction',{})
        vp.update({'queueAssets':len(entries),'readyAssets':payload['summary']['ready'],'sourceReadyAssets':payload['summary']['sourceReady'],'waitingForSource':payload['summary']['waitingForSource'],'pipeline':'visual_sources -> optimized WebP -> runtime asset'})
        dump(status_path,status)
    SOURCES.mkdir(parents=True,exist_ok=True)
    with (SOURCES/'visual_asset_queue.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['priority','kind','ownerId','variant','status','source','target','promptFile','variantDirective'])
        w.writeheader()
        for x in entries: w.writerow({k:x[k] for k in w.fieldnames})
    print(f"Visual queue: {len(entries)} assets; ready={payload['summary']['ready']}, sourceReady={payload['summary']['sourceReady']}, waiting={payload['summary']['waitingForSource']}")

if __name__=='__main__': main()
