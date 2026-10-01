#!/usr/bin/env python3
"""Apply locked native-Mandarin v13 dialogue overrides during authoring regeneration.

The override corpus intentionally contains only the 257 scenes that failed or
warned in the 2026-10-01 native Mandarin QA. Dialogue IDs and speaker sequence
are locked and must match the generated scene before replacement.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve()
REPO_ROOT = HERE.parents[2]
V13 = REPO_ROOT / "ci" / "dialogue_final_v13"

def apply_v13_override(scene: dict, level: str) -> bool:
    scene_id = scene.get("id", "")
    p = V13 / level / f"{scene_id}.json"
    if not p.exists():
        return False
    payload = json.loads(p.read_text(encoding="utf-8"))
    rows = payload.get("dialogues", [])
    old = scene.get("dialogues", [])
    if len(rows) != 100 or len(old) != 100:
        raise RuntimeError(f"{scene_id}: v13/authoring dialogue count mismatch")
    if [x.get("id") for x in rows] != [x.get("id") for x in old]:
        raise RuntimeError(f"{scene_id}: v13 dialogue IDs do not match generated authoring")
    if [x.get("speaker") for x in rows] != [x.get("speaker") for x in old]:
        raise RuntimeError(f"{scene_id}: v13 speaker sequence does not match generated authoring")
    scene["dialogues"] = rows
    scene["dialogueCount"] = 100
    scene["editorialStatus"] = "native_mandarin_v13_final_qa_pass"
    scene["nativeMandarinRevision"] = {
        "version": 13,
        "source": f"ci/dialogue_final_v13/{level}/{scene_id}.json",
        "preservedDialogueIds": True,
        "preservedSpeakerSequence": True,
        "preservedStoryAndLearningPayload": True
    }
    return True
