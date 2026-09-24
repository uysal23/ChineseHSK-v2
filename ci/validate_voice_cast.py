#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARACTERS = ROOT / "ci/dialogue_source_snapshot/app/src/main/assets/chinese_course/characters.json"
CATALOG = ROOT / "docs/dialogue_naturalization/scene_catalog.json"
CAST = ROOT / "ci/voice_cast_manifest.json"

characters = json.loads(CHARACTERS.read_text(encoding="utf-8"))["characters"]
raw_catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
scenes = raw_catalog if isinstance(raw_catalog, list) else raw_catalog.get("scenes", [])
manifest = json.loads(CAST.read_text(encoding="utf-8"))
cast = manifest["cast"]

allowed_female = {"zf_xiaobei","zf_xiaoni","zf_xiaoxiao","zf_xiaoyi"}
allowed_male = {"zm_yunjian","zm_yunxi","zm_yunxia","zm_yunyang"}
allowed = allowed_female | allowed_male

errors = []
if len(cast) != len(characters):
    errors.append(f"cast count {len(cast)} != character count {len(characters)}")

by_speaker = {x["speaker"]: x for x in cast}
if len(by_speaker) != len(cast):
    errors.append("duplicate speaker entries in cast")

for ch in characters:
    speaker = ch["nameZh"]
    row = by_speaker.get(speaker)
    if row is None:
        errors.append(f"missing cast entry: {speaker}")
        continue
    if row.get("voiceProfileId") != ch.get("voiceProfileId"):
        errors.append(f"voiceProfileId mismatch: {speaker}")
    voice = row.get("synthesis", {}).get("voice")
    gender = row.get("genderPresentation")
    if voice not in allowed:
        errors.append(f"unsupported Kokoro voice: {speaker} -> {voice}")
    if gender == "female" and voice not in allowed_female:
        errors.append(f"female role mapped to non-female base voice: {speaker} -> {voice}")
    if gender == "male" and voice not in allowed_male:
        errors.append(f"male role mapped to non-male base voice: {speaker} -> {voice}")

scene_speakers = {
    speaker
    for scene in scenes
    for speaker in scene.get("speakers", [])
    if speaker and speaker != "旁白"
}
for speaker in sorted(scene_speakers):
    if speaker not in by_speaker:
        errors.append(f"scene speaker has no cast entry: {speaker}")

for speaker in ("张伟","刘梅","李晨","张雨桐","张乐乐"):
    row = by_speaker.get(speaker, {})
    overrides = row.get("levelOverrides", {})
    missing = [f"HSK{i}" for i in range(1,7) if f"HSK{i}" not in overrides]
    if missing:
        errors.append(f"{speaker} missing age overrides: {missing}")

for speaker in ("张乐乐","小朋友","孙辈"):
    row = by_speaker.get(speaker, {})
    if row and row.get("ageClass") == "child":
        if abs(float(row.get("synthesis", {}).get("pitchSemitones", 0))) < 2:
            errors.append(f"child voice lacks child pitch treatment: {speaker}")

if errors:
    raise SystemExit("VOICE CAST VALIDATION FAILED\n- " + "\n- ".join(errors))

print(
    f"VOICE CAST OK: {len(cast)} entries, "
    f"{len(scene_speakers)} distinct scene speakers, "
    f"{len(allowed_female)} female + {len(allowed_male)} male Kokoro base voices."
)
