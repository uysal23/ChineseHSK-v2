# Native Mandarin Nihai Dil QA — 2026-10-01

## Kapsam

- HSK1–HSK6
- 300/300 sahne
- 30.000/30.000 diyalog repliği
- Kontroller: exact tekrar, sahne içi kalıp tekrarları, slot/template üretim izleri, bağlama uygunluk, ifade doğallığı, HSK seviyesine göre konuşma yapısı
- Otomatik corpus taraması + temsilî sahnelerde doğrudan dilsel inceleme

## Sonuç

**GENEL DURUM: NEEDS_REVISION — native Mandarin final release QA PASS değil.**

| Seviye | PASS | WARN | FAIL | Temel sorun |
|---|---:|---:|---:|---|
| HSK1 | 0 | 0 | 50 | Çok yüksek exact tekrar; diyaloglar alıştırma kalıbı gibi dönüyor |
| HSK2 | 0 | 0 | 50 | Aynı 64 cümlelik/benzer scaffold birçok sahnede tekrar ediyor |
| HSK3 | 43 | 7 | 0 | Büyük ölçüde kullanılabilir; bazı tekrarlı generic cevap blokları var |
| HSK4 | 0 | 1 | 49 | Konuya isim yerleştirilmiş tartışma şablonları çok yoğun |
| HSK5 | 0 | 0 | 50 | Analitik şablonlar ve semantik olarak doğal olmayan slot birleşimleri |
| HSK6 | 0 | 50 | 0 | Exact tekrar yok fakat aynı akademik söylem şablonu 50 sahnede tekrar ediyor |

Toplam:
- PASS: 43
- WARN: 58
- FAIL: 199

## Sayısal bulgular

- HSK1 exact duplicate satır: 2.793 / 5.000
- HSK2 exact duplicate satır: 1.805 / 5.000
- HSK3 exact duplicate satır: 457 / 5.000
- HSK4 exact duplicate satır: 542 / 5.000
- HSK5 exact duplicate satır: 804 / 5.000
- HSK6 exact duplicate satır: 0 / 5.000

Generic/template eşleşmeleri:
- HSK1: 0
- HSK2: 4
- HSK3: 300
- HSK4: 1.340
- HSK5: 1.477
- HSK6: 800

## Temsilî sorun örnekleri

### HSK1
SC001 içinde:
- “我明白了。” 9 kez
- “谢谢。” 9 kez
- aynı “这是X吗？ / 对，这是X。 / X在哪儿？ / X在这里。” döngüsü tekrar ediyor

SC024 içinde:
- “我也是。” 14 kez
- “你好！” 13 kez
- “很高兴认识你。” 13 kez

Bu düzeyde öğretici tekrar normaldir; ancak oran gerçek sohbet doğallığını bozacak kadar yüksektir.

### HSK2
Birçok sahnede aynı generic blok tekrar ediyor:
- “今天事情不少。”
- “我们先看看最重要的。”
- “好，慢慢来。”
- “我明白了。”
- “原来是这样。”
- “这个我记住了。”
- “听起来很清楚。”
- “好，那就按这个来。”

Konu değişse de konuşma omurgasının değişmemesi native diyalog hissini azaltıyor.

### HSK3
Genel yapı en iyi durumda. Ancak bazı sahnelerde:
- “我明白你的意思了。”
- “好，这一点我会注意。”
gibi cevaplar üçer kez dönüyor.

HSK3 önce hedefli polishing ile tamamlanabilir.

### HSK4
Konu kelimeleri sabit bir tartışma şablonuna yerleştiriliyor:
- “关于X，我想再听听大家的看法。”
- “X是我们不能忽略的一点。”
- “我们把X也列进考虑范围吧。”
- “如果X发生变化，计划也得调整。”

Bu kalıplar tek tek dilbilgisel olsa bile 50 sahne boyunca aynı yapıda kullanıldığında konuşma doğal değildir.

### HSK5
HSK4 sorunu daha da belirgin. Ayrıca semantik olarak doğal olmayan slot birleşimleri bulundu:
- “如果调整状态发生变化，计划也得调整。”
- “如果优势发生变化，计划也得调整。”
- “如果自我评价发生变化，计划也得调整。”

Bu cümleler native konuşmada bu şekilde kurulmaz; bağlama göre yeniden yazılmalıdır.

### HSK6
Exact duplicate yok, ancak aynı soyut/akademik template her sahnede farklı isimlerle tekrar ediyor:
- “谈到X，我更关心的是它背后的意义，而不只是表面的结果。”
- “X之所以重要，是因为它会影响我们接下来怎么理解这件事。”
- “如果忽略X，很多看似合理的判断其实会失去依据。”
- “我想把X放回具体语境里看，这样更容易理解彼此的选择。”

HSK6'nın dili daha ileri olabilir, fakat aile/iş/günlük yaşam sahnelerinin tamamının akademik panel tartışması gibi konuşması doğal değildir.

## Düzeltme politikası

1. Sahne başlığı, miniAdventure, karakterler, öğrenme hedefleri ve hikâye continuity korunacak.
2. Her sahne yaklaşık 100 replik yapısını koruyabilir; ancak gereksiz tekrar kaldırılacak.
3. HSK kelime/gramer hedefleri doğal konuşmanın içine dağıtılacak; “drill” hissi azaltılacak.
4. Karakterlerin yaşına, ilişkisine ve rolüne uygun register kullanılacak.
5. Aynı generic cevap blokları sahneler arasında kopyalanmayacak.
6. Pinyin ve Türkçe çeviri, Çince düzeltildikten sonra satır satır yeniden eşlenecek.
7. VoiceProfile/ID, sahne ID ve dialogue ID'ler mümkün olduğunca korunacak.
8. Her düzeltilmiş batch yeniden native-Mandarin QA gate'inden geçirilecek.

## Öncelik

Önerilen düzeltme sırası:
HSK1 -> HSK2 -> HSK4 -> HSK5 -> HSK6 -> HSK3 polishing.

Görseller tamam olsa bile bu QA açıkları giderilmeden “commercial/native editorial final PASS” verilmemelidir.
