#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "ci" / "visual_continuity_lock.json"

data = json.loads(LOCK.read_text(encoding="utf-8"))
errors = []

def expect(cond, message):
    if not cond:
        errors.append(message)

expect(data.get("lockId") == "VISUAL_CONTINUITY_LOCK_V1", "wrong lock id")
expect(data.get("status") == "LOCKED", "visual continuity lock is not LOCKED")
expect(data.get("styleFamily") == "WARM_CINEMATIC_STYLIZED_3D_CGI_V1", "style family changed")
expect(data.get("runtimeAspect") == "9:16", "runtime aspect changed")
expect(data.get("neighborWindow", {}).get("required") is True, "neighbor window must be required")
expect(data.get("neighborWindow", {}).get("rule") == "PREVIOUS_CURRENT_NEXT", "neighbor rule changed")

rules = data.get("hardRules", {})
for key in (
    "noStyleJump",
    "dialogueGenderAgeMustMatch",
    "productionCharactersAuthoritative",
    "noExtraFamilyMembers",
    "characterIdentityStable",
    "locationIdentityStable",
):
    expect(rules.get(key) is True, f"hard rule disabled: {key}")

fam = data.get("canonicalFamily", {})
expect(fam.get("张雨桐", {}).get("gender") == "female", "Yutong gender lock broken")
expect(fam.get("张乐乐", {}).get("gender") == "male", "Lele gender lock broken")
expect(fam.get("张雨桐", {}).get("ageRole") == "older_child_teen_hsk1_hsk2", "Yutong age lock broken")
expect(fam.get("张乐乐", {}).get("ageRole") == "younger_child_boy_hsk1_hsk2", "Lele age lock broken")

sc001 = data.get("sc001", {})
expect(sc001.get("requiredCast") == ["张伟","刘梅","张雨桐","张乐乐","王师傅"], "SC001 cast lock changed")
expect(sc001.get("neighborReference") == "ZH_HSK1_SC002", "SC001 neighbor reference changed")

required_gate = {
    "scene_context_match",
    "gender_age_match",
    "production_cast_match",
    "neighbor_scene_continuity",
    "style_family_match",
}
expect(set(data.get("finalGate", [])) == required_gate, "final visual gate changed")

if errors:
    raise SystemExit("VISUAL CONTINUITY LOCK FAILED\n- " + "\n- ".join(errors))

print("VISUAL CONTINUITY LOCK OK: neighbor continuity + cast + style family are locked.")
