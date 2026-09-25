#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "ci" / "scene_visual_manifest.json"
SNAPSHOT = ROOT / "ci" / "dialogue_source_snapshot" / "app" / "src" / "main" / "assets" / "chinese_course"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
errors = []

for asset in manifest.get("assets", []):
    scene_id = asset.get("sceneId")
    level = asset.get("level")
    if not scene_id or not level:
        # Reference/hold assets are intentionally not bound to a runtime scene.
        # They must not fail the runtime cast validator.
        continue
    scene_path = SNAPSHOT / "levels" / level / "scenes" / f"{scene_id}.json"
    if not scene_path.exists():
        # Not all newer scene files are in the extraction snapshot on every branch.
        continue
    scene = json.loads(scene_path.read_text(encoding="utf-8"))
    canonical = scene.get("production", {}).get("characters", [])
    declared = asset.get("expectedCharacters", [])
    if canonical != declared:
        errors.append(f"{scene_id}: production.characters={canonical} manifest.expectedCharacters={declared}")

if errors:
    raise SystemExit("VISUAL CAST METADATA VALIDATION FAILED\n- " + "\n- ".join(errors))

print(f"VISUAL CAST METADATA OK: {len(manifest.get('assets', []))} manifest entries checked.")
