#!/usr/bin/env python3
from pathlib import Path
import json
import sys

if len(sys.argv) != 3:
    raise SystemExit("usage: apply_dialogue_naturalization.py <source-root> <override-root>")

src = Path(sys.argv[1])
override_root = Path(sys.argv[2])
scene_root = src / "app" / "src" / "main" / "assets" / "chinese_course" / "levels"

if not override_root.exists():
    print("No dialogue naturalization overrides present.")
    raise SystemExit(0)

count_scenes = 0
count_turns = 0

for override_path in sorted(override_root.glob("HSK*/ZH_HSK*_SC*.json")):
    patch = json.loads(override_path.read_text(encoding="utf-8"))
    scene_id = patch["sceneId"]
    level = patch["level"]
    target = scene_root / level / "scenes" / f"{scene_id}.json"
    if not target.exists():
        raise SystemExit(f"Missing target scene: {target}")

    data = json.loads(target.read_text(encoding="utf-8"))
    original = data.get("dialogues", [])
    repl = patch.get("dialogues", [])
    if len(original) != len(repl):
        raise SystemExit(f"{scene_id}: turn count mismatch {len(original)} != {len(repl)}")

    for i, (old, new) in enumerate(zip(original, repl), 1):
        if old.get("id") != new.get("id"):
            raise SystemExit(f"{scene_id} turn {i}: dialogue id changed")
        if old.get("speaker") != new.get("speaker"):
            raise SystemExit(f"{scene_id} turn {i}: speaker changed")
        for key in ("zh", "pinyin", "tr"):
            value = str(new.get(key, "")).strip()
            if not value:
                raise SystemExit(f"{scene_id} turn {i}: blank {key}")
            old[key] = value
        count_turns += 1

    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    count_scenes += 1

print(f"Applied dialogue naturalization: {count_scenes} scenes / {count_turns} turns")
