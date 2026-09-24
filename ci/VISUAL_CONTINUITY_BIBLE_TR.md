# ChineseHSK-v2 Görsel Süreklilik Kılavuzu

## Canonical ana aile
- Zhang Wei: kısa koyu saç, siyah dikdörtgen gözlük, mavi/lacivert dış katman.
- Liu Mei: uzun koyu kahverengi saç, krem/bej sıcak tonlar.
- Yutong: uzun koyu saç, pembe/mor palet; HSK seviyesi ilerledikçe kontrollü yaşlandır.
- Lele: kısa koyu saç, mavi/yeşil palet; HSK seviyesi ilerledikçe kontrollü yaşlandır.
- Mimi: turuncu-beyaz tekir kedi.
- Büyükanne/Büyükbaba: HSK4+; gri saç, sıcak yüz oranları, aynı 3D/2.5D dünya.

## Değişmez final kuralları
- 9:16 tam ekran, sinematik 3D/2.5D çizgi-film.
- Ders UI'si, Pinyin/Türkçe altyazı ve konuşma balonları görsele gömülmez.
- Doğal mekân tabelaları olabilir.
- Konuşan karakterin %8–10 büyümesi ve ağız hareketi uygulama katmanında yapılır.
- Aynı karakterin yüz, saç, ten, ana kıyafet paleti ve yaş dönemi korunur.
- HSK5–6 için HSK1–3 çocuk görselleri tekrar kullanılmaz; yaşlandırılmış canonical set gerekir.

## Statüler
- FINAL_SELECTED: doğrudan sceneId'ye bağlı final asset.
- FAMILY_REFERENCE: aynı aile/stil; final eşleme veya yaş kontrolü bekliyor.
- HOLD_CAST_MISMATCH: kaliteli ama canonical yüz/yaş setine uymuyor; uygulamaya girmez.
- UI_REFERENCE_ONLY: UI tasarım referansı.
- REJECT_UNRELATED: uygulama sahnesi değil.

## Yeni sahne görseli kabul kapısı

- FINAL_SELECTED yapılmadan önce sahnenin gerçek `sceneId`, `locationId` ve `production.characters` alanları kaynak JSON'dan doğrulanır.
- Sahne görseli Android dikey kullanım standardında **9:16** hazırlanır; yatay 16:9 görseller runtime sahne görseli olarak seçilmez.
- Zhang ailesi kanonundaki sahnelere Li Wei/Elif gibi alternatif bir cast bağlanmaz; bu tür görseller yalnızca `HOLD_CAST_MISMATCH` referansı olabilir.
- Görsel, sahnenin olayını ve karakter listesini gerçekten göstermiyorsa aynı konuyu çağrıştırsa bile FINAL_SELECTED yapılamaz.
- Yeni final görsel mevcut `chinese_course/media/scenes/{sceneId}.webp` dosyasını ancak aynı sahne için açıkça daha doğru bir kanonik görselse değiştirebilir.

