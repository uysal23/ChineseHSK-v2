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

if len(sys.argv) != 4:
    raise SystemExit("usage: polish_dialogue_v10_final_native.py <baseline-level-root> <candidate-root> <out-root>")

BASE = Path(sys.argv[1])
CAND = Path(sys.argv[2])
OUT = Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)

def pinyin_text(s: str) -> str:
    s=s.replace("嗯","ENMARK")
    parts=[]
    for tok in jieba.lcut(s,cut_all=False):
        if tok=="ENMARK":
            parts.append("en")
        elif re.fullmatch(r"[\u3400-\u9fff]+",tok):
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

def pick(opts,key):
    h=int(hashlib.sha256(key.encode("utf-8")).hexdigest()[:8],16)
    return opts[h%len(opts)]

def han_len(s):
    return sum(1 for c in s if "\u3400"<=c<="\u9fff")

def active_cards(scene):
    cards=[x for x in scene.get("learning",{}).get("vocabularyCards",[]) if x.get("kind")=="active"]
    active=[str(x.get("zh","")).strip() for x in cards if str(x.get("zh","")).strip()]
    trmap={str(x.get("zh","")).strip():str(x.get("tr","")).strip() for x in cards}
    return active,trmap

def category(title,active,mini):
    text=title+" "+" ".join(active)+" "+mini
    tests=[
      ("health",["健康","医生","医院","护士","体检","血压","运动","照护","休息","疲劳","生活方式","病"]),
      ("education",["学校","高中","大学","学习","考试","挂科","老师","同学","毕业","作业","摄影","录取","教育"]),
      ("work",["工作","项目","客户","同事","经理","面试","实习","职业","领导","责任","退休","上班"]),
      ("business",["咖啡馆","顾客","订单","价格","成本","营业","商户","菜单","食材","店","生意"]),
      ("community",["社区","公益","志愿","募捐","居民","洪水","救助","规划","道路","地方新闻","菜园"]),
      ("travel",["火车","车站","站台","旅行","酒店","导游","出租车","公交","路线"]),
      ("family",["家人","家庭","伴侣","订婚","婚礼","结婚","恋爱","爷爷","奶奶","孩子","外孙","孙辈","全家福","两家人"]),
      ("memory",["回忆","旧","过去","往事","留下","人生","家","二十年","周年","老顾客"]),
    ]
    for c,ks in tests:
        if any(k in text for k in ks):
            return c
    return "general"

# Natural category-specific lines used only to replace course-wide boilerplate.
# Each pair is zh/tr. Pools are intentionally larger than the number normally used
# in one scene and are selected by scene+turn hash, so different scenes do not
# collapse into one shared script.
CTX = {
"family":[
("先把各自真实的感受说出来，别急着替别人做决定。","Önce herkes gerçek duygusunu söylesin; başkası adına karar vermek için acele etmeyelim."),
("一家人想法不一样很正常，重要的是把原因说明白。","Bir ailede fikirlerin farklı olması normal; önemli olan nedenlerini açıkça anlatmak."),
("现实安排可以慢慢定，先听清楚彼此真正担心什么。","Pratik düzenlemeler zamanla kararlaştırılabilir; önce birbirimizin gerçekten neden kaygılandığını anlayalım."),
("这件事对每个人的意义不一样，所以反应不同也很正常。","Bu konunun herkes için anlamı farklı; bu yüzden tepkilerin farklı olması da normal."),
("我们可以不同意，但不要替对方猜他在想什么。","Aynı fikirde olmayabiliriz ama karşımızdakinin ne düşündüğünü onun yerine varsaymayalım."),
("先把眼前能确定的事情说清楚，其他的以后再慢慢商量。","Önce şu anda netleştirebildiklerimizi konuşalım; diğerlerini sonra yavaş yavaş değerlendiririz."),
("我更在意的是，最后的安排能不能让每个人都觉得被尊重。","Benim için asıl önemli olan, son düzenlemenin herkesin kendisine saygı duyulduğunu hissettirmesi."),
("有些担心不是反对，只是需要一点时间适应。","Bazı kaygılar karşı çıkmak anlamına gelmez; bazen alışmak için biraz zamana ihtiyaç vardır."),
("如果谁心里还有顾虑，现在说出来反而更好。","Birinin içinde hâlâ kaygı varsa şimdi söylemesi daha iyi olur."),
("只要大家愿意继续沟通，很多问题都不用一次解决。","Herkes iletişim kurmaya devam ettiği sürece bütün sorunları tek seferde çözmek gerekmiyor."),
("这件事不只是安排问题，也跟每个人的感受有关。","Bu yalnızca bir düzenleme meselesi değil; herkesin duygularıyla da ilgili."),
("我希望我们最后记住的，不是谁说服了谁，而是大家都认真听过彼此。","Sonunda hatırladığımız şeyin kimin kimi ikna ettiği değil, herkesin birbirini gerçekten dinlemiş olması olmasını istiyorum."),
("先别把未来想得太满，给彼此一点调整的空间。","Geleceği şimdiden tamamen doldurmayalım; birbirimize biraz uyum alanı bırakalım."),
("有些事情听起来简单，真正落到生活里才会发现细节很多。","Bazı şeyler kulağa basit gelir; günlük hayata gelince pek çok ayrıntı ortaya çıkar."),
("大家都出于关心，只是表达关心的方式不一样。","Herkesin niyeti ilgilenmek; yalnızca bunu ifade etme biçimleri farklı."),
("我理解你的顾虑，不过也想听听另一边的感受。","Kaygını anlıyorum ama diğer tarafın duygularını da duymak istiyorum."),
],
"work":[
("先把事实和责任分开说清楚，再讨论下一步会公平一些。","Önce olguları ve sorumlulukları ayrı ayrı netleştirirsek sonraki adımı konuşmak daha adil olur."),
("这个决定会影响到谁，最好现在就弄清楚。","Bu kararın kimi etkileyeceğini şimdiden netleştirmek iyi olur."),
("先别急着找责任人，先看看问题到底出在哪个环节。","Hemen sorumlu aramayalım; önce sorunun hangi aşamada çıktığını görelim."),
("如果目标不变，执行方法其实可以调整。","Hedef değişmiyorsa uygulama yöntemi ayarlanabilir."),
("时间、资源和人的负担都要算进去，不然方案落不了地。","Zamanı, kaynakları ve insanların yükünü birlikte hesaba katmalıyız; yoksa plan uygulanamaz."),
("这个方案能不能执行，比听起来漂亮更重要。","Bu planın uygulanabilir olması, kulağa güzel gelmesinden daha önemli."),
("有不同意见没关系，关键是把依据说出来。","Farklı görüşlerin olması sorun değil; önemli olan dayanağını açıklamak."),
("先定一个可以检查的标准，之后看结果再调整。","Önce kontrol edilebilir bir ölçüt belirleyelim; sonra sonuca göre ayarlarız."),
("如果出现新情况，要尽快同步，不要等问题变大。","Yeni bir durum çıkarsa hızla paylaşalım; sorunun büyümesini beklemeyelim."),
("这个风险可以接受，但前提是我们知道怎么应对。","Bu risk kabul edilebilir; ama nasıl karşılık vereceğimizi bilmemiz şart."),
("别只看眼前的效率，长期的合作也很重要。","Yalnızca kısa vadeli verimliliğe bakmayalım; uzun vadeli iş birliği de önemli."),
("我赞成先试，但要提前约好什么时候复盘。","Önce denemeye katılıyorum ama ne zaman değerlendirme yapacağımızı baştan belirleyelim."),
("把分工说清楚以后，执行起来会顺很多。","Görev dağılımını netleştirince uygulama çok daha sorunsuz ilerler."),
("如果结果跟预期不一样，就根据事实改，不必硬撑原来的方案。","Sonuç beklediğimiz gibi olmazsa olgulara göre değiştiririz; eski planda ısrar etmek gerekmez."),
("这件事既有业务影响，也会影响团队里的信任。","Bu konu hem iş sonuçlarını hem de ekip içindeki güveni etkiler."),
("我们先解决最紧急的，再处理可以等一等的部分。","Önce en acil kısmı çözelim; bekleyebilecek konuları sonra ele alırız."),
],
"business":[
("顾客的感受要看，成本和实际操作也不能忽略。","Müşteri deneyimine bakmalıyız; maliyet ve uygulama tarafını da göz ardı edemeyiz."),
("先算清楚这件事会给店里带来什么实际变化。","Önce bunun işletmede gerçekte neyi değiştireceğini hesaplayalım."),
("如果顾客喜欢但店里做不下去，也不是一个长期办法。","Müşteri sevse bile işletme sürdüremiyorsa uzun vadeli bir çözüm değildir."),
("可以先小范围试一试，再根据顾客反应调整。","Önce küçük ölçekte deneyip müşteri tepkisine göre ayarlayabiliriz."),
("价格、品质和工作量最好放在一起看。","Fiyatı, kaliteyi ve iş yükünü birlikte değerlendirmek en iyisi."),
("这件事不能只凭感觉，最好看看最近的实际数据。","Bunu yalnızca hisle değerlendirmeyelim; son dönemin gerçek verilerine bakalım."),
("如果要改，最好先让员工知道为什么要改。","Değişiklik yapılacaksa çalışanlara nedenini önceden anlatmak iyi olur."),
("我更担心的是，忙的时候这个办法还能不能正常执行。","Ben daha çok yoğun saatlerde bu yöntemin uygulanıp uygulanamayacağını düşünüyorum."),
("别一次改太多，先把最影响顾客体验的部分处理好。","Bir seferde çok fazla şeyi değiştirmeyelim; önce müşteri deneyimini en çok etkileyen kısmı düzeltelim."),
("只要品质不受影响，细节上可以慢慢调整。","Kalite etkilenmediği sürece ayrıntıları zamanla ayarlayabiliriz."),
("店里的办法最终还是要经得住每天实际使用。","İşletmedeki yöntemler sonuçta günlük kullanımda işe yaramalı."),
("顾客的意见很重要，但也要看是不是普遍情况。","Müşteri görüşü önemli ama bunun yaygın bir durum olup olmadığına da bakmalıyız."),
("先把成本上限说清楚，后面做选择会容易很多。","Önce maliyet sınırını netleştirirsek sonrasında seçim yapmak çok daha kolay olur."),
("这个想法可以保留，不过最好先做一个简单测试。","Bu fikir kalabilir ama önce basit bir deneme yapmak iyi olur."),
("如果实际效果不好，我们就及时改，不必硬撑。","Gerçek sonuç iyi olmazsa zamanında değiştiririz; ısrar etmeye gerek yok."),
("我希望最后的做法既让顾客舒服，也不会把员工累坏。","Son yöntemin hem müşteriyi memnun etmesini hem de çalışanları yormamasını istiyorum."),
],
"health":[
("先听医生把情况说清楚，再决定接下来怎么调整。","Önce doktor durumu net anlatsın, sonra neyi değiştireceğimize karar veririz."),
("检查结果只是一个提醒，真正重要的是接下来怎么做。","Muayene sonucu bir uyarıdır; asıl önemli olan bundan sonra ne yapacağımız."),
("别一次给自己太大压力，能长期坚持的改变更重要。","Kendimize bir anda çok yüklenmeyelim; sürdürülebilir değişiklik daha önemli."),
("如果身体有新的变化，要及时告诉医生。","Vücutta yeni bir değişiklik olursa doktora zamanında söylemeliyiz."),
("休息、吃饭和运动都要一起看，不能只改一项。","Dinlenme, beslenme ve hareketi birlikte değerlendirmek gerekir; yalnızca birini değiştirmek yetmez."),
("我更关心的是，这个计划能不能真的坚持下去。","Ben daha çok bu planın gerçekten sürdürülebilir olup olmadığını önemsiyorum."),
("先从最容易做到的一件事开始，效果会更实际。","Önce en kolay yapılabilecek tek bir şeyden başlamak daha gerçekçi olur."),
("有些指标需要时间观察，不用今天就下结论。","Bazı göstergeleri zaman içinde izlemek gerekir; bugün hemen sonuç çıkarmaya gerek yok."),
("如果不舒服，就别为了完成计划硬撑。","Rahatsız hissedersen planı tamamlamak uğruna kendini zorlama."),
("我们先把最需要注意的风险记下来。","Önce en çok dikkat etmemiz gereken riskleri not edelim."),
("医生的建议要听，也要结合每天的实际生活来安排。","Doktorun önerilerini dinlemeli ve günlük yaşama göre düzenlemeliyiz."),
("改善一点就是进步，不需要一下做到完美。","Biraz iyileşmek bile ilerlemedir; bir anda kusursuz olmak gerekmez."),
("先把作息稳定下来，再看其他问题会不会跟着改善。","Önce günlük düzeni oturtalım, sonra diğer sorunlar da düzeliyor mu bakalım."),
("家人可以提醒，但最后还是要让本人愿意配合。","Aile hatırlatabilir ama kişinin kendisinin de istekli olması gerekir."),
("我们先按这个方法试一段时间，再看检查结果。","Bu yöntemi bir süre deneyelim, sonra muayene sonuçlarına tekrar bakarız."),
("健康方面宁可多确认一次，也不要因为怕麻烦而忽略。","Sağlık konusunda bir kez fazla kontrol etmek, zahmet olur diye göz ardı etmekten iyidir."),
],
"education":[
("先别因为一次结果就否定自己，先看看具体哪里出了问题。","Tek bir sonuç yüzünden kendini tamamen olumsuz değerlendirme; önce sorunun tam olarak nerede olduğunu görelim."),
("把不会的地方找出来，比反复担心分数更有用。","Bilmediğin noktaları bulmak, puanı tekrar tekrar düşünmekten daha faydalı."),
("先看看学习方法是不是适合现在这门课。","Önce çalışma yönteminin bu ders için uygun olup olmadığına bakalım."),
("老师的反馈可以参考，但也要结合自己的实际情况。","Öğretmenin geri bildirimi önemli ama kendi gerçek durumunla birlikte değerlendirmelisin."),
("如果时间安排有问题，就先调整每天的节奏。","Zaman planında sorun varsa önce günlük ritmi düzenleyelim."),
("一次失败不能说明能力不够，但能提醒我们哪里需要改变。","Bir başarısızlık yetersiz olduğun anlamına gelmez; neyin değişmesi gerektiğini gösterebilir."),
("先把最薄弱的一部分补起来，后面会轻松很多。","Önce en zayıf kısmı tamamlayalım; sonrası daha kolay olur."),
("我更想知道的是，你自己觉得哪一步最困难。","Ben daha çok senin hangi adımı en zor bulduğunu merak ediyorum."),
("别只看成绩，也看看这段时间真正学会了什么。","Yalnızca nota bakma; bu süreçte gerçekten ne öğrendiğine de bak."),
("如果方法有效，就继续；没有效果就及时换。","Yöntem işe yarıyorsa devam et; etkili değilse zamanında değiştir."),
("把目标分小一点，每完成一步都会更有信心。","Hedefi küçük parçalara böl; her adımı tamamladıkça güvenin artar."),
("同学的办法可以参考，但不一定完全适合你。","Arkadaşının yöntemi örnek alınabilir ama sana tamamen uymayabilir."),
("先把下周能做到的事情定下来，不用一次想完整个学期。","Önce gelecek hafta yapabileceklerini belirle; bütün dönemi bir kerede planlamak gerekmez."),
("如果还有不懂的，就直接问老师，不要一直拖。","Hâlâ anlamadığın yer varsa doğrudan öğretmene sor; sürekli erteleme."),
("这次的经验要留下来，下次遇到类似问题就知道怎么处理。","Bu deneyimi akılda tut; benzer bir sorun çıkarsa nasıl davranacağını bilirsin."),
("最重要的是找到适合自己的节奏，而不是跟别人比快慢。","En önemlisi kendi ritmini bulmak; başkalarıyla hız yarışı yapmak değil."),
],
"community":[
("先看看这件事会影响到哪些人，再决定怎么安排。","Önce bunun kimleri etkileyeceğini görelim, sonra nasıl düzenleyeceğimize karar veririz."),
("社区里的需求不完全一样，最好多听几种声音。","Topluluktaki ihtiyaçlar aynı değil; birkaç farklı görüşü dinlemek iyi olur."),
("先解决最急的需求，其他的再按顺序处理。","Önce en acil ihtiyacı çözelim, diğerlerini sırayla ele alırız."),
("志愿者愿意帮忙很好，但分工还是要说清楚。","Gönüllülerin yardım istemesi çok iyi ama görev dağılımı yine de net olmalı."),
("信息越透明，大家越容易互相信任。","Bilgi ne kadar şeffaf olursa insanların birbirine güvenmesi o kadar kolay olur."),
("这个办法要让老人、孩子和行动不方便的人也能用。","Bu yöntem yaşlıların, çocukların ve hareketi kısıtlı kişilerin de kullanabileceği şekilde olmalı."),
("别只看活动当天，后面的维护也要有人负责。","Yalnızca etkinlik gününe bakmayalım; sonrasındaki bakımın da sorumlusu olmalı."),
("如果资源有限，就先把最重要的部分做好。","Kaynaklar sınırlıysa önce en önemli kısmı iyi yapalım."),
("有不同意见很正常，公共事情本来就需要多商量。","Farklı görüşlerin olması normal; ortak işler zaten daha çok konuşmayı gerektirir."),
("先把能公开的信息说清楚，避免大家靠猜测做判断。","Paylaşılabilecek bilgileri açıkça anlatalım; insanların tahminle karar vermesini önleyelim."),
("我更关心的是，这个决定对普通居民会有什么实际影响。","Ben daha çok bu kararın sıradan sakinleri gerçekte nasıl etkileyeceğini önemsiyorum."),
("可以先做一个小规模试点，再决定要不要扩大。","Önce küçük ölçekli bir deneme yapıp sonra genişletip genişletmeyeceğimize karar verebiliriz."),
("遇到紧急情况时，简单清楚的安排比复杂方案更有用。","Acil durumda basit ve net düzenlemeler karmaşık planlardan daha kullanışlıdır."),
("大家愿意互相帮忙很重要，但安全规则也不能省。","İnsanların birbirine yardım etmesi önemli ama güvenlik kuralları atlanamaz."),
("事情结束以后最好再复盘一次，看看哪里还能做得更好。","İş bittikten sonra bir değerlendirme yapıp nerede daha iyi olabileceğimize bakalım."),
("一个社区真正可靠，不是因为没有问题，而是出了问题以后有人一起解决。","Güvenilir bir topluluk, hiç sorun çıkmamasıyla değil; sorun çıktığında insanların birlikte çözmesiyle anlaşılır."),
],
"travel":[
("先把时间和路线确认好，后面会轻松很多。","Önce zamanı ve rotayı netleştirirsek sonrası çok daha rahat olur."),
("遇到变化先别急，看看还有没有别的选择。","Bir değişiklik olduğunda telaşlanmayalım; başka seçenek var mı bakalım."),
("先确认最重要的信息，其他细节路上再说也来得及。","Önce en önemli bilgiyi netleştirelim; diğer ayrıntıları yolda da konuşabiliriz."),
("如果时间变了，要马上重新看后面的安排。","Saat değişirse sonraki planı hemen yeniden gözden geçirmeliyiz."),
("旅行里有一点意外很正常，关键是别让小问题影响整个行程。","Seyahatte küçük sürprizler normal; önemli olan küçük bir sorunun bütün programı bozmasına izin vermemek."),
("我更想先确认我们现在在哪里、下一步去哪儿。","Önce şu anda nerede olduğumuzu ve sonraki adımda nereye gideceğimizi netleştirmek istiyorum."),
("路线清楚以后，大家心里都会踏实一点。","Rota netleşince herkes kendini daha rahat hisseder."),
("有备用办法就不用太担心。","Yedek bir çözüm varsa fazla kaygılanmaya gerek yok."),
("别为了赶时间把重要的东西忘了。","Zamana yetişeceğiz diye önemli şeyleri unutmayalım."),
("如果需要问路，就直接问清楚，不要一直猜。","Yol sormak gerekiyorsa açıkça soralım; sürekli tahmin etmeyelim."),
("先把票、证件和手机这些东西确认一遍。","Önce bilet, belge ve telefon gibi önemli şeyleri bir kez kontrol edelim."),
("安排可以变，安全和基本信息不能马虎。","Plan değişebilir ama güvenlik ve temel bilgiler konusunda özensiz davranamayız."),
("我们先解决眼前的问题，行程后面的部分再调整。","Önce şu anki sorunu çözelim; programın kalanını sonra ayarlarız."),
("只要大家保持联系，临时变化也不难处理。","Herkes iletişimde kaldığı sürece son dakika değişikliklerini yönetmek zor olmaz."),
("这次有点折腾，不过以后就知道该提前准备什么了。","Bu kez biraz uğraştırdı ama bir dahaki sefere neyi önceden hazırlamamız gerektiğini biliyoruz."),
("旅行顺不顺利，不只看计划，也看出了问题以后怎么应对。","Bir yolculuğun iyi geçmesi yalnızca plana değil, sorun çıkınca nasıl davrandığımıza da bağlıdır."),
],
"memory":[
("有些细节可能记不清了，但当时的感受还在。","Bazı ayrıntılar unutulmuş olabilir ama o zamanki duygu hâlâ duruyor."),
("现在回头看，很多当年的小事都有了不一样的意义。","Bugün geriye baktığımızda o zamanın küçük olayları bile farklı bir anlam kazanıyor."),
("我们记住的不一定是事情本身，也可能是当时和谁在一起。","Hatırladığımız şey her zaman olayın kendisi değildir; bazen o sırada kiminle olduğumuzdur."),
("过去不能重来，但它会影响我们现在怎么看生活。","Geçmiş tekrar yaşanamaz ama bugün hayata nasıl baktığımızı etkiler."),
("有些东西留下来，不是因为贵，而是因为里面有故事。","Bazı şeyleri değerli oldukları için değil, içinde hikâye taşıdıkları için saklarız."),
("我觉得现在再看这件事，比当时多了一层理解。","Bence bugün bu konuya baktığımızda o zamana göre daha derin anlıyoruz."),
("人会变，记忆也会变，所以大家记得不一样很正常。","İnsanlar değişir, anılar da değişir; bu yüzden herkesin farklı hatırlaması normal."),
("我们不用争谁记得最准确，把各自记得的都留下来就好。","Kimin en doğru hatırladığını tartışmaya gerek yok; herkes kendi hatırladığını paylaşsın."),
("真正留下来的，常常不是一个答案，而是一种生活方式。","Geride kalan şey çoğu zaman tek bir cevap değil, bir yaşam biçimidir."),
("当年的选择未必完美，但它确实把我们带到了今天。","O zamanki seçim kusursuz olmayabilir ama bizi bugüne getirdi."),
("听别人讲同一段过去，也会发现自己以前没注意到的部分。","Aynı geçmişi başkasından dinlemek, daha önce fark etmediğimiz yönleri gösterir."),
("有些遗憾不能改，但可以让我们以后做得更好。","Bazı pişmanlıkları değiştiremeyiz ama gelecekte daha iyi davranmamıza yardım edebilir."),
("如果把这些故事留下来，下一代也能知道我们从哪里来。","Bu hikâyeleri korursak sonraki kuşak da nereden geldiğimizi bilir."),
("我更愿意把经验讲出来，而不是把它变成别人必须照做的规则。","Deneyimi paylaşmayı, başkalarının uymak zorunda olduğu bir kurala dönüştürmeye tercih ederim."),
("回忆不是为了停在过去，而是让我们更清楚现在珍惜什么。","Anılar geçmişte kalmak için değil, bugün neye değer verdiğimizi daha iyi anlamak içindir."),
("走到今天以后，我反而更能接受很多事情没有唯一答案。","Bugüne geldikten sonra birçok şeyin tek bir cevabı olmadığını daha kolay kabul ediyorum."),
],
"general":[
("先把真正的问题说清楚，别急着找一个漂亮答案。","Önce gerçek sorunu netleştirelim; kulağa güzel gelen bir cevap bulmak için acele etmeyelim."),
("每个人看到的角度不一样，把这些角度放在一起会更完整。","Herkes farklı bir açı görüyor; bu açıları bir araya getirince tablo daha tamamlanır."),
("先确认我们已经知道什么，再说还缺什么信息。","Önce ne bildiğimizi netleştirelim, sonra hangi bilginin eksik olduğunu konuşalım."),
("有不同意见没关系，只要理由说得清楚就能继续谈。","Farklı görüşlerin olması sorun değil; gerekçeler açık olduğu sürece konuşmaya devam edebiliriz."),
("如果现在还不能确定，就先保留一点调整空间。","Şu anda kesinleştiremiyorsak biraz uyum payı bırakalım."),
("我更关心这个选择实际会带来什么变化。","Ben daha çok bu seçimin gerçekte neyi değiştireceğini önemsiyorum."),
("先别把问题想得太抽象，回到具体情况会更容易判断。","Sorunu fazla soyutlaştırmayalım; somut duruma dönmek değerlendirmeyi kolaylaştırır."),
("我们先处理最关键的一点，再看其他细节。","Önce en kritik noktayı ele alalım, sonra diğer ayrıntılara bakarız."),
("这个想法可以继续讨论，不过最好再确认一下实际条件。","Bu fikir konuşulabilir ama gerçek koşulları bir kez daha doğrulamak iyi olur."),
("我同意方向，不过执行的时候需要留一点余地。","Yön konusunda katılıyorum ama uygulamada biraz esneklik bırakmak gerekiyor."),
("如果出现新情况，我们就根据新的事实调整。","Yeni bir durum çıkarsa yeni olgulara göre ayarlarız."),
("不用追求一次把所有问题都解决，先把下一步走稳。","Bütün sorunları tek seferde çözmeye çalışmayalım; önce sonraki adımı sağlam atalım."),
("我们至少已经知道彼此最在意什么了。","En azından artık birbirimizin en çok neyi önemsediğini biliyoruz."),
("把责任和时间说清楚，后面执行会容易很多。","Sorumlulukları ve zamanı netleştirince uygulama çok daha kolay olur."),
("这个决定不是不能改，以后有新情况可以重新评估。","Bu karar değiştirilemez değil; ileride yeni durum olursa yeniden değerlendirilebilir."),
("今天先把能确定的部分定下来，剩下的以后继续聊。","Bugün netleştirebildiğimiz kısmı kararlaştıralım; kalanını sonra konuşuruz."),
]
}


# v8: story-mode pools. These are used for course-wide boilerplate only.
# Crucially, they are NOT prefixed with arbitrary active-vocabulary nouns.
# That avoids unnatural lines such as "从语境这方面看..." in ordinary family scenes.
CTX["media"] = [
("先从这次采访为什么会发生说起吧。","Önce bu röportajın neden yapıldığından başlayalım."),
("我更想知道的是，这件事对平时来这里的人意味着什么。","Ben daha çok bunun buraya düzenli gelen insanlar için ne ifade ettiğini merak ediyorum."),
("可以讲一个具体例子吗？这样大家会更容易理解。","Somut bir örnek verebilir misiniz? Böylece herkes daha kolay anlar."),
("如果只说结果，听众可能不知道中间经历了什么。","Yalnızca sonucu söylersek dinleyiciler süreçte neler yaşandığını anlamayabilir."),
("这件事最打动人的地方，其实是它跟普通人的生活有关系。","Bu konunun en etkileyici yanı aslında sıradan insanların yaşamıyla ilgili olması."),
("我想听听顾客自己的感受，不只听店里怎么介绍。","Yalnızca işletmenin anlatımını değil, müşterinin kendi deneyimini de duymak istiyorum."),
("最开始的时候，你们也没想到会有今天吧？","Başlangıçta bugüne geleceğinizi siz de düşünmemiştiniz, değil mi?"),
("有些变化很小，但时间长了，大家就会感觉到不一样。","Bazı değişiklikler çok küçük olur ama zaman geçince insanlar farkı hisseder."),
("新闻里最好把背景说明白，免得大家只看到一个片段。","Haberde arka planı iyi açıklamak gerekir; yoksa insanlar yalnızca bir parçayı görür."),
("如果社区里的人愿意来、愿意留下来聊天，这本身就很说明问题。","Mahalledeki insanlar gelmek ve oturup sohbet etmek istiyorsa bu bile çok şey anlatır."),
("我们不想把事情说得太漂亮，真实一点反而更有说服力。","Konuyu olduğundan güzel göstermeye çalışmıyoruz; gerçekçi olmak daha ikna edici."),
("这次采访让我发现，很多日常小事其实很值得记录。","Bu röportaj bana günlük hayattaki pek çok küçük şeyin kayda değer olduğunu gösterdi."),
("你刚才提到的这个细节很好，我想再追问一句。","Az önce söylediğiniz ayrıntı çok iyi; bununla ilgili bir soru daha sormak istiyorum."),
("对读者来说，最重要的是知道这里的人为什么在乎这件事。","Okur için en önemlisi buradaki insanların bu konuyu neden önemsediğini anlamak."),
("如果以后再回头看，这段经历应该会很有意思。","İleride geriye dönüp bakınca bu deneyim muhtemelen çok anlamlı olacak."),
("好，最后请每个人用一句话说说自己最想留下的感受。","Tamam, son olarak herkes en çok hatırlamak istediği duyguyu bir cümleyle söylesin.")
]

CTX["relationship"] = [
("先说你们自己的感受吧，别急着考虑别人会怎么评价。","Önce kendi duygularınızı söyleyin; başkalarının ne düşüneceğini hemen düşünmeyin."),
("这对你们来说是好消息，我们当然先替你们高兴。","Bu sizin için güzel bir haber; elbette önce sizin adınıza seviniyoruz."),
("高兴归高兴，接下来要面对的现实问题也可以慢慢谈。","Sevinmek ayrı; bundan sonra karşılaşacağınız gerçek konuları da zamanla konuşabiliriz."),
("两个人做决定，最重要的是先把彼此真正想要的生活说清楚。","İki kişi karar verirken en önemlisi birbirlerinin nasıl bir yaşam istediğini açıkça konuşmasıdır."),
("家人的意见可以听，但最后的生活还是你们两个人来过。","Ailenin görüşü dinlenebilir ama sonuçta o hayatı yaşayacak olan siz ikinizsiniz."),
("如果有担心，就直接说担心什么，不要用一句‘不合适’带过去。","Bir kaygı varsa neyin kaygı verdiğini açıkça söyleyelim; yalnızca ‘uygun değil’ deyip geçmeyelim."),
("我想知道的不是你们什么时候决定，而是为什么会做这个决定。","Ben ne zaman karar verdiğinizden çok neden bu kararı verdiğinizi merak ediyorum."),
("关系走到新的阶段以后，有些习惯确实要重新商量。","İlişki yeni bir aşamaya geçince bazı alışkanlıkları yeniden konuşmak gerekir."),
("只要你们愿意把话说开，很多分歧其实都能找到办法。","Açıkça konuşmaya istekli olduğunuz sürece birçok fikir ayrılığı için çözüm bulunabilir."),
("别为了让所有人满意，把自己的真实想法藏起来。","Herkesi memnun etmek uğruna kendi gerçek düşüncelerinizi saklamayın."),
("我们可以给建议，但不会替你们做决定。","Tavsiye verebiliriz ama sizin yerinize karar vermeyiz."),
("真正的祝福不是只说好听的话，也包括认真听你们的打算。","Gerçek kutlama yalnızca güzel söz söylemek değil, planlarınızı gerçekten dinlemeyi de içerir."),
("有些问题今天不一定要回答，想清楚以后再谈也可以。","Bazı sorulara bugün cevap vermek zorunda değilsiniz; düşündükten sonra konuşabilirsiniz."),
("我更希望你们以后遇到难题时，也能像今天这样坐下来谈。","İleride zor bir durum olduğunda da bugün olduğu gibi oturup konuşabilmenizi daha çok isterim."),
("大家的反应不完全一样很正常，这不等于不支持你们。","Herkesin tepkisinin aynı olmaması normal; bu sizi desteklemedikleri anlamına gelmez."),
("今天先把高兴的事好好庆祝，其他安排我们慢慢来。","Bugün önce güzel haberi kutlayalım; diğer planları yavaş yavaş konuşuruz.")
]

CTX["retirement"] = [
("退休这件事不能只看日期，还得看以后想怎么生活。","Emeklilik yalnızca tarihe bakılarak düşünülmez; sonrasında nasıl yaşamak istediğimizi de düşünmek gerekir."),
("先把每个月真正需要的钱算清楚，心里会踏实很多。","Aylık gerçekten gereken parayı net hesaplamak insanı çok rahatlatır."),
("如果身体和家庭情况变了，原来的计划也要留一点调整空间。","Sağlık veya aile durumu değişirse eski planda da biraz esneklik bırakmak gerekir."),
("我不想退休以后什么都不做，只是希望生活慢一点。","Emekli olduktan sonra hiçbir şey yapmamak istemiyorum; yalnızca hayatın biraz yavaşlamasını istiyorum."),
("钱当然重要，但每天怎么过也一样重要。","Para elbette önemli ama günlerin nasıl geçeceği de aynı derecede önemli."),
("先把最保守的情况算一遍，再看有没有余地。","Önce en temkinli senaryoyu hesaplayalım, sonra ne kadar pay kaldığına bakalım."),
("如果还想继续做一点事，也不用把退休理解成完全停下来。","Biraz çalışmaya devam etmek isteniyorsa emekliliği tamamen durmak gibi düşünmek gerekmez."),
("我更关心的是，退休以后我们还能不能保持现在的生活质量。","Ben daha çok emeklilikten sonra mevcut yaşam kalitemizi koruyup koruyamayacağımızı düşünüyorum."),
("孩子们已经慢慢独立了，我们也可以开始想自己的下一阶段。","Çocuklar yavaş yavaş bağımsızlaşıyor; biz de kendi sonraki dönemimizi düşünmeye başlayabiliriz."),
("别为了一个理想数字把自己逼得太紧，计划要能长期坚持。","İdeal bir rakam uğruna kendimizi fazla sıkmayalım; plan uzun süre sürdürülebilir olmalı."),
("如果几年以后想法变了，再重新算一次也来得及。","Birkaç yıl sonra düşünceler değişirse yeniden hesaplamak için geç olmaz."),
("把住房、医疗和日常开销分开看，会更清楚。","Konut, sağlık ve günlük giderleri ayrı ayrı değerlendirmek daha net olur."),
("我觉得现在先定一个方向，不用今天就把每个细节决定完。","Bence bugün her ayrıntıyı bitirmek yerine şimdilik bir yön belirlemek yeterli."),
("真正让我期待的，是以后能有更多时间陪家人，也做自己喜欢的事。","Beni asıl heyecanlandıran, ileride aileme ve sevdiğim şeylere daha fazla zaman ayırabilmek."),
("只要准备得够稳，退休不一定让人不安，也可以是新的开始。","Yeterince sağlam hazırlanılırsa emeklilik kaygı verici olmak zorunda değil; yeni bir başlangıç da olabilir."),
("今天先把数字记下来，过一段时间我们再重新看看。","Bugün rakamları not edelim; bir süre sonra yeniden gözden geçiririz.")
]

def category_v8(title, active, mini, speakers=None):
    speakers = speakers or []
    text = title + " " + " ".join(active) + " " + mini
    if any(k in text for k in ["采访","新闻","记者","媒体"]) or "记者" in speakers:
        return "media"
    if any(k in text for k in ["订婚","结婚","婚礼","恋爱","伴侣","婚讯"]):
        return "relationship"
    if any(k in text for k in ["退休","退休账","退休日期"]):
        return "retirement"
    if any(k in text for k in ["健康","医生","医院","护士","体检","血压","运动","照护","休息","疲劳","生活方式","住院","过敏"]):
        return "health"
    if any(k in text for k in ["学校","高中","大学","学习","考试","挂科","老师","同学","毕业","作业","摄影比赛","录取","教育","实习"]):
        return "education"
    if any(k in text for k in ["工作","项目","客户","同事","经理","面试","职业","领导","责任","上班","工作邀请"]):
        return "work"
    if any(k in text for k in ["家人","家庭","大家庭","多代同堂","爷爷","奶奶","孩子","全家福","离家","搬家","父母","孙辈"]):
        return "family"
    if any(k in text for k in ["咖啡馆","顾客","订单","价格","成本","营业","商户","菜单","食材","店","生意","厨房"]):
        return "business"
    if any(k in text for k in ["社区","公益","志愿","募捐","居民","洪水","救助","规划","道路","菜园"]):
        return "community"
    if any(k in text for k in ["火车","车站","站台","旅行","酒店","导游","出租车","公交","路线"]):
        return "travel"
    if any(k in text for k in ["回忆","过去","往事","周年","照片","老顾客","人生回顾"]):
        return "memory"
    return category(title, active, mini)

def wrapped_context_line_v10(z, t, seed):
    # Cross-scene surface variety without forcing unrelated active nouns into a sentence.
    mode = seed % 9
    prefixes = [
        ("",""),
        ("另外，","Ayrıca, "),
        ("还有一点，","Bir nokta daha: "),
        ("换个角度看，","Başka bir açıdan bakarsak, "),
        ("从实际情况看，","Gerçek duruma bakarsak, "),
        ("说到这里，","Buraya gelmişken, "),
        ("不过，","Ancak, "),
        ("其实，","Aslında, "),
        ("我觉得，","Bence, "),
    ]
    pre, pretr = prefixes[mode]
    if not pre:
        return z, t
    z2 = pre + z
    t2 = pretr + (t[:1].lower() + t[1:] if t else "")
    return z2, t2



PERSON_TERMS_V9 = {
    "医生","老师","导师","经理","记者","律师","导游","护士","面试官","招聘者",
    "顾客","老顾客","年轻顾客","客户","家人","朋友","同事","爷爷","奶奶",
    "张伟","刘梅","张雨桐","张乐乐","李晨","伴侣","志愿者","工作人员",
    "员工","店员","服务员","司机","居民","学生","同学"
}

ROLE_POOLS = {
"media_reporter":[
("能不能先跟我们说说事情是怎么开始的？","Önce bize bunun nasıl başladığını anlatabilir misiniz?"),
("你刚才提到社区，我想再问一个具体一点的问题。","Az önce topluluktan söz ettiniz; biraz daha somut bir soru sormak istiyorum."),
("平时来的顾客最常跟你们说什么？","Düzenli gelen müşteriler size en çok ne söylüyor?"),
("有没有一件小事最能说明这里为什么受欢迎？","Buranın neden sevildiğini en iyi anlatan küçük bir olay var mı?"),
("如果让你用一句话介绍这家店，你会怎么说？","Bu kafeyi tek cümleyle tanıtsanız ne söylerdiniz?"),
("刚开店的时候，你们想到过今天会这样吗？","Kafeyi ilk açtığınızda bugünkü hale geleceğini düşünmüş müydünüz?"),
("顾客的反馈有没有改变过你们原来的想法？","Müşteri geri bildirimleri ilk düşüncelerinizi hiç değiştirdi mi?"),
("这件事对附近的居民有什么实际影响？","Bunun yakındaki sakinler üzerinde nasıl somut bir etkisi oldu?"),
("你们最希望读者从这篇报道里了解什么？","Okurların bu haberden en çok neyi anlamasını istersiniz?"),
("好，最后我想听听每个人最想补充的一句话。","Tamam, son olarak herkesin eklemek istediği bir cümleyi duymak istiyorum.")
],
"media_owner":[
("一开始我们只想把店经营好，没想到会受到这么多关注。","Başta yalnızca kafeyi iyi işletmek istiyorduk; bu kadar ilgi göreceğini düşünmemiştik."),
("对我们来说，最重要的还是让附近的人愿意进来坐一会儿。","Bizim için en önemlisi yakındaki insanların gelip biraz oturmak istemesi."),
("很多变化其实不是计划出来的，是听了顾客的意见慢慢改的。","Birçok değişiklik aslında önceden planlanmadı; müşteri görüşleriyle yavaş yavaş oluştu."),
("我们不想把自己说得多特别，只是一直在做每天该做的事。","Kendimizi çok özel göstermeye çalışmıyoruz; yalnızca her gün yapılması gereken işi yapıyoruz."),
("店里忙的时候也会出问题，所以我们一直在调整。","Kafe yoğunken sorunlar da oluyor; bu yüzden sürekli ayarlama yapıyoruz."),
("如果大家觉得这里像个可以放心坐下来的地方，我们就很开心。","İnsanlar burayı rahatça oturabilecekleri bir yer gibi görüyorsa bu bizi çok mutlu eder."),
("社区给了我们很多支持，我们也想用自己的方式回馈大家。","Topluluk bize çok destek verdi; biz de kendi yöntemimizle karşılık vermek istiyoruz."),
("新闻当然让我们高兴，不过明天还是要照常开门、照常服务。","Habere çıkmak elbette sevindirici ama yarın yine her zamanki gibi açıp hizmet vereceğiz."),
("真正留下来的不是报道本身，而是跟大家建立的关系。","Kalıcı olan haberin kendisi değil, insanlarla kurduğumuz bağ."),
("我们希望这里一直保持现在这种亲切的感觉。","Buranın bugünkü sıcak ve samimi havasını korumasını istiyoruz.")
],
"media_customer":[
("我常来这里，不只是为了喝咖啡，也因为大家都认识彼此。","Buraya sık geliyorum; yalnızca kahve için değil, insanların birbirini tanıması için de."),
("这里最舒服的地方是没人催你，坐一会儿也很自在。","Buradaki en rahat şey kimsenin sizi acele ettirmemesi; biraz oturmak çok doğal."),
("店里的人会记得老顾客的习惯，这种感觉很难得。","Çalışanların eski müşterilerin alışkanlıklarını hatırlaması çok değerli."),
("有时候邻居就是在这里认识的，后来慢慢成了朋友。","Bazen komşular burada tanışıyor, sonra yavaş yavaş arkadaş oluyor."),
("我觉得报道如果只写咖啡好不好喝，就少了一半。","Bence haber yalnızca kahvenin iyi olup olmadığını yazarsa hikâyenin yarısını kaçırır."),
("对我来说，这里更像社区里一个大家能碰面的地方。","Benim için burası daha çok mahallede insanların karşılaşabildiği bir yer."),
("有活动的时候很热闹，平时安安静静坐着也很好。","Etkinlik zamanında hareketli; normal günlerde sessizce oturmak da güzel."),
("我希望报道以后这里也别变得太商业化。","Umarım haberden sonra burası fazla ticari bir yere dönüşmez."),
("大家喜欢这里，是因为它一直很真实。","İnsanlar burayı seviyor çünkü hep doğal ve samimi kaldı."),
("如果以后还这样，我肯定会继续来。","Böyle devam ederse kesinlikle gelmeye devam ederim.")
],
"health_doctor":[
("先别只看一个数字，我想先了解你最近每天怎么过。","Önce tek bir rakama bakmayalım; son zamanlarda günlük düzeninizin nasıl olduğunu anlamak istiyorum."),
("检查结果提醒我们需要调整，但不用一下把所有事情都改掉。","Sonuçlar bazı şeyleri değiştirmemiz gerektiğini gösteriyor; her şeyi bir anda değiştirmek gerekmiyor."),
("睡眠、饮食和活动量要放在一起看。","Uyku, beslenme ve hareket miktarını birlikte değerlendirmek gerekir."),
("我建议先从最容易坚持的一项开始。","Önce en kolay sürdürülebilecek değişiklikten başlamanızı öneririm."),
("如果出现新的不舒服，要及时告诉我。","Yeni bir rahatsızlık olursa bana zamanında söyleyin."),
("这次不是吓你，是希望你早点把风险降下来。","Amacım sizi korkutmak değil; riski erken azaltmanızı istiyorum."),
("只要能坚持，小的改变也比短时间做得很猛更有效。","Sürdürülebilirse küçük değişiklikler bile kısa süreli aşırı çabadan daha etkilidir."),
("我们过一段时间再复查，看身体有没有反应。","Bir süre sonra tekrar kontrol edip vücudun nasıl yanıt verdiğine bakalım."),
("药物只是其中一部分，生活习惯也很重要。","İlaç işin yalnızca bir parçası; yaşam alışkanlıkları da önemli."),
("今天先把最需要注意的两三件事定下来。","Bugün önce en çok dikkat edilmesi gereken iki üç noktayı belirleyelim.")
],
"health_nurse":[
("我把医生刚才说的重点给你记下来。","Doktorun az önce söylediği ana noktaları sizin için not edeyim."),
("回去以后如果不清楚，可以按这个记录每天的情况。","Eve döndükten sonra emin olmadığınızda günlük durumunuzu bu şekilde kaydedebilirsiniz."),
("不用紧张，按计划一点一点来就好。","Gerilmeyin; plana göre adım adım ilerlemek yeterli."),
("复查的时间我也写在这里了。","Kontrol tarihini de buraya yazdım."),
("如果症状突然加重，就不要等到下次复查。","Belirtiler aniden ağırlaşırsa sonraki kontrolü beklemeyin."),
("家里人可以提醒，但也别给自己太大压力。","Aileniz hatırlatabilir ama kendinize fazla baskı yapmayın."),
("每天的睡眠和运动情况简单记一下就够了。","Her gün uyku ve hareket durumunu kısaca not etmeniz yeterli."),
("有变化就记下来，复查的时候医生会更容易判断。","Bir değişiklik olursa not edin; kontrolde doktorun değerlendirmesi kolaylaşır.")
],
"health_patient":[
("听你这么说，我确实得认真改一改了。","Böyle söyleyince gerçekten bazı şeyleri ciddi biçimde değiştirmem gerektiğini görüyorum."),
("我最担心的是开始几天能做到，后来又坚持不下去。","En çok, ilk birkaç gün yapıp sonra sürdürememekten endişeliyim."),
("如果先改一两项，我觉得我更有把握。","Önce bir iki şeyi değiştirirsem bunu sürdürme konusunda daha emin olurum."),
("最近确实睡得少，运动也不够。","Son zamanlarda gerçekten az uyuyorum ve yeterince hareket etmiyorum."),
("我会先把每天的时间重新安排一下。","Önce günlük programımı yeniden düzenleyeceğim."),
("家里人一直提醒我，是我自己没太当回事。","Ailem sürekli hatırlatıyordu; ben pek ciddiye almıyordum."),
("那我先按这个办法试一段时间。","O zaman önce bu yöntemi bir süre deneyeyim."),
("复查以前我会把每天的情况记下来。","Kontrole kadar günlük durumumu not edeceğim."),
("这样说我就没那么紧张了。","Böyle anlatınca artık o kadar gergin hissetmiyorum."),
("好，我知道接下来该怎么做了。","Tamam, bundan sonra ne yapmam gerektiğini biliyorum.")
],
"education_teacher":[
("一次结果说明不了全部，我们先看具体哪里出了问题。","Tek bir sonuç her şeyi göstermez; önce sorunun nerede olduğunu inceleyelim."),
("我更想知道你做题的时候卡在哪一步。","Ben daha çok soruları çözerken hangi adımda zorlandığını bilmek istiyorum."),
("先把最薄弱的部分找出来，再决定怎么补。","Önce en zayıf kısmı bulalım, sonra nasıl tamamlayacağımıza karar veririz."),
("别只盯着分数，学习方法也要一起看。","Yalnızca puana odaklanma; çalışma yöntemine de bakalım."),
("如果这套方法不适合你，换一种完全没问题。","Bu yöntem sana uygun değilse değiştirmekte hiçbir sorun yok."),
("下周先做一个小目标，我们再看效果。","Gelecek hafta için küçük bir hedef belirleyelim, sonra sonucu değerlendiririz."),
("有不懂的地方早点问，不要一直拖到考试前。","Anlamadığın yerleri erken sor; sınava kadar erteleme."),
("这次的错误很有价值，因为它告诉你下一步该练什么。","Bu hata değerli çünkü bir sonraki adımda ne çalışman gerektiğini gösteriyor."),
("你现在需要的是稳定节奏，不是一下把自己逼得很紧。","Şu anda ihtiyacın olan şey istikrarlı bir ritim; kendini bir anda fazla zorlamak değil."),
("等你把这几部分补起来，信心自然会回来。","Bu bölümleri tamamlayınca güvenin doğal olarak geri gelecek.")
],
"education_student":[
("这次结果出来以后，我确实有点怀疑自己。","Bu sonuçtan sonra gerçekten kendimden biraz şüphe ettim."),
("我觉得问题不只是知识点，还有时间安排。","Bence sorun yalnızca konu bilgisi değil, zaman planlaması da."),
("有几道题我其实会，但是考试时太着急了。","Aslında bazı soruları biliyordum ama sınavda çok acele ettim."),
("我想先把错题重新做一遍。","Önce yanlış yaptığım soruları yeniden çözmek istiyorum."),
("如果每天只改一点，我应该更容易坚持。","Her gün yalnızca küçük bir şey değiştirirsem sürdürmem daha kolay olur."),
("同学的方法对我有帮助，但我不能完全照搬。","Arkadaşımın yöntemi bana yardımcı oluyor ama aynısını tamamen kopyalayamam."),
("我现在更想知道下一步具体做什么。","Şu anda bir sonraki adımda tam olarak ne yapacağımı bilmek istiyorum."),
("这次虽然不好受，但至少让我看清了问题。","Bu kez zor geldi ama en azından sorunu görmemi sağladı."),
("我会先试一周，再看看有没有变化。","Önce bir hafta deneyeceğim, sonra değişiklik var mı bakacağım."),
("好，我不想一直纠结这一次的结果了。","Tamam, bu tek sonuca sürekli takılı kalmak istemiyorum.")
],
"relationship_couple":[
("我有点紧张，不过更多的是高兴。","Biraz heyecanlıyım ama daha çok mutluyum."),
("我们不是突然决定的，其实已经认真谈过很久了。","Bu kararı bir anda vermedik; aslında uzun süredir ciddi biçimde konuşuyoruz."),
("我最希望家里先听听我们的想法，再慢慢问问题。","En çok ailemin önce düşüncelerimizi dinlemesini, soruları sonra yavaşça sormasını istiyorum."),
("以后怎么生活，我们还有很多细节要一起商量。","Gelecekte nasıl yaşayacağımızla ilgili hâlâ birlikte konuşmamız gereken pek çok ayrıntı var."),
("听到你们祝福，我心里踏实多了。","Sizin kutlamanızı duyunca içim çok rahatladı."),
("有些事情我们还没决定，所以今天也不想勉强给答案。","Bazı şeylere henüz karar vermedik; bugün zorla cevap vermek istemiyoruz."),
("如果以后意见不一样，我们也会先把话说开。","İleride fikirlerimiz farklı olursa önce açıkça konuşacağız."),
("我们知道结婚不是只有浪漫，也有很多现实责任。","Evliliğin yalnızca romantizm olmadığını, birçok gerçek sorumluluk taşıdığını biliyoruz."),
("我们想一步一步来，不想为了赶进度把自己弄得太累。","Adım adım ilerlemek istiyoruz; yetişmeye çalışırken kendimizi yormak istemiyoruz."),
("今天能跟家里说出来，对我们很重要。","Bugün bunu aileyle paylaşabilmek bizim için çok önemli.")
],
"relationship_family":[
("听到这个消息，我们第一反应当然是高兴。","Bu haberi duyunca ilk tepkimiz elbette sevinmek oldu."),
("你们认真想过就好，我们不会替你们做决定。","Üzerinde ciddi düşündüyseniz yeter; sizin yerinize karar vermeyeceğiz."),
("我们想问问题，是因为关心，不是想控制你们。","Soru sormamızın nedeni ilgilenmemiz; sizi kontrol etmek istemiyoruz."),
("以后遇到现实问题，记得别一个人扛着。","İleride gerçek sorunlarla karşılaşırsanız her şeyi tek başınıza taşımayın."),
("两个人愿意好好沟通，比什么都重要。","İki kişinin iyi iletişim kurmaya istekli olması her şeyden daha önemli."),
("有些安排可以以后再定，今天不用一次说完。","Bazı düzenlemeler daha sonra kararlaştırılabilir; bugün her şeyi bitirmek gerekmiyor."),
("我们会尊重你们自己的节奏。","Kendi temponuza saygı duyacağız."),
("只要你们过得踏实，我们就放心。","Siz huzurlu yaşadığınız sürece bizim içimiz rahat olur."),
("家里人的看法可以不一样，但支持你们这件事不会变。","Ailedekilerin fikirleri farklı olabilir ama sizi desteklememiz değişmez."),
("今天先好好庆祝，其他问题以后慢慢谈。","Bugün önce güzelce kutlayalım; diğer konuları sonra yavaşça konuşuruz.")
]
}

def role_pool_v10(cat, speaker):
    # Large mixed pools prevent a speaker from cycling through the same 8–10
    # ideas in a 100-turn scene. Role-specific lines come first; category and
    # general lines provide natural semantic variety.
    base = CTX.get(cat, CTX["general"])
    general = CTX["general"]
    if cat == "media":
        if speaker == "记者":
            role = ROLE_POOLS["media_reporter"]
        elif speaker in {"顾客","老顾客","年轻顾客"}:
            role = ROLE_POOLS["media_customer"]
        else:
            role = ROLE_POOLS["media_owner"]
        return role + base + general
    if cat == "health":
        if speaker == "医生":
            role = ROLE_POOLS["health_doctor"]
        elif speaker == "护士":
            role = ROLE_POOLS["health_nurse"]
        elif speaker in {"张伟","刘梅","张雨桐","张乐乐","爷爷","奶奶","顾客","患者"}:
            role = ROLE_POOLS["health_patient"]
        else:
            role = []
        return role + base + general
    if cat == "education":
        if speaker in {"老师","导师"}:
            role = ROLE_POOLS["education_teacher"]
        elif speaker in {"张雨桐","张乐乐","同学","新同学","学生"}:
            role = ROLE_POOLS["education_student"]
        else:
            # Parents/family should support rather than speaking as the student.
            role = CTX["family"]
        return role + base + general
    if cat == "relationship":
        if speaker in {"张雨桐","伴侣","张雨桐伴侣"}:
            role = ROLE_POOLS["relationship_couple"]
        else:
            role = ROLE_POOLS["relationship_family"]
        return role + CTX["family"] + general
    if cat == "retirement":
        return CTX["retirement"] + CTX["family"] + general
    return base + general

DISCOURSE_STARTS = (
    "另外，","还有一点，","换个角度看，","从实际情况看，","说到这里，",
    "不过，","其实，","我觉得，","对，","嗯，","好，","那","先","如果","只要","虽然","尽管"
)

def wrapped_context_line_v10(z, t, seed):
    prefixes = [
        ("",""),
        ("另外，","Ayrıca, "),
        ("还有一点，","Bir nokta daha: "),
        ("换个角度看，","Başka bir açıdan bakarsak, "),
        ("从实际情况看，","Gerçek duruma bakarsak, "),
        ("说到这里，","Buraya gelmişken, "),
        ("不过，","Ancak, "),
        ("其实，","Aslında, "),
        ("我觉得，","Bence, "),
    ]
    # Avoid "我觉得，我觉得..." / "不过，不过..." / discourse-marker stacking.
    for offset in range(len(prefixes)):
        pre, pretr = prefixes[(seed + offset) % len(prefixes)]
        if not pre:
            return z, t
        if not z.startswith(DISCOURSE_STARTS):
            return pre + z, pretr + (t[:1].lower() + t[1:] if t else "")
    return z, t

ANCHOR_STOP = {
    "需要","小","大","好","快","慢","可以","重要","方便","清楚","实际","一点",
    "事情","情况","问题","办法","今天","以后","现在","一起","继续","选择方案"
}

def natural_anchor_line_v10(term, term_tr, cat, speaker, key):
    # Ensure every active HSK target survives without using noun-slot templates
    # that sound unnatural for verbs/adjectives.
    if term in ANCHOR_STOP:
        maps = {
            "需要": [("我们先说清楚到底需要什么。","Önce tam olarak neye ihtiyaç olduğunu netleştirelim."),
                     ("真正需要解决的部分其实很具体。","Aslında çözülmesi gereken kısım oldukça somut.")],
            "小": [("地方小一点没关系，关键是够不够用。","Yer biraz küçük olabilir; asıl mesele yeterli olup olmaması."),
                  ("虽然小，但用起来方便也可以。","Küçük olsa da kullanışlıysa olabilir.")],
            "大": [("大不一定更好，还得看实际需要。","Büyük olması mutlaka daha iyi demek değil; gerçek ihtiyaca bakmak gerekir.")],
            "方便": [("对大家来说方便不方便，是很实际的问题。","Herkes için kullanışlı olup olmaması çok somut bir konu.")],
            "重要": [("最重要的是先把眼前的问题处理好。","En önemlisi önce mevcut sorunu çözmek.")],
        }
        opts = maps.get(term, [("这个细节也值得再确认一下。","Bu ayrıntıyı da yeniden doğrulamakta yarar var.")])
        return pick(opts, key)
    if term in PERSON_TERMS_V9:
        return (f"也得听听{term}自己的想法。", f"{term_tr} tarafının kendi düşüncesini de dinlemek gerekir.")
    if cat == "media":
        return pick([
            (f"采访里提到{term}时，最好配一个具体例子。",f"Röportajda {term_tr} konusu geçerken somut bir örnek vermek iyi olur."),
            (f"说到{term}，我更想听真实经历。",f"{term_tr} söz konusu olduğunda gerçek deneyimi duymayı tercih ederim."),
            (f"{term}这部分可以说得更具体一点。",f"{term_tr} kısmı biraz daha somut anlatılabilir.")
        ], key)
    if cat == "health":
        return pick([
            (f"{term}这方面先按医生的建议来。",f"{term_tr} konusunda önce doktorun önerisine uyalım."),
            (f"关于{term}，我们先观察一段时间。",f"{term_tr} konusunda önce bir süre gözlem yapalım."),
            (f"{term}有变化的话，复查时要告诉医生。",f"{term_tr} konusunda değişiklik olursa kontrolde doktora söylemek gerekir.")
        ], key)
    if cat == "education":
        return pick([
            (f"{term}这部分我想再练一遍。",f"{term_tr} kısmını bir kez daha çalışmak istiyorum."),
            (f"关于{term}，我还需要老师再解释一下。",f"{term_tr} konusunda öğretmenin bir kez daha açıklamasına ihtiyacım var."),
            (f"{term}这一步弄清楚以后，后面就容易多了。",f"{term_tr} kısmı netleşince sonrası çok daha kolay olur.")
        ], key)
    if cat == "relationship":
        return pick([
            (f"说到{term}，我们想先听听彼此真实的想法。",f"{term_tr} konusunda önce birbirimizin gerçek düşüncelerini dinlemek istiyoruz."),
            (f"{term}对我们来说很重要，但不用今天把所有细节都决定完。",f"{term_tr} bizim için önemli ama bütün ayrıntıları bugün kararlaştırmak gerekmiyor."),
            (f"关于{term}，家里的意见可以参考，最后还是要尊重当事人的选择。",f"{term_tr} konusunda ailenin görüşü dinlenebilir ama sonuçta ilgili kişilerin seçimine saygı duymak gerekir.")
        ], key)
    if cat == "retirement":
        return pick([
            (f"{term}这部分我们最好单独算清楚。",f"{term_tr} kısmını ayrı ayrı net hesaplamak iyi olur."),
            (f"说到{term}，我更关心以后能不能长期维持。",f"{term_tr} konusunda bunun uzun vadede sürdürülebilir olup olmadığını daha çok önemsiyorum."),
            (f"{term}要留一点余地，几年以后还可以再调整。",f"{term_tr} konusunda biraz esneklik bırakmak gerekir; birkaç yıl sonra yeniden ayarlanabilir.")
        ], key)
    return pick([
        (f"关于{term}，我们还是结合实际情况来看。",f"{term_tr} konusunda yine gerçek duruma bakmak gerekir."),
        (f"{term}这一点也值得认真考虑。",f"{term_tr} noktası da ciddi biçimde değerlendirmeye değer."),
        (f"说到{term}，先把具体情况弄清楚会更好。",f"{term_tr} konusunda önce somut durumu netleştirmek daha iyi olur.")
    ], key)

def repair_hsk3_slot_v10(zh, tr):
    # Seven HSK3 polish scenes contained grammar-correct but non-native slot
    # combinations such as "关于需要..." or "小这一点...".
    m = re.fullmatch(r"关于(需要|小|大|方便|重要)，还有几个地方要说清楚。", zh)
    if m:
        term=m.group(1)
        return natural_anchor_line_v10(term, tr, "general", "", "hsk3-a")
    m = re.fullmatch(r"(需要|小|大|方便|重要)这一点也得认真考虑。", zh)
    if m:
        term=m.group(1)
        return natural_anchor_line_v10(term, tr, "general", "", "hsk3-b")
    m = re.fullmatch(r"我们最好再确认一下(需要|小|大|方便|重要)。", zh)
    if m:
        term=m.group(1)
        if term=="需要":
            return "我们最好再确认一下到底需要什么。", "Tam olarak neye ihtiyaç olduğunu bir kez daha doğrulasak iyi olur."
        return "我们最好再确认一下具体情况。", "Somut durumu bir kez daha doğrulasak iyi olur."
    return zh, tr


def repair_person_slot_v9(zh, tr, trmap):
    professional = {"医生","老师","导师","经理","记者","律师","导游","护士","面试官","招聘者"}
    customerish = {"顾客","老顾客","年轻顾客","客户"}
    patterns = [
        r"^如果(.+)方面出现新情况，我们原来的安排也要重新评估。$",
        r"^如果(.+)的情况变了，后面的计划也得重新评估。$",
        r"^(.+)要是出现新变化，我们就得及时调整计划。$",
        r"^如果(.+)的情况变了，我们的安排也要跟着调整。$",
    ]
    x = None
    for pat in patterns:
        m = re.fullmatch(pat, zh)
        if m:
            x = m.group(1)
            break
    if not x:
        return zh, tr
    if x in professional:
        if x == "医生":
            return "如果医生有新的建议，我们就按新的情况调整。", "Doktorun yeni bir önerisi olursa yeni duruma göre ayarlarız."
        if x in {"老师","导师"}:
            return "如果老师有新的反馈，我们就再调整学习安排。", "Öğretmenin yeni bir geri bildirimi olursa çalışma planını yeniden ayarlarız."
        return f"如果{x}有新的意见，我们再根据情况调整。", "Uzmanın yeni bir görüşü olursa duruma göre yeniden ayarlarız."
    if x in customerish:
        return f"如果{x}的需求变了，我们也要跟着调整。", "Müşterinin ihtiyacı değişirse bizim de buna göre uyum sağlamamız gerekir."
    if x in PERSON_TERMS_V9:
        return f"如果{x}的想法变了，我们再一起商量。", "Karşı tarafın düşüncesi değişirse yeniden birlikte konuşuruz."
    return zh, tr


HSK2_GLOBAL = {
"先别着急，我们想个办法。":[
("先别急，我们一起想办法。","Önce telaşlanmayalım, birlikte bir çözüm düşünelim."),
("别着急，总会有办法的。","Telaşlanma, mutlaka bir çözüm buluruz."),
("先冷静一下，我们再想想怎么办。","Önce sakinleşelim, sonra ne yapacağımızı düşünelim."),
("没关系，我们先想个办法。","Sorun değil, önce bir çözüm düşünelim."),
("先别慌，看看还有什么办法。","Panik yapmayalım, başka ne yapabiliriz bakalım."),
("我们慢慢想，一定有办法。","Sakin sakin düşünelim, mutlaka bir yol buluruz.")
],
"我觉得可以先做最简单的。":[
("我觉得先做最简单的比较好。","Bence önce en kolay olanı yapmak daha iyi."),
("我们可以先从简单的开始。","Önce kolay olandan başlayabiliriz."),
("先做容易的吧。","Önce kolay olanı yapalım."),
("我想先把最简单的做完。","Bence önce en kolay kısmı bitirelim."),
("要不先做最简单的？","Önce en kolay olanı yapsak?"),
("从简单的开始会快一点。","Kolay olandan başlamak biraz daha hızlı olur.")
],
"那我们把它记下来。":[
("那我们先记下来。","O zaman önce not edelim."),
("好，把这个记下来吧。","Tamam, bunu not edelim."),
("那我先把它写下来。","O zaman bunu önce yazayım."),
("别忘了，把这个记一下。","Unutmayalım, bunu not edelim."),
("好，这一点先记着。","Tamam, bu noktayı aklımızda tutalım."),
("那就先写下来。","O zaman önce yazalım.")
],
"因为时间不多，所以我们快一点。":[
("时间不多了，我们快一点吧。","Fazla zaman kalmadı, biraz hızlanalım."),
("因为时间不多，我们得快一点。","Zaman az olduğu için biraz hızlı olmalıyız."),
("快一点吧，不然时间不够。","Biraz hızlanalım, yoksa zaman yetmeyecek."),
("时间有点紧，我们动作快一点。","Zaman biraz sıkışık, biraz hızlı hareket edelim."),
("我们抓紧一点，时间不多了。","Biraz hızlanalım, fazla zaman kalmadı."),
("先快一点做，等会儿再检查。","Önce biraz hızlı yapalım, sonra yeniden kontrol ederiz.")
],
"先做这个，再做下一个。":[
("先做这个，然后再做下一个。","Önce bunu yapalım, sonra diğerine geçeriz."),
("这个做完以后再做下一个。","Bunu bitirdikten sonra diğerini yapalım."),
("我们一个一个来，先做这个。","Tek tek ilerleyelim, önce bunu yapalım."),
("先把这个完成，再看下一个。","Önce bunu tamamlayalım, sonra diğerine bakalım."),
("别一起做，先做这个。","Hepsini birden yapmayalım, önce bunu yapalım."),
("好，先这个，后面再做下一个。","Tamam, önce bu; sonra diğerini yaparız.")
],
"这个办法比刚才的好。":[
("这个办法比刚才好一点。","Bu yöntem az öncekinden biraz daha iyi."),
("我觉得这个办法更好。","Bence bu yöntem daha iyi."),
("这样比刚才方便。","Böyle yapmak az öncekinden daha kullanışlı."),
("这个办法看起来更合适。","Bu yöntem daha uygun görünüyor."),
("还是这个办法好一些。","Bu yöntem biraz daha iyi."),
("换成这个办法会更容易。","Bu yönteme geçmek daha kolay olur.")
],
"我已经试过一次了。":[
("我刚才已经试过了。","Az önce zaten denedim."),
("这个我试过一次。","Bunu bir kez denedim."),
("我已经试了一次。","Bir kez denedim."),
("刚才我试过这个办法。","Az önce bu yöntemi denedim."),
("这个办法我刚刚试过。","Bu yöntemi az önce denedim."),
("我试过了，知道是什么情况。","Denedim, durumun ne olduğunu biliyorum.")
],
"那我们换一个办法。":[
("那我们换个办法吧。","O zaman başka bir yöntem deneyelim."),
("不行的话就换一个办法。","Olmazsa başka bir yöntem deneyelim."),
("那试试别的办法。","O zaman başka bir yol deneyelim."),
("好，我们换一种做法。","Tamam, başka bir yöntem kullanalım."),
("这个不行，就换一个。","Bu olmazsa başka birini deneyelim."),
("那我们换个方法看看。","O zaman başka bir yöntem deneyelim.")
],
"太好了，终于解决了。":[
("太好了，终于解决了。","Harika, sonunda çözüldü."),
("好了，问题终于解决了。","Tamam, sorun sonunda çözüldü."),
("太好了，这下没问题了。","Harika, artık sorun yok."),
("终于好了，我放心了。","Sonunda düzeldi, içim rahatladı."),
("好，总算解决了。","Tamam, sonunda çözdük."),
("太好了，这件事解决了。","Harika, bu işi çözdük.")
],
"今天又学到一件事。":[
("今天又学到了一点。","Bugün yine bir şey öğrendik."),
("今天又知道了一个新办法。","Bugün yeni bir yöntem daha öğrendik."),
("这次我们也学到东西了。","Bu sefer de bir şey öğrendik."),
("今天这个经验很有用。","Bugünkü deneyim çok faydalı."),
("这件事让我学到了不少。","Bu olay bana epey şey öğretti."),
("以后遇到这种情况就知道怎么办了。","Bundan sonra böyle bir durumda ne yapacağımızı biliriz.")
],
"下次我们会更有经验。":[
("下次我们会更有经验。","Bir dahaki sefere daha tecrübeli oluruz."),
("下次再遇到就容易多了。","Bir daha olursa çok daha kolay olur."),
("有了这次经验，下次就知道怎么办了。","Bu deneyim sayesinde bir dahaki sefere ne yapacağımızı biliriz."),
("下次我们会准备得更好。","Bir dahaki sefere daha iyi hazırlanırız."),
("以后再遇到这种情况就不怕了。","Bundan sonra böyle bir durum olursa korkmayız."),
("这次记住了，下次会更顺利。","Bu kez öğrendik; bir dahaki sefere daha sorunsuz olur.")
],
"我理解你的立场，不过我想从另一个角度补充一点。":[
("我明白你的想法，不过我还有一个想法。","Düşünceni anlıyorum ama benim de başka bir fikrim var."),
("你说得有道理，我还想补充一点。","Söylediğin mantıklı; ben de bir şey eklemek istiyorum."),
("我懂你的意思，不过也可以换个角度想。","Ne demek istediğini anlıyorum ama başka bir açıdan da düşünebiliriz."),
("对，不过我还想到另外一点。","Evet, ama aklıma başka bir nokta daha geldi."),
("我明白，不过还有一个地方要考虑。","Anlıyorum ama düşünmemiz gereken bir nokta daha var."),
("你的想法可以，我再补充一句。","Fikrin olabilir; ben de bir şey ekleyeyim.")
],
"现在大家的立场已经比开始时清楚多了。":[
("现在大家的想法比刚开始清楚多了。","Artık herkesin düşüncesi başlangıca göre çok daha net."),
("聊到这里，大家怎么想已经很清楚了。","Buraya kadar konuşunca herkesin ne düşündüğü oldukça netleşti."),
("现在我们都知道彼此怎么想了。","Artık birbirimizin ne düşündüğünü biliyoruz."),
("大家的意见现在清楚多了。","Herkesin görüşü artık çok daha net."),
("说了这么多，大家的想法已经比较明确了。","Bu kadar konuştuktan sonra herkesin düşüncesi oldukça netleşti."),
("至少现在大家都把想法说清楚了。","En azından artık herkes düşüncesini açıkça söyledi.")
],
}

def hsk2_global_variant(zh,tr,key):
    opts=HSK2_GLOBAL.get(zh)
    return pick(opts,key) if opts else (zh,tr)

def beginner_variant(zh,tr,occ,key):
    maps={
      "好。":[("嗯，好。",tr),("行。",tr),("好的。",tr),("可以。",tr),("好啊。",tr),("那好。",tr),("没问题。",tr),("行啊。",tr),("好吧。",tr),("嗯，可以。",tr),("对，就这样。",tr),("好，就这么办。",tr)],
      "嗯，好。":[("好。",tr),("行。",tr),("好的。",tr),("可以。",tr),("好啊。",tr),("那好。",tr),("没问题。",tr),("行啊。",tr),("好吧。",tr),("嗯，可以。",tr),("对，就这样。",tr),("好，就这么办。",tr)],
      "行。":[("好。",tr),("嗯，好。",tr),("好的。",tr),("可以。",tr),("好啊。",tr),("那好。",tr),("没问题。",tr),("行啊。",tr),("好吧。",tr),("嗯，可以。",tr),("对，就这样。",tr),("好，就这么办。",tr)],
      "好的。":[("好。",tr),("嗯，好。",tr),("行。",tr),("可以。",tr),("好啊。",tr),("那好。",tr),("没问题。",tr),("行啊。",tr),("好吧。",tr),("嗯，可以。",tr),("对，就这样。",tr),("好，就这么办。",tr)],
      "谢谢。":[("谢谢你。",tr),("好，谢谢。",tr),("嗯，谢谢。",tr),("太好了，谢谢。",tr),("谢谢，帮大忙了。",tr),("真的谢谢你。",tr)],
      "好，谢谢。":[("谢谢。",tr),("谢谢你。",tr),("嗯，谢谢。",tr),("太好了，谢谢。",tr),("谢谢，帮大忙了。",tr),("真的谢谢你。",tr)],
      "嗯，谢谢。":[("谢谢。",tr),("谢谢你。",tr),("好，谢谢。",tr),("太好了，谢谢。",tr),("真的谢谢你。",tr)],
      "太好了，谢谢。":[("谢谢。",tr),("谢谢你。",tr),("好，谢谢。",tr),("嗯，谢谢。",tr),("真的谢谢你。",tr)],
      "我明白了。":[("明白了。",tr),("好，我知道了。",tr),("嗯，我懂了。",tr),("知道了。",tr),("好，明白了。",tr),("嗯，知道了。",tr)],
      "明白了。":[("我明白了。",tr),("好，我知道了。",tr),("嗯，我懂了。",tr),("知道了。",tr),("好，明白了。",tr)],
      "我也是。":[("嗯，我也是。",tr),("我也一样。",tr),("我也这么想。",tr),("对，我也是。",tr),("我也是这样。",tr)],
      "没错。":[("对。",tr),("嗯，对。",tr),("是。",tr),("对的。",tr),("嗯，没错。",tr)],
      "对。":[("没错。",tr),("嗯，对。",tr),("是。",tr),("对的。",tr),("嗯，没错。",tr)],
    }
    if zh in maps:
        return maps[zh][(occ-2)%len(maps[zh])]

    m=re.fullmatch(r"你要(.+)吗？",zh)
    if m:
        x=m.group(1)
        opts=[(f"{x}你要吗？",tr),(f"你还要{x}吗？",tr),(f"你想要{x}吗？",tr),(f"要不要{x}？",tr)]
        return opts[(occ-2)%len(opts)]
    m=re.fullmatch(r"我要(.+)，谢谢。",zh)
    if m:
        x=m.group(1)
        opts=[(f"那我要{x}，谢谢。",tr),(f"好，我要{x}。",tr),(f"我要{x}，谢谢你。",tr),(f"嗯，我要{x}。",tr)]
        return opts[(occ-2)%len(opts)]

    core=zh[:-1] if zh.endswith(("。","？","！")) else zh
    punct=zh[-1] if zh.endswith(("。","？","！")) else "。"
    if punct=="。":
        pref=["嗯，","对，","好，","是啊，","那好，","行，","没错，","对了，"][(occ-2)%8]
        if not core.startswith(("嗯，","对，","好，","是啊，","那好，","行，","没错，","对了，")):
            return pref+core+punct,tr
    if punct=="？":
        opts=[f"那{core}？",f"现在{core}？",f"所以{core}？",f"好，那{core}？"]
        return opts[(occ-2)%len(opts)],tr
    return zh,tr

def phase_pool(cat,level,idx):
    pool=CTX.get(cat,CTX["general"])
    shift={4:0,5:3,6:6}.get(level,0)+(idx//20)*3
    return pool[shift%len(pool):]+pool[:shift%len(pool)]

def wrapped_context_line(z,t,cycle):
    if cycle <= 0:
        return z,t
    wrappers=[
        ("另外，","Ayrıca, "),
        ("还有一点，","Bir nokta daha: "),
        ("换个角度看，","Başka bir açıdan bakarsak, "),
        ("从实际情况看，","Gerçek duruma bakarsak, "),
    ]
    pre,pretr=wrappers[(cycle-1)%len(wrappers)]
    return pre+z,pretr+t[:1].lower()+t[1:] if t else pretr.rstrip()

# Load baseline metadata and candidate files.
baseline={}
for lv in range(1,7):
    level=f"HSK{lv}"
    d=BASE/level/"scenes"
    if not d.exists(): d=BASE/level
    for p in d.glob(f"ZH_{level}_SC*.json"):
        x=json.loads(p.read_text(encoding="utf-8")); baseline[x["id"]]=x

cand_files=sorted(CAND.glob("HSK*/ZH_HSK*_SC*.json"))
docs={}
global_freq=Counter()
for p in cand_files:
    d=json.loads(p.read_text(encoding="utf-8"))
    docs[d["sceneId"]]=d
    global_freq.update(str(x.get("zh","")).strip() for x in d.get("dialogues",[]))

report={"scenes":0,"turns":0,"contextRewrites":0,"dedupeRewrites":0,"byLevel":Counter()}

for sid,d in sorted(docs.items()):
    scene=baseline[sid]
    level=d["level"]; ln=int(level[-1])
    active,trmap=active_cards(scene)
    cat=category_v8(scene.get("titleZh",""),active,scene.get("miniAdventureTr",""),scene.get("production",{}).get("characters",[]))
    title=scene.get("titleZh","")
    anchors=[a for a in active if 2 <= len(a) <= 10]
    if not anchors:
        anchors=[title.replace("？","").replace("！","")[:8] or "这件事"]
    turns=[]
    context_seq=0
    context_offset=int(hashlib.sha256(sid.encode("utf-8")).hexdigest()[:6],16)
    for idx,row0 in enumerate(d["dialogues"],1):
        row=dict(row0)
        zh=str(row["zh"]).strip()
        # Replace course-wide long boilerplate in HSK4-HSK6. Keep any line
        # containing active scene vocabulary, because it is already scene-grounded.
        active_hit=[a for a in active if a and a in zh]
        if ln==2 and global_freq[zh]>=20 and han_len(zh)>=7:
            z,t=hsk2_global_variant(zh,row["tr"],f"{sid}:{idx}:{zh}:hsk2global")
            row["zh"]=z;row["tr"]=t;row["pinyin"]=pinyin_text(z)
            report["contextRewrites"]+=1
        elif ln>=4 and global_freq[zh]>=20 and han_len(zh)>=8:
            # v10: all course-wide boilerplate is rewritten according to scene
            # type + speaker role. Active HSK vocabulary is restored naturally
            # after the conversational pass, rather than forcing noun slots.
            pool=role_pool_v10(cat, row.get("speaker",""))
            pos=(context_offset+context_seq)%len(pool)
            z,t=pool[pos]
            z,t=wrapped_context_line_v10(z,t,context_offset+context_seq)
            row["zh"]=z
            row["tr"]=t
            row["pinyin"]=pinyin_text(z)
            context_seq+=1
            report["contextRewrites"]+=1
        if ln >= 4:
            zfix,tfix=repair_person_slot_v9(str(row.get("zh","")).strip(), str(row.get("tr","")).strip(), trmap)
            if zfix != row.get("zh"):
                row["zh"]=zfix
                row["tr"]=tfix
                row["pinyin"]=pinyin_text(zfix)
                report["contextRewrites"]+=1
        if ln == 3:
            zfix,tfix=repair_hsk3_slot_v10(str(row.get("zh","")).strip(), str(row.get("tr","")).strip())
            if zfix != row.get("zh"):
                row["zh"]=zfix
                row["tr"]=tfix
                row["pinyin"]=pinyin_text(zfix)
                report["contextRewrites"]+=1
        turns.append(row)

    # HSK1/2: exact drill repetition is useful, but it should not dominate a
    # 100-turn story. Make repeat occurrences surface-different while retaining
    # the beginner intent and vocabulary.
    if ln<=2:
        seen=Counter()
        used=set()
        newturns=[]
        for idx,row0 in enumerate(turns,1):
            row=dict(row0); z=row["zh"]; seen[z]+=1
            if seen[z]>1:
                nz,ntr=beginner_variant(z,row["tr"],seen[z],f"{sid}:{idx}:{z}")
                # Avoid a variant that already exists in this scene.
                attempt=0
                while nz in used and attempt<10:
                    attempt+=1
                    nz,ntr=beginner_variant(z,row["tr"],seen[z]+attempt,f"{sid}:{idx}:{z}:{attempt}")
                if nz!=z:
                    row["zh"]=nz; row["tr"]=ntr; row["pinyin"]=pinyin_text(nz)
                    report["dedupeRewrites"]+=1
            used.add(row["zh"]); newturns.append(row)
        turns=newturns

    # A final generic de-duplication for long HSK4+ lines if a contextual
    # replacement still happened to collide inside one scene.
    if ln>=4:
        seen=Counter(); used=set(); newturns=[]
        pool=CTX.get(cat,CTX["general"])
        collision_seq=context_seq
        for idx,row0 in enumerate(turns,1):
            row=dict(row0); z=row["zh"]; seen[z]+=1
            if seen[z]>1 and han_len(z)>=7:
                for attempt in range(len(pool)*5):
                    pos=(context_offset+collision_seq+attempt)%len(pool)
                    cycle=(collision_seq+attempt)//len(pool)
                    z2,t2=wrapped_context_line_v10(*pool[pos], context_offset+collision_seq+attempt)
                    if z2 not in used:
                        row["zh"]=z2;row["tr"]=t2;row["pinyin"]=pinyin_text(z2)
                        collision_seq+=attempt+1
                        report["dedupeRewrites"]+=1
                        break
            used.add(row["zh"]);newturns.append(row)
        turns=newturns

    # Restore any active HSK target that disappeared after removing robotic
    # template lines. Only one natural occurrence per missing term is required.
    joined="".join(str(x.get("zh","")) for x in turns)
    missing=[a for a in active if a and a not in joined]
    if missing:
        candidate_indices=[
            i for i in range(8, max(9,len(turns)-10))
            if i < len(turns) and len(str(turns[i].get("zh",""))) >= 4
        ]
        for n,term in enumerate(missing):
            if not candidate_indices:
                break
            pos=candidate_indices[(n*7 + context_offset) % len(candidate_indices)]
            row=turns[pos]
            term_tr=trmap.get(term, "bu konu")
            z,t=natural_anchor_line_v10(term,term_tr,cat,row.get("speaker",""),f"{sid}:{pos}:{term}")
            row["zh"]=z
            row["tr"]=t
            row["pinyin"]=pinyin_text(z)
            report["contextRewrites"]+=1

    out=dict(d)
    out["naturalizationVersion"]=10
    out["status"]="FINAL_NATIVE_EDITORIAL_CANDIDATE"
    out["sceneCategory"]=cat
    out["dialogues"]=turns
    dest=OUT/level/f"{sid}.json";dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report["scenes"]+=1; report["turns"]+=len(turns); report["byLevel"][level]+=1

report["byLevel"]=dict(sorted(report["byLevel"].items()))
(OUT/"polish_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
