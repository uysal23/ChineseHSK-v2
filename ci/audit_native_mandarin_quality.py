#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--scene-root", default=str(ROOT / "chinese_hsk_android_github" / "app" / "src" / "main" / "assets" / "chinese_course" / "levels"))
parser.add_argument("--out-prefix", default="native_mandarin_qa_report")
args = parser.parse_args()
SCENE_ROOT = Path(args.scene_root)
OUT_JSON = ROOT / (args.out_prefix + ".json")
OUT_MD = ROOT / (args.out_prefix + ".md")

GENERIC_PATTERNS = [
    r"^关于.+，我想再听听大家的看法。$",
    r"^.+是我们不能忽略的一点。$",
    r"^我们把.+也列进考虑范围吧。$",
    r"^如果.+发生变化，计划也得调整。$",
    r"^.+之所以重要，是因为它会影响我们接下来怎么理解这件事。$",
    r"^如果忽略.+，很多看似合理的判断其实会失去依据。$",
    r"^我想把.+放回具体语境里看，这样更容易理解彼此的选择。$",
    r"^谈到.+，我更关心的是它背后的意义，而不只是表面的结果。$",
    r"^我同意先把它列为优先问题。$",
    r"^这个角度会影响最后的判断。$",
    r"^我们也要看看有没有反面的证据。$",
    r"^先记下来，等信息完整一点再决定。$",
    r"^我明白你的意思了。$",
    r"^好，这一点我会注意。$",
    r"^这一点我同意。$",
    r"^这个角度我刚才没有想到。$",
    r"^那确实需要重新考虑。$",
    r"^听起来比较合理。$",
]

SEMANTICALLY_AWKWARD = [
    r"如果独立发生变化",
    r"如果优势发生变化",
    r"如果调整状态发生变化",
    r"如果自我评价发生变化",
    r"如果祝福发生变化",
    r"如果语境发生变化",
    r"如果立场发生变化",
    r"如果权衡发生变化",
    r"把语境放回具体语境",
]

def han_len(text: str) -> int:
    return sum(1 for ch in text if "\u3400" <= ch <= "\u9fff")

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def active_vocab(scene: dict) -> list[str]:
    cards = scene.get("learning", {}).get("vocabularyCards", [])
    return [x.get("zh", "").strip() for x in cards if x.get("zh", "").strip() and x.get("kind") == "active"]

scene_rows = []
global_phrase_counts = Counter()
level_stats = defaultdict(lambda: {
    "scenes": 0, "fail": 0, "warn": 0, "pass": 0,
    "dialogues": 0, "duplicates": 0, "generic": 0, "awkward": 0,
})

for level_num in range(1, 7):
    level = f"HSK{level_num}"
    scene_dir = SCENE_ROOT / level
    if (scene_dir / "scenes").exists():
        scene_dir = scene_dir / "scenes"
    for path in sorted(scene_dir.glob(f"ZH_{level}_SC*.json")):
        scene = read_json(path)
        ds = scene.get("dialogues", [])
        zh = [d.get("zh", "").strip() for d in ds if d.get("zh", "").strip()]
        counts = Counter(zh)
        global_phrase_counts.update(zh)

        unique_count = len(counts)
        duplicate_lines = sum(c - 1 for c in counts.values() if c > 1)
        duplicate_ratio = duplicate_lines / len(zh) if zh else 1.0
        max_repeat = max(counts.values()) if counts else 0

        generic_hits = []
        for d in ds:
            text = d.get("zh", "").strip()
            if any(re.match(p, text) for p in GENERIC_PATTERNS):
                generic_hits.append({"id": d.get("id"), "speaker": d.get("speaker"), "zh": text})
        generic_ratio = len(generic_hits) / len(ds) if ds else 1.0

        awkward_hits = []
        for d in ds:
            text = d.get("zh", "").strip()
            if any(re.search(p, text) for p in SEMANTICALLY_AWKWARD):
                awkward_hits.append({"id": d.get("id"), "speaker": d.get("speaker"), "zh": text})

        vocab = active_vocab(scene)
        topic_lines = 0
        if vocab:
            topic_lines = sum(1 for text in zh if any(v in text for v in vocab))
        topic_ratio = topic_lines / len(zh) if zh and vocab else None

        lengths = [han_len(x) for x in zh]
        avg_han = round(sum(lengths) / len(lengths), 2) if lengths else 0

        repeated_examples = [
            {"zh": phrase, "count": count}
            for phrase, count in counts.most_common(12)
            if count > 1
        ]

        if level == "HSK1":
            fail_dup, warn_dup = 0.32, 0.18
        elif level == "HSK2":
            fail_dup, warn_dup = 0.24, 0.14
        else:
            fail_dup, warn_dup = 0.18, 0.10

        fail = (
            duplicate_ratio >= fail_dup
            or generic_ratio >= 0.22
            or len(awkward_hits) >= 2
            or max_repeat >= 8
        )
        warn = (
            not fail and (
                duplicate_ratio >= warn_dup
                or generic_ratio >= 0.10
                or len(awkward_hits) == 1
                or max_repeat >= 4
            )
        )
        status = "FAIL" if fail else "WARN" if warn else "PASS"

        row = {
            "sceneId": scene.get("id"),
            "level": level,
            "titleZh": scene.get("titleZh"),
            "titleTr": scene.get("titleTr"),
            "dialogueCount": len(ds),
            "uniqueZh": unique_count,
            "duplicateLines": duplicate_lines,
            "duplicateRatio": round(duplicate_ratio, 4),
            "maxExactRepeat": max_repeat,
            "genericTemplateHits": len(generic_hits),
            "genericTemplateRatio": round(generic_ratio, 4),
            "awkwardSlotHits": awkward_hits,
            "activeVocabulary": vocab,
            "topicVocabularyLineRatio": round(topic_ratio, 4) if topic_ratio is not None else None,
            "averageHanCharactersPerLine": avg_han,
            "repeatedExamples": repeated_examples,
            "genericExamples": generic_hits[:12],
            "status": status,
        }
        scene_rows.append(row)

        st = level_stats[level]
        st["scenes"] += 1
        st["dialogues"] += len(ds)
        st["duplicates"] += duplicate_lines
        st["generic"] += len(generic_hits)
        st["awkward"] += len(awkward_hits)
        st[status.lower()] += 1

top_global = [{"zh": phrase, "count": count} for phrase, count in global_phrase_counts.most_common(60)]

summary = {
    "method": {
        "scope": "All 300 scene JSON files / 30,000 dialogue lines",
        "focus": [
            "exact repetition",
            "slot-filled generic templates",
            "known semantically awkward slot substitutions",
            "topic vocabulary grounding",
            "per-level naturalness thresholds"
        ],
        "note": "Automated corpus-wide gate; final native-language judgment also includes targeted review of flagged scenes."
    },
    "totals": {
        "scenes": len(scene_rows),
        "dialogues": sum(x["dialogueCount"] for x in scene_rows),
        "pass": sum(x["status"] == "PASS" for x in scene_rows),
        "warn": sum(x["status"] == "WARN" for x in scene_rows),
        "fail": sum(x["status"] == "FAIL" for x in scene_rows)
    },
    "byLevel": dict(level_stats),
    "topRepeatedPhrasesAcrossCourse": top_global,
    "scenes": scene_rows
}
OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

md = []
md.append("# Native Mandarin QA — 300 Sahne / 30.000 Replik")
md.append("")
md.append(f"- PASS: {summary['totals']['pass']}")
md.append(f"- WARN: {summary['totals']['warn']}")
md.append(f"- FAIL: {summary['totals']['fail']}")
md.append("")
md.append("| Seviye | Sahne | PASS | WARN | FAIL | Exact tekrar | Generic kalıp | Awkward slot |")
md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for level, st in sorted(level_stats.items()):
    md.append(
        f"| {level} | {st['scenes']} | {st['pass']} | {st['warn']} | {st['fail']} | "
        f"{st['duplicates']} | {st['generic']} | {st['awkward']} |"
    )
md.append("")
md.append("## FAIL sahneleri")
md.append("")
for row in scene_rows:
    if row["status"] == "FAIL":
        md.append(
            f"- **{row['sceneId']} — {row['titleZh']}**: "
            f"duplicate={row['duplicateRatio']:.1%}, "
            f"generic={row['genericTemplateRatio']:.1%}, "
            f"maxRepeat={row['maxExactRepeat']}, awkward={len(row['awkwardSlotHits'])}"
        )
md.append("")
md.append("## En sık tekrarlanan kurs geneli ifadeler")
md.append("")
for x in top_global[:30]:
    md.append(f"- {x['count']}x {x['zh']}")
OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

print(json.dumps(summary["totals"], ensure_ascii=False))
print(json.dumps(summary["byLevel"], ensure_ascii=False))
