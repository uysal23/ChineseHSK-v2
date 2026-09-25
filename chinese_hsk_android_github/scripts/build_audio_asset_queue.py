#!/usr/bin/env python3
from __future__ import annotations
import csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'app' / 'src' / 'main' / 'assets' / 'chinese_course'
MEDIA = CONTENT / 'media'
SOURCE_ROOT = ROOT / 'audio_sources'


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    entries = []
    char_root = load(CONTENT / 'characters.json')
    voice_by_name = {c.get('nameZh',''): c.get('voiceProfileId','') for c in char_root.get('characters', [])}
    # Dialogue and narrator entries are derived from the canonical compiled scenes.
    for level in range(1, 7):
        scene_dir = CONTENT / 'levels' / f'HSK{level}' / 'scenes'
        for scene_path in sorted(scene_dir.glob('*.json')):
            scene = load(scene_path)
            sid = scene['id']
            narrator = ((scene.get('production') or {}).get('narrator') or {})
            if narrator.get('zh'):
                entries.append({
                    'assetId': f'NARRATOR:{sid}',
                    'kind': 'narrator',
                    'ownerId': sid,
                    'voiceProfileId': narrator.get('profileId', 'NARRATOR_ZH_001'),
                    'source': f'audio_sources/narrator/{sid}.wav',
                    'target': f'chinese_course/media/audio/narrator/{sid}.opus',
                    'channels': 1,
                    'sampleRate': 24000,
                    'bitrateKbps': 48,
                    'requiredForRelease': False,
                })
            for d in scene.get('dialogues', []):
                did = d['id']
                entries.append({
                    'assetId': did,
                    'kind': 'dialogue',
                    'ownerId': sid,
                    'speaker': d.get('speaker', ''),
                    'voiceProfileId': voice_by_name.get(d.get('speaker', ''), ''),
                    'source': f'audio_sources/dialogues/{did}.wav',
                    'target': f'chinese_course/media/audio/dialogues/{did}.opus',
                    'channels': 1,
                    'sampleRate': 24000,
                    'bitrateKbps': 48,
                    'requiredForRelease': False,
                })

    # One reusable ambience per location. These remain optional: missing audio is silent.
    locations = load(CONTENT / 'locations.json').get('locations', [])
    for loc in locations:
        lid = loc['id']
        entries.append({
            'assetId': f'AMBIENCE:{lid}',
            'kind': 'ambience',
            'ownerId': lid,
            'source': f'audio_sources/ambience/{lid}.wav',
            'target': f'chinese_course/media/ambience/{lid}.opus',
            'channels': 2,
            'sampleRate': 48000,
            'bitrateKbps': 64,
            'requiredForRelease': False,
        })

    # Optional one music bed per scene, intentionally not required for an offline functional build.
    for level in range(1, 7):
        scene_dir = CONTENT / 'levels' / f'HSK{level}' / 'scenes'
        for scene_path in sorted(scene_dir.glob('*.json')):
            sid = load(scene_path)['id']
            entries.append({
                'assetId': f'MUSIC:{sid}',
                'kind': 'music',
                'ownerId': sid,
                'source': f'audio_sources/music/{sid}.wav',
                'target': f'chinese_course/media/music/{sid}.opus',
                'channels': 2,
                'sampleRate': 48000,
                'bitrateKbps': 96,
                'requiredForRelease': False,
            })

    kind_order = {'dialogue': 1, 'narrator': 2, 'ambience': 3, 'music': 4}
    entries.sort(key=lambda e: (kind_order.get(e['kind'], 99), e['assetId']))
    payload = {
        'schemaVersion': 1,
        'policy': 'authored_opus_then_offline_tts_for_speech; silence_when_optional_soundscape_missing',
        'entries': entries,
        'counts': {k: sum(1 for e in entries if e['kind'] == k) for k in kind_order},
    }
    MEDIA.mkdir(parents=True, exist_ok=True)
    (MEDIA / 'audio_asset_queue.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    status_path = CONTENT / 'content_status.json'
    if status_path.exists():
        status = load(status_path)
        status['audioProductionQueue'] = {**payload['counts'], 'total': len(entries), 'authoredBinaryPolicy': 'optional_for_personal_build'}
        status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    csv_path = ROOT / 'audio_sources' / 'audio_asset_queue.csv'
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    cols = ['kind','assetId','ownerId','speaker','voiceProfileId','source','target','channels','sampleRate','bitrateKbps','requiredForRelease']
    with csv_path.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader(); w.writerows(entries)
    print('Audio queue:', len(entries), payload['counts'])

if __name__ == '__main__':
    main()
