#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import sys

try:
    import jieba
    from pypinyin import lazy_pinyin, Style
except Exception as e:
    raise SystemExit("pip install jieba pypinyin") from e

if len(sys.argv) != 3:
    raise SystemExit("usage: generate_dialogue_final_v6.py <baseline-level-root> <out-root>")

BASE = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

TARGET_HSK3 = {
    "ZH_HSK3_SC008","ZH_HSK3_SC015","ZH_HSK3_SC027","ZH_HSK3_SC030",
    "ZH_HSK3_SC040","ZH_HSK3_SC043","ZH_HSK3_SC050",
}

PERSON_TERMS = {
    "医生","老师","顾客","家人","朋友","同事","经理","护士","学生","邻居","爷爷","奶奶",
    "爸爸","妈妈","孩子","员工","服务员","店员","司机","律师","导游","老板","同学","记者",
    "伴侣","志愿者","工作人员","张伟","刘梅","张雨桐","张乐乐","李晨",
}

ABSTRACT_TERMS = {
    "独立","理由","选择","方案","未来计划","人生阶段","语境","立场","权衡","长期影响",
    "自我评价","调整状态","优势","反馈","匹配","支持","边界","干预","自主","分歧",
    "价值观","责任","责任感","领导能力","公平","风险","优先顺序","判断","决定",
}

BAD_FOCUS = {
    "先","再","以后","现在","今天","一点","这点","这个","那个","更","最","也","都","就",
    "已经","还","很","一下","一起","事情","情况","问题",
}

def pick(opts, key):
    h = int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:8], 16)
    return opts[h % len(opts)]

def pinyin_text(s: str) -> str:
    s = s.replace("嗯", "ENMARK")
    parts = []
    for tok in jieba.lcut(s, cut_all=False):
        if tok == "ENMARK":
            parts.append("en")
        elif re.fullmatch(r"[\u3400-\u9fff]+", tok):
            parts.append("".join(lazy_pinyin(tok, style=Style.TONE, neutral_tone_with_five=False, errors="default")))
        else:
            parts.append(tok)
    out = " ".join(parts)
    out = re.sub(r"\s+([，。？！；：、,.?!;:）)])", r"\1", out)
    out = re.sub(r"([（(《“‘])\s+", r"\1", out)
    out = out.replace("，", ",").replace("。", ".").replace("？", "?").replace("！", "!")
    out = out.replace("；", ";").replace("：", ":")
    out = re.sub(r"\s+", " ", out).strip()
    return out[:1].upper() + out[1:] if out else out

def category(level: str, title: str, active: list[str]) -> str:
    text = title + " " + " ".join(active)
    groups = [
        ("health", ["医院","医生","护士","健康","体检","血压","运动","照护","生活方式","休息","疲劳","过敏"]),
        ("education", ["学校","高中","大学","学习","考试","挂科","老师","同学","毕业","作业","社团","摄影比赛","录取"]),
        ("work", ["工作","项目","客户","同事","经理","面试","实习","职业","领导","办公室","评价","责任"]),
        ("business", ["咖啡馆","顾客","订单","价格","成本","营业","商户","食材","扩张","店","厨房"]),
        ("family", ["家人","家庭","伴侣","订婚","结婚","恋爱","爷爷","奶奶","孩子","代际","退休","全家福"]),
        ("travel", ["火车","车站","站台","出租车","公交","酒店","旅行","导游","手机丢","路线"]),
        ("community", ["社区","公益","志愿者","募捐","居民","地方新闻","规划","道路","活动","爱心厨房"]),
        ("food", ["早餐","午饭","晚饭","超市","菜市场","蛋糕","点心","食物","茶","冰淇淋"]),
        ("pet", ["咪咪","猫","兽医","宠物"]),
        ("home", ["搬家","新家","房间","箱子","门","钥匙","包裹"]),
    ]
    for name, kws in groups:
        if any(k in text for k in kws):
            return name
    return "general"

def active_cards(scene):
    cards = [x for x in scene.get("learning", {}).get("vocabularyCards", []) if x.get("kind") == "active"]
    zh = [str(x.get("zh","")).strip() for x in cards if str(x.get("zh","")).strip()]
    tr = {str(x.get("zh","")).strip(): str(x.get("tr","")).strip() for x in cards}
    return zh, tr

def focus_for(scene, old_zh: str, idx: int, last_focus: str) -> str:
    active, _ = active_cards(scene)
    matches = [x for x in active if x and x in old_zh and x not in BAD_FOCUS]
    if matches:
        return max(matches, key=len)
    usable = [x for x in active if x not in BAD_FOCUS and len(x) >= 2]
    if last_focus and last_focus not in BAD_FOCUS:
        return last_focus
    if usable:
        return usable[(idx // 4) % len(usable)]
    return scene.get("titleZh", "这件事")

def is_person(x: str) -> bool:
    return x in PERSON_TERMS or any(p in x for p in PERSON_TERMS)

def normalize_artifacts(zh: str) -> str:
    zh = re.sub(r"，对，对吗？$", "，对吗？", zh)
    zh = zh.replace("你看，你看，", "你看，")
    zh = zh.replace("准备好了吗？", "准备好了吗？")
    zh = zh.replace("好了吗？", "好了吗？")
    zh = re.sub(r"([，。！？])\1+", r"\1", zh)
    return zh

def common_hsk1_hsk2(zh: str, tr: str, level: str, key: str, cat: str):
    # Course-wide boilerplate is varied between scenes while keeping the same meaning.
    tables = {
        "今天事情不少。": [
            ("今天事情还真不少。", tr), ("今天要忙的事不少。", tr), ("今天有不少事情要做。", tr)
        ],
        "我们先看看最重要的。": [
            ("我们先看最重要的事。", tr), ("先看看哪件事最重要。", tr), ("我们先从最重要的开始。", tr)
        ],
        "好，慢慢来。": [
            ("好，别着急。", tr), ("好，我们慢慢来。", tr), ("行，一步一步来。", tr)
        ],
        "我明白了。": [
            ("明白了。", tr), ("好，我知道了。", tr), ("嗯，我懂了。", tr), ("知道了。", tr)
        ],
        "原来是这样。": [
            ("原来是这样。", tr), ("哦，是这样啊。", tr), ("这样我就懂了。", tr)
        ],
        "这个我记住了。": [
            ("好，我记住了。", tr), ("嗯，这个我记住了。", tr), ("行，我会记着。", tr)
        ],
        "听起来很清楚。": [
            ("这样就清楚了。", tr), ("嗯，听明白了。", tr), ("好，现在清楚了。", tr)
        ],
        "好，那就按这个来。": [
            ("好，那就这么办。", tr), ("行，就按这个来。", tr), ("好，我们就这样做。", tr)
        ],
        "对，我记住了。": [
            ("对，我记住了。", tr), ("嗯，我记住了。", tr), ("好，我会记着。", tr)
        ],
        "这个很实用。": [
            ("这个挺实用的。", tr), ("嗯，这个很有用。", tr), ("这个办法很实用。", tr)
        ],
        "以后还会用到。": [
            ("以后还用得上。", tr), ("以后也会用到。", tr), ("这个以后还会用。", tr)
        ],
        "我再说一次。": [
            ("我再说一遍。", tr), ("好，我再说一次。", tr), ("那我再说一遍。", tr)
        ],
        "现在更清楚了。": [
            ("现在清楚多了。", tr), ("嗯，现在明白多了。", tr), ("这样就更清楚了。", tr)
        ],
        "谢谢。": [
            ("谢谢。", tr), ("谢谢你。", tr), ("好，谢谢。", tr), ("嗯，谢谢。", tr), ("太好了，谢谢。", tr)
        ],
        "我也是。": [
            ("我也是。", tr), ("嗯，我也是。", tr), ("我也一样。", tr), ("我也这么想。", tr)
        ],
        "你好！": [
            ("你好！", tr), ("你好啊！", tr), ("嗨，你好！", tr), ("你好，来了！", tr)
        ],
        "很高兴认识你。": [
            ("很高兴认识你。", tr), ("认识你很高兴。", tr), ("太好了，认识你很高兴。", tr)
        ],
        "准备好了吗？": [
            ("准备好了吗？", tr), ("都准备好了吗？", tr), ("准备得怎么样了？", tr)
        ],
        "准备好了。": [
            ("准备好了。", tr), ("嗯，准备好了。", tr), ("都准备好了。", tr)
        ],
        "对。": [
            ("对。", tr), ("嗯，对。", tr), ("是。", tr), ("没错。", tr)
        ],
        "好的。": [
            ("好的。", tr), ("好。", tr), ("嗯，好。", tr), ("行。", tr)
        ],
        "好。": [
            ("好。", tr), ("嗯，好。", tr), ("行。", tr), ("好的。", tr)
        ],
        "很好看。": [
            ("很好看。", tr), ("嗯，挺好看的。", tr), ("真的很好看。", tr)
        ],
        "喜欢。": [
            ("喜欢。", tr), ("嗯，喜欢。", tr), ("我喜欢。", tr)
        ],
        "这边走。": [
            ("这边走。", tr), ("往这边走。", tr), ("来，这边走。", tr), ("从这边走。", tr)
        ],
    }
    if zh in tables:
        return pick(tables[zh], key)

    # Keep beginner location grammar but vary the surface naturally.
    m = re.fullmatch(r"这是(.+)吗？", zh)
    if m:
        x = m.group(1)
        return pick([(f"这是{x}吗？",tr),(f"这个是{x}吗？",tr),(f"这是{x}，对吗？",tr)], key)
    m = re.fullmatch(r"对，这是(.+)。", zh)
    if m:
        x = m.group(1)
        return pick([(f"对，这是{x}。",tr),(f"没错，这是{x}。",tr),(f"嗯，这就是{x}。",tr)], key)
    m = re.fullmatch(r"(.+)在哪儿？", zh)
    if m:
        x = m.group(1)
        return pick([(f"{x}在哪儿？",tr),(f"{x}呢？",tr),(f"请问，{x}在哪儿？",tr)], key)
    m = re.fullmatch(r"(.+)在这里。", zh)
    if m:
        x = m.group(1)
        return pick([(f"{x}在这里。",tr),(f"就在这里。",tr),(f"你看，{x}在这儿。",tr)], key)
    m = re.fullmatch(r"(.+)在那边。", zh)
    if m:
        x = m.group(1)
        return pick([(f"{x}在那边。",tr),(f"就在那边。",tr),(f"你看，{x}在那边。",tr)], key)

    # A few category repairs for lines that were pedagogically copied into unrelated scenes.
    if level == "HSK1":
        if cat == "travel":
            swaps = {
                "很高兴认识你。": ("当然，你说。", tr),
                "我也是。": ("谢谢。", tr),
                "今天学了很多。": ("路线现在清楚了。", tr),
            }
            if zh in swaps: return swaps[zh]
        if cat == "school":
            swaps = {
                "今天学了很多。": ("今天学得不错。", tr),
                "我也是。": ("好啊。", tr),
            }
            if zh in swaps: return swaps[zh]
        if cat == "pet":
            swaps = {
                "今天学了很多。": ("现在放心多了。", tr),
                "我也是。": ("嗯，好。", tr),
            }
            if zh in swaps: return swaps[zh]
        if cat in {"home","food","family","community","general"} and zh == "今天学了很多。":
            return ("今天挺顺利的。", tr)
    return zh, tr

def naturalize_hsk4(zh: str, tr: str, focus: str, key: str, cat: str):
    m = re.fullmatch(r"今天我们先谈谈(.+)。", zh)
    if m:
        x=m.group(1)
        opts=[
            f"今天先聊聊{x}吧。", f"我们先把{x}这件事说清楚吧。", f"先从{x}说起吧。",
            f"关于{x}，我们先把情况理一理。"
        ]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"关于(.+)，我想再听听大家的看法。", zh)
    if m:
        x=m.group(1)
        opts=[
            f"关于{x}，你们怎么看？", f"{x}这件事，大家还有什么要补充的？",
            f"对{x}还有别的想法吗？", f"说到{x}，大家最在意的是什么？"
        ]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"(.+)是我们不能忽略的一点。", zh)
    if m:
        x=m.group(1)
        if is_person(x):
            opts=[f"{x}的意见也得听进去。",f"我们也得顾到{x}的想法。",f"{x}这边的意见不能漏掉。"]
        else:
            opts=[f"{x}也得考虑进去。",f"{x}这方面不能忽略。",f"我们还得顾到{x}。",f"{x}也是关键的一点。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"我们把(.+)也列进考虑范围吧。", zh)
    if m:
        x=m.group(1)
        opts=[f"那把{x}也一起考虑进去吧。",f"{x}这方面也别漏了。",f"我们把{x}也算进去。",f"那再把{x}这一点加上。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"如果(.+)发生变化，计划也得调整。", zh)
    if m:
        x=m.group(1)
        if x in ABSTRACT_TERMS:
            opts=[f"如果大家对{x}的想法变了，我们的安排也要跟着调整。",f"如果{x}方面出现新情况，原来的安排就得再改。"]
        else:
            opts=[f"如果{x}的情况变了，我们的安排也要跟着调整。",f"{x}要是有新变化，我们就得重新安排。"]
        return pick([(z,tr) for z in opts], key)

    # v5-style forms, if present in baseline later.
    m = re.fullmatch(r"如果(.+)有变化，我们的安排也得及时调整。", zh)
    if m:
        x=m.group(1)
        if x in ABSTRACT_TERMS:
            opts=[f"如果大家对{x}的想法有变化，我们的安排也要跟着调整。",f"如果{x}方面出现新情况，我们再及时调整安排。"]
        else:
            opts=[f"如果{x}的情况有变化，我们再及时调整安排。",f"{x}要是有新情况，我们的安排也得跟着改。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"这一点我同意。", zh)
    if m:
        opts=["这一点我同意。","对，我也这么看。","嗯，这一点我赞成。","这点我没有意见。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"这个角度我刚才没有想到。", zh)
    if m:
        opts=["这个角度我刚才没想到。","你这么一说，我才想到这一层。","对，这方面刚才确实漏了。","这个提醒很有用，我刚才没想到。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"那确实需要重新考虑。", zh)
    if m:
        opts=["那确实得重新想一想。","这样的话，我们得再考虑一下。","那原来的想法可能要调整。","对，这一点值得再想想。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"听起来比较合理。", zh)
    if m:
        opts=["听起来挺合理。","这么安排我觉得可以。","这样更符合实际。","嗯，这个思路比较稳妥。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"我先把这一点记下来。", zh)
    if m:
        opts=["我先把这一点记下来。","好，这点我记一下。","这一条先记下来。","行，我先记着。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"我们再看看还有没有别的影响。", zh)
    if m:
        opts=["我们再看看还有没有别的影响。","再想想还有没有别的影响。","我们也看看会不会影响别的方面。","先别急，再看看还有没有其他影响。"]
        return pick([(z,tr) for z in opts], key)
    return zh, tr

def naturalize_hsk5(zh: str, tr: str, focus: str, key: str, cat: str):
    # Higher-level speech should sound like real family/work/community discussion,
    # not a sequence of abstract nouns inserted into one template.
    m = re.fullmatch(r"关于(.+)，我想再听听大家的看法。", zh)
    if m:
        x=m.group(1)
        if cat=="education":
            opts=[f"说到{x}，你觉得最需要改进的是什么？",f"{x}这件事，你自己怎么看？",f"关于{x}，你最担心哪一点？"]
        elif cat=="health":
            opts=[f"说到{x}，最近实际情况怎么样？",f"{x}这方面现在最需要注意什么？",f"关于{x}，医生最担心的是什么？"]
        elif cat=="work":
            opts=[f"说到{x}，现在最现实的问题是什么？",f"{x}会对接下来的工作造成什么影响？",f"关于{x}，你觉得先处理哪一部分？"]
        elif cat=="business":
            opts=[f"说到{x}，顾客和成本两边都得看看。",f"{x}对店里的实际影响有多大？",f"关于{x}，你最担心经营上的哪一点？"]
        elif cat=="family":
            opts=[f"说到{x}，你自己最在意的是什么？",f"{x}这件事，你心里真正担心什么？",f"关于{x}，我们先听听每个人的感受。"]
        elif cat=="community":
            opts=[f"说到{x}，对社区里的人会有什么实际影响？",f"{x}会影响到哪些人？",f"关于{x}，大家最关心的是什么？"]
        else:
            opts=[f"说到{x}，你怎么看？",f"关于{x}，还有什么需要确认的？",f"{x}这件事，最关键的问题是什么？"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"(.+)是我们不能忽略的一点。", zh)
    if m:
        x=m.group(1)
        opts=[f"{x}这一点不能忽略。",f"{x}会直接影响后面的判断。",f"我们还得把{x}算进去。",f"{x}也是决定里很关键的一部分。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"我们把(.+)也列进考虑范围吧。", zh)
    if m:
        x=m.group(1)
        opts=[f"那把{x}也一起考虑进去。",f"{x}这一项也加进去吧。",f"我们还得把{x}算在里面。",f"那再补上{x}这一点。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"如果(.+)发生变化，计划也得调整。", zh)
    if m:
        x=m.group(1)
        if x in ABSTRACT_TERMS:
            opts=[f"如果{x}方面出现新情况，我们原来的安排也要重新评估。",f"如果我们对{x}的判断变了，后面的计划也得跟着调整。"]
        else:
            opts=[f"如果{x}的情况变了，后面的计划也得重新评估。",f"{x}要是出现新变化，我们就得及时调整计划。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"我同意先把它列为优先问题。", zh)
    if m:
        opts=[f"我同意，先把{focus}放在前面处理。","我赞成先解决最紧要的部分。","可以，先把最重要的问题处理掉。","我也觉得应该先分清轻重缓急。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"这个角度会影响最后的判断。", zh)
    if m:
        opts=[f"从{focus}这个角度看，结论可能会不一样。","这一点会影响我们最后怎么判断。","把这个因素算进去以后，结论可能会变。","这个角度确实会影响最后的决定。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"我们也要看看有没有反面的证据。", zh)
    if m:
        opts=["我们也要看看有没有不同的情况。","也别只看支持这一边，还得看看相反的信息。","最好再找找有没有不一样的证据。","我们也得确认有没有例外。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"先记下来，等信息完整一点再决定。", zh)
    if m:
        opts=[f"先把{focus}这一点记下来，等信息更完整再决定。","先记着，不用现在马上下结论。","这点先保留，等信息齐一点再判断。","先把它记下来，后面再结合新信息决定。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"这个信息很关键。", zh)
    if m:
        opts=["这个信息很关键。","这条信息很重要。","这一点会影响后面的判断。","这个细节不能忽略。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"这样解释以后，我更理解你的立场了。", zh)
    if m:
        opts=["你这么解释以后，我更理解你的想法了。","这样说我就明白你为什么这么想了。","听你解释完，我更能理解你的立场。","这样一说，你的考虑就清楚多了。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"这一点值得继续确认。", zh)
    if m:
        opts=["这一点还要再确认。","这部分值得继续核实。","这个细节我们再确认一下。","这点先别定死，还要再看看。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"我觉得这个建议比较稳妥。", zh)
    if m:
        opts=["我觉得这个建议比较稳妥。","这个办法相对稳妥。","这样处理风险会小一些。","我觉得先按这个思路走比较保险。"]
        return pick([(z,tr) for z in opts], key)
    return zh, tr

def naturalize_hsk6(zh: str, tr: str, focus: str, key: str, cat: str):
    # Rewrite the old academic slot templates into idiomatic advanced conversation.
    m = re.fullmatch(r"谈到(.+)，我更关心的是它背后的意义，而不只是表面的结果。", zh)
    if m:
        x=m.group(1)
        special={
            "语境":["把这件事放回当时的语境里看，很多反应就更容易理解了。","离开具体语境谈这件事，很容易误解彼此。"],
            "立场":["我更想知道每个人为什么会站在现在这个立场上。","比起表面的结论，我更在意各自立场背后的原因。"],
            "权衡":["真正难的不是选哪一个，而是怎么权衡两边的得失。","我更关心我们是怎么做这个权衡的。"],
            "长期影响":["眼前的结果是一方面，我更在意它长期会带来什么变化。","这件事不能只看现在，长期影响也要算进去。"],
        }
        opts=special.get(x,[f"说到{x}，我更在意它实际会带来什么影响。",f"{x}这件事，我想多看一层，不只看表面的结果。",f"关于{x}，真正重要的是背后的原因和影响。"])
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"(.+)之所以重要，是因为它会影响我们接下来怎么理解这件事。", zh)
    if m:
        x=m.group(1)
        special={
            "语境":["语境很重要，因为同一句话放在不同情况下，意思可能完全不一样。","如果不看当时的语境，很容易把别人的意思理解偏。"],
            "立场":["立场不同，看同一件事的重点也会不一样。","先弄清彼此的立场，后面的讨论才不会各说各话。"],
            "权衡":["权衡很重要，因为每个选择都有代价。","真正的难点在于怎么权衡，而不是只找一个简单答案。"],
            "长期影响":["长期影响不能忽略，它会决定我们今天的选择是否值得。","把长期影响看清楚，眼前的决定才更稳妥。"],
        }
        opts=special.get(x,[f"{x}很重要，因为它会影响我们后面怎么判断。",f"先把{x}说清楚，后面的讨论才有基础。",f"{x}会影响我们怎么看这件事，所以不能跳过去。"])
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"如果忽略(.+)，很多看似合理的判断其实会失去依据。", zh)
    if m:
        x=m.group(1)
        special={
            "语境":["如果忽略当时的语境，很多判断都会变得片面。","不看具体语境，表面上合理的结论也可能站不住脚。"],
            "立场":["如果不考虑彼此的立场，很多判断会显得过于简单。","忽略不同立场，很容易把复杂的问题看成单一答案。"],
            "权衡":["如果不做权衡，所谓最好的选择往往只是看起来简单。","不把得失放在一起比较，结论很容易失真。"],
            "长期影响":["如果忽略长期影响，眼前看起来合适的选择以后可能会出问题。","只看眼前、不看长期影响，判断很容易偏。"],
        }
        opts=special.get(x,[f"如果忽略{x}，我们的判断很可能会失去一部分依据。",f"不把{x}算进去，结论可能会太片面。",f"{x}要是被忽略，很多看起来合理的判断也未必可靠。"])
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"我想把(.+)放回具体语境里看，这样更容易理解彼此的选择。", zh)
    if m:
        x=m.group(1)
        special={
            "语境":["我觉得还是要回到具体情况里看，不能只谈抽象的原则。","把事情放回当时的情境里，彼此的选择就更容易理解。"],
            "立场":["如果把各自的立场放回具体情况里看，很多分歧就没那么难理解。","先理解每个人站在什么位置，再看他的选择会更公平。"],
            "权衡":["把当时需要权衡的因素都摆出来，我们就更能理解那个选择。","只有看清当时怎么权衡，才能真正理解最后的决定。"],
            "长期影响":["把长期影响也放进来，我们才看得懂为什么有人会做不同选择。","如果考虑长期影响，彼此的选择就更容易理解。"],
        }
        opts=special.get(x,[f"把{x}放回具体情况里看，彼此的选择就更容易理解。",f"如果结合当时的情况看{x}，很多决定就没那么难理解。",f"{x}不能脱离具体情况来看。"])
        return pick([(z,tr) for z in opts], key)

    # Common HSK6 discussion lines are varied to avoid the same panel-discussion cadence.
    exact = {
        "我觉得现在最重要的是让大家都轻松一点。":[
            "我觉得现在最重要的是别让谁压力太大。","眼下最重要的，是让大家都能放松一点。",
            "我更希望大家先把压力放下来，再慢慢谈。","现在不用急，先让每个人都舒服一点。",
            "我觉得先把气氛放松下来更重要。"
        ],
        "听到这里，你现在最期待的是什么？":[
            "听到这里，你现在最期待什么？","那你接下来最期待的是什么？","说到这里，你最盼着哪件事发生？",
            "现在你心里最期待的是哪一部分？","如果往前看，你最期待什么？"
        ],
        "至少现在大家都知道彼此怎么想了。":[
            "至少现在大家都知道彼此是怎么想的。","现在大家的想法总算都说开了。","至少我们已经把各自的想法听清楚了。",
            "现在彼此的想法比刚才清楚多了。"
        ],
        "那你觉得现在最需要的是什么？":[
            "那你觉得现在最需要什么？","如果只选一件事，你觉得现在最需要先做什么？",
            "眼下你最需要的是什么？","那你希望大家现在先做什么？"
        ],
        "我觉得这一点已经比刚开始清楚多了。":[
            "这一点现在比刚开始清楚多了。","至少这一点我们已经理得比较清楚了。","现在回头看，这个问题已经清楚不少。",
            "这部分总算比一开始明确多了。"
        ],
        "说到这里，你现在最担心的还有什么？":[
            "说到这里，你还有什么担心？","现在还有哪一点最让你不放心？","我们聊到这里，你心里还有什么顾虑？",
            "还有什么是你现在最担心的？"
        ],
        "我同意，这样理解起来更完整。":[
            "我同意，这样看就完整多了。","对，这样理解会更全面。","嗯，把这一层加进来就更完整了。",
            "我也这么看，这样不会只看到一面。"
        ],
        "如果换个角度看，你会怎么想？":[
            "如果换个角度，你会怎么看？","换一个位置想想，你的看法会变吗？","如果从另一面看呢？",
            "要是站在对方的角度，你会怎么想？"
        ],
    }
    if zh in exact:
        return (pick(exact[zh], key), tr)

    m = re.fullmatch(r"好，(.+)这部分清楚了，我们接着往下聊。", zh)
    if m:
        x=m.group(1)
        opts=[f"好，{x}这部分先说到这里，我们看下一件事。",f"行，{x}已经比较清楚了，接着聊后面的。",f"好，关于{x}先到这里，我们继续。",f"{x}这部分差不多了，我们往下谈。"]
        return pick([(z,tr) for z in opts], key)

    m = re.fullmatch(r"好，(.+)这部分我们已经说清楚了。", zh)
    if m:
        x=m.group(1)
        opts=[f"好，{x}这部分已经比较清楚了。",f"行，关于{x}大家已经说得很明白了。",f"{x}这件事现在基本说开了。",f"好，{x}这一块先算理清了。"]
        return pick([(z,tr) for z in opts], key)
    return zh, tr

def diversify_duplicate(zh: str, tr: str, level: str, occurrence: int, key: str):
    if occurrence <= 1:
        return zh, tr
    core = zh[:-1] if zh.endswith(("。","！","？")) else zh
    punct = zh[-1] if zh.endswith(("。","！","？")) else "。"

    # Dedicated safe variants for very common conversational responses.
    maps = {
        "谢谢。":["谢谢你。","好，谢谢。","嗯，谢谢。","太好了，谢谢。","谢谢，帮大忙了。"],
        "我明白了。":["明白了。","好，我知道了。","嗯，我懂了。","知道了。","好，明白了。"],
        "我也是。":["嗯，我也是。","我也一样。","我也这么想。","对，我也是。"],
        "对。":["嗯，对。","是。","没错。","对的。"],
        "好的。":["好。","嗯，好。","行。","可以。"],
        "好。":["嗯，好。","行。","好的。","可以。"],
        "准备好了。":["嗯，准备好了。","都准备好了。","好了。","我这边好了。"],
        "准备好了吗？":["都准备好了吗？","准备得怎么样了？","大家都准备好了吗？","可以开始了吗？"],
        "很高兴认识你。":["认识你很高兴。","我也很高兴认识你。","太好了，很高兴认识你。"],
        "你好！":["你好啊！","嗨，你好！","你好，来了！","你好，很高兴见到你！"],
        "这边走。":["往这边走。","来，这边走。","从这边走。","走这边。"],
        "喜欢。":["嗯，喜欢。","我喜欢。","挺喜欢的。","对，我喜欢。"],
        "很好看。":["嗯，挺好看的。","真的很好看。","对，很好看。","我觉得很好看。"],
    }
    if zh in maps:
        opts=maps[zh]
        return opts[(occurrence-2) % len(opts)], tr

    # Generic safe discourse-marker variation for repeated statements/questions.
    if punct == "。" and len(core) <= 18:
        prefixes = ["嗯，","对，","好，","是啊，","没错，"]
        p = prefixes[(occurrence-2) % len(prefixes)]
        if not core.startswith(("嗯，","对，","好，","是啊，","没错，")):
            return p + core + punct, tr
    if punct == "？" and len(core) <= 18:
        variants = [
            "那" + core + "？",
            "现在" + core + "？",
            "你觉得" + core + "？" if not core.startswith("你") else "那" + core + "？",
        ]
        return variants[(occurrence-2) % len(variants)], tr
    return zh, tr

def process_scene(scene):
    sid=scene["id"]; level=scene["level"]
    if level=="HSK3" and sid not in TARGET_HSK3:
        return None
    if level not in {"HSK1","HSK2","HSK3","HSK4","HSK5","HSK6"}:
        return None

    active, trmap = active_cards(scene)
    cat = category(level, scene.get("titleZh",""), active)
    last_focus = next((x for x in active if x not in BAD_FOCUS), scene.get("titleZh","这件事"))
    out=[]
    for idx, old in enumerate(scene.get("dialogues",[]), start=1):
        zh=str(old.get("zh","")).strip()
        tr=str(old.get("tr","")).strip()
        focus=focus_for(scene, zh, idx, last_focus)
        if focus and focus not in BAD_FOCUS:
            last_focus=focus
        key=f"{sid}:{idx}:{zh}"

        if level in {"HSK1","HSK2"}:
            zh,tr=common_hsk1_hsk2(zh,tr,level,key,cat)
        elif level=="HSK3":
            # Seven WARN scenes only: keep meaning, remove exact-response recycling
            # and replace the remaining old generator boilerplate.
            exact={
                "我明白你的意思了.":("嗯，我懂你的意思了。",tr),
                "我明白你的意思了。":pick([("嗯，我懂你的意思了。",tr),("好，我明白你的意思了。",tr),("这样我就明白了。",tr)],key),
                "好，这一点我会注意。":pick([("好，这一点我会留意。",tr),("嗯，这点我会注意。",tr),("好，我会记着这一点。",tr)],key),
                "对，我们继续看下一项。":pick([("好，我们再看下一件事。",tr),("行，那接着看后面的。",tr),("好，这一点清楚了，我们继续。",tr)],key),
            }
            if zh in exact:
                val=exact[zh]
                zh,tr=val if isinstance(val,tuple) else (val,tr)
            m3=re.fullmatch(r"(.+)是这次要考虑的重点之一。", zh)
            if m3:
                x=m3.group(1)
                zh=pick([
                    f"{x}这一点也得认真考虑。",
                    f"我们还得把{x}算进去。",
                    f"{x}也是这次需要注意的一点。",
                ],key)
            m3=re.fullmatch(r"关于(.+)，我们还要再讨论一下。", zh)
            if m3:
                x=m3.group(1)
                zh=pick([f"{x}这件事我们还得再聊聊。",f"关于{x}，还有几个地方要说清楚。",f"{x}这部分还需要再讨论一下。"],key)
        elif level=="HSK4":
            zh,tr=naturalize_hsk4(zh,tr,focus,key,cat)
        elif level=="HSK5":
            zh,tr=naturalize_hsk5(zh,tr,focus,key,cat)
        elif level=="HSK6":
            zh,tr=naturalize_hsk6(zh,tr,focus,key,cat)

        zh=normalize_artifacts(zh)
        out.append({
            "id":old["id"],"speaker":old["speaker"],"zh":zh,
            "pinyin":pinyin_text(zh),"tr":tr
        })

    # Second pass: cap exact within-scene recycling. Pedagogical repetition remains,
    # but the exact same sentence should not dominate a natural conversation.
    seen=Counter()
    fixed=[]
    for i,row in enumerate(out, start=1):
        z=row["zh"]
        seen[z]+=1
        if level=="HSK1":
            cap=2
        elif level=="HSK2":
            cap=2
        elif level=="HSK3":
            cap=2
        elif level=="HSK4":
            cap=2
        else:
            cap=1
        if seen[z] > cap:
            nz,ntr=diversify_duplicate(z,row["tr"],level,seen[z],f"{sid}:dup:{i}:{z}")
            row=dict(row); row["zh"]=normalize_artifacts(nz); row["tr"]=ntr; row["pinyin"]=pinyin_text(row["zh"])
        fixed.append(row)

    return {
        "naturalizationVersion":6,
        "status":"FINAL_NATIVE_QA_CANDIDATE",
        "sceneId":sid,
        "level":level,
        "sceneCategory":cat,
        "sourceTitleZh":scene.get("titleZh"),
        "sourceTitleTr":scene.get("titleTr"),
        "sourceMiniAdventureTr":scene.get("miniAdventureTr"),
        "dialogues":fixed,
    }

count=0
turns=0
by_level=Counter()
for level_num in range(1,7):
    level=f"HSK{level_num}"
    scene_dir=BASE/level/"scenes"
    if not scene_dir.exists():
        scene_dir=BASE/level
    for p in sorted(scene_dir.glob(f"ZH_{level}_SC*.json")):
        scene=json.loads(p.read_text(encoding="utf-8"))
        result=process_scene(scene)
        if result is None:
            continue
        dest=OUT/level/f"{scene['id']}.json"
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        count+=1; turns+=len(result["dialogues"]); by_level[level]+=1

report={
    "naturalizationVersion":6,
    "targetSceneCount":count,
    "targetTurnCount":turns,
    "byLevel":dict(sorted(by_level.items())),
    "order":["HSK1","HSK2","HSK4","HSK5","HSK6","HSK3 polishing"],
    "preserved":["dialogue id","speaker","scene story/metadata","HSK learning targets"],
}
(OUT/"generation_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
