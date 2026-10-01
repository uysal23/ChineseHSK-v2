#!/usr/bin/env python3
"""Generate deterministic Mandarin dialogue audio with Kokoro.

Free/offline production path:
- Kokoro-82M Mandarin (lang_code='z')
- Misaki Chinese G2P
- ffmpeg -> mono 24 kHz Opus

Input: ci/dialogue_final_v5 + ci/voice_cast_manifest.json
Output:
  <out>/files/<level>/<hash>.opus
  <out>/audio_manifest_<level>.json

Repeated utterances with identical effective voice settings are synthesized once
and reused by dialogue ID through the manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline

ROOT = Path(__file__).resolve().parents[1]
DIALOGUES = ROOT / "ci" / "dialogue_final_v5"
CAST_FILE = ROOT / "ci" / "voice_cast_manifest.json"
SAMPLE_RATE = 24000

# Large post-synthesis pitch shifts can make Mandarin voices sound synthetic and
# can damage tone perception. Keep age treatment subtle; identity should come
# primarily from the selected native Mandarin voice and speaking rate.
MAX_ABS_PITCH_SEMITONES = 1.75
MIN_ENERGY = 0.94
MAX_ENERGY = 1.06


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def normalize_tts_text(text: str) -> str:
    """Normalize typography without rewriting the authored Mandarin."""
    text = unicodedata.normalize("NFKC", text or "").strip()
    text = text.replace("...", "……")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*([，。！？；：、])\s*", r"\1", text)
    if text and text[-1] not in "。！？?!……":
        text += "。"
    return text


def load_cast():
    data = json.loads(CAST_FILE.read_text(encoding="utf-8"))
    return {x["speaker"]: x for x in data["cast"]}


def effective_profile(cast_row, level):
    base = cast_row["synthesis"]
    override = cast_row.get("levelOverrides", {}).get(level, {})
    requested_pitch = float(override.get("pitch", base.get("pitchSemitones", 0.0)))
    requested_energy = float(override.get("energy", base.get("energy", 1.0)))
    return {
        "voice": base["voice"],
        "speed": float(override.get("speed", base.get("speed", 1.0))),
        "pitchRequested": requested_pitch,
        "pitchApplied": clamp(
            requested_pitch,
            -MAX_ABS_PITCH_SEMITONES,
            MAX_ABS_PITCH_SEMITONES,
        ),
        "energyRequested": requested_energy,
        "energyApplied": clamp(requested_energy, MIN_ENERGY, MAX_ENERGY),
        "age": override.get("age", cast_row.get("ageClass", "adult")),
        "tone": cast_row.get("intendedTone", ""),
    }


def audio_key(text, profile):
    payload = json.dumps(
        {
            "text": text,
            "voice": profile["voice"],
            "speed": round(profile["speed"], 4),
            "pitch": round(profile["pitchApplied"], 4),
            "energy": round(profile["energyApplied"], 4),
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()[:20]


def result_audio(item):
    # Kokoro versions expose either a Result.audio field or tuple[2].
    audio = getattr(item, "audio", None)
    if audio is None and isinstance(item, (tuple, list)) and len(item) >= 3:
        audio = item[2]
    if audio is None:
        return None
    if hasattr(audio, "detach"):
        audio = audio.detach()
    if hasattr(audio, "cpu"):
        audio = audio.cpu()
    if hasattr(audio, "numpy"):
        audio = audio.numpy()
    return np.asarray(audio, dtype=np.float32).reshape(-1)


def synthesize(pipeline, text, profile, dest):
    chunks = []
    for item in pipeline(text, voice=profile["voice"], speed=profile["speed"]):
        audio = result_audio(item)
        if audio is not None and audio.size:
            chunks.append(audio)
    if not chunks:
        raise RuntimeError(f"Kokoro returned no audio for: {text!r}")

    waveform = np.concatenate(chunks)
    dest.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="kokoro-voice-") as td:
        wav = Path(td) / "raw.wav"
        sf.write(wav, waveform, SAMPLE_RATE, subtype="PCM_16")

        semitones = profile["pitchApplied"]
        factor = math.pow(2.0, semitones / 12.0)
        filters = []

        # Avoid needless resampling for tiny pitch changes. Kokoro's own voice
        # prosody is usually more natural than aggressive DSP.
        if abs(semitones) >= 0.35:
            filters.extend(
                [
                    f"asetrate={SAMPLE_RATE}*{factor:.8f}",
                    f"aresample={SAMPLE_RATE}",
                    f"atempo={1.0/factor:.8f}",
                ]
            )

        energy = profile["energyApplied"]
        if abs(energy - 1.0) > 0.01:
            filters.append(f"volume={energy:.5f}")

        cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav)]
        if filters:
            cmd += ["-af", ",".join(filters)]
        cmd += [
            "-map_metadata",
            "-1",
            "-ac",
            "1",
            "-ar",
            str(SAMPLE_RATE),
            "-c:a",
            "libopus",
            "-b:a",
            "24k",
            "-vbr",
            "on",
            "-application",
            "voip",
            str(dest),
        ]
        subprocess.run(cmd, check=True)


def collect(level, cast, max_items=0):
    scene_dir = DIALOGUES / level
    if not scene_dir.exists():
        raise SystemExit(f"Dialogue level not found: {scene_dir}")

    assets = {}
    unique = {}
    metadata = {}

    files = sorted(scene_dir.glob("*.json"))
    for scene_file in files:
        scene = json.loads(scene_file.read_text(encoding="utf-8"))
        for dlg in scene.get("dialogues", []):
            speaker = dlg.get("speaker", "").strip()
            authored_text = dlg.get("zh", "").strip()
            text = normalize_tts_text(authored_text)
            did = dlg.get("id", "").strip()
            if not did or not text:
                continue
            row = cast.get(speaker)
            if row is None:
                raise RuntimeError(f"No voice cast entry for speaker {speaker!r} in {did}")
            profile = effective_profile(row, level)
            key = audio_key(text, profile)
            rel = f"chinese_course/media/audio/generated/{level}/{key}.opus"
            assets[did] = rel
            unique.setdefault(key, (text, profile, speaker))
            metadata[did] = {
                "speaker": speaker,
                "voice": profile["voice"],
                "age": profile["age"],
                "tone": profile["tone"],
                "speed": profile["speed"],
                "pitchRequested": profile["pitchRequested"],
                "pitchApplied": profile["pitchApplied"],
                "energyApplied": profile["energyApplied"],
                "audioKey": key,
                "ttsText": text,
            }

    if max_items > 0:
        keep_keys = list(sorted(unique))[:max_items]
        keep = set(keep_keys)
        unique = {k: unique[k] for k in keep_keys}
        assets = {
            did: path
            for did, path in assets.items()
            if metadata[did]["audioKey"] in keep
        }
        metadata = {
            did: row
            for did, row in metadata.items()
            if row["audioKey"] in keep
        }

    return assets, unique, metadata, len(files)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", required=True, choices=[f"HSK{i}" for i in range(1, 7)])
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-items", type=int, default=0)
    ap.add_argument("--repo-id", default="hexgrad/Kokoro-82M")
    args = ap.parse_args()

    out = Path(args.out)
    cast = load_cast()
    assets, unique, metadata, scene_count = collect(args.level, cast, args.max_items)

    print(
        f"{args.level}: {len(assets)} dialogue mappings, "
        f"{len(unique)} unique synthesized utterances across {scene_count} scenes"
    )

    pipeline = KPipeline(lang_code="z", repo_id=args.repo_id, device="cpu")

    generated = 0
    for idx, (key, (text, profile, speaker)) in enumerate(
        sorted(unique.items()), start=1
    ):
        dest = out / "files" / args.level / f"{key}.opus"
        if not dest.exists() or dest.stat().st_size < 256:
            synthesize(pipeline, text, profile, dest)
            generated += 1
        if idx == 1 or idx % 100 == 0 or idx == len(unique):
            print(f"{args.level}: {idx}/{len(unique)} ready; generated={generated}")

    manifest = {
        "schemaVersion": 2,
        "engine": "Kokoro-82M",
        "productionMode": "free_offline_native_mandarin",
        "language": "zh-CN",
        "level": args.level,
        "sampleRate": SAMPLE_RATE,
        "codec": "opus",
        "bitrate": "24k",
        "postProcessing": {
            "maxAbsPitchSemitones": MAX_ABS_PITCH_SEMITONES,
            "energyRange": [MIN_ENERGY, MAX_ENERGY],
            "reason": "Preserve Mandarin tone/prosody and avoid robotic age shifting.",
        },
        "assets": assets,
        "metadata": metadata,
        "uniqueAudioCount": len(unique),
        "dialogueMappingCount": len(assets),
    }
    (out / f"audio_manifest_{args.level}.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
