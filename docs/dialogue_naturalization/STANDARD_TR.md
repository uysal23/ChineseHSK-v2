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
