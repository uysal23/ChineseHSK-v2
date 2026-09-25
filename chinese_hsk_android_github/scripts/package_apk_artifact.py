#!/usr/bin/env python3
from pathlib import Path
import hashlib
import shutil
import sys

if len(sys.argv) < 3:
    raise SystemExit('Usage: package_apk_artifact.py <apk> <dist-dir> [variant]')

apk = Path(sys.argv[1])
dist = Path(sys.argv[2])
variant = sys.argv[3] if len(sys.argv) > 3 else 'personal'
if not apk.exists():
    raise SystemExit(f'APK not found: {apk}')

version = Path('VERSION').read_text(encoding='utf-8').strip()
dist.mkdir(parents=True, exist_ok=True)
out = dist / f'ChineseHSK-v{version}-{variant}.apk'
shutil.copy2(apk, out)
sha = hashlib.sha256(out.read_bytes()).hexdigest()
(dist / f'{out.name}.sha256.txt').write_text(f'{sha}  {out.name}\n', encoding='utf-8')

reports = [
    Path('VALIDATION_REPORT.txt'),
    Path(f'VALIDATION_REPORT_v{version}.txt'),
    Path('MEDIA_READINESS_REPORT_v1.6.0.txt'),
]
for report in reports:
    if report.exists():
        shutil.copy2(report, dist / report.name)

summary = [
    f'Chinese HSK Journey v{version}',
    f'APK: {out.name}',
    f'Variant: {variant}',
    f'SHA-256: {sha}',
    '',
    'Kurs: HSK1-HSK6 / 300 sahne / offline-first',
    'Not: debug APK kişisel test içindir. Sabit güncelleme imzası için GitHub signing secrets kullanılır.',
]
(dist / 'BUILD_SUMMARY_TR.txt').write_text('\n'.join(summary) + '\n', encoding='utf-8')
print(out)
print(sha)
