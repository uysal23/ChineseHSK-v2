#!/usr/bin/env python3
"""Compile human/authoring blueprints into Android asset scene files.
HSK1–HSK6 are mapped with the same authoring contract; production payloads are layered on top.
"""
import json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
AUTHORING=ROOT/'authoring'
CONTENT=ROOT/'app'/'src'/'main'/'assets'/'chinese_course'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(p,obj): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def compile_level(level):
    src=AUTHORING/f'{level.lower()}_blueprints.json'
    if not src.exists():
        print(f'SKIP {level}: no authoring file')
        return 0
    data=load(src); scenes=data['scenes']; outdir=CONTENT/'levels'/level/'scenes'; story_arc=data.get('storyArc','')
    index=[]
    for bp in scenes:
        p=outdir/f"{bp['id']}.json"
        old=load(p) if p.exists() else {}
        # Single source of truth: authoring content wins when present. Existing compiled
        # payload is only a fallback for older levels that still contain blueprint-only data.
        merged=dict(old)
        merged.update({k:v for k,v in bp.items() if k not in ('dialogues','learning')})
        merged_learning=dict(old.get('learning') or {})
        merged_learning.update(bp.get('learning') or {})
        merged['learning']=merged_learning
        authored_dialogues=bp.get('dialogues') or []
        fallback_dialogues=old.get('dialogues') or []
        merged['dialogues']=authored_dialogues if authored_dialogues else fallback_dialogues
        if len(merged['dialogues']) >= 90 and bp.get('complete') is True:
            merged['complete']=True
            merged['productionStatus']='complete'
            merged.pop('draftDialogueCount',None)
        elif merged['dialogues']:
            merged['complete']=False
            merged['productionStatus']='dialogue_draft'
            merged['draftDialogueCount']=len(merged['dialogues'])
        else:
            merged['dialogues']=[]
            merged['complete']=False
            merged['productionStatus']='blueprint_ready'
        dump(p,merged)
        index.append({k:merged.get(k) for k in ('id','number','titleZh','titleTr','complete','productionStatus')})
    complete=sum(1 for x in index if x['complete'])
    blueprint=sum(1 for x in index if x['productionStatus'] in ('blueprint_ready','dialogue_draft','complete'))
    dump(CONTENT/'levels'/level/'index.json',{
        'level':level,'storyArc': story_arc,
        'blueprintReadyScenes':blueprint,'completeScenes':complete,'scenes':index})
    return blueprint

def main():
    count=0
    for i in range(1,7): count += compile_level(f'HSK{i}')
    manifest=load(CONTENT/'manifest.json')
    for lv in manifest['levels']:
        idx=load(CONTENT/'levels'/lv['id']/'index.json')
        lv['completeScenes']=idx.get('completeScenes',sum(1 for x in idx['scenes'] if x.get('complete')))
        lv['blueprintReadyScenes']=idx.get('blueprintReadyScenes',0)
    dump(CONTENT/'manifest.json',manifest)
    complete=sum(x.get('completeScenes',0) for x in manifest['levels'])
    blueprint=sum(x.get('blueprintReadyScenes',0) for x in manifest['levels'])
    draft_scenes=0
    for lv in manifest['levels']:
        for meta in load(CONTENT/'levels'/lv['id']/'index.json').get('scenes',[]):
            if meta.get('productionStatus') == 'dialogue_draft': draft_scenes += 1
    editorial_review=0
    for i in range(1,7):
        level=f'HSK{i}'
        for meta in load(CONTENT/'levels'/level/'index.json').get('scenes',[]):
            scene=load(CONTENT/'levels'/level/'scenes'/(meta['id']+'.json'))
            if 'requires_native_review' in scene.get('editorialStatus',''):
                editorial_review += 1
    next_level = next((lv['id'] for lv in manifest['levels'] if lv.get('completeScenes',0) < 50), 'COURSE_COMPLETE')
    next_text = ('All 300 scenes are data-complete; proceed to final editorial/native review and release QA.'
                 if next_level == 'COURSE_COMPLETE'
                 else f'Continue full dialogue and learning production for {next_level} while retaining one-package build.')
    dump(CONTENT/'content_status.json',{
        'schemaVersion':2,'course':manifest.get('projectId','CHINESE_HSK_LIFE_JOURNEY_001'),
        'totalLevels':6,'totalSceneSlots':300,'blueprintReadyScenes':blueprint,
        'completeScenes':complete,'dialogueDraftScenes':draft_scenes,
        'editorialReviewRecommendedScenes':editorial_review,
        'nextProductionTarget':next_text,
        'noteTr':f'{blueprint}/300 blueprint hazır; {complete}/300 sahne 90-110 diyalog ve zorunlu öğrenme modülleriyle veri açısından tamdır. Native/editoryal kalite kontrolü ayrı olarak takip edilir.'
    })
    print(f'Compiled {count} blueprint-ready scenes.')
    return 0
if __name__=='__main__': sys.exit(main())
