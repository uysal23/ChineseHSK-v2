#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict
import json, re, sys

try:
    import jieba
    from pypinyin import lazy_pinyin, Style
except Exception as e:
    raise SystemExit("pip install jieba pypinyin") from e

if len(sys.argv) != 4:
    raise SystemExit("usage: generate_dialogue_naturalization_v2.py <baseline-root> <draft-root> <out-root>")

base_root = Path(sys.argv[1])
draft_root = Path(sys.argv[2])
out_root = Path(sys.argv[3])
out_root.mkdir(parents=True, exist_ok=True)

# Exact-source corpus frequencies help identify boilerplate.
freq = Counter()
for p in sorted(base_root.glob("HSK*/scenes/ZH_HSK*_SC*.json")):
    d=json.loads(p.read_text(encoding="utf-8"))
    for x in d.get("dialogues",[]): freq[str(x.get("zh","")).strip()] += 1

PERSON_TERMS = {
    "医生","老师","顾客","家人","朋友","同事","经理","护士","学生","邻居","爷爷","奶奶",
    "爸爸","妈妈","孩子","员工","服务员","店员","司机","律师","导游","老板","同学"
}

def pinyin_text(s):
    # Phrase segmentation avoids one-character-per-syllable display.
    s=s.replace("嗯","ENMARK")
    pieces=[]
    for token in jieba.lcut(s, cut_all=False):
        if token=="ENMARK":
            pieces.append("en")
            continue
        if not token:
            continue
        if re.fullmatch(r"[\u3400-\u9fff]+", token):
            pys=lazy_pinyin(token, style=Style.TONE, neutral_tone_with_five=False, errors="default")
            pieces.append("".join(pys))
        else:
            pieces.append(token)
    out=" ".join(pieces)
    out=re.sub(r"\s+([，。？！；：、,.?!;:）)])",r"\1",out)
    out=re.sub(r"([（(《“‘])\s+",r"\1",out)
    out=out.replace("，",",").replace("。",".").replace("？","?").replace("！","!")
    out=out.replace("；",";").replace("：",":")
    out=re.sub(r"\s+"," ",out).strip()
    if out:
        out=out[0].upper()+out[1:]
    return out

def pick_focus(active, original_zh, last_focus, index):
    # Prefer explicit active vocabulary in this or previous content.
    matches=[z for z,_ in active if z and z in original_zh]
    if matches:
        return max(matches,key=len)
    if last_focus:
        return last_focus
    if active:
        return active[(index//4)%len(active)][0]
    return ""

def tr_for(active, focus):
    for z,t in active:
        if z==focus: return t
    return focus

def is_person(term):
    return term in PERSON_TERMS or any(x in term for x in ("老师","医生","顾客","经理","同事","家人","朋友","学生","员工"))

def anchored(level, old, draft, focus, focus_tr, idx, scene_title):
    # Keep already scene-specific lines unless they match known boilerplate.
    repetitive = freq.get(old,0) >= 20
    robotic = bool(re.search(
        r"(是这次要考虑的重点之一|我们继续看下一项|确认一下觉得|如果.{1,12}发生变化，计划也得调整|"
        r".{1,12}是我们不能忽略的一点|我们把.{1,12}也列进考虑范围吧|关于.{1,12}，我想再听听大家的看法)",
        old
    ))
    if not repetitive and not robotic:
        return draft, None

    f=focus or "这件事"
    ft=focus_tr or "bu konu"

    # Universal response/continuation patterns.
    exact = {
        "我明白了。": (f"嗯，{f}这部分我明白了。", f"Anladım; {ft} kısmı şimdi daha net."),
        "我明白你的意思了。": (f"嗯，说到{f}，我明白你的意思了。", f"Evet, {ft} konusunda ne demek istediğini anladım."),
        "我也是。": (f"嗯，{f}这点我也是这么想的。", f"Evet, {ft} konusunda ben de aynı düşünüyorum."),
        "说得对。": (f"对，{f}这点你说得对。", f"Evet, {ft} konusunda haklısın."),
        "这个很实用。": (f"嗯，{f}这点确实很实用。", f"Evet, {ft} gerçekten işe yarar."),
        "这个我记住了。": (f"好，{f}这点我记住了。", f"Tamam, {ft} konusunu aklımda tutacağım."),
        "现在更清楚了。": (f"嗯，{f}这部分现在清楚多了。", f"Evet, {ft} kısmı şimdi çok daha net."),
        "好，这一点我会注意。": (f"好，{f}这点我会注意。", f"Tamam, {ft} konusuna dikkat edeceğim."),
        "这个安排比较实际。": (f"这样安排{f}，确实比较实际。", f"{ft} konusunu böyle düzenlemek gerçekten daha uygulanabilir."),
        "我觉得可以接受。": (f"如果是这样安排{f}，我觉得可以接受。", f"{ft} böyle düzenlenecekse bence kabul edilebilir."),
        "这样的话就清楚多了。": (f"这么一说，{f}这部分就清楚多了。", f"Böyle açıklayınca {ft} kısmı çok daha net oldu."),
        "这一点我同意。": (f"说到{f}，这一点我同意。", f"{ft} konusunda buna katılıyorum."),
        "这个角度我刚才没有想到。": (f"从{f}这个角度看，我刚才确实没想到。", f"{ft} açısından bakınca bunu az önce düşünmemiştim."),
        "那确实需要重新考虑。": (f"如果涉及{f}，那确实得重新考虑一下。", f"{ft} devreye giriyorsa bunu yeniden düşünmek gerekir."),
        "听起来比较合理。": (f"这样处理{f}，听起来比较合理。", f"{ft} konusunu böyle ele almak daha mantıklı geliyor."),
        "这个信息很关键。": (f"对，{f}这条信息很关键。", f"Evet, {ft} hakkındaki bu bilgi çok önemli."),
        "这样解释以后，我更理解你的立场了。": (f"你这么解释{f}以后，我更理解你的想法了。", f"{ft} konusunu böyle açıklayınca düşünceni daha iyi anladım."),
        "这一点值得继续确认。": (f"对，{f}这点还值得再确认一下。", f"Evet, {ft} konusunu biraz daha doğrulamak gerekiyor."),
        "我觉得这个建议比较稳妥。": (f"关于{f}，我觉得这个建议比较稳妥。", f"{ft} konusunda bu öneri bana daha güvenli geliyor."),
        "我同意先把它列为优先问题。": (f"我同意，先把{f}列为优先问题。", f"Katılıyorum; önce {ft} konusunu öncelik yapalım."),
        "这个角度会影响最后的判断。": (f"{f}这个角度会影响最后的判断。", f"{ft} açısından bakmak son değerlendirmeyi etkiler."),
        "我们也要看看有没有反面的证据。": (f"关于{f}，我们也得看看有没有相反的情况。", f"{ft} konusunda tersini gösteren durumlar var mı ona da bakalım."),
        "先记下来，等信息完整一点再决定。": (f"先把{f}记下来，等信息更完整一点再决定。", f"{ft} konusunu not edelim; bilgi tamamlanınca karar veririz."),
    }
    if old in exact:
        return exact[old]

    # Common generated template repairs.
    m=re.fullmatch(r"(.+?)是这次要考虑的重点之一。", old)
    if m:
        x=m.group(1); return (f"说到{x}，这确实是我们现在要认真考虑的一点。", f"{x} konusunda, bunu şu anda ciddi biçimde değerlendirmemiz gerekiyor.")
    m=re.fullmatch(r"关于(.+?)，我们还要再讨论一下。", old)
    if m:
        x=m.group(1); return (f"说到{x}，我觉得我们还得再聊一聊。", f"{x} konusunda biraz daha konuşmamız gerekiyor.")
    m=re.fullmatch(r"如果(.+?)没有问题，我们就继续。", old)
    if m:
        x=m.group(1); return (f"先把{x}确认好，没问题我们再继续。", f"Önce {x} konusunu netleştirelim; sorun yoksa devam ederiz.")
    m=re.fullmatch(r"我们最好再确认一下(.+?)。", old)
    if m:
        x=m.group(1)
        if x in {"觉得","需要","同意","决定"}: x=f
        return (f"{x}这部分我们最好再确认一下。", f"{x} kısmını bir kez daha doğrulasak iyi olur.")
    m=re.fullmatch(r"(.+?)是我们不能忽略的一点。", old)
    if m:
        x=m.group(1)
        if is_person(x):
            return (f"{x}的意见也不能忽略。", f"{x} görüşünü de göz ardı etmemeliyiz.")
        return (f"{x}这一点也不能忽略。", f"{x} konusunu da göz ardı etmemeliyiz.")
    m=re.fullmatch(r"我们把(.+?)也列进考虑范围吧。", old)
    if m:
        x=m.group(1)
        if is_person(x):
            return (f"那把{x}的意见也考虑进去吧。", f"O zaman {x} görüşünü de hesaba katalım.")
        return (f"那把{x}也一起考虑进去吧。", f"O zaman {x} konusunu da birlikte değerlendirelim.")
    m=re.fullmatch(r"如果(.+?)发生变化，计划也得调整。", old)
    if m:
        x=m.group(1)
        if is_person(x):
            return (f"如果{x}那边有新的情况，我们的安排也得跟着调整。", f"{x} tarafında yeni bir durum olursa planımızı da ayarlamamız gerekir.")
        return (f"如果{x}有变化，我们的安排也得及时调整。", f"{x} değişirse planımızı da zamanında güncellememiz gerekir.")
    m=re.fullmatch(r"关于(.+?)，我想再听听大家的看法。", old)
    if m:
        x=m.group(1); return (f"说到{x}，大家还有什么想法？", f"{x} konusunda başka ne düşünüyorsunuz?")

    # Focus-aware smoothing for high-frequency boilerplate.
    if repetitive:
        if old.endswith("？"):
            return draft, None
        if old in {"好。","好的。","对。"}:
            return (f"嗯，{f}这点就这么办。", f"Tamam, {ft} konusunda böyle yapalım.")
        if "继续" in old:
            return (f"好，{f}这部分清楚了，我们接着往下聊。", f"Tamam, {ft} kısmı netleşti; devam edelim.")
        if "谢谢" in old:
            return (f"好，谢谢你帮我把{f}说清楚。", f"Tamam, {ft} konusunu netleştirmeme yardım ettiğin için teşekkürler.")
        if "放心" in old:
            return (f"这样一来，{f}这部分我就放心多了。", f"Böylece {ft} konusunda çok daha rahatladım.")
        if "问题" in old and "解决" in old:
            return (f"好，{f}这边的问题算是解决了。", f"Tamam, {ft} tarafındaki sorun çözülmüş sayılır.")
        if "计划" in old:
            return (f"那{f}这部分就按现在的安排继续。", f"O halde {ft} kısmında mevcut plana göre devam edelim.")
    return draft, None

report=defaultdict(lambda:{"scenes":0,"turns":0,"changed":0})
for bp in sorted(base_root.glob("HSK*/scenes/ZH_HSK*_SC*.json")):
    base=json.loads(bp.read_text(encoding="utf-8"))
    level=base["level"]; sid=base["id"]
    dp=draft_root/level/f"{sid}.json"
    draft=json.loads(dp.read_text(encoding="utf-8"))
    active=[(str(x.get("zh","")).strip(),str(x.get("tr","")).strip()) for x in base.get("learning",{}).get("vocabularyCards",[]) if x.get("kind")=="active"]
    last_focus=""
    out=[]
    changed=0
    source=base.get("dialogues",[])
    draft_turns=draft.get("dialogues",[])
    for i,(o,d) in enumerate(zip(source,draft_turns)):
        old=str(o.get("zh","")).strip()
        dz=str(d.get("zh","")).strip()
        focus=pick_focus(active, old, last_focus, i)
        if focus: last_focus=focus
        ft=tr_for(active,focus)
        nz,ntr=anchored(level,old,dz,focus,ft,i,base.get("titleZh",""))
        if ntr is None: ntr=str(d.get("tr","")).strip()
        if nz!=old: changed+=1
        out.append({
            "id":o["id"],"speaker":o["speaker"],"zh":nz,
            "pinyin":pinyin_text(nz),"tr":ntr
        })
    payload={
        "naturalizationVersion":2,"status":"FINAL_CANDIDATE",
        "sceneId":sid,"level":level,
        "sourceTitleZh":base.get("titleZh"),"sourceTitleTr":base.get("titleTr"),
        "sourceMiniAdventureTr":base.get("miniAdventureTr"),
        "dialogues":out
    }
    dest=out_root/level/f"{sid}.json"; dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report[level]["scenes"]+=1; report[level]["turns"]+=len(out); report[level]["changed"]+=changed

summary={"sceneCount":sum(v["scenes"] for v in report.values()),"turnCount":sum(v["turns"] for v in report.values()),"levels":dict(sorted(report.items()))}
(out_root/"generation_report.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=False))
