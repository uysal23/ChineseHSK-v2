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
    "HSK2": [(55, 95)],
    "HSK3": [(1, 18), (76, 94)],
    "HSK4": [(78, 94)],
    "HSK5": [(71, 94)],
    "HSK6": [(1, 100)],
}

BLOCKS = {
    ("HSK2",55,95): [
        ("好，我们把刚才看的再整理一下。","Tamam, az önce baktıklarımızı bir kez daha toparlayalım."),
        ("先从最需要确认的地方开始。","Önce en çok teyit edilmesi gereken yerden başlayalım."),
        "Q",
        ("我觉得先看实际情况比较好。","Bence önce gerçek duruma bakmak daha iyi."),
        ("对，不合适就换一个。","Evet, uygun değilse başka birini deneriz."),
        ("别急，慢慢来。","Acele etmeyelim, yavaş yavaş ilerleyelim."),
        "S",
        ("这样就清楚多了。","Böylece çok daha net oldu."),
        ("那再看下一个。","O zaman sonrakine bakalım."),
        ("好，我记住了。","Tamam, aklımda."),
        "Q",
        ("我先试试看。","Önce bir deneyeyim."),
        ("如果不合适，我就换。","Uygun olmazsa değiştiririm."),
        ("对，这样比较方便。","Evet, böyle daha kullanışlı."),
        "S",
        ("那就先这么做吧。","O zaman şimdilik böyle yapalım."),
        ("做完以后我们再检查。","Bitirdikten sonra bir kez daha kontrol ederiz."),
        ("好，有问题马上说。","Tamam, sorun olursa hemen söyleyelim."),
        "Q",
        ("我觉得这个选择可以。","Bence bu seçenek uygun."),
        ("不过还要再比较一下。","Ama yine de biraz daha karşılaştırmak gerekiyor."),
        ("对，比较一下会更清楚。","Evet, karşılaştırınca daha net olur."),
        "S",
        ("那再试一次。","O zaman bir kez daha deneyelim."),
        ("现在比刚才好多了。","Şimdi az öncekinden çok daha iyi."),
        ("嗯，已经很接近了。","Evet, artık oldukça yaklaştık."),
        "Q",
        ("我觉得这次可以先定下来。","Bence bu kez şimdilik karar verebiliriz."),
        ("好，不过最后再确认一次。","Tamam, ama son kez bir daha teyit edelim."),
        ("对，别漏掉细节。","Evet, ayrıntıları atlamayalım."),
        "S",
        ("这样就不容易弄错了。","Böylece hata yapmak daha zor olur."),
        ("那把剩下的也看完。","O zaman kalanlara da bakalım."),
        ("好，快结束了。","Tamam, neredeyse bitti."),
        "Q",
        ("我觉得主要问题已经解决了。","Bence ana sorun artık çözüldü."),
        ("剩下的按刚才说的做就行。","Kalanını az önce konuştuğumuz gibi yapmamız yeterli."),
        ("最后再检查一次吧。","Son kez bir daha kontrol edelim."),
        "S",
        ("嗯，这次应该没问题了。","Evet, bu kez sorun olmamalı."),
        ("好，那这一部分就完成了。","Tamam, bu kısmı da tamamladık."),
    ],
    ("HSK3",1,18): [
        "TITLE",
        ("好，先听听大家怎么想。","Tamam, önce herkesin ne düşündüğünü dinleyelim."),
        "Q",
        ("我先说吧，我最担心的是实际情况会不会跟我们想的一样。","Önce ben söyleyeyim; en çok gerçek durumun düşündüğümüz gibi olup olmayacağını merak ediyorum."),
        ("对，所以先把重点找出来。","Evet, bu yüzden önce ana noktayı bulalım."),
        ("那就一项一项看。","O zaman maddeleri tek tek ele alalım."),
        "S",
        ("这点我同意，先记下来。","Bu noktaya katılıyorum, önce not edelim."),
        "Q",
        ("我觉得先把这一点说清楚比较好。","Bence önce bu noktayı netleştirmek daha iyi."),
        ("对，不然等会儿容易混在一起。","Evet, yoksa birazdan konular birbirine karışabilir."),
        ("那就先确认大家的想法。","O zaman önce herkesin fikrini netleştirelim."),
        "S",
        ("好，这一项先放在这里。","Tamam, bu maddeyi şimdilik burada bırakalım."),
        "Q",
        ("我觉得这部分也需要认真考虑。","Bence bu kısmı da ciddi biçimde değerlendirmek gerekiyor."),
        ("嗯，先别急着决定。","Evet, karar vermek için acele etmeyelim."),
        ("好，我们把这些都说清楚以后再看下一步。","Tamam, bunları netleştirdikten sonra sonraki adıma bakalım."),
    ],
    ("HSK3",76,94): [
        ("刚才的办法基本可行，不过最后还要把几件事确认清楚。","Az önceki yöntem genel olarak uygulanabilir; ama son olarak birkaç noktayı netleştirmeliyiz."),
        "Q",
        ("我觉得这一点现在已经比刚开始清楚多了。","Bence bu nokta başlangıca göre artık çok daha net."),
        ("对，先把需要做的事情分一下。","Evet, önce yapılacak işleri paylaştıralım."),
        ("好，有变化就及时说。","Tamam, değişiklik olursa hemen söyleyelim."),
        "S",
        ("这样安排以后，后面会顺利很多。","Böyle düzenleyince sonrası çok daha sorunsuz ilerler."),
        ("我同意，不过还得留一点调整空间。","Katılıyorum, ama biraz ayarlama payı bırakmak gerekiyor."),
        ("没问题，遇到情况再改。","Sorun değil, durum çıkarsa yeniden değiştiririz."),
        "Q",
        ("我觉得这部分可以先按现在的想法来。","Bence bu kısmı şimdilik mevcut fikrimize göre yapabiliriz."),
        ("那就先试，效果不好再调整。","O zaman önce deneyelim; sonuç iyi olmazsa yeniden ayarlarız."),
        ("好，我把这个也记下来。","Tamam, bunu da not ediyorum."),
        "S",
        ("现在主要问题已经基本说清楚了。","Ana sorun artık büyük ölçüde netleşti."),
        ("对，剩下的就是按计划做。","Evet, geriye plana göre uygulamak kalıyor."),
        ("最后再确认一遍吧。","Son kez bir daha teyit edelim."),
        "Q",
        ("好，这一点确认以后我们就可以收尾了。","Tamam, bu noktayı da teyit edince konuşmayı tamamlayabiliriz."),
    ],
    ("HSK4",78,94): [
        ("前面的方案已经比较清楚了，最后再把细节过一遍。","Önceki plan artık oldukça net; son olarak ayrıntıları bir kez daha gözden geçirelim."),
        "Q",
        ("我觉得这一点需要结合实际情况看。","Bence bu noktayı gerçek koşullarla birlikte değerlendirmek gerekiyor."),
        ("对，不能只看一个方面。","Evet, yalnızca tek bir açıdan bakamayız."),
        "S",
        ("那就把可能的变化也算进去。","O zaman olası değişiklikleri de hesaba katalım."),
        ("好，这样会稳妥一些。","Tamam, böyle daha temkinli olur."),
        "Q",
        ("我想先确认一下，这会不会影响刚才的安排。","Önce bunun az önceki planı etkileyip etkilemeyeceğini teyit etmek istiyorum."),
        ("如果会，就提前留出调整空间。","Etkileyecekse önceden ayarlama payı bırakalım."),
        "S",
        ("这样一来，大家的责任也更清楚。","Böylece herkesin sorumluluğu da daha net olur."),
        ("对，有变化就及时沟通。","Evet, değişiklik olursa zamanında iletişim kuralım."),
        "Q",
        ("我觉得现在的信息已经够我们做一个决定了。","Bence mevcut bilgiler artık bir karar vermek için yeterli."),
        ("我同意，不过执行以后还要再看效果。","Katılıyorum, ama uyguladıktan sonra sonucu yeniden değerlendirmeliyiz."),
        "S",
    ],
    ("HSK5",71,94): [
        ("刚才的事实和风险已经比较清楚了，接下来把决定落下来。","Olgular ve riskler artık oldukça net; şimdi kararı somutlaştıralım."),
        "Q",
        ("我觉得这一点需要先说明白理由。","Bence önce bunun gerekçesini açıkça anlatmak gerekiyor."),
        ("对，不然别人很难理解这个决定。","Evet, yoksa başkalarının bu kararı anlaması zor olur."),
        "S",
        ("我们也要看看有没有相反的情况。","Ters yönde bir durum olup olmadığına da bakmalıyız."),
        ("如果有，就把它一起放进判断里。","Varsa onu da değerlendirmeye dahil edelim."),
        ("这样会比只看一个角度稳妥。","Bu, yalnızca tek açıdan bakmaktan daha temkinli olur."),
        "Q",
        ("我觉得可以先设一个可以检查的标准。","Bence önce kontrol edilebilir bir ölçüt belirleyebiliriz."),
        ("对，到时候用结果说话。","Evet, zamanı geldiğinde sonucu esas alırız."),
        "S",
        ("那就把时间和责任也一起定下来。","O zaman zamanlamayı ve sorumlulukları da birlikte belirleyelim."),
        ("好，这样执行的时候不会互相等。","Tamam, böylece uygulama sırasında birbirimizi beklemeyiz."),
        "Q",
        ("我还想确认，这个选择会影响到谁。","Bu seçimin kimi etkileyeceğini de teyit etmek istiyorum."),
        ("这个问题很重要，不能只看我们自己。","Bu önemli bir soru; yalnızca kendimize bakamayız."),
        "S",
        ("如果有人有不同意见，就把理由说清楚。","Farklı görüşü olan varsa gerekçesini açıkça anlatsın."),
        ("对，分歧本身不是问题。","Evet, görüş ayrılığının kendisi sorun değildir."),
        "Q",
        ("我觉得现在已经可以做一个暂时的决定了。","Bence artık geçici bir karar verebiliriz."),
        ("那就设一个复查时间，之后再评估。","O zaman bir yeniden değerlendirme zamanı belirleyelim."),
        ("好，这样既不草率，也不会一直拖下去。","Tamam, böylece ne aceleci oluruz ne de işi sürekli uzatırız."),
    ],
    ("HSK6",1,6): [
        "TITLE",
        ("我也想先听听大家最真实的想法。","Ben de önce herkesin en gerçek düşüncesini duymak istiyorum."),
        ("这件事来得有点突然，有不同反应很正常。","Bu konu biraz ani gelişti; farklı tepkiler olması çok normal."),
        ("先别急着下结论，把各自最在意的地方说清楚。","Hemen sonuca varmayalım; herkes en çok neyi önemsediğini netleştirsin."),
        "S",
        ("我同意，先听完彼此怎么想，再看下一步。","Katılıyorum; önce birbirimizi dinleyelim, sonra sonraki adıma bakalım."),
    ],
    ("HSK6",71,92): [
        ("现在最重要的不是再扩大讨论，而是把刚才说清楚的几点落下来。","Şimdi önemli olan tartışmayı büyütmek değil, az önce netleştirdiğimiz noktaları somutlaştırmak."),
        ("对，先确认大家都理解彼此的想法。","Evet, önce herkesin birbirinin düşüncesini anladığından emin olalım."),
        "Q",
        ("我觉得这一点可以再说得具体一点。","Bence bu noktayı biraz daha somut ifade edebiliriz."),
        ("我最关心的是，这个决定会不会让谁觉得被忽略。","En çok bu kararın birine kendini göz ardı edilmiş hissettirip hissettirmeyeceğini önemsiyorum."),
        ("那就把每个人的顾虑再说一遍。","O zaman herkesin kaygısını bir kez daha söyleyelim."),
        "S",
        ("这样做不是为了重新争论，而是为了避免误会。","Bunu yeniden tartışmak için değil, yanlış anlamaları önlemek için yapıyoruz."),
        ("我同意，真正需要决定的事情其实已经不多了。","Katılıyorum; aslında karar verilmesi gereken çok az konu kaldı."),
        ("那就把能现在决定的先定下来。","O zaman şimdi karar verebileceklerimizi netleştirelim."),
        "Q",
        ("我觉得这部分可以留一点时间。","Bence bu kısım için biraz zaman bırakabiliriz."),
        ("有些答案不用今天一次说完。","Bazı cevapların bugün tek seferde verilmesi gerekmiyor."),
        ("只要大家知道下一步怎么走就够了。","Herkes sonraki adımın ne olduğunu bildiği sürece yeterli."),
        "S",
        ("我也会把自己的想法再整理一下。","Ben de kendi düşüncelerimi yeniden toparlayacağım."),
        ("以后如果情况变化，我们再一起谈。","İleride durum değişirse yeniden birlikte konuşuruz."),
        ("对，重要的是保持这种沟通方式。","Evet, önemli olan bu iletişim biçimini sürdürmek."),
        "Q",
        ("现在听起来比刚开始清楚多了。","Şimdi başlangıca göre çok daha net geliyor."),
        ("嗯，我也安心多了。","Evet, ben de çok daha rahatladım."),
        ("好，那最后再确认一下我们刚才的决定。","Tamam, son olarak az önceki kararımızı bir kez daha teyit edelim."),
    ],
}


HSK6_FLOW = [
    "TITLE",
    ("好，我也想听听大家最真实的想法。","Tamam, ben de önce herkesin en gerçek düşüncesini duymak istiyorum."),
    ("这件事来得有点突然，有不同反应很正常。","Bu konu biraz ani gelişti; farklı tepkiler olması çok normal."),
    "Q",
    ("我觉得先把事实和感受分开说清楚比较好。","Bence önce olguları ve duyguları ayrı ayrı netleştirmek daha iyi."),
    "S",
    ("先别急着找一个统一答案，大家可以把顾虑都说出来。","Hemen tek bir ortak cevap bulmaya çalışmayalım; herkes kaygılarını açıkça söylesin."),
    ("这样比较容易知道分歧到底在哪里。","Böylece görüş ayrılığının tam olarak nerede olduğunu anlamak daha kolay olur."),
    "Q",
    ("我先说一个我最担心的地方。","Önce beni en çok düşündüren noktayı söyleyeyim."),
    "S",
    ("这个角度我刚才没有完全想到。","Bu açıyı az önce tam olarak düşünmemiştim."),
    ("那我们把它也放进考虑范围。","O zaman bunu da değerlendirmeye dahil edelim."),
    "Q",
    ("听你这么说，我能理解你为什么会这样想。","Böyle anlatınca neden böyle düşündüğünü anlayabiliyorum."),
    "S",
    ("好，第一轮先把大家最关心的点都说出来。","Tamam, ilk aşamada herkesin en çok önemsediği noktaları ortaya koyalım."),
    ("接下来再看看这些想法之间有没有冲突。","Sonra bu düşünceler arasında çatışan noktalar var mı ona bakalım."),

    ("我发现大家担心的其实不是同一件事。","Aslında herkesin aynı şeyden kaygılanmadığını fark ediyorum."),
    "Q",
    ("对，有些是现实问题，有些是感受问题。","Evet, bazıları pratik meseleler, bazıları ise duygularla ilgili."),
    "S",
    ("这两种都不能只看一边。","Bu iki tarafın da yalnızca birine bakmak doğru olmaz."),
    ("如果只顾眼前，后面的影响可能会被忽略。","Yalnızca bugüne odaklanırsak sonraki etkileri gözden kaçırabiliriz."),
    "Q",
    ("我觉得这个问题需要一个更具体的答案。","Bence bu sorunun daha somut bir cevaba ihtiyacı var."),
    "S",
    ("那就先把能确认的部分确认下来。","O zaman önce doğrulayabildiğimiz kısımları netleştirelim."),
    ("还不确定的先留着，不必硬做结论。","Henüz emin olmadığımız noktaları şimdilik açık bırakalım; zorla sonuç çıkarmayalım."),
    "Q",
    ("我同意，给彼此一点时间反而更稳妥。","Katılıyorum; birbirimize biraz zaman vermek daha temkinli olur."),
    "S",
    ("这样讨论下来，大家的立场已经清楚多了。","Bu konuşmadan sonra herkesin duruşu çok daha netleşti."),
    ("不过还有几个实际问题需要继续谈。","Ama konuşmamız gereken birkaç pratik konu daha var."),
    ("那我们进入下一部分吧。","O zaman sonraki kısma geçelim."),
    ("好，先从最现实的影响开始。","Tamam, önce en somut etkiden başlayalım."),

    ("现在要考虑的是，接下来具体怎么做。","Şimdi düşünmemiz gereken şey bundan sonra somut olarak ne yapacağımız."),
    "Q",
    ("我希望这个选择既照顾现实，也尊重每个人的想法。","Bu seçimin hem gerçek koşulları gözetmesini hem de herkesin düşüncesine saygı duymasını istiyorum."),
    "S",
    ("这点我同意，但执行的时候最好留一点调整空间。","Buna katılıyorum; ama uygulamada biraz ayarlama payı bırakmak iyi olur."),
    ("万一情况和预想的不一样，我们还可以改。","Durum beklediğimiz gibi olmazsa yeniden değiştirebiliriz."),
    "Q",
    ("我更关心的是，这个选择会影响到谁。","Ben daha çok bu seçimin kimi etkileyeceğini önemsiyorum."),
    "S",
    ("对，不能让一个人承担所有后果。","Evet, bütün sonuçları tek bir kişinin üstlenmesini bekleyemeyiz."),
    ("如果是大家一起决定，就应该一起面对结果。","Kararı birlikte alıyorsak sonucunu da birlikte karşılamalıyız."),
    "Q",
    ("我觉得先设一个检查时间会比较好。","Bence önce bir kontrol zamanı belirlemek iyi olur."),
    "S",
    ("到时候再根据实际情况调整，不用一次定死。","O zaman gerçek duruma göre yeniden ayarlarız; her şeyi tek seferde kesinleştirmemiz gerekmiyor."),
    ("这样既不会拖得太久，也不会太草率。","Böylece ne gereğinden fazla uzar ne de aceleci davranmış oluruz."),
    ("好，这一部分我们基本有共识了。","Tamam, bu konuda büyük ölçüde ortak noktaya geldik."),
    ("下一步把分工和时间说清楚。","Sonraki adımda görev dağılımını ve zamanı netleştirelim."),

    ("那我先把刚才的结论整理一下。","O zaman az önce vardığımız sonuçları önce ben toparlayayım."),
    "Q",
    ("我觉得这件事需要有人持续跟进。","Bence bu konunun birinin tarafından düzenli olarak takip edilmesi gerekiyor."),
    "S",
    ("如果有变化，要尽快告诉大家。","Bir değişiklik olursa herkese mümkün olduğunca hızlı haber vermeliyiz."),
    ("对，信息越透明，误会越少。","Evet, bilgi ne kadar açık olursa yanlış anlaşılma o kadar azalır."),
    "Q",
    ("这一点我可以负责确认。","Bu noktayı teyit etme işini ben üstlenebilirim."),
    "S",
    ("其他人也可以把自己的部分说清楚。","Diğerleri de kendi sorumluluklarını net biçimde söyleyebilir."),
    ("这样以后遇到问题就知道先找谁。","Böylece ileride bir sorun çıkarsa önce kime başvuracağımız belli olur."),
    "Q",
    ("我觉得现在比刚开始具体多了。","Bence konu artık başlangıca göre çok daha somut."),
    "S",
    ("还有不同意见也没关系，可以继续保留。","Hâlâ farklı görüşlerin olması sorun değil; bunlar açık kalabilir."),
    ("重要的是我们都知道为什么这样决定。","Önemli olan hepimizin neden böyle karar verdiğimizi bilmesi."),
    ("好，执行以前再最后检查一次。","Tamam, uygulamadan önce son kez bir daha kontrol edelim."),
    ("没问题的话就按刚才说的来。","Sorun yoksa az önce konuştuğumuz gibi ilerleyelim."),

    ("现在回头看，最开始担心的几个问题已经清楚多了。","Şimdi geri baktığımızda başlangıçta kaygı duyduğumuz birkaç konu çok daha net."),
    "Q",
    ("我的想法比刚开始更明确了。","Benim düşüncem başlangıca göre çok daha netleşti."),
    "S",
    ("我也是，至少知道下一步该做什么。","Ben de; en azından sonraki adımda ne yapacağımızı biliyoruz."),
    ("有些答案还需要时间验证。","Bazı cevapların doğrulanması için zamana ihtiyaç var."),
    "Q",
    ("对，不必今天把所有事情一次解决。","Evet, her şeyi bugün tek seferde çözmek zorunda değiliz."),
    "S",
    ("只要沟通还在，后面就能继续调整。","İletişim sürdüğü sürece sonrasında da ayarlama yapabiliriz."),
    ("我觉得这次最重要的是大家都把真话说出来了。","Bence bu konuşmadaki en önemli şey herkesin gerçek düşüncesini söylemiş olması."),
    "Q",
    ("这个问题现在也有比较清楚的方向了。","Bu konu için de artık oldukça net bir yönümüz var."),
    "S",
    ("那就把能做的事情先做好。","O zaman yapabildiğimiz şeyleri önce iyi yapalım."),
    ("剩下的等有新情况再讨论。","Kalan konuları yeni bir durum olduğunda yeniden konuşuruz."),
    ("好，我会把今天的决定记下来。","Tamam, bugünkü kararları not edeceğim."),
    ("有变化我们再一起商量。","Bir değişiklik olursa yeniden birlikte konuşuruz."),
    ("听到这里，我已经放心多了。","Bu noktaya gelince kendimi çok daha rahat hissediyorum."),
    ("那就这样，下一步我们一起面对。","O zaman böyle yapalım; sonraki adımla birlikte yüzleşiriz."),
    ("今天最重要的几件事已经说清楚了。","Bugün en önemli birkaç konuyu netleştirdik."),
    ("剩下的不用一次全部解决。","Kalan her şeyi tek seferde çözmek zorunda değiliz."),
    ("有新情况，我们再及时调整。","Yeni bir durum olursa zamanında yeniden ayarlarız."),
    ("大家都知道接下来该注意什么了。","Artık herkes bundan sonra nelere dikkat etmesi gerektiğini biliyor."),
    ("好，先把眼前最重要的事情做好。","Tamam, önce şu anda en önemli olan şeyi iyi yapalım."),
    ("其他细节可以边走边看。","Diğer ayrıntıları süreç içinde değerlendirebiliriz."),
    ("有变化就及时联系。","Bir değişiklik olursa hemen iletişim kuralım."),
    ("那今天就先到这里吧。","O zaman bugünlük burada bitirelim."),
]

if len(HSK6_FLOW) != 100:
    raise RuntimeError(f"HSK6 flow must have 100 turns, got {len(HSK6_FLOW)}")

HSK6_REFLECT_SCENES = {
    "ZH_HSK6_SC005","ZH_HSK6_SC008","ZH_HSK6_SC009",
    "ZH_HSK6_SC015","ZH_HSK6_SC016","ZH_HSK6_SC025",
    "ZH_HSK6_SC026","ZH_HSK6_SC027","ZH_HSK6_SC029",
    "ZH_HSK6_SC033","ZH_HSK6_SC039","ZH_HSK6_SC040",
    "ZH_HSK6_SC043","ZH_HSK6_SC045","ZH_HSK6_SC046",
    "ZH_HSK6_SC047","ZH_HSK6_SC048","ZH_HSK6_SC049",
    "ZH_HSK6_SC050",
}
HSK6_CELEBRATE_SCENES = {
    "ZH_HSK6_SC001","ZH_HSK6_SC002","ZH_HSK6_SC007",
    "ZH_HSK6_SC010","ZH_HSK6_SC021","ZH_HSK6_SC022",
    "ZH_HSK6_SC024","ZH_HSK6_SC028","ZH_HSK6_SC044",
}
HSK6_WAIT_SCENES = {"ZH_HSK6_SC023"}
HSK6_CRISIS_SCENES = {
    "ZH_HSK6_SC006","ZH_HSK6_SC013","ZH_HSK6_SC036",
    "ZH_HSK6_SC037","ZH_HSK6_SC038","ZH_HSK6_SC041",
}

def hsk6_mode(scene_id):
    if scene_id in HSK6_REFLECT_SCENES:
        return "reflect"
    if scene_id in HSK6_CELEBRATE_SCENES:
        return "celebrate"
    if scene_id in HSK6_WAIT_SCENES:
        return "wait"
    if scene_id in HSK6_CRISIS_SCENES:
        return "crisis"
    return "plan"

HSK6_REFLECT_OVERRIDES = {
    3: ("这件事一提起来，我脑子里一下子冒出很多以前的画面。","Bu konu açılınca aklıma bir anda geçmişten birçok görüntü geliyor."),
    7: ("先别急着总结，我们把想到的事情慢慢说出来。","Hemen sonuç çıkarmayalım; aklımıza gelenleri yavaş yavaş anlatalım."),
    10: ("我先说一个我印象最深的细节。","Önce aklımda en güçlü kalan ayrıntıyı anlatayım."),
    17: ("好，先把大家记得最清楚的都说出来。","Tamam, önce herkes en net hatırladığı şeyleri anlatsın."),
    18: ("听听彼此记得的版本也挺有意思。","Birbirimizin hatırladığı farklı versiyonları dinlemek de ilginç."),
    19: ("同一段经历，每个人记住的地方还真不一样。","Aynı deneyimde herkesin aklında kalan noktalar gerçekten farklı."),
    24: ("有些感受当时没注意，现在回头看反而更清楚。","O zaman fark etmediğimiz bazı duygular, şimdi geriye bakınca daha net görünüyor."),
    26: ("我觉得不用急着找答案，先把故事说完整。","Bence hemen bir cevap aramak yerine önce hikâyeyi tamamlayalım."),
    28: ("那就先把还能记得的细节慢慢拼起来。","O zaman hâlâ hatırladığımız ayrıntıları yavaş yavaş bir araya getirelim."),
    29: ("记不清的地方也没关系，不必勉强。","Net hatırlamadığımız yerler de sorun değil; zorlamaya gerek yok."),
    34: ("这样听下来，很多事情的前后都连起来了。","Böyle dinleyince birçok olayın öncesi ve sonrası birbirine bağlanıyor."),
    35: ("我还想听听，这些年大家的感受有没有变化。","Yıllar içinde herkesin duygularının değişip değişmediğini de duymak istiyorum."),
    36: ("好，那就从后来发生的事接着说。","Tamam, o zaman sonrasında olanlardan devam edelim."),
    37: ("现在再看这段经历，和当时的感觉已经不太一样了。","Bu deneyime şimdi baktığımda, o zamanki hissimden oldukça farklı geliyor."),
    39: ("我更想知道，这段经历为什么到现在还让我们记得。","Ben daha çok bu deneyimin neden hâlâ aklımızda kaldığını merak ediyorum."),
    41: ("这点我同意，有些意义是过很久以后才看得出来的。","Buna katılıyorum; bazı anlamlar ancak uzun zaman geçince ortaya çıkıyor."),
    42: ("如果换成现在的我们，也许会有不一样的理解。","Bugünkü hâlimizle baksak belki farklı bir anlam çıkarırdık."),
    44: ("我最在意的不是结果，而是当时大家为什么会那样想。","Benim için en önemli şey sonuç değil, o zaman neden öyle düşündüğümüz."),
    46: ("对，不能只用现在的眼光去评价以前。","Evet, geçmişi yalnızca bugünün bakışıyla değerlendiremeyiz."),
    47: ("把当时的条件放回去看，很多事情就容易理解了。","O dönemin koşullarını hesaba katınca birçok şeyi anlamak kolaylaşıyor."),
    49: ("我觉得可以把这些故事好好留下来。","Bence bu hikâyeleri iyi biçimde koruyabiliriz."),
    51: ("以后再回头看，也许还会有新的理解。","İleride yeniden baktığımızda belki yeni anlamlar çıkaracağız."),
    52: ("这样既保留了记忆，也不会把过去说得太简单。","Böylece hem anıları koruruz hem de geçmişi gereğinden fazla basitleştirmemiş oluruz."),
    53: ("嗯，这部分我听明白了。","Evet, bu kısmı şimdi daha iyi anladım."),
    54: ("接下来再说说，这些经历到底给我们留下了什么。","Şimdi de bu deneyimlerin bize ne bıraktığını konuşalım."),
    55: ("我先把刚才说到的几件事理一理。","Az önce konuştuğumuz birkaç şeyi önce bir toparlayayım."),
    57: ("我觉得这些故事值得有人认真记下来。","Bence bu hikâyeler dikkatle kayda geçirilmeye değer."),
    59: ("以后想起新的细节，再补上也不迟。","İleride yeni bir ayrıntı hatırlarsak eklemek için geç olmaz."),
    60: ("对，记忆本来就会随着时间慢慢变化。","Evet, anılar zaten zamanla yavaş yavaş değişir."),
    62: ("这一点我想再找找当时留下的东西。","Bu noktada o zamandan kalan şeylere yeniden bakmak istiyorum."),
    64: ("大家记得的不一样也很正常。","Herkesin farklı hatırlaması da çok normal."),
    65: ("这些不同反而能让这段经历更完整。","Bu farklılıklar aslında deneyimi daha bütünlüklü hâle getiriyor."),
    67: ("现在听起来比刚开始有层次多了。","Şimdi konu başlangıca göre çok daha katmanlı geliyor."),
    70: ("重要的是我们知道这些经历为什么到现在还重要。","Önemli olan bu deneyimlerin neden bugün hâlâ önemli olduğunu bilmemiz."),
    71: ("好，最后再说说今天听完以后最大的感受。","Tamam, son olarak bugün bunları dinledikten sonraki en güçlü duygumuzu söyleyelim."),
    72: ("我觉得已经比一开始更明白了。","Bence başlangıca göre çok daha iyi anlıyoruz."),
    73: ("现在回头看，最开始想到的那些画面已经连得更完整了。","Şimdi geriye baktığımızda başlangıçta aklımıza gelen görüntüler daha bütünlüklü bir hâl aldı."),
    75: ("我的感受比刚开始更清楚了。","Benim duygum başlangıca göre daha net."),
    77: ("我也是，很多以前没想过的地方现在看清楚了。","Ben de; daha önce düşünmediğim birçok noktayı şimdi daha net görüyorum."),
    78: ("有些理解还需要时间慢慢沉下来。","Bazı anlamların oturması için biraz zamana ihtiyaç var."),
    80: ("对，不必今天把所有感受都说到最后。","Evet, bütün duyguları bugün son noktasına kadar açıklamak zorunda değiliz."),
    82: ("只要愿意继续聊，以后还会有新的发现。","Konuşmaya devam etmeye açık olduğumuz sürece ileride yeni şeyler fark ederiz."),
    83: ("我觉得这次最重要的是大家都把真实的感受说出来了。","Bence bu konuşmadaki en önemli şey herkesin gerçek duygusunu söylemesi oldu."),
    85: ("这个问题现在不用急着有唯一答案。","Bu sorunun şu anda tek bir cevabı olmak zorunda değil."),
    87: ("那就把今天记住的先好好留下来。","O zaman bugün hatırladıklarımızı önce iyi biçimde koruyalım."),
    89: ("好，我会把今天说到的重点记下来。","Tamam, bugün konuştuğumuz önemli noktaları not edeceğim."),
    92: ("那就这样，以后想起新的故事我们再接着聊。","O zaman böyle bırakalım; ileride yeni bir hikâye hatırlarsak yeniden devam ederiz."),
    93: ("今天聊完，我对这段经历又有了新的理解。","Bugünkü konuşmadan sonra bu deneyimi yeniden ve daha derinden anlıyorum."),
    94: ("很多细节以后可能还会慢慢想起来。","Birçok ayrıntı ileride yavaş yavaş yeniden aklımıza gelebilir."),
    95: ("不必急着给过去下一个最后的结论。","Geçmiş hakkında hemen kesin bir sonuca varmak zorunda değiliz."),
    96: ("能把这些故事重新说出来，本身就很有意义。","Bu hikâyeleri yeniden anlatabilmek bile başlı başına anlamlı."),
    97: ("以后再想起什么，我们就继续补上。","İleride başka bir şey hatırlarsak eklemeye devam ederiz."),
    98: ("这些记忆留在大家心里，本身就很珍贵。","Bu anıların hepimizin içinde kalması zaten çok değerli."),
    99: ("好，今天先聊到这里。","Tamam, bugünlük burada bırakalım."),
    100: ("下次想起来，我们再接着讲。","Bir dahaki sefere aklımıza geldiğinde anlatmaya devam ederiz."),
}

HSK6_CELEBRATE_OVERRIDES = {
    3: ("这个消息一说出来，我第一反应还是高兴。","Bu haber söylenince ilk hissettiğim şey yine de sevinç oldu."),
    7: ("先别急着想太远，大家先说说现在的感受。","Hemen çok ileriye gitmeyelim; önce şu an ne hissettiğimizi konuşalım."),
    10: ("我先说，我其实挺激动的。","Önce ben söyleyeyim; aslında oldukça heyecanlıyım."),
    17: ("好，先把想说的祝福和担心都说出来。","Tamam, önce söylemek istediğimiz iyi dilekleri ve kaygıları paylaşalım."),
    18: ("高兴归高兴，有些现实问题也可以慢慢谈。","Sevinç ayrı; bazı pratik meseleleri de yavaş yavaş konuşabiliriz."),
    19: ("我觉得大家的反应其实都很真实。","Bence herkesin tepkisi oldukça gerçek ve doğal."),
    24: ("眼前先好好享受这个时刻，后面的事可以一步一步来。","Şimdilik bu anın tadını çıkaralım; sonrasını adım adım ele alırız."),
    26: ("有些问题不用现在马上回答。","Bazı soruların cevabını hemen şimdi vermek gerekmiyor."),
    28: ("先把确定的消息和安排说清楚就好。","Şimdilik kesinleşen haberleri ve temel düzenlemeleri netleştirmemiz yeterli."),
    29: ("其他细节可以等以后再慢慢补。","Diğer ayrıntıları daha sonra yavaş yavaş tamamlayabiliriz."),
    34: ("这样一说，大家的心情也放松多了。","Böyle konuşunca herkesin içi biraz daha rahatladı."),
    35: ("接下来再聊聊，有什么地方需要我们帮忙。","Şimdi de hangi konularda yardım gerekebileceğini konuşalım."),
    36: ("好，从最实际的事情开始。","Tamam, en pratik konudan başlayalım."),
    37: ("现在最重要的是让当事人自己觉得舒服。","Şu anda en önemli şey, asıl ilgili kişinin kendini rahat hissetmesi."),
    39: ("我希望大家的关心不会变成压力。","Herkesin ilgisinin baskıya dönüşmemesini istiyorum."),
    41: ("对，支持比替别人做决定更重要。","Evet, destek olmak başkası adına karar vermekten daha önemli."),
    42: ("需要的时候我们再一起商量。","Gerektiğinde yeniden birlikte konuşuruz."),
    44: ("我更关心的是，当事人自己真正想要什么。","Ben daha çok asıl ilgili kişinin gerçekten ne istediğini önemsiyorum."),
    46: ("对，不应该让一个人面对所有压力。","Evet, bütün baskıyla tek bir kişinin yüzleşmesini beklememeliyiz."),
    47: ("是家里的事就一起支持，但也要尊重彼此的边界。","Aileyi ilgilendiriyorsa birlikte destek olalım ama birbirimizin sınırlarına da saygı duyalım."),
    49: ("我觉得可以先定几个最基本的安排。","Bence önce birkaç temel düzenlemeyi netleştirebiliriz."),
    51: ("后面的细节有变化再调整。","Sonraki ayrıntıları değişiklik oldukça ayarlarız."),
    52: ("这样不会太着急，也不会什么都不准备。","Böylece ne acele etmiş oluruz ne de hazırlıksız kalırız."),
    53: ("好，大家至少方向是一致的。","Tamam, en azından herkes genel yönde aynı fikirde."),
    54: ("接下来需要谁帮忙，再具体说就行。","Sonrasında kimin yardımına ihtiyaç olursa o zaman netleştiririz."),
    55: ("那我先把刚才说到的安排理一理。","O zaman az önce konuştuğumuz düzenlemeleri önce bir toparlayayım."),
    57: ("我觉得最重要的还是需要的时候有人搭把手。","Bence en önemlisi ihtiyaç olduğunda birinin yardım edebilmesi."),
    59: ("有新情况就及时告诉大家。","Yeni bir durum olursa herkese zamanında haber verelim."),
    60: ("对，别让关心变成大家互相猜。","Evet, ilgimizin birbirimizin ne düşündüğünü tahmin etmeye dönüşmesine izin vermeyelim."),
    62: ("这一点我可以帮着确认。","Bu noktayı teyit etmeye ben yardımcı olabilirim."),
    64: ("其他人也看看自己能帮什么。","Diğerleri de nerede yardımcı olabileceklerine baksın."),
    65: ("这样真需要帮忙时就不会手忙脚乱。","Böylece gerçekten yardım gerektiğinde telaş etmeyiz."),
    67: ("现在比刚听到消息的时候踏实多了。","Şimdi haberi ilk duyduğumuz ana göre çok daha sakinim."),
    70: ("重要的是大家都知道怎么支持彼此。","Önemli olan herkesin birbirini nasıl destekleyeceğini bilmesi."),
    71: ("好，最后再看看还有没有遗漏的地方。","Tamam, son olarak gözden kaçan bir nokta var mı bakalım."),
    72: ("没问题的话就先按现在的节奏来。","Sorun yoksa şimdilik bu tempoda ilerleyelim."),
    73: ("现在回头看，刚听到消息时的那些担心已经少多了。","Şimdi geriye bakınca haberi ilk duyduğumuzdaki kaygılar çok azalmış görünüyor."),
    75: ("我的心情也比刚开始轻松多了。","Benim de içim başlangıca göre çok daha rahat."),
    77: ("我也是，现在更多的是期待。","Ben de; artık daha çok güzel bir beklenti hissediyorum."),
    78: ("有些事情还是要等时间慢慢展开。","Bazı şeylerin zamanla yavaş yavaş ortaya çıkmasını beklemek gerekiyor."),
    80: ("对，不必今天把后面的所有事情都安排完。","Evet, gelecekteki her şeyi bugün planlamak zorunda değiliz."),
    82: ("有需要及时说，后面都能慢慢安排。","İhtiyaç olduğunda hemen söylersek sonrasını yavaş yavaş düzenleyebiliriz."),
    83: ("我觉得这次最重要的是大家都把真实的想法说出来了。","Bence bu konuşmadaki en önemli şey herkesin gerçek düşüncesini söylemesi oldu."),
    85: ("这个问题现在已经有比较清楚的想法了。","Bu konu hakkında artık oldukça net bir fikrimiz var."),
    87: ("那就先把眼前该做的做好。","O zaman önce şu anda yapılması gerekenleri iyi yapalım."),
    89: ("好，今天说到的安排我记住了。","Tamam, bugün konuştuğumuz düzenlemeleri aklımda tutacağım."),
    92: ("那就这样，接下来大家一起往前走吧。","O zaman böyle yapalım; bundan sonra hep birlikte ilerleyelim."),
    93: ("今天最重要的是把好消息和真实的想法都分享出来了。","Bugün en önemlisi güzel haberi ve gerçek düşüncelerimizi paylaşmış olmamız."),
    94: ("后面的事情不用一次全都安排好。","Sonraki her şeyi tek seferde planlamak zorunda değiliz."),
    95: ("需要帮忙的时候就随时说。","Yardıma ihtiyaç olduğunda hemen söyleyin."),
    96: ("大家都在，不用一个人把所有事情扛下来。","Herkes burada; bütün yükü tek başına taşımaya gerek yok."),
    97: ("先好好享受眼前这个阶段吧。","Önce içinde bulunduğumuz bu dönemin tadını çıkaralım."),
    98: ("以后有新的安排，我们再一起商量。","İleride yeni bir düzenleme olduğunda yeniden birlikte konuşuruz."),
    99: ("今天说完，我心里踏实多了。","Bugün konuştuktan sonra içim çok daha rahat."),
    100: ("好，那就带着这份期待慢慢往前走。","Tamam, bu güzel beklentiyle adım adım ilerleyelim."),
}

HSK6_WAIT_OVERRIDES = {
    3: ("现在最难的其实就是等，大家心里都不太踏实。","Şu anda en zor şey beklemek; kimsenin içi tam rahat değil."),
    7: ("先别想太多，能确认的消息我们一条一条听。","Çok fazla düşünmeyelim; doğrulanmış haberleri tek tek takip edelim."),
    10: ("我最担心的就是一直没有消息。","Benim en büyük kaygım uzun süre haber gelmemesi."),
    17: ("好，大家先把心里最担心的说出来。","Tamam, herkes önce içinde en çok kaygı duyduğu şeyi söylesin."),
    24: ("现在猜再多也没用，还是等确定的消息。","Şu anda ne kadar tahmin etsek de faydası yok; kesin haberi beklemek daha iyi."),
    35: ("接下来最重要的是互相陪着，别让谁一个人胡思乱想。","Şimdi en önemlisi birbirimize eşlik etmek ve kimseyi yalnız başına kaygıyla bırakmamak."),
    37: ("我们现在能做的其实不多，但陪在这里本身就很重要。","Şu anda yapabileceğimiz çok şey yok ama burada birlikte olmak bile önemli."),
    49: ("我觉得可以隔一会儿再问一次情况。","Bence biraz sonra durumu yeniden sorabiliriz."),
    55: ("那我先把已经知道的消息理一理。","O zaman bildiğimiz kesin bilgileri önce bir toparlayayım."),
    67: ("现在比刚才踏实一点了。","Şimdi az öncekine göre biraz daha sakinim."),
    73: ("回头看，最难熬的那段时间已经过去一些了。","Geriye bakınca en zor bekleyiş kısmının biraz geride kaldığını görüyoruz."),
    83: ("我觉得大家能在这里互相陪着已经很重要了。","Bence burada birbirimize eşlik edebilmemiz bile çok önemli."),
    92: ("那就这样，我们继续一起等消息。","O zaman böyle yapalım; haberi birlikte beklemeye devam edelim."),
    93: ("现在能做的就是继续等确定的消息。","Şu anda yapabileceğimiz şey kesin haberi beklemeye devam etmek."),
    94: ("大家都在这里，先别一个人担心。","Herkes burada; kaygınla tek başına kalma."),
    95: ("有消息我们马上互相告诉。","Bir haber gelirse hemen birbirimize söyleyelim."),
    96: ("累了就坐一会儿，别一直硬撑着。","Yorulduysan biraz otur; sürekli güçlü durmaya çalışma."),
    97: ("只要有新的情况，我们再一起商量。","Yeni bir durum olduğunda yeniden birlikte konuşuruz."),
    98: ("好，先安静等一会儿。","Tamam, şimdi biraz sakin biçimde bekleyelim."),
    99: ("我现在比刚才踏实一点了。","Şimdi az öncekine göre biraz daha sakinim."),
    100: ("嗯，我们一起等。","Evet, birlikte bekleyelim."),
}

HSK6_CRISIS_OVERRIDES = {
    93: ("现在最重要的风险和分工已经说清楚了。","En önemli riskler ve görev paylaşımı artık net."),
    94: ("先按应急安排执行，不要各自行动。","Önce acil durum planına göre hareket edelim; herkes kendi başına davranmasın."),
    95: ("有变化就立刻通知所有人。","Bir değişiklik olursa herkese hemen haber verelim."),
    96: ("保持联系，先确认每个人都安全。","İletişimde kalalım ve önce herkesin güvende olduğundan emin olalım."),
    97: ("先处理最紧急的部分。","Önce en acil kısmı halledelim."),
    98: ("安全以后再处理其他问题。","Güvenlik sağlandıktan sonra diğer sorunlara geçeriz."),
    99: ("最后再确认一次联系方式。","Son olarak iletişim bilgilerini bir kez daha teyit edelim."),
    100: ("好，就按这个方案行动。","Tamam, bu plana göre hareket edelim."),
}

def adapt_hsk6_generic(scene_id, turn, role):
    mode=hsk6_mode(scene_id)
    if not isinstance(role, tuple):
        return role
    if mode=="reflect":
        return HSK6_REFLECT_OVERRIDES.get(turn,role)
    if mode=="celebrate":
        return HSK6_CELEBRATE_OVERRIDES.get(turn,role)
    if mode=="wait":
        return HSK6_WAIT_OVERRIDES.get(turn,role)
    if mode=="crisis":
        return HSK6_CRISIS_OVERRIDES.get(turn,role)
    return role

def hsk6_followup(mode, is_question, variant):
    if mode=="reflect":
        q=[
            ("说到这里，你最想起的是什么？","Buraya kadar konuştuktan sonra aklına en çok ne geliyor?"),
            ("这段经历里，你印象最深的是哪一点？","Bu deneyimde aklında en güçlü kalan nokta hangisi?"),
            ("如果从今天回头看，你最想补充什么？","Bugünden geriye baktığında en çok ne eklemek istersin?"),
            ("听完这些，你有没有想起别的细节？","Bunları dinleyince aklına başka bir ayrıntı geldi mi?"),
        ]
        st=[
            ("我觉得这一点现在比以前看得更清楚。","Bence bu noktayı şimdi geçmişe göre daha net görüyoruz."),
            ("听你这么说，我也想起了不少以前的事。","Böyle anlatınca benim de geçmişten birçok şey aklıma geldi."),
            ("对，这样把前后连起来就更容易理解了。","Evet, öncesi ve sonrasını bağlayınca anlamak daha kolay oluyor."),
            ("有些感受过了很久才会真正明白。","Bazı duyguların anlamını ancak uzun zaman sonra gerçekten kavrıyoruz."),
        ]
    elif mode=="celebrate":
        q=[
            ("听到这里，你现在最期待的是什么？","Buraya kadar konuştuktan sonra en çok neyi bekliyorsun?"),
            ("还有什么想说的祝福吗？","Söylemek istediğin başka bir iyi dilek var mı?"),
            ("那你觉得现在最需要的是什么？","Peki sence şu anda en çok neye ihtiyaç var?"),
            ("大家还有什么想补充的吗？","Herkesin eklemek istediği başka bir şey var mı?"),
        ]
        st=[
            ("我觉得现在最重要的是让大家都轻松一点。","Bence şu anda en önemlisi herkesin biraz rahatlaması."),
            ("对，高兴的同时也可以把实际事情慢慢安排好。","Evet, sevinirken pratik işleri de yavaş yavaş düzenleyebiliriz."),
            ("至少现在大家都知道彼此怎么想了。","En azından artık herkes birbirinin ne düşündüğünü biliyor."),
            ("我觉得这样一步一步来就很好。","Bence böyle adım adım ilerlemek çok iyi."),
        ]
    elif mode=="wait":
        q=[
            ("现在你最担心的是什么？","Şu anda seni en çok kaygılandıran şey ne?"),
            ("还有什么消息需要再确认吗？","Yeniden teyit etmemiz gereken başka bir haber var mı?"),
            ("要不要先休息一下，等新的消息？","Yeni haber gelene kadar biraz dinlenelim mi?"),
            ("你现在感觉好一点了吗？","Şimdi kendini biraz daha iyi hissediyor musun?"),
        ]
        st=[
            ("我觉得先等确定的消息最稳妥。","Bence en güvenlisi kesin haberi beklemek."),
            ("对，现在互相陪着比乱猜更重要。","Evet, şu anda birbirimize eşlik etmek tahmin yürütmekten daha önemli."),
            ("有消息以后我们再一起商量。","Haber gelince yeniden birlikte konuşuruz."),
            ("先别急，大家都在这里。","Acele etme; herkes burada."),
        ]
    else:
        q=[
            ("说到这里，你现在最担心的还有什么？","Buraya kadar konuştuktan sonra hâlâ en çok neyi merak ediyorsun?"),
            ("听完这些，你还想补充哪一点？","Bunları dinledikten sonra hangi noktayı eklemek istersin?"),
            ("如果换个角度看，你会怎么想？","Başka bir açıdan bakarsan nasıl düşünürsün?"),
            ("这一点大家还有不同意见吗？","Bu konuda hâlâ farklı görüşü olan var mı?"),
        ]
        st=[
            ("我觉得这一点已经比刚开始清楚多了。","Bence bu nokta başlangıca göre çok daha net."),
            ("至少大家都把自己的想法说出来了。","En azından herkes kendi düşüncesini açıkça söyledi."),
            ("我同意，这样理解起来更完整。","Katılıyorum; böyle daha bütünlüklü anlaşılıyor."),
            ("对，这个角度也值得保留。","Evet, bu bakış açısını da korumak gerekiyor."),
        ]
    arr=q if is_question else st
    return arr[variant % len(arr)]

for (lvl,a,b), seq in BLOCKS.items():
    expected=b-a+1
    if len(seq)!=expected:
        raise RuntimeError(f"BLOCK length mismatch {lvl} {a}-{b}: {len(seq)} != {expected}")

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

def term_question(card, level, variant=0):
    z=str(card.get("zh","")).strip()
    t=str(card.get("tr","")).strip()
    ex=str(card.get("exampleZh","")).strip()
    k=term_kind(card)

    if level=="HSK6":
        forms=[
            (f"说到{z}，你最先想到的是什么？", f"{t} denince aklına ilk ne geliyor?"),
            (f"关于{z}，你现在怎么看？", f"{t} konusunda şu anda ne düşünüyorsun?"),
            (f"{z}这件事，对你来说最重要的是什么？", f"{t} konusunda senin için en önemli nokta ne?"),
            (f"说到{z}，还有什么想补充的吗？", f"{t} konusunda eklemek istediğin başka bir şey var mı?"),
            (f"现在再看{z}，你的想法和刚开始一样吗？", f"{t} konusuna şimdi tekrar baktığında düşüncen başlangıçtakiyle aynı mı?"),
        ]
        return forms[variant % len(forms)]

    if k=="verb":
        if ex.startswith(z+"以前"):
            return f"说到{z}，你现在怎么看？", f"{t} konusunda şu anda ne düşünüyorsun?"
        return f"那要不要先{z}一下？", f"O zaman önce “{t}” kısmını ele alalım mı?"
    if k=="adj":
        return f"你觉得{z}怎么样？", f"“{t}” seçeneği hakkında ne düşünüyorsun?"
    if level=="HSK2":
        return f"那{z}呢？", f"Peki {t}?"
    return f"说到{z}，你怎么看？", f"{t} konusunda ne düşünüyorsun?"

def term_statement(card, level, variant=0):
    z=str(card.get("zh","")).strip()
    t=str(card.get("tr","")).strip()
    ex=str(card.get("exampleZh","")).strip()
    k=term_kind(card)

    if level=="HSK6":
        forms=[
            (f"我觉得{z}这一点确实不能忽略。", f"Bence {t} konusunu kesinlikle göz ardı edemeyiz."),
            (f"对，{z}会影响我们后面怎么看这件事。", f"Evet, {t} bundan sonra bu konuya nasıl bakacağımızı etkileyebilir."),
            (f"关于{z}，我觉得大家的想法都应该说出来。", f"{t} konusunda bence herkes düşüncesini açıkça söylemeli."),
            (f"至少在{z}这件事上，我们已经知道彼此最在意什么了。", f"En azından {t} konusunda artık birbirimizin en çok neyi önemsediğini biliyoruz."),
            (f"说到{z}，我觉得还是要给彼此一点空间。", f"{t} konusunda bence birbirimize biraz alan bırakmalıyız."),
        ]
        return forms[variant % len(forms)]

    if k=="verb":
        if ex.startswith(z+"以前"):
            return f"我觉得{z}以前还要再确认一下。", f"Bence {t} öncesinde bir kez daha teyit etmek gerekiyor."
        return f"我觉得先{z}一下比较好。", f"Bence önce “{t}” kısmını ele almak daha iyi olur."
    if k=="adj":
        return f"我觉得{z}会更合适。", f"Bence “{t}” seçeneği daha uygun olur."
    if level=="HSK2":
        return f"我觉得{z}也很重要。", f"Bence {t} de önemli."
    return f"我觉得{z}这一点也不能忽略。", f"Bence {t} konusunu da göz ardı etmemeliyiz."

def block_role(level, turn):
    for (lvl,a,b), seq in BLOCKS.items():
        if lvl==level and a <= turn <= b:
            return seq[turn-a]
    return None

def scaffold_line(level, turn, data, cards, term_cursor):
    scene_id=data.get("id","")
    if level=="HSK6":
        role=adapt_hsk6_generic(scene_id,turn,HSK6_FLOW[turn-1])
    else:
        role=block_role(level,turn)

    if role is None:
        raise RuntimeError(f"No block role for {level} turn {turn}")

    if role=="TITLE":
        first=cards[0]
        z=str(first.get("zh","这件事")).strip()
        t=str(first.get("tr","bu konu")).strip()
        if level=="HSK6":
            mode=hsk6_mode(scene_id)
            if mode=="reflect":
                zh=f"说到{z}，我一下子想起了很多事，今天正好大家一起聊聊吧。"
                tr=f"{t} deyince aklıma birçok şey geliyor; bugün hep birlikte biraz konuşalım."
            elif mode=="celebrate":
                zh=f"既然说到{z}，大家也把现在的心情都说说吧。"
                tr=f"{t} konusu açılmışken herkes şu an ne hissettiğini paylaşsın."
            elif mode=="wait":
                zh="大家都在这里等消息，先别让自己太紧张。"
                tr="Hepimiz burada haber bekliyoruz; önce kendimizi fazla germeyelim."
            elif mode=="crisis":
                zh=f"关于{z}，我们先把现在的情况和接下来要做的事说清楚。"
                tr=f"{t} konusunda önce mevcut durumu ve bundan sonra ne yapacağımızı netleştirelim."
            else:
                zh=f"关于{z}，我们今天把各自的想法和实际问题都说清楚吧。"
                tr=f"{t} konusunda bugün herkes düşüncesini ve pratik sorunları açıkça ortaya koysun."
            return zh,tr,True
        return (
            f"今天正好有时间，我们聊聊{z}这件事吧。",
            f"Bugün vaktimiz varken {t} konusunu konuşalım.",
            True,
        )

    if role=="Q":
        if level=="HSK6" and term_cursor >= len(cards):
            zh,tr=hsk6_followup(hsk6_mode(scene_id),True,turn)
            return zh,tr,False
        card=cards[term_cursor % len(cards)]
        zh,tr=term_question(card,level,term_cursor)
        return zh,tr,True

    if role=="S":
        if level=="HSK6" and term_cursor >= len(cards):
            zh,tr=hsk6_followup(hsk6_mode(scene_id),False,turn)
            return zh,tr,False
        card=cards[term_cursor % len(cards)]
        zh,tr=term_statement(card,level,term_cursor)
        return zh,tr,True

    zh,tr=role
    return zh,tr,False

def pinyin_text(text):
    text=t2s.convert(text)
    parts=lazy_pinyin(
        text,
        style=Style.TONE,
        neutral_tone_with_five=False,
        strict=False,
        errors=lambda x:list(x),
    )
    s=" ".join(parts)
    s=re.sub(r"\s+([，。？！；：、,.?!;:])",r"\1",s)
    s=s.replace("，",",").replace("。",".").replace("？","?").replace("！","!")
    s=s.replace("；",";").replace("：",":")
    s=s.replace("nǎ ér","nǎr").replace("zhè ér","zhèr").replace("nà ér","nàr")
    s=s.replace("ń","èn").replace("ň","èn")
    s=re.sub(r"\s+"," ",s).strip()
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
        term_cursor=0

        for i,d in enumerate(src,1):
            old=t2s.convert(str(d.get("zh","")).strip())
            key=f"{scene_id}:{d.get('id')}:{prev}"
            if level in PHASE and is_rebuild(level,i):
                new,tr,used_term=scaffold_line(level,i,data,cards,term_cursor)
                if used_term:
                    term_cursor+=1
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

        # Final safety net: every active vocabulary item that existed in the
        # source dialogue must still appear at least once after rebuilding.
        original_text="".join(t2s.convert(str(x.get("zh",""))) for x in src)
        final_text="".join(x["zh"] for x in out)
        missing=[c for c in cards if str(c.get("zh","")).strip() in original_text and str(c.get("zh","")).strip() not in final_text]
        if missing:
            candidates=[
                pos for pos in range(1,len(out)+1)
                if is_rebuild(level,pos) and isinstance(block_role(level,pos),tuple)
            ]
            used=set()
            for card,pos in zip(missing,candidates):
                if pos in used:
                    continue
                zh,tr=term_statement(card,level)
                out[pos-1]["zh"]=zh
                out[pos-1]["pinyin"]=pinyin_text(zh)
                out[pos-1]["tr"]=tr
                used.add(pos)

        changed=sum(
            1 for old_item,new_item in zip(src,out)
            if t2s.convert(str(old_item.get("zh","")).strip()) != new_item["zh"]
        )

        patch={
            "naturalizationVersion":7,
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
        "naturalizationVersion":7,
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
