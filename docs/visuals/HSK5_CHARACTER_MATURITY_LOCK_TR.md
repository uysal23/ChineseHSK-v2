# HSK5 Karakter Olgunluk ve Görsel Süreklilik Kilidi

Durum: **LOCKED**

Bu kilit HSK5 görsellerinde characters.json içindeki HSK5 portre varyantlarını ve HSK4'ten HSK5'e görünür zaman ilerlemesini esas alır.

- **张伟 / Zhang Wei:** HSK4'teki aynı yüz geometrisi, kısa dalgalı koyu saç ve siyah dikdörtgen gözlük korunur. HSK5 SENIOR varyantı uygulanır: olgun, hafif kırlaşmış ve ince yaş çizgileri olan yetişkin; yorgun veya güçsüz yaşlı görünümüne dönmez. Lacivert/mavi dış katman ve açık gömlek ana siluettir.
- **刘梅 / Liu Mei:** aynı yüz kimliği, koyu saç, krem/bej dış katman ve muted yeşil üst korunur. HSK5 SENIOR varyantı ile ölçülü yaş çizgileri ve az miktarda kırlaşma eklenir.
- **张雨桐 / Yutong:** HSK5 ADULT varyantı; üniversite çağındaki genç yetişkin kadın. Koyu saç/at kuyruğu kimliği ve sade lila/pembe palet korunur.
- **张乐乐 / Lele:** HSK5 YOUNG_ADULT varyantı; geç ergen/18 yaş ve üzeri genç erkek. Kısa dağınık koyu saç ve mavi/yeşil palet korunur; çocuk veya chibi görünümüne dönmez.
- **爷爷 / 奶奶:** HSK5 boyunca yaşlı yetişkin kimlikleri, gri saç ve sakin aile büyüğü görünümü korunur.
- **咪咪:** HSK5 OLDER_CAT varyantı kullanılır.
- Destekleyici sınıf arkadaşı, öğretmen, kafe yöneticisi/çalışanı, iş arkadaşı, müşteri ve proje üyesi sahne rolüne uygun yetişkin yaş bandında çizilir. Aynı ardışık sahnede tekrar eden destek karakterlerinin yüzü, saç/kıyafeti ve rol kimliği sabit kalır.
- **Görsel dil:** WARM_CINEMATIC_STYLIZED_3D_CGI_V1; doğal yumuşak ışık, temiz doygun renkler, yüz/anatomi ve render gerçekçiliği HSK4 SC050 ile aynı ailede kalır.
- Her görsel tek sahne, 9:16 dikey ve metinsizdir. Kolaj, split-screen, uygulama arayüzü, altyazı, konuşma balonu, logo/filigran, okunabilir yazı ve gereksiz karakter ekleme yasaktır.
- Tüm diyalog konuşmacıları kadrajda ve yüzleri görünür olur. Kadın karakter kıyafetleri yaşa uygun ve sade olur; mini etek veya cinselleştirilmiş kıyafet kullanılmaz.
- Her sahnede kaynak JSON'daki production.characters listesi kadroyu belirler. Ardışık sahneler story.previousSceneId ve story.nextSceneId alanlarına göre görsel olarak kontrol edilir; ilk HSK5 sahnesi HSK4 SC050'ye bağlanır.
- Bu karakter kilidi HSK5 görsel üretiminin tamamında geçerlidir. SC001–SC050 grupları entegre edilmiştir; HSK5 görsel seti tamamlanmıştır. APK build açık kullanıcı onayı olmadan başlatılmaz.
