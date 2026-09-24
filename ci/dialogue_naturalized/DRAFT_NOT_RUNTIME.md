# DRAFT — RUNTIME'A UYGULAMA

Bu klasördeki 300 sahnelik corpus ilk otomatik bağlam-yumuşatma denemesidir.

**FINAL değildir ve APK/runtime build'e uygulanmamalıdır.**

Neden:
- Yapısal koruma başarılı: 300 sahne / 30.000 replik / speaker sırası korunuyor.
- Ancak bazı sahnelerde hâlâ ders kitabı kalıp tekrarları ve yeterince güçlü olmayan replikler arası bağ var.
- İlk Pinyin üretim yöntemi bazı çok heceli kelimeleri istenmeyen biçimde ayırdı.

Final kabul kriteri:
- Her sahne baştan sona tek konuşma olayı olarak yeniden yazılacak.
- Her replik önceki repliğe doğal cevap/tepki/ilerletme ilişkisi kuracak.
- MiniAdventure ve öğrenme hedefleri korunacak.
- Simplified Chinese, doğru Pinyin ve uyumlu Türkçe birlikte doğrulanacak.
- Sahne ancak SCENE_COHERENCE_RULES_TR.md kriterlerini geçerse runtime'a alınacak.
