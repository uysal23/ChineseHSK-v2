#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "chinese_hsk_android_github" / "app" / "src" / "main" / "assets" / "chinese_course"
AUTHORING = ROOT / "chinese_hsk_android_github" / "authoring"
V13 = ROOT / "ci" / "dialogue_final_v13"

ORDER = ["HSK1", "HSK2", "HSK4", "HSK5", "HSK6", "HSK3"]
EXPECTED = {"HSK1": 50, "HSK2": 50, "HSK4": 50, "HSK5": 50, "HSK6": 50, "HSK3": 7}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def dump(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def validate_dialogues(scene_id: str, old_rows: list[dict], new_rows: list[dict]):
    if len(old_rows) != 100 or len(new_rows) != 100:
        raise SystemExit(f"{scene_id}: expected 100 dialogues, old={len(old_rows)} new={len(new_rows)}")
    old_ids = [x.get("id") for x in old_rows]
    new_ids = [x.get("id") for x in new_rows]
    if old_ids != new_ids:
        raise SystemExit(f"{scene_id}: dialogue IDs changed")
    old_speakers = [x.get("speaker") for x in old_rows]
    new_speakers = [x.get("speaker") for x in new_rows]
    if old_speakers != new_speakers:
        raise SystemExit(f"{scene_id}: speaker sequence changed")
    for i, row in enumerate(new_rows, 1):
        for key in ("id", "speaker", "zh", "pinyin", "tr"):
            if not str(row.get(key, "")).strip():
                raise SystemExit(f"{scene_id} line {i}: missing {key}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes; otherwise validate only")
    args = ap.parse_args()

    targets: dict[str, list[Path]] = {}
    for level in ORDER:
        files = sorted((V13 / level).glob(f"ZH_{level}_SC*.json"))
        targets[level] = files
        if len(files) != EXPECTED[level]:
            raise SystemExit(f"{level}: expected {EXPECTED[level]} v13 files, found {len(files)}")

    total = sum(len(v) for v in targets.values())
    if total != 257:
        raise SystemExit(f"Expected 257 target scenes, found {total}")

    authoring_docs = {}
    authoring_maps = {}
    for level in ORDER:
        p = AUTHORING / f"{level.lower()}_blueprints.json"
        doc = load(p)
        authoring_docs[level] = (p, doc)
        authoring_maps[level] = {s["id"]: s for s in doc["scenes"]}

    changed = []
    for level in ORDER:
        for candidate_path in targets[level]:
            cand = load(candidate_path)
            scene_id = cand["sceneId"]
            if cand.get("level") != level:
                raise SystemExit(f"{scene_id}: v13 level mismatch")
            rows = cand.get("dialogues", [])
            app_path = COURSE / "levels" / level / "scenes" / f"{scene_id}.json"
            app_scene = load(app_path)
            if app_scene.get("id") != scene_id:
                raise SystemExit(f"{scene_id}: canonical scene ID mismatch")
            if cand.get("sourceTitleZh") and cand["sourceTitleZh"] != app_scene.get("titleZh"):
                raise SystemExit(f"{scene_id}: titleZh mismatch")
            if cand.get("sourceTitleTr") and cand["sourceTitleTr"] != app_scene.get("titleTr"):
                raise SystemExit(f"{scene_id}: titleTr mismatch")
            validate_dialogues(scene_id, app_scene.get("dialogues", []), rows)

            bp = authoring_maps[level].get(scene_id)
            if bp is None:
                raise SystemExit(f"{scene_id}: missing from authoring")
            validate_dialogues(scene_id, bp.get("dialogues", []), rows)

            if args.apply:
                app_scene["dialogues"] = rows
                app_scene["dialogueCount"] = 100
                app_scene["editorialStatus"] = "native_mandarin_v13_applied_pending_final_qa"
                app_scene["nativeMandarinRevision"] = {
                    "version": 13,
                    "source": f"ci/dialogue_final_v13/{level}/{scene_id}.json",
                    "preservedDialogueIds": True,
                    "preservedSpeakerSequence": True,
                    "preservedStoryAndLearningPayload": True
                }
                dump(app_path, app_scene)

                bp["dialogues"] = rows
                bp["dialogueCount"] = 100
                bp["editorialStatus"] = "native_mandarin_v13_applied_pending_final_qa"
                bp["nativeMandarinRevision"] = {
                    "version": 13,
                    "source": f"ci/dialogue_final_v13/{level}/{scene_id}.json",
                    "preservedDialogueIds": True,
                    "preservedSpeakerSequence": True,
                    "preservedStoryAndLearningPayload": True
                }
            changed.append(scene_id)

    if args.apply:
        for level in ORDER:
            p, doc = authoring_docs[level]
            dump(p, doc)

    print(json.dumps({
        "status": "OK",
        "apply": args.apply,
        "count": len(changed),
        "order": ORDER,
        "byLevel": {level: len(targets[level]) for level in ORDER},
        "first": changed[:3],
        "last": changed[-3:]
    }, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
