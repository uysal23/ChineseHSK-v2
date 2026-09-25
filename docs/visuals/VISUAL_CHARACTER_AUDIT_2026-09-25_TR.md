# Görsel–Karakter Eşleşme Denetimi — 2026-09-25

Bu denetim, mevcut APK içindeki 135 sahne görseli ile sonradan üretilen HSK3 SC011–SC050 görsellerini; sahne `production.characters` listesi ve ana karakter görsel kimlikleriyle karşılaştırmak için yapıldı.

## Sabit ana karakter kuralları

- 张伟 / Zhang Wei: yetişkin erkek, siyah dikdörtgen gözlük, koyu lacivert/mavi dış katman.
- 刘梅 / Liu Mei: yetişkin kadın, koyu saç, krem/bej dış katman, muted yeşil üst.
- 张雨桐 / Yutong: büyük çocuk; HSK1–2'de ergen/genç kız, lilac/pembe vurgu.
- 张乐乐 / Lele: küçük çocuk; HSK1–2'de erkek çocuk, kısa dağınık koyu saç, mavi/yeşil vurgu.
- 爷爷: yaşlı erkek.
- 奶奶: yaşlı kadın.

## Denetim sonucu

### Kritik sistemik bulgu
Eski HSK1–HSK2 görsel setinin önemli bir bölümünde Lele'nin erkek çocuk kimliği korunmamış; küçük kız olarak çizildiği veya sahneye beklenmeyen başka çocukların eklendiği örnekler var. Bu nedenle bu iki seviyenin eski görselleri “cast-safe” kabul edilmemelidir.

### HSK1 yüksek güvenli eşleşme sorunları
Özellikle şu sahnelerde Lele'nin cinsiyet/yaş tiplemesi veya aile kadrosu açık biçimde sorunlu görünüyor:
SC001–SC008, SC011–SC018, SC020, SC028, SC030, SC037–SC039, SC042, SC045–SC046, SC049.

### HSK2 yüksek güvenli eşleşme sorunları
Özellikle şu sahnelerde aynı tür sorun görüldü:
SC001, SC004, SC008, SC011, SC016–SC017, SC020, SC026–SC027, SC030, SC037, SC040–SC043, SC047–SC050.

### HSK3 son üretilen set
SC031–SC050 setinde ana karakterlerin cinsiyet/yaş kimliği genel olarak çok daha tutarlı. Ancak aşağıdaki sahnelerde beklenmeyen ek aile bireyleri veya bağlam dışı kişiler var:
SC041, SC042, SC043, SC046, SC048.

Ayrıca daha önce bilinen bağlam/continuity sorunları:
- SC012: canonical kadro dışında köpek.
- SC019: canonical olmayan okunabilir “Sunrise Café” tabelası.
- SC028: otel varışı yerine istasyon vurgusu.
- SC029: beklenmeyen ek genç erkek.
- SC030: iş sunumu bağlamı güçlü ancak sahne kadrosu ile görseldeki kişiler bire bir eşleşmiyor.

### HSK4–HSK6
Mevcut sınırlı görsellerde ana yetişkin cinsiyetleri büyük ölçüde doğru; fakat bazı aile sahnelerinde beklenmeyen çocuk/yan karakter eklemeleri görülüyor. Bu seviyelerde hikâye yaş ilerlemesi nedeniyle yaş değerlendirmesi HSK1–2 kadar katı yapılmamalıdır.

## Bundan sonraki üretim kuralı

Her sahne görseli üretilmeden önce sırasıyla:
1. `production.characters`
2. canonical character bible
3. HSK seviyesine göre yaş görünümü
4. sahne amacı / locationId
5. kompozisyonda yalnızca gerekli karakterler

kilitlenecek.

Yutong/Lele kuralı özellikle bloklayıcıdır:
- Yutong = büyük kız
- Lele = küçük erkek çocuk (HSK1–2)

Beklenmeyen aile bireyi sahneye eklenmemelidir.
