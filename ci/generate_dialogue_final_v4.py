#!/usr/bin/env python3
from pathlib import Path
import json,re,sys

try:
    import jieba
    from pypinyin import lazy_pinyin, Style
except Exception as e:
    raise SystemExit("pip install jieba pypinyin") from e

if len(sys.argv)!=4:
    raise SystemExit("usage: generate_dialogue_final_v4.py <baseline-root> <v3-root> <out-root>")

base_root=Path(sys.argv[1]); v3_root=Path(sys.argv[2]); out_root=Path(sys.argv[3])
out_root.mkdir(parents=True,exist_ok=True)

PERSON={"医生","老师","顾客","护士","朋友","家人","同事","经理","学生","员工","邻居","爷爷","奶奶"}

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

def category_hsk1(title, active):
    text=title+" "+" ".join(active)
    if any(k in text for k in ["丢失","找","钥匙","包裹"]): return "lost"
    if any(k in text for k in ["火车","站台","车站","出租车","公交车","路"]): return "travel"
    if any(k in text for k in ["早餐","早饭","午饭","超市","蛋糕","茶","饭","冰淇淋"]): return "food"
    if any(k in text for k in ["学校","高中","班级","铅笔","考试","老师","学生","画"]): return "school"
    if any(k in text for k in ["工作","面试","同事","工资","上班","办公室"]): return "work"
    if any(k in text for k in ["猫","兽医","宠物"]): return "pet"
    if any(k in text for k in ["公园","雨","天气"]): return "weather"
    if any(k in text for k in ["邻居","做客","社区","活动"]): return "social"
    if any(k in text for k in ["家","箱子","门","房间","全家福"]): return "home"
    return "general"

def category_hsk5(title, active):
    text=title+" "+" ".join(active)
    if any(k in text for k in ["健康","医生","医院","预防保健","血压","运动","照护","生活方式"]): return "health"
    if any(k in text for k in ["项目","客户","工作","职业","实习","面试","简历","领导","截止日期"]): return "work"
    if any(k in text for k in ["咖啡馆","生意","价格","成本","商户","营业额","塑料用品"]): return "business"
    if any(k in text for k in ["家人","伴侣","婚","恋爱","隐私","奶奶","爷爷","一代人","代际"]): return "family"
    if any(k in text for k in ["社区","公益","募捐","志愿者","城市规划","道路施工","公共服务"]): return "community"
    if any(k in text for k in ["退休","人生","价值观","陪伴","往事","遗憾","提前退休"]): return "reflection"
    if any(k in text for k in ["大学","学习","挂科","学业","毕业","数字媒体","假消息"]): return "education"
    return "general"

def nonperson_focus(active):
    for z in active:
        if z not in PERSON and not any(p in z for p in PERSON):
            return z
    return active[0] if active else "这件事"

def active_tr_map(cards):
    return {str(x.get("zh","")).strip():str(x.get("tr","")).strip() for x in cards}

def hsk1_repair(cat, zh, tr, focus, focus_tr, i):
    # Remove off-topic textbook social blocks while keeping beginner language short.
    if cat=="lost":
        table={
            "这是我们的学生。":("那个学生也来帮忙找。","O öğrenci de aramaya yardım ediyor."),
            "这是我们的老师。":("老师也过来帮忙了。","Öğretmen de yardıma geldi."),
            "你好！":("找到了吗？","Buldunuz mu?"),
            "很高兴认识你。":("还没有，我们再看看。","Henüz değil, biraz daha bakalım."),
            "我也是。":("我也来帮忙。","Ben de yardım edeyim."),
            "今天学了很多。":("总算找到了。","Sonunda bulduk."),
            "都好了吗？":("东西都找齐了吗？","Her şeyi bulduk mu?"),
            "都好了。":("嗯，都找齐了。","Evet, hepsini bulduk."),
        }
        if zh in table:return table[zh]
    if cat=="school":
        table={
            "这是我们的学生。":("这是我们班的学生。","Bu bizim sınıftan bir öğrenci."),
            "这是我们的老师。":("老师也在教室里。","Öğretmen de sınıfta."),
            "很高兴认识你。":("以后一起学习吧。","Bundan sonra birlikte çalışalım."),
            "我也是。":("好啊。","Olur."),
            "今天学了很多。":("今天学得不错。","Bugün iyi çalıştık."),
        }
        if zh in table:return table[zh]
    if cat=="work":
        table={
            "这是我们的朋友。":("这个朋友也知道工作的情况。","Bu arkadaş da işin durumunu biliyor."),
            "你好！":("你好，我想问一下工作。","Merhaba, iş hakkında bir şey sormak istiyorum."),
            "很高兴认识你。":("好，你先说说你的情况。","Tamam, önce durumunu anlat."),
            "我也是。":("好的。","Tamam."),
            "今天学了很多。":("今天准备得差不多了。","Bugünkü hazırlık neredeyse tamam."),
        }
        if zh in table:return table[zh]
    if cat=="travel":
        table={
            "你好！":("你好，请问一下。","Merhaba, bir şey sorabilir miyim?"),
            "很高兴认识你。":("当然，你说。","Elbette, buyurun."),
            "我也是。":("谢谢。","Teşekkürler."),
            "今天学了很多。":("路线终于清楚了。","Yol artık netleşti."),
        }
        if zh in table:return table[zh]
    if cat=="pet":
        table={
            "你好！":("你好，我想问问这只猫。","Merhaba, bu kedi hakkında sormak istiyorum."),
            "很高兴认识你。":("好，先看看它怎么了。","Tamam, önce ne olduğuna bakalım."),
            "我也是。":("嗯，好。","Evet, tamam."),
            "今天学了很多。":("现在放心多了。","Şimdi çok daha rahatız."),
        }
        if zh in table:return table[zh]
    if cat in {"food","weather","social","home"}:
        table={
            "很高兴认识你。":("好，我们慢慢来。","Tamam, yavaş yavaş ilerleyelim."),
            "我也是。":("好啊。","Olur."),
            "今天学了很多。":("今天挺顺利的。","Bugün oldukça iyi geçti."),
        }
        if zh in table:return table[zh]
    return zh,tr

def hsk5_repair(cat, zh, tr, focus, focus_tr, cards, i):
    # Category-specific language instead of generic meeting boilerplate.
    if cat=="health":
        zh=zh.replace(f"说到{focus}，大家还有什么想法？",f"说到{focus}，最近实际做得怎么样？")
        zh=zh.replace(f"{focus}这一点也不能忽略。",f"{focus}这点必须认真对待。")
        zh=zh.replace(f"关于{focus}，我们也得看看有没有相反的情况。",f"关于{focus}，我们还得看看最近有没有改善。")
        if focus in PERSON and "意见" not in zh:
            zh=zh.replace(f"先把{focus}记下来，等信息更完整一点再决定。",f"先把{focus}的建议记下来，再看看哪些地方最需要改。")
        if i>=90 and "今天关于" in zh:
            main=nonperson_focus([str(x.get("zh","")) for x in cards])
            zh=f"好，今天关于{main}就先说到这里，接下来按建议去做。"
    elif cat=="work":
        zh=zh.replace(f"说到{focus}，大家还有什么想法？",f"说到{focus}，现在最现实的问题是什么？")
        zh=zh.replace(f"{focus}这一点也不能忽略。",f"{focus}这一点会直接影响接下来的安排。")
        zh=zh.replace(f"关于{focus}，我们也得看看有没有相反的情况。",f"关于{focus}，还得看看执行上会不会有别的问题。")
        if i>=90 and "今天关于" in zh:
            zh=f"好，{focus}这部分先按今天说的方案推进。"
    elif cat=="business":
        zh=zh.replace(f"说到{focus}，大家还有什么想法？",f"说到{focus}，顾客和成本两边都得一起看。")
        zh=zh.replace(f"{focus}这一点也不能忽略。",f"{focus}会直接影响实际经营，不能忽略。")
        if i>=90 and "今天关于" in zh:
            zh=f"好，{focus}这部分先按现在的办法试一段时间。"
    elif cat=="family":
        zh=zh.replace(f"说到{focus}，大家还有什么想法？",f"说到{focus}，你自己最在意的是什么？")
        zh=zh.replace(f"{focus}这一点也不能忽略。",f"{focus}这件事还是要尊重每个人的感受。")
        if i>=90 and "今天关于" in zh:
            zh=f"好，{focus}这件事今天先聊到这里，大家都想一想。"
    elif cat=="community":
        zh=zh.replace(f"说到{focus}，大家还有什么想法？",f"说到{focus}，对社区里的人会有什么实际影响？")
        zh=zh.replace(f"{focus}这一点也不能忽略。",f"{focus}对大家的实际影响不能忽略。")
        if i>=90 and "今天关于" in zh:
            zh=f"好，{focus}这部分先把大家的意见整理好。"
    elif cat=="reflection":
        zh=zh.replace(f"说到{focus}，大家还有什么想法？",f"说到{focus}，你现在最真实的感受是什么？")
        zh=zh.replace(f"{focus}这一点也不能忽略。",f"{focus}这件事对我们来说确实很重要。")
        if i>=90 and "今天关于" in zh:
            zh=f"好，{focus}今天先聊到这里，剩下的以后慢慢说。"
    elif cat=="education":
        zh=zh.replace(f"说到{focus}，大家还有什么想法？",f"说到{focus}，现在最需要改进的是什么？")
        zh=zh.replace(f"{focus}这一点也不能忽略。",f"{focus}会影响后面的学习安排，不能忽略。")
        if i>=90 and "今天关于" in zh:
            zh=f"好，{focus}这部分先按今天定的办法去做。"
    return zh,tr

for bp in sorted(base_root.glob("HSK*/scenes/ZH_HSK*_SC*.json")):
    b=json.loads(bp.read_text(encoding="utf-8"))
    level=b["level"]; sid=b["id"]; title=b.get("titleZh","")
    v3=json.loads((v3_root/level/f"{sid}.json").read_text(encoding="utf-8"))
    cards=[x for x in b.get("learning",{}).get("vocabularyCards",[]) if x.get("kind")=="active"]
    active=[str(x.get("zh","")).strip() for x in cards]
    trmap=active_tr_map(cards)
    cat=category_hsk1(title,active) if level=="HSK1" else category_hsk5(title,active) if level=="HSK5" else "other"
    last_focus=nonperson_focus(active)
    out=[]
    for i,(o,n) in enumerate(zip(b["dialogues"],v3["dialogues"]),1):
        zh=str(n["zh"]).strip(); tr=str(n["tr"]).strip()
        matches=[a for a in active if a and (a in str(o.get("zh","")) or a in zh)]
        if matches:last_focus=max(matches,key=len)
        focus=last_focus; focus_tr=trmap.get(focus,"bu konu")
        if level=="HSK1":
            zh,tr=hsk1_repair(cat,zh,tr,focus,focus_tr,i)
        elif level=="HSK5":
            zh,tr=hsk5_repair(cat,zh,tr,focus,focus_tr,cards,i)
        out.append({"id":o["id"],"speaker":o["speaker"],"zh":zh,"pinyin":pinyin_text(zh),"tr":tr})
    payload={
      "naturalizationVersion":4,"status":"FINAL",
      "sceneId":sid,"level":level,"sceneCategory":cat,
      "sourceTitleZh":b.get("titleZh"),"sourceTitleTr":b.get("titleTr"),
      "sourceMiniAdventureTr":b.get("miniAdventureTr"),
      "dialogues":out
    }
    dest=out_root/level/f"{sid}.json";dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("Generated FINAL v4")
