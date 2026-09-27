# Character Cast Lock — Görsel Üretim Kuralları

Yeni sahne görsellerinde karakter seçimi tahmine bırakılmaz.

## Ana aile
- 张伟 / Zhang Wei — erkek yetişkin; kısa koyu saç; siyah dikdörtgen gözlük; lacivert/mavi dış katman; açık mavi gömlek.
- 刘梅 / Liu Mei — kadın yetişkin; uzun koyu saç; krem/bej dış katman; muted yeşil üst.
- 张雨桐 / Yutong — kız; HSK1–2 ergen/genç; koyu at kuyruğu; lilac/pembe.
- 张乐乐 / Lele — erkek; HSK1–2 küçük çocuk; kısa dağınık koyu saç; mavi/yeşil.
- 爷爷 — yaşlı erkek.
- 奶奶 — yaşlı kadın.
- 咪咪 — turuncu-beyaz tekir kedi.

## Zorunlu üretim sırası
1. Sahne JSON'dan `production.characters` okunur.
2. Yalnızca bu karakterler ana kadro olarak prompt'a girer.
3. Her isim için cinsiyet + yaş bandı + canonical kıyafet/saç kilitlenir.
4. HSK seviyesine göre yaş ilerlemesi uygulanır.
5. Prompt'a “do not add extra family members or children” kuralı eklenir.
6. 9:16 portre, UI/yazı/altyazı/konuşma balonu yok.
7. Görsel uygulamaya alınmadan önce visual-cast audit yapılır.

## Bloklayıcı hata örnekleri
- Lele'nin kız olarak çizilmesi.
- Yutong'un küçük çocuk olarak çizilmesi.
- Sahne kadrosunda olmayan Yutong/Lele'nin eklenmesi.
- Anne/baba yerine genç öğrenci görünümü kullanılması.
- Büyükbaba/büyükanne rollerinin genç yetişkin olarak çizilmesi.

## HSK3 yaş / olgunluk patch'i — LOCKED

HSK3–HSK4 için yaş bantları `visual_generation_policy.json` ile bloklayıcı olarak uygulanır:

- Zhang Wei: `mature_adult`
- Liu Mei: `mature_adult`
- Yutong: `young_adult`
- Lele: `teen_boy`

Yutong her zaman Lele'den daha büyük/olgun görünmelidir.

**Lele HSK3'te küçük çocuk olarak çizilemez.** Toddler, okul öncesi, aşırı bebeksi veya chibi oran; HSK1–HSK2 küçük çocuk görünümünün aynen tekrar edilmesi; kız/belirsiz cinsiyet görünümü bloklayıcı manifest hatasıdır ve görsel FINAL olamaz.

Ayrıntılı kilit: `docs/visuals/HSK3_CHARACTER_MATURITY_LOCK_TR.md`

