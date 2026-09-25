# VISUAL_CONTINUITY_LOCK_V1 — Görsel Süreklilik Kilidi

Bu dosya ChineseHSK-v2 için bloklayıcı görsel üretim kuralıdır.

## 1. Tek görsel dil
Tüm sahneler aynı stil ailesinde kalır:

**WARM_CINEMATIC_STYLIZED_3D_CGI_V1**

Temel özellikler:
- sıcak sinematik stylized 3D/CGI,
- doğal ve yumuşak ışık,
- temiz doygun renkler,
- hafif shallow depth of field,
- aynı yüz/anatomi yaklaşımı,
- aynı render gerçekçilik seviyesi,
- 9:16 runtime düzeni,
- uygulama UI'si, altyazı, Pinyin/Türkçe yazı veya görsel içine gömülü konuşma balonu yok.

Bir sahne 3D/CGI iken komşu sahne 2.5D cartoon, anime, flat illustration veya photorealistic tarza geçemez.

## 2. Üçlü süreklilik penceresi zorunlu
SC(N) üretilmeden önce mutlaka:
- SC(N-1) görseli,
- SC(N) sahne JSON'u ve diyalogları,
- SC(N+1) görseli

birlikte incelenir.

Yeni SC(N), SC(N-1) ve SC(N+1) ile aynı hikâyenin ardışık karesi gibi görünmelidir.

İlk sahnede sonraki iki sahne; son sahnede önceki iki sahne referans alınır.

## 3. Karakter kimliği bloklayıcıdır
Sahne JSON'undaki `production.characters` ana kaynaktır.

Ana aile:
- 张伟 / Zhang Wei = yetişkin erkek/baba, siyah dikdörtgen gözlük.
- 刘梅 / Liu Mei = yetişkin kadın/anne.
- 张雨桐 / Yutong = büyük çocuk, kız; HSK1–2'de ergen/genç kız.
- 张乐乐 / Lele = küçük çocuk, erkek; HSK1–2'de belirgin biçimde Yutong'dan küçük.
- 爷爷 = yaşlı erkek.
- 奶奶 = yaşlı kadın.

Cinsiyet, yaş grubu, yüz kimliği ve aile rolü değiştirilemez.
Sahnede olmayan aile bireyi veya çocuk rastgele eklenemez.

## 4. Ardışık sahne bütünlüğü
Komşu sahnelerde aynı karakter için mümkün olduğunca şu unsurlar korunur:
- yüz ve saç kimliği,
- yaş görünümü,
- vücut oranları,
- kıyafet ailesi / renk mantığı,
- mekân mimarisi,
- kafe/ev/ofis gibi tekrar kullanılan locationId kimliği,
- ışık ve renk grading'i,
- kamera/render dili.

Senaryo açıkça zaman veya mekân değişikliği gerektiriyorsa yalnızca gerekli unsurlar değişir; stil ailesi değişmez.

## 5. Final kabul kapısı
Bir görsel ancak şu beş kontrol geçerse FINAL olabilir:
1. Diyalog ve olay bağlamı doğru.
2. Cinsiyet ve yaş grupları doğru.
3. production.characters ile kadro uyumlu.
4. SC(N-1) ve SC(N+1) ile stil/karakter/mekân sürekliliği uyumlu.
5. WARM_CINEMATIC_STYLIZED_3D_CGI_V1 stil ailesi korunmuş.

Bu kontrollerden biri başarısızsa görsel uygulamaya alınmaz; yeniden üretilir.

## 6. HSK1 SC001 özel final kuralı
SC001 kadrosu:
张伟, 刘梅, 张雨桐, 张乐乐, 王师傅.

SC001:
- Yutong'u büyük kız,
- Lele'yi küçük erkek çocuk
olarak göstermelidir.
Görsel sunum düzeni ve render dili SC002 ile aynı aileden olmalıdır.

Bu kilit kaldırılmadıkça hiçbir sonraki görsel üretiminde bu kurallardan taviz verilemez.
