#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import re
import sys

try:
    import jieba
    from pypinyin import lazy_pinyin, Style
except Exception as e:
    raise SystemExit("pip install jieba pypinyin") from e

if len(sys.argv) != 3:
    raise SystemExit("usage: polish_dialogue_v13_exact_repeat.py <candidate-root> <out-root>")

CAND = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

TARGET = {
    "ZH_HSK4_SC012","ZH_HSK4_SC030",
    "ZH_HSK5_SC006","ZH_HSK5_SC015",
    "ZH_HSK6_SC004","ZH_HSK6_SC027","ZH_HSK6_SC030","ZH_HSK6_SC034","ZH_HSK6_SC042",
}

VARIANTS = {
"先把真正的问题说清楚，别急着找一个漂亮答案。":[
("先把真正的问题说透，别急着给出一个听起来完美的答案。","Önce asıl sorunu iyice netleştirelim; kulağa kusursuz gelen bir cevap vermek için acele etmeyelim."),
("先弄清楚问题到底是什么，再谈什么答案最合适。","Önce sorunun tam olarak ne olduğunu netleştirelim, sonra hangi cevabın uygun olduğunu konuşalım."),
("别急着下结论，先把真正需要解决的问题找出来。","Hemen sonuca varmayalım; önce gerçekten çözmemiz gereken sorunu bulalım.")
],
"每个人看到的角度不一样，把这些角度放在一起会更完整。":[
("大家看到的侧重点不一样，放在一起看才比较完整。","Herkes farklı bir noktaya odaklanıyor; hepsini birlikte değerlendirince tablo daha tamamlanıyor."),
("每个人关注的地方不同，把这些看法放在一起会更全面。","Herkes farklı bir noktayı önemsiyor; bu görüşleri bir araya getirince değerlendirme daha kapsamlı oluyor."),
("我们站的位置不同，所以把各自看到的都说出来会更完整。","Bulunduğumuz konumlar farklı; bu yüzden herkes gördüğünü anlatırsa tablo daha tamamlanır.")
],
"先确认我们已经知道什么，再说还缺什么信息。":[
("先把已经确定的信息理清楚，再看看还缺什么。","Önce doğrulanmış bilgileri netleştirelim, sonra neyin eksik olduğuna bakalım."),
("我们先分清哪些已经确定，哪些还需要继续确认。","Önce nelerin kesin olduğunu, nelerin hâlâ doğrulanması gerektiğini ayıralım."),
("先盘点一下现有信息，再决定还要补充什么。","Önce elimizdeki bilgileri gözden geçirelim, sonra neyi tamamlamamız gerektiğine karar verelim.")
],
"如果现在还不能确定，就先保留一点调整空间。":[
("现在还拿不准的话，就先给后面的调整留一点余地。","Şu anda emin değilsek sonraki ayarlamalar için biraz esneklik bırakalım."),
("暂时不能确定也没关系，先别把安排定得太死。","Şimdilik kesinleştiremiyorsak sorun değil; düzenlemeyi fazla katılaştırmayalım."),
("如果信息还不够，就先留出以后修改的空间。","Bilgi henüz yeterli değilse ileride değiştirmek için alan bırakalım.")
],
"先别把问题想得太抽象，回到具体情况会更容易判断。":[
("先回到眼前的具体情况，别把问题说得太抽象。","Önce somut mevcut duruma dönelim; konuyu fazla soyutlaştırmayalım."),
("把具体情况摆出来以后，这个问题会更容易判断。","Somut durumu ortaya koyunca bu konuyu değerlendirmek daha kolay olur."),
("我们先看实际发生了什么，再谈更大的判断。","Önce gerçekte ne olduğuna bakalım, daha geniş değerlendirmeyi sonra yapalım.")
],
"这个想法可以继续讨论，不过最好再确认一下实际条件。":[
("这个想法可以保留，但还得再核对一下现实条件。","Bu fikir kalabilir ama gerçek koşulları bir kez daha kontrol etmemiz gerekiyor."),
("方向可以继续谈，不过先看看实际条件能不能支持。","Bu yönü konuşmaya devam edebiliriz ama önce gerçek koşulların bunu destekleyip desteklemediğine bakalım."),
("我不反对这个想法，只是还想再确认几个现实条件。","Bu fikre karşı değilim; yalnızca birkaç gerçek koşulu daha doğrulamak istiyorum.")
],
"今天先把能确定的部分定下来，剩下的以后继续聊。":[
("今天先把已经能决定的事情定下来，其他的以后再谈。","Bugün karar verebildiğimiz konuları netleştirelim; diğerlerini sonra konuşuruz."),
("能确定的今天先定，暂时没有答案的以后再慢慢商量。","Kesinleştirebildiklerimizi bugün kararlaştıralım; henüz cevabı olmayanları sonra konuşuruz."),
("我们先把眼下能决定的部分落实，剩下的留到下一次。","Şu anda kararlaştırabildiklerimizi uygulamaya koyalım; kalanını sonraki görüşmeye bırakalım.")
],
"不用追求一次把所有问题都解决，先把下一步走稳。":[
("没必要一次解决所有问题，先把下一步做好更重要。","Bütün sorunları tek seferde çözmek gerekmiyor; önce sonraki adımı sağlam atmak daha önemli."),
("先把眼前这一小步走稳，不必今天把所有问题都解决。","Önce önümüzdeki küçük adımı sağlam atalım; bugün her şeyi çözmek zorunda değiliz."),
("我们不用一次想完所有事情，先确定接下来怎么做。","Her şeyi tek seferde düşünmek zorunda değiliz; önce bundan sonra ne yapacağımızı belirleyelim.")
],
"我同意方向，不过执行的时候需要留一点余地。":[
("大方向我同意，不过执行时最好保留一些调整空间。","Genel yönü kabul ediyorum ama uygulamada biraz ayarlama payı bırakmak iyi olur."),
("这个方向可以，但真正做的时候别把安排定得太死。","Bu yön uygun ama uygularken planı fazla katılaştırmayalım."),
("思路没问题，只是执行过程中还要允许根据情况调整。","Yaklaşımda sorun yok; yalnızca uygulama sırasında duruma göre ayarlamaya izin vermeliyiz.")
],
"如果出现新情况，我们就根据新的事实调整。":[
("后面如果有新情况，就按新的事实及时调整。","Sonradan yeni bir durum çıkarsa yeni olgulara göre zamanında ayarlarız."),
("情况一旦有变化，我们就根据实际情况重新安排。","Durum değişirse gerçek koşullara göre yeniden düzenleriz."),
("以后有新信息，就用新信息来修正现在的决定。","İleride yeni bilgi çıkarsa bugünkü kararı o bilgiye göre düzeltiriz.")
],
"我们至少已经知道彼此最在意什么了。":[
("至少现在我们已经听清楚彼此最在意的是什么。","En azından artık birbirimizin en çok neyi önemsediğini net biçimde duyduk."),
("现在至少有一点很清楚：大家最在意的地方我们都知道了。","Artık en azından bir şey açık: herkesin en çok neyi önemsediğini biliyoruz."),
("至少彼此真正关心什么，现在已经比刚才清楚多了。","En azından birbirimizin gerçekten neyi önemsediği şimdi az öncekinden çok daha net.")
],
"有不同意见没关系，只要理由说得清楚就能继续谈。":[
("意见不一样没关系，把理由说清楚就还能继续商量。","Görüşlerin farklı olması sorun değil; gerekçeleri açıkça anlatırsak konuşmaya devam edebiliriz."),
("有分歧很正常，关键是大家愿意把原因讲明白。","Görüş ayrılığı normal; önemli olan herkesin nedenini açıkça anlatmaya istekli olması."),
("我们可以不同意，但只要把依据说出来，讨论就能继续。","Aynı fikirde olmayabiliriz; dayanaklarımızı açıkladığımız sürece tartışma devam edebilir.")
],
"把责任和时间说清楚，后面执行会容易很多。":[
("把谁负责、什么时候做说清楚，后面执行会顺很多。","Kimin sorumlu olduğunu ve ne zaman yapılacağını netleştirirsek uygulama çok daha sorunsuz ilerler."),
("责任和时间一旦明确，真正做起来就不会那么乱。","Sorumluluk ve zaman netleşince uygulama sırasında işler o kadar karışmaz."),
("先把分工和时间点定清楚，后面的执行会轻松不少。","Önce görev dağılımını ve zamanı netleştirelim; sonraki uygulama çok daha kolay olur.")
],
"这个决定不是不能改，以后有新情况可以重新评估。":[
("这个决定以后还能调整，有新情况时我们再重新评估。","Bu karar ileride ayarlanabilir; yeni bir durum çıkarsa yeniden değerlendiririz."),
("今天的决定不是一成不变，情况变了就再看一次。","Bugünkü karar değişmez değil; durum değişirse yeniden bakarız."),
("先这样决定并不代表永远不改，以后有新信息可以再评估。","Şimdilik böyle karar vermek sonsuza dek değişmeyeceği anlamına gelmez; yeni bilgi çıkarsa yeniden değerlendirebiliriz.")
],
"我更关心这个选择实际会带来什么变化。":[
("我更想知道这个选择最后会给实际生活带来什么变化。","Ben daha çok bu seçimin gerçek hayatta neyi değiştireceğini bilmek istiyorum."),
("比起听起来好不好，我更在意这个选择实际会改变什么。","Kulağa nasıl geldiğinden çok bu seçimin gerçekte neyi değiştireceğini önemsiyorum."),
("我最关心的还是它真正实施以后会带来什么影响。","Benim asıl önemsediğim, gerçekten uygulandığında ne tür bir etkisi olacağı.")
],
"我们先处理最关键的一点，再看其他细节。":[
("我们先把最关键的问题处理好，再慢慢看其他细节。","Önce en kritik sorunu çözelim, sonra diğer ayrıntılara yavaşça bakarız."),
("先抓住最重要的一点，其他细节可以往后放。","Önce en önemli noktaya odaklanalım; diğer ayrıntıları sonraya bırakabiliriz."),
("最关键的部分先解决，剩下的细节再一个个处理。","Önce en kritik kısmı çözelim; kalan ayrıntıları sonra tek tek ele alırız.")
],
"嗯，这一点我赞成。":[
("对，这一点我也赞成。","Evet, bu noktaya ben de katılıyorum."),
("嗯，这个想法我同意。","Evet, bu fikre katılıyorum."),
("这点我没有意见。","Bu noktaya itirazım yok.")
],
"这样更符合实际。":[
("对，这样更符合实际。","Evet, böyle yapmak gerçek koşullara daha uygun."),
("这么做会更贴近实际情况。","Böyle yapmak gerçek duruma daha yakın olur."),
("我觉得这样更现实一些。","Bence böyle yapmak biraz daha gerçekçi.")
],
}

PREFIXES = [
("另外，","Ayrıca, "),
("还有一点，","Bir nokta daha: "),
("换个角度看，","Başka bir açıdan bakarsak, "),
("从实际情况看，","Gerçek duruma bakarsak, "),
("说到这里，","Buraya gelmişken, "),
("我想补充一句，","Bir şey daha eklemek istiyorum: "),
("再往前想一步，","Bir adım ilerisini düşünürsek, "),
("如果考虑后面的安排，","Sonraki düzenlemeyi düşünürsek, "),
]

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

def diversify(zh: str, tr: str, occurrence: int):
    opts=VARIANTS.get(zh)
    if opts:
        return opts[(occurrence-2) % len(opts)]
    pre,pretr=PREFIXES[(occurrence-2) % len(PREFIXES)]
    if zh.startswith(("嗯，","对，","好，","行，")) and "，" in zh:
        core=zh.split("，",1)[1]
        return pre+core, pretr+(tr[:1].lower()+tr[1:] if tr else "")
    return pre+zh, pretr+(tr[:1].lower()+tr[1:] if tr else "")

report={"version":13,"targetScenes":[],"rewrites":0,"remainingDuplicateLines":{}}

for p in sorted(CAND.glob("HSK*/ZH_HSK*_SC*.json")):
    d=json.loads(p.read_text(encoding="utf-8"))
    sid=d["sceneId"]
    rows=[dict(x) for x in d.get("dialogues",[])]
    if sid in TARGET:
        seen=Counter()
        for row in rows:
            z=str(row.get("zh","")).strip()
            seen[z]+=1
            if seen[z] > 1:
                nz,ntr=diversify(z,str(row.get("tr","")).strip(),seen[z])
                row["zh"]=nz
                row["tr"]=ntr
                row["pinyin"]=pinyin_text(nz)
                report["rewrites"]+=1
        remaining=Counter(str(x.get("zh","")).strip() for x in rows)
        dup=sum(c-1 for c in remaining.values() if c>1)
        report["remainingDuplicateLines"][sid]=dup
        report["targetScenes"].append(sid)
    d["naturalizationVersion"]=13
    d["status"]="FINAL_NATIVE_RELEASE_CANDIDATE_V13"
    d["dialogues"]=rows
    dest=OUT/p.parent.name/p.name
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if set(report["targetScenes"]) != TARGET:
    raise SystemExit(f"Target mismatch: got {sorted(report['targetScenes'])}")
if any(report["remainingDuplicateLines"].values()):
    raise SystemExit(f"v13 still has exact duplicates in targets: {report['remainingDuplicateLines']}")

(OUT/"v13_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
