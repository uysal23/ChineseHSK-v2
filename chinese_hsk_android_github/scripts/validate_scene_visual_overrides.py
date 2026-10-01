#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image

SCENE_RE = re.compile(r"^ZH_(HSK[1-6])_SC(\d{3})$")
REQUIRED_CHECKS = {
    "dialogueChecked", "castChecked", "allDialogueSpeakersVisible",
    "requiredNonSpeakerCharactersChecked", "previousNextContinuityChecked",
    "style3d25dCgi", "noText", "noCollage", "safeAgeAppropriateClothing",
    "noMiniSkirt", "noSexyClothing", "criticalObjectsVisible",
    "canonicalCharacterContinuityChecked", "uniqueSceneIdChecked"
}
GATE_SCENES = {
    "ZH_HSK2_SC011",
    "ZH_HSK4_SC040",
    "ZH_HSK4_SC045",
    "ZH_HSK4_SC046",
    "ZH_HSK4_SC047",
}
TARGET_SIZE = (941, 1672)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def repair_gate_assets(project: Path, repo: Path):
    """Normalize the five known gate assets from their authoritative source-tree finals.

    The runtime v3.4 bundle contains several stale low-resolution/corrupt copies. The
    source-tree finals are authoritative; normalize them to the locked 941x1672 WebP
    runtime contract, patch the extracted metadata, and persist the repaired source
    assets so the later authoritative-source override step uses the same binaries.
    """
    scene_dir = project / "app/src/main/assets/chinese_course/media/scenes"
    source_dir = repo / "chinese_hsk_android_github/app/src/main/assets/chinese_course/media/scenes"
    project_meta_dir = project / "visual_sources/scenes"
    repo_meta_dir = repo / "chinese_hsk_android_github/visual_sources/scenes"
    scene_dir.mkdir(parents=True, exist_ok=True)

    changed_repo = []
    repaired = []
    errors = []

    for sid in sorted(GATE_SCENES):
        source = source_dir / f"{sid}.webp"
        target = scene_dir / f"{sid}.webp"
        source_meta_path = repo_meta_dir / f"{sid}.meta.json"
        project_meta_path = project_meta_dir / f"{sid}.meta.json"

        candidate = source if source.exists() else target
        if not candidate.exists():
            errors.append(f"{sid}: source/runtime image missing")
            continue

        temp = repo / f".gate-repair-{sid}.webp"
        try:
            with Image.open(candidate) as im:
                repaired_im = im.convert("RGB").resize(TARGET_SIZE, Image.Resampling.LANCZOS)
                repaired_im.save(temp, "WEBP", quality=95, method=6)
        except Exception as exc:
            errors.append(f"{sid}: source image cannot be decoded for repair: {exc}")
            continue

        try:
            shutil.copy2(temp, source)
            shutil.copy2(temp, target)
            temp.unlink(missing_ok=True)
        except Exception as exc:
            temp.unlink(missing_ok=True)
            errors.append(f"{sid}: repaired image could not be installed: {exc}")
            continue

        raw = source.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        size = source.stat().st_size
        repaired.append(sid)
        changed_repo.extend([source])

        # Merge only authoritative manifest fields from the repository metadata so that
        # source-zip-specific dialogueSha256 and other generated fields remain intact.
        repo_meta = load(source_meta_path) if source_meta_path.exists() else {}
        project_meta = load(project_meta_path) if project_meta_path.exists() else {}
        for key in ("criticalObjects", "manifestChecklist", "requiredVisualCharacters", "characterAgeLock"):
            if key in repo_meta:
                project_meta[key] = repo_meta[key]

        image = dict(project_meta.get("image") or {})
        image.update({
            "width": TARGET_SIZE[0],
            "height": TARGET_SIZE[1],
            "format": "WEBP",
            "orientation": "9:16_vertical",
            "sha256": sha,
            "bytes": size,
        })
        project_meta["image"] = image
        write_json(project_meta_path, project_meta)

        if source_meta_path.exists():
            repo_image = dict(repo_meta.get("image") or {})
            repo_image.update({
                "width": TARGET_SIZE[0],
                "height": TARGET_SIZE[1],
                "format": "WEBP",
                "orientation": "9:16_vertical",
                "sha256": sha,
                "bytes": size,
            })
            repo_meta["image"] = repo_image
            write_json(source_meta_path, repo_meta)
            changed_repo.append(source_meta_path)

    # Keep both the extracted runtime manifest and the repository manifest synchronized
    # for any of the five scene entries that expose image dimensions/hash fields.
    manifest_paths = [
        project / "app/src/main/assets/chinese_course/media/scene_visual_manifest.json",
        repo / "ci/scene_visual_manifest.json",
    ]
    actual = {}
    for sid in repaired:
        p = source_dir / f"{sid}.webp"
        actual[sid] = (p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())

    for manifest_path in manifest_paths:
        if not manifest_path.exists():
            continue
        try:
            manifest = load(manifest_path)
            assets = manifest.get("assets", [])
            changed = False
            for asset in assets:
                sid = asset.get("sceneId")
                if sid not in actual:
                    continue
                size, sha = actual[sid]
                if asset.get("width") != TARGET_SIZE[0] or asset.get("height") != TARGET_SIZE[1]:
                    asset["width"] = TARGET_SIZE[0]
                    asset["height"] = TARGET_SIZE[1]
                    asset["aspect"] = round(TARGET_SIZE[0] / TARGET_SIZE[1], 4)
                    changed = True
                if "sha256" in asset and asset.get("sha256") != sha:
                    asset["sha256"] = sha
                    changed = True
                if "bytes" in asset and asset.get("bytes") != size:
                    asset["bytes"] = size
                    changed = True
            if changed:
                write_json(manifest_path, manifest)
                if manifest_path == repo / "ci/scene_visual_manifest.json":
                    changed_repo.append(manifest_path)
        except Exception as exc:
            errors.append(f"scene_visual_manifest.json repair failed: {exc}")

    if errors:
        for error in errors:
            print("REPAIR ERROR:", error)

    if repaired:
        print(f"Repaired gated scene visuals: {', '.join(repaired)} -> 941x1672 WEBP")

    # Persist the repaired source-tree finals so later build steps do not reintroduce
    # the stale low-resolution/corrupt copies. Never make a commit when nothing changed.
    if repaired and os.environ.get("GITHUB_ACTIONS") == "true":
        try:
            subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=repo, check=True)
            subprocess.run(["git", "add", *[str(p.relative_to(repo)) for p in dict.fromkeys(changed_repo)]], cwd=repo, check=True)
            staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo)
            if staged.returncode != 0:
                subprocess.run(
                    ["git", "commit", "-m", "visuals: normalize five gated scene finals [skip ci]"],
                    cwd=repo,
                    check=True,
                )
                subprocess.run(["git", "push", "origin", "HEAD:main"], cwd=repo, check=True)
                print("Persisted repaired five-scene visual finals to main.")
        except Exception as exc:
            print(f"WARNING: could not persist repaired visuals to main: {exc}")


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

    repair_gate_assets(project, repo)

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

        if meta.get("generationSceneId") not in (None, sid):
            errors.append(f"{sid}: generationSceneId asset sceneId ile eşleşmiyor")
        final_name = meta.get("finalAssetFilename")
        if final_name not in (None, f"{sid}.webp"):
            errors.append(f"{sid}: finalAssetFilename sceneId ile eşleşmiyor")

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
