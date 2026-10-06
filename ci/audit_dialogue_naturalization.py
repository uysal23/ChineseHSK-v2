#!/usr/bin/env python3
"""Validate authored dialogue overrides before applying them to runtime assets."""
from collections import Counter
from pathlib import Path
import json
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: audit_dialogue_naturalization.py <source-root> <override-root>")

source_root = Path(sys.argv[1])
override_root = Path(sys.argv[2])
scene_root = source_root / "app" / "src" / "main" / "assets" / "chinese_course" / "levels"
allowed_emotions = {
    "neutral", "happy", "sad", "playful", "curious",
    "worried", "angry", "comforting",
}
errors = []
scene_count = 0
turn_count = 0

for override_path in sorted(override_root.glob("HSK*/ZH_HSK*_SC*.json")):
    patch = json.loads(override_path.read_text(encoding="utf-8"))
    scene_id = patch["sceneId"]
    level = patch["level"]
    target = scene_root / level / "scenes" / f"{scene_id}.json"
    if not target.exists():
        errors.append(f"{scene_id}: missing source scene")
        continue

    original = json.loads(target.read_text(encoding="utf-8")).get("dialogues", [])
    revised = patch.get("dialogues", [])
    if len(revised) != 100:
        errors.append(f"{scene_id}: expected 100 turns, got {len(revised)}")
    if len(original) != len(revised):
        errors.append(f"{scene_id}: turn count changed ({len(original)} -> {len(revised)})")

    texts = []
    for index, (before, after) in enumerate(zip(original, revised), 1):
        for key in ("id", "speaker"):
            if before.get(key) != after.get(key):
                errors.append(f"{scene_id} turn {index}: {key} changed")
        for key in ("zh", "pinyin", "tr"):
            if not str(after.get(key, "")).strip():
                errors.append(f"{scene_id} turn {index}: blank {key}")
        zh = str(after.get("zh", "")).strip()
        if zh:
            texts.append(zh)
        emotion = after.get("emotion")
        if emotion and emotion not in allowed_emotions:
            errors.append(f"{scene_id} turn {index}: unsupported emotion {emotion!r}")
        if "actionTr" in after and not str(after["actionTr"]).strip():
            errors.append(f"{scene_id} turn {index}: blank actionTr")

    repeated = {text: count for text, count in Counter(texts).items() if count > 1}
    if repeated:
        examples = " / ".join(f"{text} ({count}x)" for text, count in list(repeated.items())[:3])
        errors.append(f"{scene_id}: repeated full utterances: {examples}")

    scene_count += 1
    turn_count += len(revised)

if errors:
    print("\n".join(f"FAIL: {error}" for error in errors))
    raise SystemExit(1)

print(f"PASS: {scene_count} scenes / {turn_count} turns; no exact repeated utterances.")
