#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re,sys

try:
    import jieba
    from pypinyin import lazy_pinyin, Style
except Exception as e:
    raise SystemExit("pip install jieba pypinyin") from e

if len(sys.argv)!=4:
    raise SystemExit("usage: generate_dialogue_final_v5.py <baseline-root> <v4-root> <out-root>")

base_root=Path(sys.argv[1]); v4_root=Path(sys.argv[2]); out_root=Path(sys.argv[3])
out_root.mkdir(parents=True,exist_ok=True)
CJK_RE=re.compile(r"[\u3400-\u9fff]")

def pick(opts,key):
    h=int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:8],16)
    return opts[h%len(opts)]

def pinyin_text(s):
    s=s.replace("嗯","ENMARK")
    parts=[]
    for tok in jieba.lcut(s,cut_all=False):
        if tok=="ENMARK": parts.append("en"); continue
        if re.fullmatch(r"[\u3400-\u9fff]+",tok):
            parts.append("".join(lazy_pinyin(tok,style=Style.TONE,neutral_tone_with_five=False,errors="default")))
        else: parts.append(tok)
    out=" ".join(parts)
    out=re.sub(r"\s+([，。？！；：、,.?!;:）)])",r"\1",out)
    out=re.sub(r"([（(《“‘])\s+",r"\1",out)
    out=out.replace("，",",").replace("。",".").replace("？","?").replace("！","!")
    out=out.replace("；",";").replace("：",":")
    out=re.sub(r"\s+"," ",out).strip()
    return out[:1].upper()+out[1:] if out else out

def hsk1_variant(zh,tr,key):
    exact={
      "谢谢。":[("谢谢。",tr),("好，谢谢。",tr),("谢谢你。",tr),("嗯，谢谢。",tr)],
      "谢谢你。":[("谢谢你。",tr),("真的谢谢你。",tr),("好，谢谢你。",tr)],
      "我明白了。":[("我明白了。",tr),("明白了。",tr),("好，我知道了。",tr),("嗯，知道了。",tr)],
      "好的。":[("好的。",tr),("好。",tr),("嗯，好。",tr),("行。",tr)],
      "好。":[("好。",tr),("嗯，好。",tr),("行。",tr),("好的。",tr)],
      "对。":[("对。",tr),("嗯，对。",tr),("是的。",tr)],
      "我也是。":[("我也是。",tr),("嗯，我也是。",tr),("我也一样。",tr)],
      "准备好了吗？":[("准备好了吗？",tr),("都准备好了吗？",tr),("准备得怎么样了？",tr)],
      "准备好了。":[("准备好了。",tr),("嗯，准备好了。",tr),("都准备好了。",tr)],
      "我们继续。":[("我们继续。",tr),("好，继续吧。",tr),("那我们接着来。",tr)],
      "太好了！":[("太好了！",tr),("真好！",tr),("太棒了！",tr)],
      "没关系。":[("没关系。",tr),("没事。",tr),("没关系，别急。",tr)],
      "很好看。":[("很好看。",tr),("嗯，挺好看。",tr),("我也觉得好看。",tr)],
      "喜欢。":[("喜欢。",tr),("嗯，喜欢。",tr),("我喜欢。",tr)],
    }
    if zh in exact:return pick(exact[zh],key)

    m=re.fullmatch(r"这是(.+)吗？",zh)
    if m:
      x=m.group(1)
      opts=[f"这是{x}吗？",f"这个是{x}，对吗？",f"这是{x}吧？"]
      return pick([(z,tr) for z in opts],key)

    m=re.fullmatch(r"对，这是(.+)。",zh)
    if m:
      x=m.group(1)
      opts=[f"对，这是{x}。",f"没错，是{x}。",f"嗯，这就是{x}。"]
      return pick([(z,tr) for z in opts],key)

    m=re.fullmatch(r"(.+)在哪儿？",zh)
    if m:
      x=m.group(1)
      opts=[f"{x}在哪儿？",f"{x}呢？",f"你看到{x}了吗？"]
      return pick([(z,tr) for z in opts],key)

    m=re.fullmatch(r"(.+)在这里。",zh)
    if m:
      x=m.group(1)
      opts=[f"{x}在这里。",f"就在这里。",f"你看，{x}在这儿。"]
      return pick([(z,tr) for z in opts],key)

    m=re.fullmatch(r"(.+)在那边。",zh)
    if m:
      x=m.group(1)
      opts=[f"{x}在那边。",f"就在那边。",f"你看，{x}在那边。"]
      return pick([(z,tr) for z in opts],key)

    m=re.fullmatch(r"你喜欢(.+)吗？",zh)
    if m:
      x=m.group(1)
      opts=[f"你喜欢{x}吗？",f"{x}你喜欢吗？",f"你觉得{x}怎么样？"]
      return pick([(z,tr) for z in opts],key)

    m=re.fullmatch(r"这个是(.+)的。",zh)
    if m:
      x=m.group(1)
      opts=[f"这个是{x}的。",f"对，这个是{x}的。",f"你看，这是{x}的。"]
      return pick([(z,tr) for z in opts],key)

    return zh,tr

def hsk5_category(title,active):
    text=title+" "+" ".join(active)
    if any(k in text for k in ["健康","医生","医院","预防保健","血压","运动","照护","生活方式"]): return "health"
    if any(k in text for k in ["项目","客户","工作","职业","实习","面试","简历","领导","截止日期","公平","排班","制度","申诉","管理","调查","证据","客观"]): return "work"
    if any(k in text for k in ["咖啡馆","生意","价格","成本","商户","营业额","塑料用品"]): return "business"
    if any(k in text for k in ["家人","伴侣","婚","恋爱","隐私","奶奶","爷爷","一代人","代际"]): return "family"
    if any(k in text for k in ["社区","公益","募捐","志愿者","城市规划","道路施工","公共服务"]): return "community"
    if any(k in text for k in ["退休","人生","价值观","陪伴","往事","遗憾","提前退休"]): return "reflection"
    if any(k in text for k in ["大学","学习","挂科","学业","毕业","数字媒体","假消息"]): return "education"
    return "general"

def translate_focus(trmap,focus):
    return trmap.get(focus,focus)

def align_hsk5(cat,zh,tr,trmap):
    # Align Turkish with category-specific Chinese generated in v4.
    m=re.fullmatch(r"说到(.+?)，最近实际做得怎么样？",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda son zamanlarda işler gerçekte nasıl gidiyor?"
    m=re.fullmatch(r"(.+?)这点必须认真对待。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunu ciddiye almak gerekiyor."
    m=re.fullmatch(r"关于(.+?)，我们还得看看最近有没有改善。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda son zamanlarda iyileşme olup olmadığına da bakmalıyız."
    m=re.fullmatch(r"先把(.+?)的建议记下来，再看看哪些地方最需要改。",zh)
    if m:
      f=m.group(1); return zh,f"Önce {translate_focus(trmap,f)} önerilerini not edelim; sonra en çok neyi değiştirmemiz gerektiğine bakalım."
    m=re.fullmatch(r"好，今天关于(.+?)就先说到这里，接下来按建议去做。",zh)
    if m:
      f=m.group(1); return zh,f"Tamam, bugün {translate_focus(trmap,f)} konusunu burada bırakalım; şimdi önerileri uygulayalım."

    m=re.fullmatch(r"说到(.+?)，现在最现实的问题是什么？",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda şu anda en gerçekçi sorun ne?"
    m=re.fullmatch(r"(.+?)这一点会直接影响接下来的安排。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} sonraki planı doğrudan etkileyecek."
    m=re.fullmatch(r"关于(.+?)，还得看看执行上会不会有别的问题。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda uygulamada başka sorun çıkıp çıkmayacağına da bakmalıyız."
    m=re.fullmatch(r"好，(.+?)这部分先按今天说的方案推进。",zh)
    if m:
      f=m.group(1); return zh,f"Tamam, {translate_focus(trmap,f)} kısmında bugün konuştuğumuz plana göre ilerleyelim."

    m=re.fullmatch(r"说到(.+?)，顾客和成本两边都得一起看。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda hem müşteriyi hem maliyeti birlikte düşünmeliyiz."
    m=re.fullmatch(r"(.+?)会直接影响实际经营，不能忽略。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} işletmeyi doğrudan etkiler; göz ardı edemeyiz."

    m=re.fullmatch(r"说到(.+?)，你自己最在意的是什么？",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda senin için en önemli olan ne?"
    m=re.fullmatch(r"(.+?)这件事还是要尊重每个人的感受。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda herkesin duygusuna saygı duymak gerekir."

    m=re.fullmatch(r"说到(.+?)，对社区里的人会有什么实际影响？",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} mahalledeki insanları pratikte nasıl etkiler?"
    m=re.fullmatch(r"(.+?)对大家的实际影响不能忽略。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunun insanlar üzerindeki gerçek etkisini göz ardı edemeyiz."

    m=re.fullmatch(r"说到(.+?)，你现在最真实的感受是什么？",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda şu anda gerçekten ne hissediyorsun?"
    m=re.fullmatch(r"(.+?)这件事对我们来说确实很重要。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} bizim için gerçekten önemli."

    m=re.fullmatch(r"说到(.+?)，现在最需要改进的是什么？",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} konusunda şimdi en çok neyi geliştirmek gerekiyor?"
    m=re.fullmatch(r"(.+?)会影响后面的学习安排，不能忽略。",zh)
    if m:
      f=m.group(1); return zh,f"{translate_focus(trmap,f)} sonraki öğrenme planını etkiler; göz ardı edemeyiz."
    return zh,tr

for bp in sorted(base_root.glob("HSK*/scenes/ZH_HSK*_SC*.json")):
    b=json.loads(bp.read_text(encoding="utf-8"))
    level=b["level"];sid=b["id"];title=b.get("titleZh","")
    v4=json.loads((v4_root/level/f"{sid}.json").read_text(encoding="utf-8"))
    cards=[x for x in b.get("learning",{}).get("vocabularyCards",[]) if x.get("kind")=="active"]
    trmap={str(x.get("zh","")).strip():str(x.get("tr","")).strip() for x in cards}
    active=list(trmap.keys())
    cat=hsk5_category(title,active) if level=="HSK5" else v4.get("sceneCategory","other")
    out=[]
    for i,(o,n) in enumerate(zip(b["dialogues"],v4["dialogues"]),1):
      zh=str(n["zh"]).strip();tr=str(n["tr"]).strip()
      key=f"{sid}:{i}:{zh}"
      if level=="HSK1":
        zh,tr=hsk1_variant(zh,tr,key)
      if level=="HSK5":
        zh,tr=align_hsk5(cat,zh,tr,trmap)
      if CJK_RE.search(tr):
        tr=str(o.get("tr","")).strip()
      out.append({"id":o["id"],"speaker":o["speaker"],"zh":zh,"pinyin":pinyin_text(zh),"tr":tr})
    payload={
      "naturalizationVersion":5,"status":"FINAL",
      "sceneId":sid,"level":level,"sceneCategory":cat,
      "sourceTitleZh":b.get("titleZh"),"sourceTitleTr":b.get("titleTr"),
      "sourceMiniAdventureTr":b.get("miniAdventureTr"),"dialogues":out
    }
    dest=out_root/level/f"{sid}.json";dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Generated FINAL v5")
