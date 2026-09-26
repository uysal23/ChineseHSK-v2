# HSK Görsel Üretim Manifestosu — LOCKED_V2

Bu belge HSK1–HSK6 sahne görselleri için kilitli üretim ve GitHub entegrasyon kuralıdır.

1. Her görselden önce ilgili sahnenin GitHub'daki kesin diyalog kaynağı okunur; tahminle sahne üretilmez.
2. Diyalogdan konuşan karakterler, sahnede bulunması gereken ek karakterler, mekan, ana eylem, kritik objeler ve duygu çıkarılır.
3. Diyalogda konuşan her kişi final görselde görünür; konuşan kişi sayısı ve kimlikleri kaynak diyalogla eşleşir.
4. Çocuk, abla, anne, baba, dede, babaanne ve yardımcı kişi rolleri karıştırılmaz; yaş ve rol tutarlılığı korunur.
5. Canonical karakter kimlikleri tüm sahnelerde korunur: yüz, saç, yaş algısı, beden oranı ve temel stil süreklidir.
6. Bir önceki ve bir sonraki sahnenin mekan, kıyafet, zaman ve hikaye sürekliliği kontrol edilir.
7. Ana stil sıcak sinematik 3D/2.5D CGI'dır.
8. Ana sahne görselleri 9:16 dikey mobil formattadır.
9. Görseller metinsizdir; altyazı, konuşma balonu, okunur tabela, logo ve UI görselin içine gömülmez.
10. Kolaj, split-screen ve çoklu panel yasaktır; tek sahne ve tek zaman anı kullanılır.
11. Mini etek, cinselleştirilmiş veya yaşa uygunsuz kıyafet yasaktır.
12. Kritik objeler diyalogla uyumlu ve görünür olmalıdır.
13. Mekan diyalogla doğrudan uyumlu olmalıdır; estetik uğruna yanlış mekan seçilmez.
14. Yüz ifadeleri ve beden dili sahnedeki konuşma ve duyguya uygun olmalıdır.
15. Bozuk el/parmak, yanlış uzuv, eriyen nesne, bozuk perspektif veya fiziksel olarak anlamsız poz final sayılmaz.
16. Görsel güvenli, aile dostu ve öğrenme uygulamasına uygun olmalıdır.
17. Sahneye özel final görsel ortak location background yerine `media/scenes/<sceneId>.webp` olarak tutulur; böylece aynı lokasyonu kullanan başka sahneler etkilenmez.
18. Her final görsel için `visual_sources/scenes/<sceneId>.meta.json` oluşturulur. Metadata; kaynak diyalogu, konuşanları, gerekli karakterleri, kritik objeleri ve manifesto kontrol sonucunu kaydeder.
19. `chinese_hsk_android_github/` otoritatif çalışma alanıdır. Yeni çalışma ZIP veya `ci/runtime_visuals` üzerinde elle yapılmaz. Senkron iş akışı legacy build ZIP'ini ve runtime görsel aynalarını otomatik yeniler.
20. Görseller ardışık 10 sahnelik paketler halinde ilerler.
21. Her 10 sahnelik paket için görseller ilgili `media/scenes/` konumuna yerleştirilir ve metadata tamamlanır.
22. Kaynak değişikliklerinin GitHub'a gönderilmesi APK build başlatmaz; yalnızca doğrulama ve senkronizasyon yapılır.
23. Paket 10/10 tamamlanınca `visual_batch_status.json` durumu `READY_FOR_BUILD` yapılır ve kullanıcıdan açık GitHub build onayı istenir.
24. Kullanıcı build onayı verilmeden `ci/build_trigger.txt` değiştirilmez ve APK build tetiklenmez.
25. Mevcut v3.4 build zinciri korunur. Kaynak sahne görselleri senkron iş akışıyla `ci/runtime_visuals` içine aynalanır; böylece aynı sceneId için kaynak görsel build sırasında son otorite olur.
26. Manifestoya uymayan görsel final sayılmaz, uygulamaya bağlanmaz ve build-ready pakete dahil edilmez.

## GitHub patch protokolü

Her sahne için minimum değişiklik seti: `media/scenes/<sceneId>.webp` + `visual_sources/scenes/<sceneId>.meta.json` + `visual_batch_status.json`. 10 sahnelik paket tamamlandığında doğrulama PASS olmadan build onayı istenmez.
27. Üretilen her görsel, GitHub'a veya uygulama assetlerine eklenmeden önce görsel olarak tekrar kontrol edilir. Diyalog/karakter/mekan/obje/stil/metinsizlik/9:16/giyim/süreklilik maddelerinden herhangi biri bozuksa görsel otomatik olarak REDDEDİLİR; final sayılmaz, sahneye bağlanmaz, batch tamamlanmış kabul edilmez ve yeniden üretilir.

## 28. Kilitli Aile Görsel Kimlik Tablosu

Aşağıdaki tablo çekirdek ailenin HSK1-HSK6 boyunca değiştirilemez görsel kimlik ve yaş-gelişim referansıdır. Tüm sahne görselleri bu tabloya uymak zorundadır.

| Karakter ID | Ad | Aile Rolü | Cinsiyet | HSK1-HSK2 | HSK3-HSK4 | HSK5-HSK6 | Değişmez Kimlik Kuralı |
|---|---|---|---|---|---|---|---|
| CHR_ZH_ZHANGWEI_001 | 张伟 / Zhang Wei | Baba | Erkek | Yetişkin baba | Daha olgun yetişkin | Olgun yetişkin | Aynı yüz/saç/temel beden oranı; baba rolü değişmez |
| CHR_ZH_LIUMEI_001 | 刘梅 / Liu Mei | Anne | Kadın | Yetişkin anne | Daha olgun yetişkin | Olgun yetişkin | Aynı yüz/saç/temel beden oranı; anne rolü değişmez |
| CHR_ZH_ZHANGYUTONG_001 | 张雨桐 / Zhang Yutong | Abla / büyük çocuk | Kız | Ergen kız | Genç yetişkinliğe geçiş | Yetişkin genç kadın | Her zaman Lele'den büyük; kız kimliği değişmez |
| CHR_ZH_ZHANGLELE_001 | 张乐乐 / Zhang Lele | Küçük çocuk / oğul | **Erkek** | **Küçük erkek çocuk** | Ergen erkek | Genç yetişkin erkek | **Kesinlikle kız olarak üretilemez**; kısa dağınık koyu saç ve mavi/yeşil temel renk dili korunur |
| CHR_ZH_MIMI_001 | 咪咪 / Mimi | Evcil hayvan | — | Kedi | Kedi | Kedi | Ailenin aynı kedisi olarak korunur |

### 28.1 Yaş ve oran sürekliliği kilidi

- Karakterler HSK1'den HSK6'ya doğru kademeli yaş alır; bir seviyeden diğerine ani yaş sıçraması yapılamaz.
- Zhang Yutong her zaman Zhang Lele'den daha büyük görünür. Kardeşlerin yaş sırası hiçbir seviyede değişmez.
- Lele'nin çocuk → ergen → genç yetişkin gelişimi erkek kimliğiyle devam eder.
- Yutong'un ergen kız → genç yetişkin → yetişkin kadın gelişimi aynı yüz kimliği korunarak devam eder.
- Anne ve baba da zaman içinde doğal biçimde olgunlaşır; yüz kimlikleri ve ebeveyn rolleri değişmez.
- Aynı seviyede komşu sahneler arasında boy, yüz, saç ve beden oranı sıçraması yapılamaz.
- Kıyafet değişebilir; ancak yaş/cinsiyet/rol/kimlik ve aile içi oran ilişkileri değişemez.
- Bir karakterin canonical kimliği başka bir aile üyesi veya yardımcı karakterle karıştırılırsa görsel REDDEDİLİR.

## 29. Tek Kaynak Manifesto Kilidi

Bu dosya, **HSK1-HSK6 tüm sahne görselleri için tek kural otoritesidir**.

- Üretim promptları, scene analysis dosyaları, metadata ve otomatik doğrulama kuralları bu manifestodan türetilmiş yardımcı kayıtlardır; manifestonun yerine geçemez.
- Bir yardımcı dosya ile bu manifesto çelişirse **bu manifesto geçerlidir**.
- Yeni bir görsel üretilmeden önce diyalog GitHub'dan okunur ve ardından bu manifestonun tamamı uygulanır.
- Görsel üretim sonrası QA da yine bu manifestoya göre yapılır.
- Manifestoya uymayan görsel uygulamaya, GitHub final asset klasörüne veya build paketine alınamaz.

