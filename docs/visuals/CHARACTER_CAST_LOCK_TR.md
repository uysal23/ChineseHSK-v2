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
