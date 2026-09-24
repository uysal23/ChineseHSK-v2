#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json, re, sys

if len(sys.argv) != 3:
    raise SystemExit("usage: score_dialogue_coherence.py <baseline-root> <naturalized-root>")

base_root = Path(sys.argv[1])
new_root = Path(sys.argv[2])

ROBOTIC = [
    re.compile(r"是这次要考虑的重点之一"),
    re.compile(r"我们继续看下一项"),
    re.compile(r"确认一下觉得"),
    re.compile(r"如果.{1,10}发生变化，计划也得调整"),
    re.compile(r".{1,10}是我们不能忽略的一点"),
    re.compile(r"我们把.{1,10}也列进考虑范围吧"),
    re.compile(r"关于.{1,10}，我想再听听大家的看法"),
]
GENERIC_END = (
    "今天就先到这里", "下一步按计划", "继续看下一项", "主要问题已经",
    "按计划做", "重新评估", "充分讨论", "优先顺序"
)

results = []
for p in sorted(new_root.glob("HSK*/ZH_HSK*_SC*.json")):
    n = json.loads(p.read_text(encoding="utf-8"))
    level = n["level"]; sid = n["sceneId"]
    bp = base_root / level / "scenes" / f"{sid}.json"
    b = json.loads(bp.read_text(encoding="utf-8"))
    turns = n.get("dialogues", [])
    zh_lines = [str(x.get("zh","")).strip() for x in turns]
    joined = "".join(zh_lines)

    cards = [x for x in b.get("learning",{}).get("vocabularyCards",[]) if x.get("kind")=="active"]
    active = [str(x.get("zh","")).strip() for x in cards if str(x.get("zh","")).strip()]
    present = sum(1 for v in active if v in joined)
    active_ratio = present / max(1, len(active))

    counts = Counter(zh_lines)
    repeated_excess = sum(max(0, c-3) for c in counts.values())
    repetition_penalty = min(30, repeated_excess * 0.7)

    robotic_hits = sum(1 for z in zh_lines for pat in ROBOTIC if pat.search(z))
    robotic_penalty = min(35, robotic_hits * 2.5)

    # Topic continuity: active vocabulary or title tokens should remain visible across the scene.
    title = str(b.get("titleZh",""))
    anchors = [v for v in active if len(v)>=2]
    if len(title)>=2:
        anchors.append(title)
    windows = [zh_lines[i:i+20] for i in range(0, len(zh_lines), 20)]
    anchored_windows = 0
    for w in windows:
        t = "".join(w)
        if any(a in t for a in anchors):
            anchored_windows += 1
    continuity_ratio = anchored_windows / max(1, len(windows))

    end = "".join(zh_lines[-20:])
    end_anchor = any(a in end for a in anchors)
    generic_end_hits = sum(1 for g in GENERIC_END if g in end)

    score = 100.0
    score -= (1-active_ratio) * 30
    score -= (1-continuity_ratio) * 25
    score -= repetition_penalty
    score -= robotic_penalty
    if not end_anchor:
        score -= 10
    score -= min(10, generic_end_hits * 2)
    score = max(0.0, round(score,1))

    results.append({
        "sceneId": sid, "level": level, "score": score,
        "activeVocabularyCoverage": round(active_ratio,3),
        "topicWindowCoverage": round(continuity_ratio,3),
        "roboticHits": robotic_hits,
        "repeatedExcess": repeated_excess,
        "endHasTopicAnchor": end_anchor,
        "status": "PASS" if score >= 80 and active_ratio >= .8 and continuity_ratio >= .8 else "REWRITE"
    })

summary = {
    "sceneCount": len(results),
    "passCount": sum(1 for x in results if x["status"]=="PASS"),
    "rewriteCount": sum(1 for x in results if x["status"]=="REWRITE"),
    "averageScore": round(sum(x["score"] for x in results)/max(1,len(results)),1),
    "byLevel": {}
}
for level in sorted({x["level"] for x in results}):
    xs=[x for x in results if x["level"]==level]
    summary["byLevel"][level]={
        "scenes":len(xs),
        "pass":sum(1 for x in xs if x["status"]=="PASS"),
        "rewrite":sum(1 for x in xs if x["status"]=="REWRITE"),
        "averageScore":round(sum(x["score"] for x in xs)/len(xs),1)
    }

out = new_root / "coherence_report.json"
out.write_text(json.dumps({"summary":summary,"scenes":results},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
