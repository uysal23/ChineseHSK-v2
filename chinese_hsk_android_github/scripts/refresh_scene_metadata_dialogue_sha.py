#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=None)
    args = ap.parse_args()

    project = Path(__file__).resolve().parents[1]
    repo = Path(args.repo_root).resolve() if args.repo_root else project.parent
    meta_dir = project / "visual_sources" / "scenes"

    updated = 0
    checked = 0
    errors = []

    for meta_path in sorted(meta_dir.glob("ZH_HSK*_SC*.meta.json")):
        checked += 1
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        source = meta.get("dialogueSource", "")
        if not source:
            continue

        dialogue_path = repo / source if source.startswith("ci/") else project / source
        if not dialogue_path.exists():
            errors.append(f"{meta_path.name}: dialogueSource bulunamadı: {source}")
            continue

        raw = dialogue_path.read_bytes()
        dialogue_sha = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw)

        speakers = []
        for item in data.get("dialogues", []):
            speaker = item.get("speaker", "")
            if speaker and speaker != "旁白" and speaker not in speakers:
                speakers.append(speaker)

        changed = False
        if meta.get("dialogueSha256") != dialogue_sha:
            meta["dialogueSha256"] = dialogue_sha
            changed = True
        if meta.get("dialogueSpeakers") != speakers:
            meta["dialogueSpeakers"] = speakers
            changed = True

        if changed:
            meta_path.write_text(
                json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            updated += 1

    if errors:
        print("DIALOGUE METADATA REFRESH: FAIL")
        for err in errors:
            print(" -", err)
        raise SystemExit(1)

    print(f"DIALOGUE METADATA REFRESH: PASS checked={checked} updated={updated}")

if __name__ == "__main__":
    main()
