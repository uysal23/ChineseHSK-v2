#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, pathlib, shutil, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'app' / 'src' / 'main' / 'assets'
MEDIA = ASSETS / 'chinese_course' / 'media'
QUEUE = MEDIA / 'audio_asset_queue.json'


def sha256(path: pathlib.Path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def run_ffmpeg(src: pathlib.Path, dst: pathlib.Path, channels: int, sample_rate: int, bitrate_kbps: int):
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(src),
        '-vn', '-map_metadata', '-1', '-ac', str(channels), '-ar', str(sample_rate),
        '-c:a', 'libopus', '-b:a', f'{bitrate_kbps}k', '-vbr', 'on', '-compression_level', '10',
        str(dst)
    ]
    subprocess.run(cmd, check=True)


def probe(path: pathlib.Path):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
           '-show_entries', 'stream=codec_name,sample_rate,channels:format=duration',
           '-of', 'json', str(path)]
    data = json.loads(subprocess.check_output(cmd, text=True))
    stream = (data.get('streams') or [{}])[0]
    fmt = data.get('format') or {}
    return {
        'codec': stream.get('codec_name', ''),
        'sampleRate': int(stream.get('sample_rate') or 0),
        'channels': int(stream.get('channels') or 0),
        'durationSec': float(fmt.get('duration') or 0.0),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--strict-sources', action='store_true')
    args = ap.parse_args()
    if shutil.which('ffmpeg') is None or shutil.which('ffprobe') is None:
        raise SystemExit('ffmpeg/ffprobe are required to prepare authored audio')
    queue = json.loads(QUEUE.read_text(encoding='utf-8'))
    inventory = []
    missing = []
    built = reused = 0
    for e in queue['entries']:
        src = ROOT / e['source']
        dst = ASSETS / e['target']
        if src.exists():
            run_ffmpeg(src, dst, int(e['channels']), int(e['sampleRate']), int(e['bitrateKbps']))
            built += 1
        elif dst.exists():
            reused += 1
        else:
            missing.append(e['assetId']); continue
        p = probe(dst)
        inventory.append({
            'assetId': e['assetId'], 'kind': e['kind'], 'ownerId': e['ownerId'], 'target': e['target'],
            **p, 'bytes': dst.stat().st_size, 'sha256': sha256(dst)
        })
    payload = {
        'schemaVersion': 1,
        'builtFromSources': built,
        'reusedExisting': reused,
        'missingCount': len(missing),
        'missingSample': missing[:100],
        'assets': inventory,
    }
    (MEDIA / 'audio_binary_inventory.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared audio assets: built={built}, reused={reused}, missing={len(missing)}')
    if args.strict_sources and missing:
        raise SystemExit(f'Missing authored audio assets: {len(missing)}')

if __name__ == '__main__':
    main()
