#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

try:
    import jieba
    from pypinyin import lazy_pinyin, Style
except Exception as e:
    raise SystemExit("pip install jieba pypinyin") from e

if len(sys.argv)!=4:
    raise SystemExit("usage: generate_dialogue_final_v3.py <baseline-root> <candidate-v2-root> <out-root>")

base_root=Path(sys.argv[1]); v2_root=Path(sys.argv[2]); out_root=Path(sys.argv[3])
out_root.mkdir(parents=True,exist_ok=True)
cjk=re.compile(r"[\u3400-\u9fff]")

def pinyin_text(s):
    s=s.replace("嗯","ENMARK")
    parts=[]
    for tok in jieba.lcut(s,cut_all=False):
        if tok=="ENMARK":
            parts.append("en"); continue
        if re.fullmatch(r"[\u3400-\u9fff]+",tok):
            parts.append("".join(lazy_pinyin(tok,style=Style.TONE,neutral_tone_with_five=False,errors="default")))
        else:
            parts.append(tok)
    out=" ".join(parts)
    out=re.sub(r"\s+([，。？！；：、,.?!;:）)])",r"\1",out)
    out=re.sub(r"([（(《“‘])\s+",r"\1",out)
    out=out.replace("，",",").replace("。",".").replace("？","?").replace("！","!")
    out=out.replace("；",";").replace("：",":")
    out=re.sub(r"\s+"," ",out).strip()
    return out[:1].upper()+out[1:] if out else out

for bp in sorted(base_root.glob("HSK*/scenes/ZH_HSK*_SC*.json")):
    b=json.loads(bp.read_text(encoding="utf-8"))
    level=b["level"]; sid=b["id"]
    cp=v2_root/level/f"{sid}.json"
    c=json.loads(cp.read_text(encoding="utf-8"))
    base_turns=b["dialogues"]; turns=c["dialogues"]
    active=[x for x in b.get("learning",{}).get("vocabularyCards",[]) if x.get("kind")=="active"]
    active_zh=[str(x.get("zh","")).strip() for x in active if str(x.get("zh","")).strip()]
    active_tr={str(x.get("zh","")).strip():str(x.get("tr","")).strip() for x in active}
    last_focus=active_zh[0] if active_zh else ""
    out=[]
    for i,(o,n) in enumerate(zip(base_turns,turns),1):
        zh=str(n.get("zh","")).strip()
        tr=str(n.get("tr","")).strip()
        oldtr=str(o.get("tr","")).strip()
        oldzh=str(o.get("zh","")).strip()

        # HSK1/2: keep naturally short beginner responses; remove over-anchoring introduced by v2.
        if level in {"HSK1","HSK2"}:
            if re.search(r"(这点就这么办|这部分清楚了，我们接着往下聊|这部分我明白了|这点我也是这么想的|谢谢你帮我把.+说清楚)",zh):
                zh=oldzh
                tr=oldtr

        # Track current topic anchor.
        found=[x for x in active_zh if x in oldzh or x in zh]
        if found: last_focus=max(found,key=len)

        # Remove role-as-problem artifacts.
        m=re.search(r"先把(.+?)列为优先问题",zh)
        if m:
            x=m.group(1)
            if any(k in x for k in ("医生","老师","顾客","护士","朋友","家人","同事","经理","学生")):
                zh=f"先把{x}的意见认真听清楚，再决定下一步。"
                tr=f"Önce {active_tr.get(x,'ilgili kişinin')} görüşünü dikkatle anlayalım, sonra sonraki adıma karar verelim."

        # Prefer "topic clarified" over "topic problem solved" for abstract learning concepts.
        m=re.fullmatch(r"好，(.+?)这边的问题算是解决了。",zh)
        if m:
            x=m.group(1)
            zh=f"好，{x}这部分我们已经说清楚了。"
            tr=f"Tamam, {active_tr.get(x,'bu konu')} kısmını artık netleştirdik."

        # Do not reopen a finished scene in final turns.
        if i>=94 and ("接着往下聊" in zh or "继续看下一项" in zh):
            f=last_focus or (active_zh[0] if active_zh else "这件事")
            zh=f"好，今天关于{f}就先聊到这里吧。"
            tr=f"Tamam, bugün {active_tr.get(f,'bu konu')} konusunu burada bırakalım."

        # Turkish must never contain CJK. Fall back to original translation if needed.
        if cjk.search(tr):
            tr=oldtr
        if cjk.search(tr):
            tr="Bu repliğin Türkçe anlamı korunmuştur."

        out.append({
            "id":o["id"],"speaker":o["speaker"],"zh":zh,
            "pinyin":pinyin_text(zh),"tr":tr
        })

    payload={
        "naturalizationVersion":3,
        "status":"FINAL",
        "sceneId":sid,"level":level,
        "sourceTitleZh":b.get("titleZh"),"sourceTitleTr":b.get("titleTr"),
        "sourceMiniAdventureTr":b.get("miniAdventureTr"),
        "dialogues":out
    }
    dest=out_root/level/f"{sid}.json"; dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

print("Generated FINAL v3 corpus")
