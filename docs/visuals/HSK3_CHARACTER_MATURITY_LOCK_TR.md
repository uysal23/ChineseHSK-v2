# HSK3 CHARACTER MATURITY LOCK V1 — Yaş / Olgunluk Patch'i

**Durum:** LOCKED  
**Proje:** ChineseHSK-v2  
**Kapsam:** HSK3 görsel üretimi, yeniden üretim ve görsel QA  
**Bağlayıcılık:** `visual_generation_policy.json`, `CHARACTER_CAST_LOCK_TR.md` ve `VISUAL_CONTINUITY_LOCK_TR.md` ile birlikte uygulanır. Çelişki halinde mevcut LOCKED_V2 yaş ilerleme tanımları esas alınır.

## 1. HSK3 zaman ilerlemesi zorunludur

HSK3 karakterleri HSK1–HSK2 görsellerinin aynı yaşta yeniden çizilmiş hâli olamaz. Aynı canonical kimlik korunurken doğal zaman ilerlemesi görünür olmalıdır.

HSK3–HSK4 için authoritative yaş bantları:

- **张伟 / Zhang Wei:** `mature_adult`
- **刘梅 / Liu Mei:** `mature_adult`
- **张雨桐 / Yutong:** `young_adult`
- **张乐乐 / Lele:** `teen_boy`

Relative age lock korunur:

**Yutong, Lele'den görsel olarak daha büyük/olgun görünmelidir.**

## 2. Zhang Wei

- HSK1–HSK2'deki yüz kimliği, siyah dikdörtgen gözlük ve temel renk ailesi korunur.
- HSK3'te öğrenci/genç yetişkin gibi görünemez.
- Daha oturmuş yetişkin yüz oranı, duruş ve sorumluluk hissi taşımalıdır.
- Yaşlılaştırılmaz; yalnızca doğal yetişkin olgunlaşması uygulanır.

## 3. Liu Mei

- Canonical yüz, uzun koyu saç ve sıcak kimlik korunur.
- HSK3'te daha kararlı, girişimci ve kendine güvenen yetişkin görünümü gerekir.
- Ev içi sıcaklık korunurken iş kurma/planlama sorumluluğu beden diline yansır.
- Aşırı gençleştirme veya glamorize/sexualized görünüm yasaktır.

## 4. Yutong

- HSK3–HSK4'te `young_adult` görünmelidir.
- HSK1–HSK2'deki ergen/genç kız oranları aynen tekrar edilemez.
- Boy, yüz oranları, beden dili ve sorumluluk hissi doğal biçimde olgunlaşmış olmalıdır.
- Yutong hiçbir durumda küçük çocuk gibi görünemez.
- Yutong, Lele'den açıkça daha büyük görünmelidir.

## 5. Lele — BLOKLAYICI YAŞ KİLİDİ

Lele'nin kimliği:

- erkek,
- Zhang ailesinin küçük oğlu,
- Yutong'dan daha genç,
- HSK3–HSK4 döneminde `teen_boy`.

HSK3 Lele için zorunlu görsel özellikler:

- HSK1–HSK2'ye göre belirgin biçimde büyümüş olmalı,
- teenage boy / ergen erkek görünümü vermeli,
- daha uzun ve dengeli vücut oranlarına sahip olmalı,
- kafa-gövde oranı küçük çocuk/toddler seviyesinde olmamalı,
- yüz aşırı tombul/bebeksi olmamalı,
- davranışları daha bilinçli, yardımcı ve katılımcı görünmeli,
- mavi/yeşil canonical renk ailesi korunabilir,
- erkek kimliği tartışmasız okunmalıdır.

### Lele için HARD FAIL

Aşağıdakilerden biri varsa görsel **FINAL olamaz ve uygulamaya alınamaz**:

- Lele'nin kız olarak veya cinsiyeti belirsiz çizilmesi,
- toddler / okul öncesi çocuk görünümü,
- HSK1–HSK2 küçük çocuk oranlarının HSK3'te aynen kullanılması,
- aşırı büyük kafa / kısa gövde / chibi-bebeksi oran,
- Yutong ile yaş farkının tersine dönmesi veya belirsizleşmesi,
- Lele'nin Yutong kadar veya Yutong'dan daha büyük görünmesi.

## 6. HSK3 QA kapısı

Her HSK3 sahnesi FINAL olmadan önce aşağıdaki maddelerin tamamı PASS olmalıdır:

- [ ] Canonical yüz/saç/rol kimliği korunuyor.
- [ ] Zhang Wei `mature_adult` görünüyor.
- [ ] Liu Mei `mature_adult` görünüyor.
- [ ] Yutong `young_adult` görünüyor.
- [ ] Lele `teen_boy` görünüyor.
- [ ] Yutong > Lele relative age order net.
- [ ] Lele toddler/bebeksi/chibi görünmüyor.
- [ ] Lele erkek kimliği net.
- [ ] HSK1–HSK2'ye göre cross-level proportional growth görünür.
- [ ] WARM_CINEMATIC_STYLIZED_3D_CGI_V1 sürekliliği korunuyor.

Bu maddelerden biri FAIL ise `rejectOnAnyManifestMismatch=true` kuralı uygulanır ve görsel yeniden üretilir.

## 7. Kısa üretim patch notu

**HSK3 görsel promptlarına zorunlu yaş eki:**

> Preserve canonical identity but advance the family naturally from HSK1-HSK2. Zhang Wei and Liu Mei are mature adults. Yutong is a young adult and must clearly look older than Lele. Lele is a teenage boy, not a small child: taller school/teen proportions, less baby-like face, no toddler/chibi proportions, clearly male. Preserve family resemblance, continuity, modest age-appropriate clothing, warm cinematic stylized 3D CGI, 9:16, no embedded text.

Bu kilit kullanıcı açıkça değiştirmedikçe HSK3 görsel üretiminde kaldırılamaz.
