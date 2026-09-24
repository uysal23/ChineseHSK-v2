#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json, re, sys

if len(sys.argv) != 3:
    raise SystemExit("usage: validate_dialogue_naturalization.py <baseline-root> <naturalized-root>")

baseline_root = Path(sys.argv[1])
naturalized_root = Path(sys.argv[2])

# Obvious traditional-only forms. This is a guardrail, not a full converter.
traditional_only = set("臺灣國學會體這個門書車裡來說對還點開關問題經過發現應該讓從與為時後麼們實際選擇")
known_robotic = [
    re.compile(r"确认一下觉得"),
    re.compile(r"是这次要考虑的重点之一"),
    re.compile(r"我们继续看下一项"),
]

errors = []
warnings = []
scene_count = 0
turn_count = 0
paths = sorted(naturalized_root.glob("HSK*/ZH_HSK*_SC*.json"))

for new_path in paths:
    patch = json.loads(new_path.read_text(encoding="utf-8"))
    level = patch.get("level")
    scene_id = patch.get("sceneId")
    old_path = baseline_root / level / "scenes" / f"{scene_id}.json"
    if not old_path.exists():
        errors.append(f"{scene_id}: baseline missing")
        continue

    old = json.loads(old_path.read_text(encoding="utf-8"))
    a = old.get("dialogues", [])
    b = patch.get("dialogues", [])
    if len(a) != len(b):
        errors.append(f"{scene_id}: turn count {len(a)} -> {len(b)}")
        continue

    scene_count += 1
    seen_zh = Counter()
    old_text = "".join(str(x.get("zh", "")) for x in a)
    new_text = "".join(str(x.get("zh", "")) for x in b)

    # Preserve active teaching anchors if they were used in the original dialogue.
    cards = old.get("learning", {}).get("vocabularyCards", [])
    for card in cards:
        if card.get("kind") != "active":
            continue
        term = str(card.get("zh", "")).strip()
        if term and term in old_text and term not in new_text:
            errors.append(f"{scene_id}: active vocabulary disappeared from dialogue: {term}")

    for idx, (x, y) in enumerate(zip(a, b), 1):
        if x.get("id") != y.get("id"):
            errors.append(f"{scene_id}:{idx}: id changed")
        if x.get("speaker") != y.get("speaker"):
            errors.append(f"{scene_id}:{idx}: speaker changed")

        zh = str(y.get("zh", "")).strip()
        py = str(y.get("pinyin", "")).strip()
        tr = str(y.get("tr", "")).strip()
        if not zh or not py or not tr:
            errors.append(f"{scene_id}:{idx}: blank zh/pinyin/tr")

        if idx > 1 and zh == str(b[idx-2].get("zh", "")).strip():
            errors.append(f"{scene_id}:{idx}: identical consecutive dialogue line")
        seen_zh[zh] += 1

        old_len = max(1, len(str(x.get("zh", "")).strip()))
        ratio = len(zh) / old_len
        if ratio < 0.65 or ratio > 1.45:
            warnings.append(f"{scene_id}:{idx}: length ratio {ratio:.2f}")

        if any(ch in zh for ch in traditional_only):
            warnings.append(f"{scene_id}:{idx}: inspect for Traditional Chinese: {zh}")

        for pattern in known_robotic:
            if pattern.search(zh):
                warnings.append(f"{scene_id}:{idx}: robotic template remains: {zh}")
                break

        turn_count += 1

    repeated = [(z, n) for z, n in seen_zh.items() if z and n >= 8]
    if repeated:
        warnings.append(f"{scene_id}: high within-scene repetition {repeated[:5]}")

if len(paths) == 300 and scene_count != 300:
    errors.append(f"Expected 300 valid scene overrides, got {scene_count}")

print(f"Validated {scene_count} naturalized scenes / {turn_count} turns")
print(f"Warnings: {len(warnings)}")
for w in warnings[:300]:
    print("WARN", w)
if errors:
    for e in errors[:300]:
        print("ERROR", e)
    raise SystemExit(f"Dialogue naturalization validation failed with {len(errors)} errors")
