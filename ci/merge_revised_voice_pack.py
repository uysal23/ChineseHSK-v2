"""Merge audited scene voices into the existing six-level pack without changing layout."""
import argparse, hashlib, json, zipfile
from pathlib import Path

def merge(base_path, revision_path, scene_ids, output_path):
    with zipfile.ZipFile(base_path) as base, zipfile.ZipFile(revision_path) as revision:
        manifest_path = 'chinese_course/media/audio_manifest.json'
        old = json.loads(base.read(manifest_path))
        merged = json.loads(json.dumps(old))
        assert len(old['assets']) == 30000, 'Base must preserve all six levels'
        replacements = {}
        changed = set()
        for scene_id in scene_ids:
            level = scene_id.split('_')[1]
            source = json.loads(revision.read(f'voice-output/{level}/audio_manifest_{level}.json'))
            assert source['language'] in ('zh','zh-CN') and old['language'] in ('zh','zh-CN'), 'Expected Mandarin'
            for field in ('engine','codec','sampleRate','bitrate'):
                assert source[field] == old[field], f'Voice format changed: {field}'
            expected = {f'DLG_{scene_id}_{n:03d}' for n in range(1,101)}
            assert expected <= old['assets'].keys() and expected <= source['assets'].keys()
            for dialogue_id in sorted(expected):
                row = source['metadata'][dialogue_id]
                key = row['audioKey']
                assert source['assets'][dialogue_id].endswith('/'+key+'.opus')
                asset = f'chinese_course/media/audio/generated/{level}/{key}.opus'
                data = revision.read(f'voice-output/{level}/files/{level}/{key}.opus')
                assert len(data) >= 256 and data.startswith(b'OggS') and b'OpusHead' in data[:100]
                if asset in replacements:
                    assert replacements[asset] == data, 'Conflicting audio key'
                replacements[asset] = data
                merged['assets'][dialogue_id] = asset
                merged['metadata'][dialogue_id] = row
                changed.add(dialogue_id)
        untouched = set(old['assets']) - changed
        assert all(merged['assets'][d] == old['assets'][d] and merged['metadata'][d] == old['metadata'][d] for d in untouched)
        untouched_paths = {old['assets'][d] for d in untouched}
        for path in untouched_paths & replacements.keys():
            assert replacements[path] == base.read(path), 'Revision would change shared unrevised audio'
        merged['uniqueAudioCount'] = len(set(merged['assets'].values()))
        for level, counts in merged['levels'].items():
            paths = [v for k,v in merged['assets'].items() if k.startswith(f'DLG_ZH_{level}_')]
            assert len(paths) == 5000
            counts.update(dialogueMappingCount=len(paths), uniqueAudioCount=len(set(paths)))
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as output:
            for name in base.namelist():
                if name == manifest_path or name in replacements:
                    continue
                output.writestr(name, base.read(name))
            for name,data in replacements.items():
                output.writestr(name, data)
            output.writestr(manifest_path, json.dumps(merged,ensure_ascii=False,indent=2)+'\n')
        with zipfile.ZipFile(output_path) as output:
            published = json.loads(output.read(manifest_path))
            assert published == merged
            for path in set(merged['assets'].values()):
                data=output.read(path)
                assert len(data) >= 256 and data.startswith(b'OggS') and b'OpusHead' in data[:100]
            # All unrevised levels/scenes keep byte-identical audio, metadata and mapping.
            for path in untouched_paths:
                assert output.read(path) == base.read(path)
            assert output.read('chinese_course/voice_cast.json') == base.read('chinese_course/voice_cast.json')
        return dict(sceneIds=scene_ids, revisedMappingCount=len(changed), untouchedMappingCount=len(untouched),
                    totalMappingCount=30000, uniqueMappedAudioCount=merged['uniqueAudioCount'],
                    voiceCastBytesPreserved=True, engineAndFormatPreserved=True,
                    allMappedOpusHeaders='PASS', untouchedAudioBytes='PASS',
                    outputSha256=hashlib.sha256(output_path.read_bytes()).hexdigest(),
                    runtimeIntegration='PENDING', listeningQA='PENDING', apkBuildStarted=False)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--base',required=True);parser.add_argument('--revision',required=True)
    parser.add_argument('--scenes',nargs='+',required=True);parser.add_argument('--output',required=True)
    parser.add_argument('--report',required=True)
    args=parser.parse_args()
    report=merge(args.base,args.revision,args.scenes,args.output)
    Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
