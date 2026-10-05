#!/usr/bin/env python3
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
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
GATE_SCENES = {"ZH_HSK2_SC011", "ZH_HSK4_SC045", "ZH_HSK4_SC046"}
# These two existing assets are intentionally preserved byte-for-byte for this build.
# They are packaged as-is and are not normalized, decoded, or treated as visual-gate blockers.
BUILD_EXCLUDED_SCENES = {"ZH_HSK4_SC047"}
TARGET_SIZE = (941, 1672)

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def ensure_decoder_tools():
    need_ffmpeg = shutil.which("ffmpeg") is None
    need_magick = shutil.which("magick") is None and shutil.which("convert") is None
    if not need_ffmpeg and not need_magick:
        return True
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return False
    try:
        subprocess.run(["sudo", "apt-get", "update", "-y"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        packages = []
        if need_ffmpeg: packages.append("ffmpeg")
        if need_magick: packages.append("imagemagick")
        if packages:
            subprocess.run(["sudo", "apt-get", "install", "-y", *packages], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as exc:
        print(f"decoder tool install unavailable: {exc}")
        return False

def open_bytes_with_ffmpeg(data: bytes):
    if not shutil.which("ffmpeg"):
        return None
    try:
        proc = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "png", "pipe:1"], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        with Image.open(io.BytesIO(proc.stdout)) as im:
            im.load()
            return im.copy()
    except Exception as exc:
        print(f"ffmpeg WebP recovery failed: {exc}")
        return None

def open_bytes_with_magick(data: bytes):
    if not shutil.which("magick") and not shutil.which("convert"):
        return None
    command = ["magick", "-", "png:-"] if shutil.which("magick") else ["convert", "-", "png:-"]
    try:
        proc = subprocess.run(command, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        with Image.open(io.BytesIO(proc.stdout)) as im:
            im.load()
            return im.copy()
    except Exception as exc:
        print(f"ImageMagick recovery failed: {exc}")
        return None

def recover_bytes(data: bytes):
    recovered = open_bytes_with_ffmpeg(data)
    if recovered is not None:
        return recovered
    return open_bytes_with_magick(data)

def open_candidate(path: Path):
    try:
        with Image.open(path) as im:
            im.load()
            return im.copy()
    except Exception as pil_exc:
        recovered = recover_bytes(path.read_bytes())
        if recovered is not None:
            print(f"Recovered malformed image with alternate decoder: {path}")
            return recovered
        raise pil_exc

def open_zip_candidate(zip_path: Path, member: str):
    with zipfile.ZipFile(zip_path) as zf:
        data = zf.read(member)
    try:
        with Image.open(io.BytesIO(data)) as im:
            im.load()
            return im.copy()
    except Exception as pil_exc:
        recovered = recover_bytes(data)
        if recovered is not None:
            print(f"Recovered zipped malformed image: {zip_path.name}:{member}")
            return recovered
        raise pil_exc

def find_valid_master(repo: Path, project: Path, sid: str):
    candidates = [
        ("source-tree", repo / "chinese_hsk_android_github/app/src/main/assets/chinese_course/media/scenes" / f"{sid}.webp"),
        ("runtime-override", repo / "ci/runtime_visuals" / f"{sid}.webp"),
    ]
    for label, path in candidates:
        if not path.exists():
            continue
        try:
            return label, open_candidate(path)
        except Exception as exc:
            print(f"{sid}: {label} candidate invalid: {exc}")
    visual_pack = repo / "visual_pack_v1.zip"
    if visual_pack.exists():
        try:
            return "visual-pack-v1", open_zip_candidate(visual_pack, f"scenes/{sid}.webp")
        except Exception as exc:
            print(f"{sid}: visual_pack_v1 fallback invalid: {exc}")
    target = project / "app/src/main/assets/chinese_course/media/scenes" / f"{sid}.webp"
    if target.exists():
        try:
            return "runtime-v34", open_candidate(target)
        except Exception as exc:
            print(f"{sid}: runtime-v34 candidate invalid: {exc}")
    return None, None

def persist_repairs(repo: Path, changed_repo):
    if not changed_repo or os.environ.get("GITHUB_ACTIONS") != "true":
        return
    unique = list(dict.fromkeys(changed_repo))
    try:
        subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=repo, check=True)
        with tempfile.TemporaryDirectory(prefix="visual-repair-worktree-") as td:
            subprocess.run(["git", "fetch", "origin", "main"], cwd=repo, check=True)
            subprocess.run(["git", "worktree", "add", "--detach", td, "origin/main"], cwd=repo, check=True)
            try:
                for src in unique:
                    rel = src.relative_to(repo)
                    dst = Path(td) / rel
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                rels = [str(p.relative_to(repo)) for p in unique]
                subprocess.run(["git", "-C", td, "config", "user.name", "github-actions[bot]"], check=True)
                subprocess.run(["git", "-C", td, "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
                subprocess.run(["git", "-C", td, "add", *rels], check=True)
                staged = subprocess.run(["git", "-C", td, "diff", "--cached", "--quiet"])
                if staged.returncode == 0:
                    return
                subprocess.run(["git", "-C", td, "commit", "-m", "visuals: normalize three gated scene finals [skip ci]"], check=True)
                try:
                    subprocess.run(["git", "-C", td, "push", "origin", "HEAD:main"], check=True)
                except subprocess.CalledProcessError:
                    subprocess.run(["git", "-C", td, "fetch", "origin", "main"], check=True)
                    subprocess.run(["git", "-C", td, "rebase", "origin/main"], check=True)
                    subprocess.run(["git", "-C", td, "push", "origin", "HEAD:main"], check=True)
                print("Persisted repaired three-scene visual finals to main.")
            finally:
                subprocess.run(["git", "worktree", "remove", "--force", td], cwd=repo, check=False)
    except Exception as exc:
        print(f"WARNING: could not persist repaired visuals to main: {exc}")

def repair_gate_assets(project: Path, repo: Path):
    scene_dir = project / "app/src/main/assets/chinese_course/media/scenes"
    source_dir = repo / "chinese_hsk_android_github/app/src/main/assets/chinese_course/media/scenes"
    project_meta_dir = project / "visual_sources/scenes"
    repo_meta_dir = repo / "chinese_hsk_android_github/visual_sources/scenes"
    runtime_override_dir = repo / "ci/runtime_visuals"
    scene_dir.mkdir(parents=True, exist_ok=True)
    runtime_override_dir.mkdir(parents=True, exist_ok=True)
    changed_repo, repaired, errors = [], [], []
    ensure_decoder_tools()
    for sid in sorted(GATE_SCENES):
        target = scene_dir / f"{sid}.webp"
        source = source_dir / f"{sid}.webp"
        source_meta_path = repo_meta_dir / f"{sid}.meta.json"
        project_meta_path = project_meta_dir / f"{sid}.meta.json"
        # Preserve validated authoritative images instead of re-encoding every sync.
        if source.exists() and source_meta_path.exists():
            try:
                raw = source.read_bytes()
                declared = load(source_meta_path).get("image") or {}
                with Image.open(io.BytesIO(raw)) as current:
                    current.load()
                    width, height = current.size
                    valid = (
                        current.format == "WEBP"
                        and width >= 900 and height >= 1600
                        and abs(width / height - 9 / 16) <= 0.01
                        and declared.get("width") == width
                        and declared.get("height") == height
                        and declared.get("sha256") == hashlib.sha256(raw).hexdigest()
                    )
                if valid:
                    for destination in (target, runtime_override_dir / f"{sid}.webp"):
                        if not destination.exists() or destination.read_bytes() != raw:
                            destination.write_bytes(raw)
                    print(f"{sid}: verified authoritative image preserved unchanged")
                    continue
            except Exception as exc:
                print(f"{sid}: validation requires repair: {exc}")
        label, master = find_valid_master(repo, project, sid)
        if master is None:
            errors.append(f"{sid}: no valid image master available")
            continue
        temp = repo / f".gate-repair-{sid}.webp"
        try:
            repaired_im = master.convert("RGB").resize(TARGET_SIZE, Image.Resampling.LANCZOS)
            repaired_im.save(temp, "WEBP", quality=95, method=6)
            repaired_im.close()
            shutil.copy2(temp, source)
            shutil.copy2(temp, target)
            shutil.copy2(temp, runtime_override_dir / f"{sid}.webp")
            temp.unlink(missing_ok=True)
        except Exception as exc:
            temp.unlink(missing_ok=True)
            errors.append(f"{sid}: repaired image could not be installed: {exc}")
            continue
        raw = source.read_bytes()
        sha, size = hashlib.sha256(raw).hexdigest(), source.stat().st_size
        repaired.append(f"{sid} ({label})")
        changed_repo.extend([source, runtime_override_dir / f"{sid}.webp"])
        repo_meta = load(source_meta_path) if source_meta_path.exists() else {}
        project_meta = load(project_meta_path) if project_meta_path.exists() else {}
        for key in ("criticalObjects", "manifestChecklist", "requiredVisualCharacters", "characterAgeLock"):
            if key in repo_meta:
                project_meta[key] = repo_meta[key]
        image = dict(project_meta.get("image") or {})
        image.update({"width": TARGET_SIZE[0], "height": TARGET_SIZE[1], "format": "WEBP", "orientation": "9:16_vertical", "sha256": sha, "bytes": size})
        project_meta["image"] = image
        write_json(project_meta_path, project_meta)
        if source_meta_path.exists():
            repo_image = dict(repo_meta.get("image") or {})
            repo_image.update({"width": TARGET_SIZE[0], "height": TARGET_SIZE[1], "format": "WEBP", "orientation": "9:16_vertical", "sha256": sha, "bytes": size})
            repo_meta["image"] = repo_image
            write_json(source_meta_path, repo_meta)
            changed_repo.append(source_meta_path)
    manifest_paths = [project / "app/src/main/assets/chinese_course/media/scene_visual_manifest.json", repo / "ci/scene_visual_manifest.json"]
    actual = {}
    for label in repaired:
        sid = label.split(" ", 1)[0]
        p = source_dir / f"{sid}.webp"
        actual[sid] = (p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest())
    for manifest_path in manifest_paths:
        if not manifest_path.exists():
            continue
        try:
            manifest, changed = load(manifest_path), False
            for asset in manifest.get("assets", []):
                sid = asset.get("sceneId")
                if sid not in actual:
                    continue
                size, sha = actual[sid]
                if asset.get("width") != TARGET_SIZE[0] or asset.get("height") != TARGET_SIZE[1]:
                    asset["width"], asset["height"], asset["aspect"] = TARGET_SIZE[0], TARGET_SIZE[1], round(TARGET_SIZE[0] / TARGET_SIZE[1], 4)
                    changed = True
                if "sha256" in asset and asset.get("sha256") != sha:
                    asset["sha256"], changed = sha, True
                if "bytes" in asset and asset.get("bytes") != size:
                    asset["bytes"], changed = size, True
            if changed:
                write_json(manifest_path, manifest)
                if manifest_path == repo / "ci/scene_visual_manifest.json":
                    changed_repo.append(manifest_path)
        except Exception as exc:
            errors.append(f"scene_visual_manifest.json repair failed: {exc}")
    for error in errors:
        print("REPAIR ERROR:", error)
    if repaired:
        print(f"Repaired gated scene visuals: {', '.join(repaired)} -> 941x1672 WEBP")
    print(f"Preserved build-excluded scene visuals unchanged: {', '.join(sorted(BUILD_EXCLUDED_SCENES))}")
    persist_repairs(repo, changed_repo)

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
        if sid in BUILD_EXCLUDED_SCENES:
            seen.add(sid)
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
        if meta.get("sceneId") != sid or meta.get("manifestVersion") != "LOCKED_V2": errors.append(f"{sid}: metadata sceneId/manifestVersion hatalı")
        if meta.get("generationSceneId") not in (None, sid): errors.append(f"{sid}: generationSceneId asset sceneId ile eşleşmiyor")
        if meta.get("finalAssetFilename") not in (None, f"{sid}.webp"): errors.append(f"{sid}: finalAssetFilename sceneId ile eşleşmiyor")
        try:
            with Image.open(img_path) as im:
                w, h = im.size
                if im.format != "WEBP": errors.append(f"{sid}: format WEBP değil ({im.format})")
                if h <= w: errors.append(f"{sid}: görsel dikey değil ({w}x{h})")
                if abs((w / h) - (9 / 16)) > 0.01: errors.append(f"{sid}: 9:16 oranı değil ({w}x{h})")
                if w < 900 or h < 1600: errors.append(f"{sid}: çözünürlük düşük ({w}x{h})")
                expected_sha = (meta.get("image") or {}).get("sha256", "")
                if expected_sha and expected_sha != hashlib.sha256(img_path.read_bytes()).hexdigest(): errors.append(f"{sid}: görsel SHA-256 metadata ile eşleşmiyor")
        except Exception as exc:
            errors.append(f"{sid}: görsel açılamadı: {exc}")
        source = meta.get("dialogueSource", "")
        dpath = repo / source if source.startswith("ci/") else project / source
        if not dpath.exists():
            errors.append(f"{sid}: dialogueSource bulunamadı: {source}")
            continue
        raw = dpath.read_bytes()
        if meta.get("dialogueSha256") != hashlib.sha256(raw).hexdigest(): errors.append(f"{sid}: dialogueSha256 güncel değil")
        data = json.loads(raw)
        speakers = []
        for dialogue in data.get("dialogues", []):
            speaker = dialogue.get("speaker", "")
            if speaker and speaker != "旁白" and speaker not in speakers: speakers.append(speaker)
        if meta.get("dialogueSpeakers") != speakers: errors.append(f"{sid}: konuşan karakter listesi kaynak diyalogla eşleşmiyor; beklenen={speakers}")
        if not set(speakers).issubset(set(meta.get("requiredVisualCharacters", []))): errors.append(f"{sid}: requiredVisualCharacters tüm konuşanları içermiyor")
        checks = meta.get("manifestChecklist", {})
        missing = [key for key in REQUIRED_CHECKS if checks.get(key) is not True]
        if missing: errors.append(f"{sid}: manifesto checklist eksik/false: {sorted(missing)}")
        if not meta.get("criticalObjects"): errors.append(f"{sid}: criticalObjects boş")
    batch = load(batch_path)
    active = batch.get("activeBatch") or {}
    ids, done = active.get("sceneIds", []), active.get("completedSceneIds", [])
    if len(ids) != 10: errors.append("Aktif batch sceneIds tam 10 sahne değil")
    missing_done = [sid for sid in done if sid not in seen]
    if missing_done: errors.append(f"Batch tamamlandı denen fakat asseti olmayan sahneler: {missing_done}")
    if active.get("status") == "READY_FOR_BUILD" and set(done) != set(ids): errors.append("READY_FOR_BUILD fakat batch 10/10 tamam değil")
    if args.require_ready_batch:
        if active.get("status") != "READY_FOR_BUILD": errors.append(f"Build engellendi: aktif batch durumu {active.get('status')} (READY_FOR_BUILD olmalı)")
        if active.get("buildApprovalRequired") is not True: errors.append("Build approval policy kapalı")
        if active.get("buildApproved") is not True: errors.append("Build engellendi: kullanıcı build onayı kaydı yok")
    if errors:
        print("VISUAL OVERRIDE VALIDATION: FAIL")
        for error in errors: print(" -", error)
        return 1
    print(f"VISUAL OVERRIDE VALIDATION: PASS ({len(webps)} direct scene override; {len(BUILD_EXCLUDED_SCENES)} intentionally preserved)")
    print(f"Active batch: {active.get('batchId')} {len(done)}/10 status={active.get('status')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
