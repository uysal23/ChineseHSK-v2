#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
MEDIA=ROOT/'app'/'src'/'main'/'assets'/'chinese_course'/'media'

def load(p, default):
    try: return json.loads(p.read_text(encoding='utf-8'))
    except Exception: return default

vqueue=load(MEDIA/'visual_asset_queue.json',{'entries':[]})
vinv=load(MEDIA/'visual_binary_inventory.json',{'assets':[]})
aqueue=load(MEDIA/'audio_asset_queue.json',{'entries':[]})
ainv=load(MEDIA/'audio_binary_inventory.json',{'assets':[]})

vcounts={}
for e in vqueue.get('entries',[]): vcounts[e['kind']]=vcounts.get(e['kind'],0)+1
vpresent={}
for e in vinv.get('assets',[]): vpresent[e['kind']]=vpresent.get(e['kind'],0)+1
acounts={}
for e in aqueue.get('entries',[]): acounts[e['kind']]=acounts.get(e['kind'],0)+1
apresent={}
for e in ainv.get('assets',[]): apresent[e['kind']]=apresent.get(e['kind'],0)+1

payload={
 'schemaVersion':1,
 'visual':{'planned':vcounts,'present':vpresent,'fallback':'compose_stage'},
 'audio':{'planned':acounts,'present':apresent,'speechFallback':'offline_android_mandarin_tts','soundscapeFallback':'silent'},
 'personalBuildReadyWithoutAuthoredMedia': True,
 'commercialMediaReviewRequired': True,
}
(MEDIA/'media_readiness.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
lines=['MEDIA READINESS REPORT','======================','']
lines.append('VISUAL')
for k in sorted(set(vcounts)|set(vpresent)): lines.append(f'- {k}: {vpresent.get(k,0)}/{vcounts.get(k,0)} authored binaries')
lines += ['', 'AUDIO']
for k in sorted(set(acounts)|set(apresent)): lines.append(f'- {k}: {apresent.get(k,0)}/{acounts.get(k,0)} authored binaries')
lines += ['', 'Fallbacks:', '- Visual: Compose scene fallback', '- Dialogue/Narrator: offline Android Mandarin TTS', '- Ambience/Music: silent when missing', '', 'Personal APK build can run without authored media binaries.']
(ROOT/'MEDIA_READINESS_REPORT_v1.5.0.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('\n'.join(lines))
