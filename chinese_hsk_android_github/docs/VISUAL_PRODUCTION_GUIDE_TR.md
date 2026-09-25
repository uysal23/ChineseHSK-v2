# Görsel Üretim Kılavuzu — v1.3.0

Bu proje, aynı karakteri veya mekânı her sahnede yeniden tasarlamaz. Ana kural: **bir kez kimlik ver, varyant üret, tekrar kullan**.

## Stil
- Warm Semi-Realistic Visual Novel.
- Güncel, gündelik Çin yaşamı; ne karikatürize ne de aşırı anime.
- Karakterler ayrı şeffaf WebP katmanlarıdır; arka planlara karakter gömülmez.
- Runtime karakter hedefi: 768×1152, şeffaf WebP.
- Runtime arka plan hedefi: 1280×720, WebP.
- Büyük master dosyaları daha yüksek çözünürlükte üretilebilir; APK için optimize edilir.

## Kimlik kilidi
Karakter yaşlansa veya kıyafet değiştirse de yüz kimliği korunur: yüz formu, göz/kaş yapısı, burun, saç çizgisi ve genel siluet birdenbire değişmez.

`media/visual_bible.json` ana kimlikleri içerir. `media/prompts/characters/` klasöründe karakter üretim promptları, `media/prompts/locations/` klasöründe mekân promptları bulunur.

## İlk üretilecek karakterler
1. 张伟 / Zhang Wei
2. 刘梅 / Liu Mei
3. 张雨桐 / Zhang Yutong
4. 张乐乐 / Zhang Lele
5. 咪咪 / Mimi
6. 李晨 / Li Chen
7. 李晨妻子 / Li Chen'in eşi
8. 爷爷 / büyükbaba
9. 奶奶 / büyükanne

## İlk üretilecek mekânlar
Yeni ev, aile kafesi, Zhang'ın iş yeri, lise, ilkokul, Li Chen'in evi, park, topluluk merkezi, büyükanne-büyükbaba evi, çiftlik, üniversite, hastane, yeni kasaba istasyonu, tren ve kasaba merkezi.

## Varyant kuralı
- Karakter: `base.webp`, sonra yaş/kıyafet/ifade varyantları.
- Mekân: önce `_DAY.webp`; sonra yalnızca gerekiyorsa `_NIGHT`, `_RAIN`, `_HOLIDAY`.
- Mimari ve ana mobilyalar varyantlar arasında yer değiştirmez.

## Eksik medya davranışı
Gerçek binary görsel yoksa uygulama Compose fallback kullanmaya devam eder. Bu yüzden görsel üretimi kademeli yapılabilir; uygulama bozulmaz.
