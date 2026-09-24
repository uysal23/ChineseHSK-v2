#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json, re, sys

if len(sys.argv) != 3:
    raise SystemExit("usage: validate_dialogue_final.py <baseline-root> <candidate-root>")

base_root=Path(sys.argv[1]); cand_root=Path(sys.argv[2])
errors=[]; warnings=[]; scenes=0; turns=0
cjk=re.compile(r"[\u3400-\u9fff]")
bad_zh=[
    re.compile(r"确认一下觉得"),
    re.compile(r"是这次要考虑的重点之一"),
    re.compile(r"我们继续看下一项"),
    re.compile(r"先把医生列为优先问题"),
]
for cp in sorted(cand_root.glob("HSK*/ZH_HSK*_SC*.json")):
    c=json.loads(cp.read_text(encoding="utf-8")); level=c["level"]; sid=c["sceneId"]
    bp=base_root/level/"scenes"/f"{sid}.json"
    b=json.loads(bp.read_text(encoding="utf-8"))
    old=b.get("dialogues",[]); new=c.get("dialogues",[])
    if len(old)!=len(new):
        errors.append(f"{sid}: turn count changed"); continue
    scenes+=1
    active=[str(x.get("zh","")).strip() for x in b.get("learning",{}).get("vocabularyCards",[]) if x.get("kind")=="active"]
    joined="".join(str(x.get("zh","")) for x in new)
    for term in active:
        if term and term in "".join(str(x.get("zh","")) for x in old) and term not in joined:
            errors.append(f"{sid}: lost active vocab {term}")
    for i,(o,n) in enumerate(zip(old,new),1):
        turns+=1
        if o.get("id")!=n.get("id") or o.get("speaker")!=n.get("speaker"):
            errors.append(f"{sid}:{i}: structure changed")
        zh=str(n.get("zh","")).strip(); py=str(n.get("pinyin","")).strip(); tr=str(n.get("tr","")).strip()
        if not zh or not py or not tr: errors.append(f"{sid}:{i}: blank field")
        if cjk.search(tr): errors.append(f"{sid}:{i}: Turkish contains CJK: {tr}")
        for pat in bad_zh:
            if pat.search(zh): errors.append(f"{sid}:{i}: rejected robotic pattern: {zh}")
        if i>=94 and ("接着往下聊" in zh or "继续看下一项" in zh):
            errors.append(f"{sid}:{i}: closing reopens topic: {zh}")
    cnt=Counter(str(x.get("zh","")).strip() for x in new)
    for z,n in cnt.items():
        if n>=10:
            warnings.append(f"{sid}: repeated {n}x: {z}")

print(f"Final validation: {scenes} scenes / {turns} turns")
print(f"Warnings: {len(warnings)}")
for w in warnings[:100]: print("WARN",w)
if errors:
    for e in errors[:300]: print("ERROR",e)
    raise SystemExit(f"FAILED: {len(errors)} errors")
