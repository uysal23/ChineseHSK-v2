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
