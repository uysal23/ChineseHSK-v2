#!/usr/bin/env python3
import argparse, hashlib, json, re, sys
from pathlib import Path
from PIL import Image

SCENE_RE = re.compile(r"^ZH_(HSK[1-6])_SC(\\d{3})$")
REQUIRED_CHECKS = {
    "dialogueChecked", "castChecked", "allDialogueSpeakersVisible",
    "requiredNonSpeakerCharactersChecked", "previousNextContinuityChecked",
    "style3d25dCgi", "noText", "noCollage", "safeAgeAppropriateClothing",
    "noMiniSkirt", "noSexyClothing", "criticalObjectsVisible",
    "canonicalCharacterContinuityChecked"
}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=None)
    ap.add_argument("--require-ready-batch", action="store_true")
    args = ap.parse_args()

    project = Path(__file__).resolve().parents[1]
    repo = Path(args.repo_root).resolve() if args.repo_root else project.parent
    scenes_dir = project / "app/src/main/assets/chinese_course/media/scenes"
    meta_dir = project / "visual_sources/scenes"
    batch_path = project / "visual_sources/visual_batch_status.json"
    policy_path = project / "visual_sources/visual_generation_policy.json"
    errors = []

    policy = load(policy_path)
    if policy.get("policyVersion") != "LOCKED_V2" or policy.get("batchSize") != 10:
        errors.append("visual_generation_policy.json LOCKED_V2 / batchSize=10 değil")

    webps = sorted(scenes_dir.glob("ZH_HSK*_SC*.webp")) if scenes_dir.exists() else []
    seen = set()

    for img_path in webps:
        sid = img_path.stem
        match = SCENE_RE.match(sid)
        if not match:
            errors.append(f"Geçersiz scene asset adı: {img_path.name}")
            continue

        level = match.group(1)
        seen.add(sid)
        scene_path = project / f"app/src/main/assets/chinese_course/levels/{level}/scenes/{sid}.json"
        if not scene_path.exists():
            errors.append(f"{sid}: scene JSON yok")
            continue

        meta_path = meta_dir / f"{sid}.meta.json"
        if not meta_path.exists():
            errors.append(f"{sid}: metadata yok: {meta_path.relative_to(project)}")
            continue

        meta = load(meta_path)
        if meta.get("sceneId") != sid or meta.get("manifestVersion") != "LOCKED_V2":
            errors.append(f"{sid}: metadata sceneId/manifestVersion hatalı")

        try:
            with Image.open(img_path) as im:
                w, h = im.size
                if im.format != "WEBP":
                    errors.append(f"{sid}: format WEBP değil ({im.format})")
                if h <= w:
                    errors.append(f"{sid}: görsel dikey değil ({w}x{h})")
                if abs((w / h) - (9 / 16)) > 0.01:
                    errors.append(f"{sid}: 9:16 oranı değil ({w}x{h})")
                if w < 900 or h < 1600:
                    errors.append(f"{sid}: çözünürlük düşük ({w}x{h})")
                expected_sha = (meta.get("image") or {}).get("sha256", "")
                if expected_sha:
                    actual_sha = hashlib.sha256(img_path.read_bytes()).hexdigest()
                    if expected_sha != actual_sha:
                        errors.append(f"{sid}: görsel SHA-256 metadata ile eşleşmiyor")
        except Exception as exc:
            errors.append(f"{sid}: görsel açılamadı: {exc}")

        source = meta.get("dialogueSource", "")
        dpath = repo / source if source.startswith("ci/") else project / source
        if not dpath.exists():
            errors.append(f"{sid}: dialogueSource bulunamadı: {source}")
            continue

        raw = dpath.read_bytes()
        if meta.get("dialogueSha256") != hashlib.sha256(raw).hexdigest():
            errors.append(f"{sid}: dialogueSha256 güncel değil")

        data = json.loads(raw)
        speakers = []
        for dialogue in data.get("dialogues", []):
            speaker = dialogue.get("speaker", "")
            if speaker and speaker != "旁白" and speaker not in speakers:
                speakers.append(speaker)

        if meta.get("dialogueSpeakers") != speakers:
            errors.append(f"{sid}: konuşan karakter listesi kaynak diyalogla eşleşmiyor; beklenen={speakers}")

        required = set(meta.get("requiredVisualCharacters", []))
        if not set(speakers).issubset(required):
            errors.append(f"{sid}: requiredVisualCharacters tüm konuşanları içermiyor")

        checks = meta.get("manifestChecklist", {})
        missing = [key for key in REQUIRED_CHECKS if checks.get(key) is not True]
        if missing:
            errors.append(f"{sid}: manifesto checklist eksik/false: {sorted(missing)}")
        if not meta.get("criticalObjects"):
            errors.append(f"{sid}: criticalObjects boş")

    batch = load(batch_path)
    active = batch.get("activeBatch") or {}
    ids = active.get("sceneIds", [])
    done = active.get("completedSceneIds", [])

    if len(ids) != 10:
        errors.append("Aktif batch sceneIds tam 10 sahne değil")

    missing_done = [sid for sid in done if sid not in seen]
    if missing_done:
        errors.append(f"Batch tamamlandı denen fakat asseti olmayan sahneler: {missing_done}")

    if active.get("status") == "READY_FOR_BUILD" and set(done) != set(ids):
        errors.append("READY_FOR_BUILD fakat batch 10/10 tamam değil")

    if args.require_ready_batch:
        if active.get("status") != "READY_FOR_BUILD":
            errors.append(f"Build engellendi: aktif batch durumu {active.get('status')} (READY_FOR_BUILD olmalı)")
        if active.get("buildApprovalRequired") is not True:
            errors.append("Build approval policy kapalı")
        if active.get("buildApproved") is not True:
            errors.append("Build engellendi: kullanıcı build onayı kaydı yok")

    if errors:
        print("VISUAL OVERRIDE VALIDATION: FAIL")
        for error in errors:
            print(" -", error)
        return 1

    print(f"VISUAL OVERRIDE VALIDATION: PASS ({len(webps)} direct scene override)")
    print(f"Active batch: {active.get('batchId')} {len(done)}/10 status={active.get('status')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
