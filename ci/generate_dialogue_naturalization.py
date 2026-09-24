#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict
import hashlib, json, re, sys

try:
    from pypinyin import lazy_pinyin, Style
    from opencc import OpenCC
except Exception as e:
    raise SystemExit("pip install pypinyin opencc-python-reimplemented") from e

if len(sys.argv) != 3:
    raise SystemExit("usage: generate_dialogue_naturalization.py <snapshot-scene-root> <out-root>")

scene_root = Path(sys.argv[1])
out_root = Path(sys.argv[2])
out_root.mkdir(parents=True, exist_ok=True)
t2s = OpenCC("t2s")

REBUILD_RANGES = {
    "HSK2": [(2, 21), (55, 95)],
    "HSK3": [(1, 18), (76, 94)],
    "HSK4": [(1, 22), (78, 94)],
    "HSK5": [(3, 22), (71, 94)],
    "HSK6": [(1, 6), (15, 92)],
}

COMMON = {
    "我明白了。": ["嗯，我明白了。", "好，明白了。", "这下明白了。"],
    "好的。": ["好的。", "好。", "嗯，好。"],
    "好。": ["好。", "嗯，好。", "行。"],
    "对。": ["对。", "嗯，对。", "没错。"],
    "谢谢。": ["谢谢。", "谢谢啊。", "好，谢谢。"],
    "谢谢你。": ["谢谢你。", "谢谢啊。", "真谢谢你。"],
    "不客气。": ["不客气。", "别客气。", "没事，不客气。"],
    "太好了！": ["太好了！", "真好！", "太棒了！"],
    "我也是。": ["我也是。", "嗯，我也是。", "我也一样。"],
    "我们继续。": ["好，我们接着来。", "那我们继续吧。", "好，继续。"],
    "好，我们继续。": ["好，那继续吧。", "行，我们接着来。", "好，继续。"],
    "说得对。": ["你说得对。", "嗯，说得对。", "对，就是这样。"],
    "我也是这么想的。": ["嗯，我也是这么想的。", "对，我也这么觉得。", "我的想法也一样。"],
}

# Six generic connective lines per 20-turn phase.
# Slots 0 and 4 are filled with scene-specific active-vocabulary lines.
PHASE = {
"HSK2": [
[
("好，我先听听你怎么想。","Tamam, önce senin ne düşündüğünü dinleyeyim."),
("先别急，我们慢慢看。","Acele etmeyelim, yavaş yavaş bakalım."),
("对，先把最重要的弄清楚。","Evet, önce en önemli noktayı netleştirelim."),
("嗯，这一点也要注意。","Evet, buna da dikkat etmek gerekiyor."),
("那我们先试试看。","O zaman önce deneyelim."),
("好，这样就清楚多了。","Tamam, böyle çok daha net oldu.")
],
[
("我觉得可以先从简单的开始。","Bence önce kolay olandan başlayabiliriz."),
("对，做完这个再看下一个。","Evet, bunu bitirince sonrakine bakarız."),
("如果不合适，我们再换一个办法。","Uygun olmazsa başka bir yol deneriz."),
("嗯，这样比较方便。","Evet, böyle daha kullanışlı."),
("那就先这么做吧。","O zaman şimdilik böyle yapalım."),
("好，我们接着看。","Tamam, devam edelim.")
],
[
("现在比刚才清楚多了。","Şimdi az öncekinden çok daha net."),
("不过还有一点要确认。","Ama teyit etmemiz gereken bir nokta daha var."),
("那我们再看一遍。","O zaman bir kez daha bakalım."),
("对，这样不容易弄错。","Evet, böyle hata yapmak daha zor olur."),
("我来记住这一点。","Bu noktayı ben aklımda tutayım."),
("好，继续吧。","Tamam, devam edelim.")
],
[
("这一步做好以后，后面就容易多了。","Bu adım tamamlanınca sonrası çok daha kolay olacak."),
("嗯，我们一步一步来。","Evet, adım adım ilerleyelim."),
("有问题就马上说。","Bir sorun olursa hemen söyleyelim."),
("对，别等到最后才发现。","Evet, en sonda fark etmeyi beklemeyelim."),
("那就再确认一下。","O zaman bir kez daha teyit edelim."),
("好，现在好多了。","Tamam, şimdi çok daha iyi.")
],
[
("主要的问题已经解决了。","Ana sorun artık çözüldü."),
("剩下的按刚才说的做就行。","Kalanını az önce konuştuğumuz gibi yapmamız yeterli."),
("最后再检查一次吧。","Son kez bir daha kontrol edelim."),
("嗯，这次应该没问题了。","Evet, bu kez sorun olmamalı."),
("今天又学到一点东西。","Bugün yine yeni bir şey öğrendik."),
("好，那今天先这样。","Tamam, bugünlük böyle bırakalım.")
]],
"HSK3": [
[
("我先说吧，我觉得先把情况弄清楚比较好。","Önce ben söyleyeyim; bence önce durumu netleştirmek daha iyi."),
("对，先别急着下结论。","Evet, hemen sonuca varmayalım."),
("那我们先听听大家的意见。","O zaman önce herkesin fikrini dinleyelim."),
("这一点也不能忽略。","Bu noktayı da göz ardı edemeyiz."),
("好，先把重点记下来。","Tamam, önce ana noktaları not edelim."),
("这样后面就好处理了。","Böylece sonrasını yönetmek daha kolay olur.")
],
[
("我觉得先试一个小办法比较好。","Bence önce küçük bir çözümü denemek daha iyi."),
("虽然有点麻烦，不过可以先试试。","Biraz zahmetli olsa da önce deneyebiliriz."),
("如果有效，我们就继续。","İşe yararsa devam ederiz."),
("对，有问题再调整。","Evet, sorun olursa yeniden ayarlarız."),
("那我把这一点记下来。","O zaman bunu not edeyim."),
("好，我们接着看下一步。","Tamam, sonraki adıma bakalım.")
],
[
("事情现在越来越清楚了。","Durum şimdi giderek netleşiyor."),
("不过还有几个细节要确认。","Ama teyit edilmesi gereken birkaç ayrıntı daha var."),
("那就一个一个来。","O zaman tek tek ilerleyelim."),
("只要准备好，就可以继续。","Hazırlık tamam olduğu sürece devam edebiliriz."),
("我同意，这样比较实际。","Katılıyorum, böyle daha uygulanabilir."),
("好，先按这个办法来。","Tamam, önce bu yöntemle ilerleyelim.")
],
[
("现在主要问题已经找到了。","Ana sorunu artık bulduk."),
("一边做，一边检查会更放心。","Yaparken aynı zamanda kontrol etmek daha güvenli olur."),
("对，这样能早点发现问题。","Evet, böylece sorunları daha erken fark ederiz."),
("如果情况变了，我们再调整。","Durum değişirse yeniden ayarlarız."),
("那就把分工也说清楚吧。","O zaman görev dağılımını da netleştirelim."),
("好，有变化随时说。","Tamam, bir değişiklik olursa hemen söyleyelim.")
],
[
("今天讨论得比刚开始顺利多了。","Bugünkü konuşma başlangıca göre çok daha iyi ilerledi."),
("我也觉得，至少方向已经清楚了。","Ben de öyle düşünüyorum; en azından yön artık net."),
("最后再确认一遍吧。","Son kez bir daha teyit edelim."),
("好，没问题的话就按计划继续。","Tamam, sorun yoksa plana göre devam edelim."),
("这次的经验以后还会用到。","Bu deneyim ileride yine işimize yarayacak."),
("行，今天先到这里。","Tamam, bugünlük burada bitirelim.")
]],
"HSK4": [
[
("我觉得先把实际情况说清楚比较好。","Bence önce gerçek durumu netleştirmek daha iyi."),
("对，先别急着做最后决定。","Evet, son kararı vermek için acele etmeyelim."),
("我们可以先把最重要的条件列出来。","Önce en önemli koşulları sıralayabiliriz."),
("这样比较容易看出差别。","Böylece farkları görmek daha kolay olur."),
("这一点也应该考虑进去。","Bu noktayı da değerlendirmeye almalıyız."),
("好，先把它记下来。","Tamam, bunu önce not edelim.")
],
[
("我理解你的担心，不过我们还可以再看看。","Endişeni anlıyorum ama biraz daha bakabiliriz."),
("与其马上决定，不如先把信息弄清楚。","Hemen karar vermek yerine önce bilgileri netleştirmek daha iyi."),
("对，这样会稳妥一些。","Evet, böyle daha temkinli olur."),
("不过也要看看会不会影响别的地方。","Ama başka bir yeri etkileyip etkilemeyeceğine de bakmalıyız."),
("那我们先比较几个选择。","O zaman birkaç seçeneği karşılaştıralım."),
("好，再听听大家的意见。","Tamam, herkesin fikrini bir kez daha dinleyelim.")
],
[
("现在的信息已经比刚才完整多了。","Şimdiki bilgiler az öncekinden çok daha tamamlanmış durumda."),
("不过有些细节还不能忽略。","Ama bazı ayrıntıları hâlâ göz ardı edemeyiz."),
("那就先把最重要的部分处理好。","O zaman önce en önemli kısmı halledelim."),
("一方面要看眼前，另一方面也要考虑以后。","Bir yandan bugünü, diğer yandan geleceği düşünmeliyiz."),
("这样做比较公平，也容易让大家接受。","Böyle yapmak daha adil ve herkes için kabul etmesi daha kolay."),
("好，我们继续往下看。","Tamam, devam edelim.")
],
[
("现在方案已经比较清楚了。","Plan artık oldukça net."),
("我建议最后再检查一次风险。","Son olarak riskleri bir kez daha kontrol etmeyi öneriyorum."),
("即使有变化，我们也还有调整空间。","Değişiklik olsa bile hâlâ ayarlama payımız var."),
("对，有备用办法会放心很多。","Evet, yedek plan olması insanı daha çok rahatlatıyor."),
("那就把责任和时间也说清楚。","O zaman sorumlulukları ve zamanı da netleştirelim."),
("好，有变化及时告诉大家。","Tamam, değişiklik olursa herkese zamanında haber verelim.")
],
[
("主要问题已经有比较清楚的处理办法了。","Ana sorun için artık oldukça net bir çözüm var."),
("剩下的先按这个方案执行。","Kalanını şimdilik bu plana göre uygulayalım."),
("过一段时间再看看要不要调整。","Bir süre sonra yeniden bakıp ayarlama gerekip gerekmediğine karar veririz."),
("我同意，这样比较稳妥。","Katılıyorum, böyle daha temkinli."),
("今天大家把意见都说清楚了。","Bugün herkes görüşünü net biçimde ifade etti."),
("好，那今天先到这里。","Tamam, bugünlük burada bitirelim.")
]],
"HSK5": [
[
("我觉得先把事实和判断分开比较好。","Bence önce olgularla yorumları ayırmak daha iyi."),
("对，先把问题定义清楚，后面才好讨论。","Evet, önce sorunu net tanımlarsak sonrası daha kolay tartışılır."),
("我们也要把不同的影响一起摆出来。","Farklı etkileri de birlikte ortaya koymalıyız."),
("这样才能知道真正需要解决的是什么。","Böylece gerçekten neyin çözülmesi gerektiğini anlayabiliriz."),
("这一点值得继续确认。","Bu noktayı teyit etmeye devam etmek gerekiyor."),
("好，先记下来，不急着下结论。","Tamam, önce not edelim; hemen sonuca varmayalım.")
],
[
("我理解你的立场，不过还想补充一个现实问题。","Bakış açını anlıyorum ama bir pratik noktayı daha eklemek istiyorum."),
("如果只看眼前，很容易忽略后面的影响。","Yalnızca bugüne bakarsak sonraki etkileri gözden kaçırmak kolay olur."),
("对，我们最好把短期和长期放在一起比较。","Evet, kısa ve uzun vadeyi birlikte karşılaştırmalıyız."),
("有不同意见没关系，关键是把理由说清楚。","Farklı görüşler sorun değil; önemli olan gerekçeleri açıkça söylemek."),
("那就先设一个判断标准。","O zaman önce bir değerlendirme ölçütü belirleyelim."),
("好，再看看有没有相反的证据。","Tamam, ters yönde kanıt var mı ona da bakalım.")
],
[
("现在大家的立场已经清楚多了。","Şimdi herkesin duruşu çok daha net."),
("不过时间和资源够不够也要考虑。","Ama zaman ve kaynakların yeterli olup olmadığını da düşünmeliyiz."),
("这个提醒很重要，不然方案可能做不下去。","Bu uyarı önemli; yoksa plan uygulanamayabilir."),
("那我们先想清楚最坏的情况。","O zaman önce en kötü durumu netleştirelim."),
("只要风险在哪里说清楚，就比较容易决定。","Riskin nerede olduğunu netleştirirsek karar vermek daha kolay olur."),
("好，先做一个暂时的决定。","Tamam, önce geçici bir karar verelim.")
],
[
("我同意，后面的责任也要分清楚。","Katılıyorum; sonraki sorumlulukları da netleştirmeliyiz."),
("团队做的决定，也要一起面对结果。","Ekip olarak alınan kararın sonucunu da birlikte karşılamalıyız."),
("我会把结论和没解决的问题分别记下来。","Sonuçları ve çözülmemiş sorunları ayrı ayrı not edeceğim."),
("这样下次就不用从头开始。","Böylece bir dahaki sefere baştan başlamamız gerekmez."),
("如果有新信息，要尽快共享。","Yeni bilgi çıkarsa mümkün olduğunca hızlı paylaşılmalı."),
("透明一点，反而更容易建立信任。","Daha şeffaf olmak güven kurmayı kolaylaştırır.")
],
[
("现在主要事实、风险和选择都比较清楚了。","Artık temel olgular, riskler ve seçenekler oldukça net."),
("我们先按今天确定的优先顺序推进。","Bugün belirlediğimiz öncelik sırasına göre ilerleyelim."),
("如果新信息出现，就及时重新评估。","Yeni bilgi çıkarsa zamanında yeniden değerlendirelim."),
("这样既不会太草率，也不会一直拖下去。","Böylece ne fazla aceleci oluruz ne de işi gereksiz uzatırız."),
("这次至少是充分讨论以后做的决定。","Bu karar en azından yeterli bir tartışmadan sonra alındı."),
("好，那就按计划继续。","Tamam, plana göre devam edelim.")
]],
"HSK6": [
[
("我也想先听听大家最真实的想法。","Ben de önce herkesin en gerçek düşüncesini duymak istiyorum."),
("这件事来得有点突然，有不同反应很正常。","Bu konu biraz ani gelişti; farklı tepkiler olması çok normal."),
("先别急着下结论，把各自最在意的地方说清楚。","Hemen sonuca varmayalım; herkes en çok neyi önemsediğini netleştirsin."),
("我同意，先听完彼此怎么想，再看下一步。","Katılıyorum; önce birbirimizi dinleyelim, sonra sonraki adıma bakalım."),
("好，那就一件一件说。","Tamam, o zaman konuları tek tek ele alalım."),
("这样比较容易理解彼此的立场。","Böylece birbirimizin bakış açısını anlamak daha kolay olur.")
],
[
("我更想知道，这件事对每个人意味着什么。","Ben daha çok bunun herkes için ne anlama geldiğini bilmek istiyorum."),
("对，不能只看表面的结果。","Evet, yalnızca yüzeydeki sonuca bakamayız."),
("如果只从自己的位置出发，很容易忽略别人的感受。","Yalnızca kendi konumumuzdan bakarsak başkalarının duygularını gözden kaçırmak kolay olur."),
("所以先把事实和感受分开说清楚。","Bu yüzden önce olguları ve duyguları ayrı ayrı netleştirelim."),
("这一点会影响我们后面怎么理解整件事。","Bu nokta sonrasında tüm konuyu nasıl anlayacağımızı etkileyecek."),
("好，先把不同的看法都放在桌面上。","Tamam, farklı görüşlerin hepsini açıkça ortaya koyalım.")
],
[
("与其马上下结论，不如先确认几个关键细节。","Hemen sonuca varmak yerine birkaç kritik ayrıntıyı teyit etmek daha iyi."),
("我同意，理由说清楚比急着决定更重要。","Katılıyorum; gerekçeyi net söylemek aceleyle karar vermekten daha önemli."),
("这个决定不仅关系到眼前，也会影响以后。","Bu karar yalnızca bugünü değil, geleceği de etkileyecek."),
("所以短期和长期都要放在一起考虑。","Bu nedenle kısa ve uzun vadeyi birlikte değerlendirmeliyiz."),
("有不同意见不代表谁对谁错。","Farklı görüşler olması birinin haklı diğerinin haksız olduğu anlamına gelmez."),
("关键是怎么在不同需要之间找到平衡。","Önemli olan farklı ihtiyaçlar arasında nasıl denge kurulacağı.")
],
[
("现在大家的立场已经比开始时清楚多了。","Şimdi herkesin duruşu başlangıca göre çok daha net."),
("不过现实条件也不能忽略。","Ama gerçek koşulları da göz ardı edemeyiz."),
("即使方向没问题，执行的时候也要留一点调整空间。","Yön doğru olsa bile uygulamada biraz ayarlama payı bırakmalıyız."),
("如果情况变了，就及时修改计划。","Durum değişirse planı zamanında değiştirelim."),
("无论最后怎么选，都应该把责任和理由说清楚。","Sonunda ne seçersek seçelim sorumlulukları ve gerekçeleri netleştirmeliyiz."),
("这样大家会更安心。","Böylece herkes kendini daha rahat hisseder.")
],
[
("今天没有把所有问题都解决，但最重要的已经说清楚了。","Bugün bütün sorunları çözmedik ama en önemli noktaları netleştirdik."),
("有些答案需要时间验证，不必今天全部确定。","Bazı cevapları zaman doğrulayacak; bugün her şeyi kesinleştirmek gerekmiyor."),
("真正的理解不是完全同意，而是知道对方为什么这样想。","Gerçek anlayış tamamen aynı fikirde olmak değil, karşıdakinin neden öyle düşündüğünü bilmektir."),
("我同意，给彼此留一点空间反而更真诚。","Katılıyorum; birbirimize biraz alan bırakmak daha samimi."),
("以后再回头看今天，也许会有新的理解。","İleride bugüne geri baktığımızda belki yeni bir anlayışımız olacak."),
("好，下一步我们一起面对。","Tamam, bir sonraki adımla birlikte yüzleşiriz.")
]]
}

def stable_pick(options, key):
    h=hashlib.sha256(key.encode("utf-8")).digest()
    return options[int.from_bytes(h[:4],"big") % len(options)]

def is_rebuild(level, turn):
    return any(a <= turn <= b for a,b in REBUILD_RANGES.get(level, []))

def active_cards(data):
    cards=[x for x in data.get("learning",{}).get("vocabularyCards",[]) if x.get("kind")=="active" and x.get("zh")]
    if not cards:
        cards=[{"zh":data.get("titleZh","这件事"),"tr":data.get("titleTr","bu konu"),"exampleZh":"","exampleTr":""}]
    return cards

def term_kind(card):
    term=str(card.get("zh","")).strip()
    ex=str(card.get("exampleZh","")).strip()
    if re.search(rf"(先|要|需要|可以|再){re.escape(term)}", ex) or ex.startswith(term+"以前"):
        return "verb"
    if any(x in term for x in ("一点","一些")):
        return "adj"
    if term in {"试","选择","确认","等","调整","决定","沟通","帮忙","检查","安排","解决","比较","讨论","联系","准备","继续","改变","涨价"}:
        return "verb"
    return "noun"

def term_question(card, level):
    z=str(card.get("zh","")).strip()
    t=str(card.get("tr","")).strip()
    k=term_kind(card)
    if k=="verb":
        if level=="HSK2":
            return f"那要不要先{z}一下？", f"O zaman önce {t} deneyelim mi?"
        return f"那这一步要不要先{z}一下？", f"O zaman bu adımda önce {t} gerekir mi?"
    if k=="adj":
        return f"你觉得{z}怎么样？", f"{t} olması hakkında ne düşünüyorsun?"
    if level=="HSK2":
        return f"那{z}呢？", f"Peki {t}?"
    return f"说到{z}，你怎么看？", f"{t} konusunda ne düşünüyorsun?"

def term_statement(card, level):
    z=str(card.get("zh","")).strip()
    t=str(card.get("tr","")).strip()
    k=term_kind(card)
    if k=="verb":
        return f"我觉得先{z}一下比较好。", f"Bence önce {t} daha iyi olur."
    if k=="adj":
        return f"我觉得{z}会更合适。", f"Bence {t} olması daha uygun olur."
    if level=="HSK2":
        return f"我觉得{z}也很重要。", f"Bence {t} de önemli."
    return f"我觉得{z}这一点也不能忽略。", f"Bence {t} konusunu da göz ardı etmemeliyiz."

def scaffold_line(level, turn, data, cards):
    phase=min(4,(turn-1)//20)
    slot=(turn-1)%8
    idx=((turn-1)//4) % len(cards)
    card=cards[idx]
    next_card=cards[(idx+1)%len(cards)]

    if level=="HSK6" and turn==1:
        return f"今天就把“{data.get('titleZh','这件事')}”这件事好好聊一聊吧。", f"Bugün “{data.get('titleTr','bu konu')}” konusunu açıkça konuşalım."
    if slot==0:
        return term_question(card, level)
    if slot==4:
        return term_statement(next_card, level)

    generic_slots=[1,2,3,5,6,7]
    j=generic_slots.index(slot)
    return PHASE[level][phase][j]

def pinyin_text(text):
    # Safety-first display: correct syllables separated by spaces.
    out=[]
    for ch in t2s.convert(text):
        if "\u3400" <= ch <= "\u9fff":
            if ch=="嗯":
                out.append("èn")
            else:
                py=lazy_pinyin(ch,style=Style.TONE,neutral_tone_with_five=False,strict=False,errors="default")[0]
                out.append(py)
        elif ch in "，。？！；：、,.?!;:":
            if out:
                out[-1]=out[-1]+{
                    "，":",","。":".","？":"?","！":"!","；":";", "：":":"
                }.get(ch,ch)
            else:
                out.append(ch)
        elif ch.isspace():
            continue
        else:
            out.append(ch)
    s=" ".join(out)
    s=s.replace("nǎ ér","nǎr").replace("zhè ér","zhèr").replace("nà ér","nàr")
    s=s.replace("ń","èn").replace("ň","èn")
    for i,c in enumerate(s):
        if c.isalpha():
            s=s[:i]+c.upper()+s[i+1:]
            break
    return s

def naturalize_existing(level, zh, prev, turn, key):
    zh=t2s.convert(zh.strip())

    # Beginner question/answer patterns: keep target vocabulary but make the exchange less textbook-like.
    if level in {"HSK1","HSK2"}:
        m=re.fullmatch(r"这是(.+?)吗？",zh)
        if m:
            x=m.group(1)
            return stable_pick([f"这是{x}吗？",f"这个是{x}吗？",f"这是{x}，对吗？"],key)
        m=re.fullmatch(r"对，这是(.+?)。",zh)
        if m:
            x=m.group(1)
            return stable_pick([f"对，就是{x}。",f"嗯，对，这是{x}。",f"没错，是{x}。"],key)
        m=re.fullmatch(r"(.+?)在哪儿？",zh)
        if m:
            x=m.group(1)
            return stable_pick([f"{x}在哪儿？",f"那{x}在哪儿？",f"{x}呢？"],key)
        m=re.fullmatch(r"(.+?)在这里。",zh)
        if m:
            x=m.group(1)
            return stable_pick([f"{x}在这儿。","就在这里。",f"你看，{x}在这儿。"],key)
        m=re.fullmatch(r"(.+?)在那边。",zh)
        if m:
            x=m.group(1)
            return stable_pick([f"{x}在那边。","就在那边。",f"你看，{x}在那边。"],key)
        m=re.fullmatch(r"这个(.+?)在这里。",zh)
        if m:
            x=m.group(1)
            return stable_pick([f"你看，这个{x}在这儿。",f"这个{x}就在这里。"],key)
        m=re.fullmatch(r"我们先(.+?)。",zh)
        if m and len(m.group(1)) <= 4:
            x=m.group(1)
            return f"我们先{x}一下吧。"

    # Repair known generator-shaped sentences.
    m=re.fullmatch(r"(.+?)是这次要考虑的重点之一。",zh)
    if m:
        x=m.group(1); return f"{x}这一点也得认真考虑。"
    m=re.fullmatch(r"关于(.+?)，我们还要再讨论一下。",zh)
    if m:
        x=m.group(1); return f"说到{x}，我们还得再商量一下。"
    m=re.fullmatch(r"我们最好再确认一下(.+?)。",zh)
    if m:
        x=m.group(1)
        if x in {"觉得","需要","同意","决定"}: return "这一点我们最好再确认一下。"
        return f"{x}这部分我们最好再确认一下。"
    m=re.fullmatch(r"如果(.+?)没有问题，我们就继续。",zh)
    if m:
        return f"如果{m.group(1)}这边没问题，我们就继续。"

    opts=COMMON.get(zh)
    if opts:
        return stable_pick(opts,key)

    if prev.endswith("？") and zh.startswith(("我觉得","我同意")) and not zh.startswith("嗯，"):
        return "嗯，"+zh
    return zh

def main():
    stats=defaultdict(lambda:{"scenes":0,"turns":0,"changedTurns":0,"rebuiltTurns":0})
    before=Counter(); after=Counter()
    files=sorted(scene_root.glob("HSK*/scenes/ZH_HSK*_SC*.json"))

    for path in files:
        data=json.loads(path.read_text(encoding="utf-8"))
        level=data.get("level") or path.parts[-3]
        scene_id=data["id"]
        cards=active_cards(data)
        src=data.get("dialogues",[])
        out=[]
        changed=rebuilt=0
        prev=""

        for i,d in enumerate(src,1):
            old=t2s.convert(str(d.get("zh","")).strip())
            key=f"{scene_id}:{d.get('id')}:{prev}"
            if level in PHASE and is_rebuild(level,i):
                new,tr=scaffold_line(level,i,data,cards)
                rebuilt+=1
            else:
                new=naturalize_existing(level,old,prev,i,key)
                tr=str(d.get("tr","")).strip()

            new=t2s.convert(new)
            new=re.sub(r"^(嗯，){2,}","嗯，",new)
            if out and new==out[-1]["zh"]:
                new=("嗯，" if level in {"HSK1","HSK2","HSK3"} else "对，")+new

            py=str(d.get("pinyin","")).strip() if new==old else pinyin_text(new)
            out.append({"id":d.get("id"),"speaker":d.get("speaker"),"zh":new,"pinyin":py,"tr":tr})

            before[old]+=1; after[new]+=1
            if new!=old: changed+=1
            prev=new

        patch={
            "naturalizationVersion":3,
            "sceneId":scene_id,
            "level":level,
            "sourceTitleZh":data.get("titleZh"),
            "sourceTitleTr":data.get("titleTr"),
            "sourceMiniAdventureTr":data.get("miniAdventureTr"),
            "dialogues":out,
        }
        dest=out_root/level/path.name
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(json.dumps(patch,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        stats[level]["scenes"]+=1
        stats[level]["turns"]+=len(src)
        stats[level]["changedTurns"]+=changed
        stats[level]["rebuiltTurns"]+=rebuilt

    report={
        "naturalizationVersion":3,
        "sceneCount":len(files),
        "turnCount":sum(x["turns"] for x in stats.values()),
        "changedTurnCount":sum(x["changedTurns"] for x in stats.values()),
        "rebuiltTurnCount":sum(x["rebuiltTurns"] for x in stats.values()),
        "uniqueZhBefore":len(before),
        "uniqueZhAfter":len(after),
        "duplicateTurnsBefore":sum(n-1 for n in before.values() if n>1),
        "duplicateTurnsAfter":sum(n-1 for n in after.values() if n>1),
        "levels":dict(sorted(stats.items())),
    }
    (out_root/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False))

if __name__=="__main__":
    main()
