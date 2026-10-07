# Diyalog Doğallaştırma Standardı

## Amaç
300 sahnedeki mevcut diyalogları, sahne yapısını ve öğrenme hedeflerini bozmadan doğal Simplified Chinese konuşmaya dönüştürmek.

## Değişmezler
Her sahnede:
- scene ID değişmez.
- dialogue ID değişmez.
- konuşmacı ve konuşmacı sırası değişmez.
- diyalog sayısı değişmez.
- sahnenin konusu, mini-adventure olayı, problem/çözüm çizgisi ve öğrenme hedefi değişmez.
- HSK seviyesi korunur.
- replik uzunluğu mümkün olduğunca orijinalin yaklaşık ±15% bandında tutulur.
- yalnızca Simplified Chinese kullanılır.
- `zh`, `pinyin`, `tr` birlikte tutarlı tutulur.

## Doğallık kuralları
1. Replik tek başına değil, önceki ve sonraki replikle birlikte değerlendirilir.
2. Her cevap bir önceki repliğe doğal tepki, cevap, soru, onay, itiraz, açıklama veya devam niteliğinde olmalıdır.
3. Konuşma sahnenin başından sonuna kadar tek bir olay akışı gibi ilerlemelidir.
4. Aynı kalıp gereksiz yere tekrarlanmaz.
5. Ders kitabı kalıpları gerçek konuşma biçimine yaklaştırılır; ancak seviyeyi aşan argo veya aşırı yerel kullanım eklenmez.
6. `嗯、对啊、那、其实、好吧、要不、等等、我也是这么想的` gibi doğal bağlayıcılar yalnızca bağlama uygunsa kullanılır.
7. Bir replikte ortaya atılan soru veya sorun sonraki repliklerde karşılıksız bırakılmaz.
8. Konu aniden değişmez; konu geçişleri doğal bağlayıcılarla yapılır.
9. Sahne sonunda başlangıçtaki olay/sorun anlamlı biçimde kapanır veya sonraki sahneye doğal geçiş hazırlanır.
10. Karakterlerin konuşma biçimi mümkün olduğunca tutarlı kalır.

## Kalite kontrol
Bir sahne ancak aşağıdaki kontroller geçerse kabul edilir:
- aynı ID listesi
- aynı speaker listesi
- aynı turn sayısı
- Simplified Chinese
- boş zh/pinyin/tr yok
- replik uzunluğu sapma raporu
- aşırı tekrar raporu
- ardışık tamamen aynı replik yok
- doğal akış için manuel/model sahne bazlı son okuma


## Duygu ve oyunculuk metaverisi
- Gerektiğinde `emotion` alanında `neutral`, `happy`, `sad`, `playful`, `curious`, `worried`, `angry`, `comforting` değerlerinden birini kullan.
- `actionTr`, ekranda gösterilecek kısa ve gözlenebilir bir oyunculuk yönergesidir (ör. “Gülümseyerek fincanı uzatır.”). Diyalog metnine parantez içi sahne yönergesi ekleme.
- Duygu, söylenen sözle ve sahne olayıyla örtüşmeli; tek bir etiket bütün sahneye kopyalanmamalı. Nötr kalması doğal olan repliklerde alanı atla.
- `emotion` ve `actionTr` isteğe bağlıdır; anlam ve öğrenme içeriği Simplified Chinese `zh` alanında kalır.

## Konuşma balonu davranışı
- Her replik sırasında yalnızca o repliğin `speaker` alanına karşılık gelen karakterin balonu görünür.
- Küçük, boş (metin içermeyen) balon ilgili karakterin ağzının hemen yanında gösterilir; diyalog metni mevcut arayüzdeki yerinde kalır.
- Balon, aktif replik/speaker değiştiğinde aynı anda doğru karaktere geçer; önceki karakterde kalmaz ve başka karakterlerde eşzamanlı görünmez.
- Karakterin sahnedeki yüz/ağız konumu kullanılır; genel ekran konumuna sabitlenmiş balon kabul edilmez. Portre veya sahne yerleşimi değişince bağlama noktası da onunla taşınır.
- Sahne açılışı, diyaloglar arası bekleme, duraklatma ve sahneden çıkış sırasında balon görünmez. Hızlı replik geçişlerinde eski balonun kısa süre yanlış karakterde kalmaması doğrulanır.

## İş listesi ve uygulama sınırları
1. 300 sahnenin diyaloglarını sahne sahne yeniden yaz: doğal tepki zinciri, tek olay akışı, duygu ve karakter ses tutarlılığı; Simplified Chinese, mevcut HSK hedefleri.
2. Her sahnede 100 repliği, dialogue ID’leri, konuşmacı adlarını ve sırasını koru.
3. `zh`, pinyin ve Türkçe anlamı birlikte güncelle; gerektiği repliklere `emotion` ve kısa `actionTr` ekle.
4. Konuşma balonunu yalnızca aktif repliğin konuşmacısına, o karakterin ağız yanındaki sahne koordinatına bağla; sahne/replik geçişlerini test et.
5. Mevcut ses üretimi ve oynatma düzenini aynen sürdür. Sağlayıcıyı, iş akışını, dosya biçimini, kimlik eşlemesini veya ses davranışını değiştirme. `zh` değişen replikler için aynı mevcut iş akışıyla sesi yeniden üret.
6. Her grup için ID/speaker/sayı, boş alan, tekrar, HSK seviyesi ve insan tarafından sahne baştan sona okunması kontrollerini çalıştır.

Yeni bir doğallaştırma paketi uygulanmadan önce `ci/audit_dialogue_naturalization.py` çalıştırılmalıdır. Bu otomatik kontrol; 100 replik sayısını, kimlik ve konuşmacı sırasını, boş alanları, duygu etiketlerini ve sahne içi birebir tekrarları denetler. Doğal diyalog için sahne bazında editoryal son okumanın yerine geçmez.


## Güncel uygulama durumu
- [x] Kullanıcı kararı: sahne başına 100 replik; ID ve konuşmacı sırası korunacak.
- [x] Duygu/oyunculuk alanlarının aktarım sırasında korunması.
- [x] Yeni diyalog paketleri için yapısal ve tekrar denetimi.
- [ ] 300 sahnenin doğal Simplified Chinese metin, pinyin ve Türkçe anlam revizyonu.
- [ ] Her sahne görselinde karakter adıyla doğrulanmış ağız konumu kaydı. Yüzlerin soldan sağa sırasını konuşmacı sırasıyla eşlemek kimlik doğrulaması değildir.
- [ ] Derlemede kullanılan `ci/SceneStage.kt` ve `ci/MainActivity.kt` katmanında küçük boş balonun aktif dialogue ID ve speaker ile eşleşmesi.
- [ ] Görsel kırpma/ölçekleme sonrası ağız konumunun ekrana doğru dönüşümü; replik geçişi, tekrar dinletme, duraklatma, anlatıcı ve sahne çıkışı testleri.
- [ ] Değişen konuşma metinlerinin mevcut ses üretim hattıyla yeniden üretilmesi ve metin-ses eşleşmesinin dinlenerek doğrulanması.
- [ ] APK: kullanıcı onayı alındıktan sonra.

Bu aşamada boş balonun bütün sahnelerde doğru ağız konumunda gösterildiği doğrulanmış değildir. Mevcut ses üretimi/oynatımı değiştirilmemiştir.
