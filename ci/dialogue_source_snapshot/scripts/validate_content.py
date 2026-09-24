#!/usr/bin/env python3
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / "app" / "src" / "main" / "assets" / "chinese_course"
AUTHORING = ROOT / "authoring"

def load(path):
    with path.open(encoding="utf-8") as f: return json.load(f)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--strict',action='store_true',help='Require all 300 scenes complete with 90-110 dialogues')
    args=ap.parse_args()
    errors=[]; warnings=[]; scene_ids=set(); dlg_ids=set(); total=0; complete=0; blueprint_ready=0
    manifest=load(CONTENT/'manifest.json')
    expected=[f'HSK{i}' for i in range(1,7)]
    actual=[x['id'] for x in manifest['levels']]
    if actual!=expected: errors.append(f'Level order mismatch: {actual}')

    loc_ids=set()
    locfile=CONTENT/'locations.json'
    locations=[]
    if locfile.exists():
        locations=load(locfile).get('locations',[])
        loc_ids={x['id'] for x in locations}

    charfile=CONTENT/'characters.json'
    characters=load(charfile).get('characters',[]) if charfile.exists() else []
    char_names={x.get('nameZh') for x in characters if x.get('nameZh')}
    voicefile=CONTENT/'voices.json'
    voices=load(voicefile).get('voices',[]) if voicefile.exists() else []
    voice_ids={x.get('id') for x in voices if x.get('id')}
    media_visual=CONTENT/'media'/'visual_manifest.json'
    media_audio=CONTENT/'media'/'audio_manifest.json'
    if not characters: errors.append('Missing or empty characters.json media catalog')
    if not locations: errors.append('Missing or empty locations.json media catalog')
    if not voices: errors.append('Missing or empty voices.json media catalog')
    if not media_visual.exists(): errors.append('Missing media/visual_manifest.json')
    if not media_audio.exists(): errors.append('Missing media/audio_manifest.json')
    for c in characters:
        if not c.get('portraitAsset'): errors.append(f"Character {c.get('id')} missing portraitAsset")
        if not c.get('voiceProfileId'): errors.append(f"Character {c.get('id')} missing voiceProfileId")
        elif c.get('voiceProfileId') not in voice_ids: errors.append(f"Character {c.get('id')} references unknown voice {c.get('voiceProfileId')}")
    for loc in locations:
        for key in ('theme','icon','backgroundAsset'):
            if not loc.get(key): errors.append(f"Location {loc.get('id')} missing {key}")

    required_blueprint=('miniAdventureTr','learning','locationId','story','productionStatus')
    for level in expected:
        idxp=CONTENT/'levels'/level/'index.json'
        if not idxp.exists(): errors.append(f'Missing {idxp}'); continue
        idx=load(idxp); scenes=idx.get('scenes',[])
        if len(scenes)!=50: errors.append(f'{level}: expected 50 index entries, got {len(scenes)}')
        for meta in scenes:
            total+=1; sid=meta['id']
            if sid in scene_ids: errors.append(f'Duplicate scene id: {sid}')
            scene_ids.add(sid)
            p=CONTENT/'levels'/level/'scenes'/(sid+'.json')
            if not p.exists(): errors.append(f'Missing scene file: {p}'); continue
            s=load(p)
            if s.get('id')!=sid: errors.append(f'Scene ID mismatch in {p}')
            if s.get('level')!=level: errors.append(f'Wrong level in {sid}')
            status=s.get('productionStatus','planned')
            if status in ('blueprint_ready','dialogue_draft','complete'):
                blueprint_ready += 1
                for key in required_blueprint:
                    if key not in s: errors.append(f'{sid}: blueprint missing {key}')
                if s.get('locationId') and loc_ids and s['locationId'] not in loc_ids:
                    errors.append(f"{sid}: unknown locationId {s['locationId']}")
                production=s.get('production') or {}
                for speaker_name in production.get('characters',[]):
                    if char_names and speaker_name not in char_names:
                        errors.append(f"{sid}: production character missing from character catalog: {speaker_name}")
                learning=s.get('learning',{})
                for key in ('communicationGoals','vocabularyTheme','grammarTheme','pronunciationTheme'):
                    if not learning.get(key): errors.append(f'{sid}: learning missing {key}')
            dialogues=s.get('dialogues',[])
            is_complete=bool(s.get('complete'))
            if is_complete:
                complete+=1
                if not (90<=len(dialogues)<=110): errors.append(f'{sid}: complete scene has {len(dialogues)} dialogues')
                learning=s.get('learning',{})
                cards=learning.get('vocabularyCards') or []
                exercises=learning.get('sentenceExercises') or []
                rules=learning.get('examRules') or {}
                if not cards: errors.append(f'{sid}: complete scene missing vocabularyCards')
                if not exercises: errors.append(f'{sid}: complete scene missing sentenceExercises')
                if not learning.get('comprehensionQuestions'): errors.append(f'{sid}: complete scene missing comprehensionQuestions')
                if not learning.get('pronunciationItems'): errors.append(f'{sid}: complete scene missing pronunciationItems')
                if not learning.get('interactiveDialogue'): errors.append(f'{sid}: complete scene missing interactiveDialogue')
                if not s.get('production'): errors.append(f'{sid}: complete scene missing production data')
                exercise_types={x.get('type') for x in exercises}
                for needed in ('word_order','fill_blank','sentence_repair'):
                    if needed not in exercise_types: errors.append(f'{sid}: complete scene missing exercise type {needed}')
                if rules.get('vocabularyPassPercent') != 90:
                    errors.append(f'{sid}: vocabularyPassPercent must be 90')
                if rules.get('sentencePassPercent') != 85:
                    errors.append(f'{sid}: sentencePassPercent must be 85')
                if rules.get('lockNextSceneUntilPassed') is not True:
                    errors.append(f'{sid}: next scene must stay locked until both exams pass')
                for c in cards:
                    for key in ('id','zh','pinyin','tr'):
                        if not c.get(key): errors.append(f'{sid}: vocabulary card missing {key}')
                for ex in exercises:
                    if not ex.get('id') or not ex.get('type'):
                        errors.append(f'{sid}: sentence exercise missing id/type')
            elif dialogues and not (90<=len(dialogues)<=110):
                warnings.append(f'{sid}: draft has {len(dialogues)} dialogues (target 90-110)')
            for d in dialogues:
                did=d.get('id')
                if not did: errors.append(f'{sid}: dialogue without id'); continue
                if did in dlg_ids: errors.append(f'Duplicate dialogue id: {did}')
                dlg_ids.add(did)
                for key in ('speaker','zh','pinyin','tr'):
                    if not d.get(key): errors.append(f'{did}: missing {key}')
            story=s.get('story') or {}
            nxt=story.get('nextSceneId'); prev=story.get('previousSceneId')
            if nxt and nxt not in scene_ids and level=='HSK6' and sid=='ZH_HSK6_SC050': pass
            # full cross-reference validation is done after collection below

    # Second pass for navigation links after all scene IDs are known.
    for level in expected:
        for meta in load(CONTENT/'levels'/level/'index.json').get('scenes',[]):
            s=load(CONTENT/'levels'/level/'scenes'/(meta['id']+'.json'))
            story=s.get('story') or {}
            for key in ('previousSceneId','nextSceneId'):
                ref=story.get(key)
                if ref and ref not in scene_ids: errors.append(f"{s['id']}: broken {key} -> {ref}")

    if total!=300: errors.append(f'Expected 300 indexed scenes, got {total}')
    if args.strict and complete!=300: errors.append(f'Strict mode: expected 300 complete scenes, got {complete}')
    print(f'Levels: {len(expected)}')
    print(f'Indexed scenes: {total}/300')
    print(f'Blueprint-ready scenes: {blueprint_ready}/300')
    print(f'Complete scenes: {complete}/300')
    print(f'Dialogue IDs checked: {len(dlg_ids)}')
    print(f'Character/role profiles: {len(characters)}')
    print(f'Location profiles: {len(locations)}')
    print(f'Voice profiles: {len(voices)}')
    if warnings:
        print('\nWARNINGS:'); [print(' -',w) for w in warnings]
    if errors:
        print('\nERRORS:'); [print(' -',e) for e in errors]; return 1
    print('\nValidation passed.'); return 0
if __name__=='__main__': sys.exit(main())
