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

## R1 sıralı yürütme — 2026-10-07
Kullanıcı bütün 300 sahnenin HSK1 SC001 → HSK6 SC050 sırasıyla, sahne/paket başına yeniden onay beklenmeden işlenmesini istedi. Tamamlanan paketler main'e uygulanır. APK için ayrı kullanıcı onayı gerekir.

Metin revizyonu: HSK1 SC001–SC003 ve HSK4 SC001 (4/300). İlk iki HSK1 sahnesinin mevcut Kokoro ses hattı çalışıyor: https://github.com/uysal23/ChineseHSK-v2/actions/runs/37644418289 . Bu iş SC003'ün yeni metnini içermez; sonraki ses paketinde üretilmelidir. Ses üretimi bitişi, uygulamaya entegrasyon ve dinleme kontrolü ayrı aşamalardır.

Adla ve görsel SHA256 ile bağlı ağız manifesti: HSK1 SC001–SC003 (3/300). SC002/SC003 Lele erkek çocuk kimliği ve Zhang Wei gözlük sürekliliği SC001 referansıyla düzeltildi. Kadın istasyon görevlisine hitap SC003'te 阿姨 olarak eşlendi.

Derlemede kullanılan ci/SceneStage.kt artık küçük boş balonu gösterir; altyazı alt panelde kalır. Balon sadece aktif ses/replik kimliği eşleşirken görünür. Aynı görsel için doğrulanmış ağız noktası yoksa kimlik tahmini yapılmaz. Kırpma dönüşümü kaynak görsel koordinatından hesaplanır. Eski oynatım geri çağrısının yeni repliği etkilemesi nesil sayacıyla önlenir. Diğer 297 sahne kalibrasyon bekler. Android derleme ve cihazda zamanlama testi henüz yapılmamıştır; kaynak kontrolleri geçti. Ses motoru, üretim betiği, ses kastı ve oynatıcı sınıfı değiştirilmedi.

SC004 güncellemesi: metin revizyonu 5/300, adla ağız kalibrasyonu 4/300 (18 konuşmacı). HSK1 ses sentezi tamamlandı fakat eski find/head doğrulama zinciri Broken pipe hatası verdi; ses motoru değişmeden bu denetim düzeltildi ve yeniden üretim gerekir. Kullanıcı 30 dakikada bir otomatik arka plan devamını açıkça onayladı; ChineseHSK 300 sahneyi sırayla tamamla otomasyonu ACTIVE. Sıradaki metin sahnesi HSK1 SC005. APK onayı bekleniyor.


SC005 güncellemesi: 6/300 metin revizyonu, 5/300 görselde adla ağız kalibrasyonu. Lele’nin oyuncak treni koltuk altında bulunur; SC004 kahvaltı ve SC006 pencere sahnesi arasında süreklilik korunur. İlk dört HSK1 sahnesinin ses üretimi 37649172754 başarıyla bitti; 400/400 metin/konuşmacı/kast/hash ve Opus başlık eşleşmesi geçti. Dinleme ve gerçek uygulama entegrasyonu bekliyor. APK başlatılmadı. Sıradaki: HSK1 SC006.


SC006 güncellemesi: 7/300 metin revizyonu, 6/300 görselde adla ağız kalibrasyonu. Şehir ilk görüş, eski arkadaşları özleme ve aile desteği doğal tepki zinciriyle yazıldı; SC005 oyuncak ve SC007 istasyon sürekliliği korundu. SC005 ses işi 37680079039 çalışmaya devam ediyor, SC006 ses metni sonraki mevcut hat paketinde üretilecek. Cihazda balon zamanlaması/dinleme henüz doğrulanmadı. APK başlatılmadı. Sıradaki: HSK1 SC007.


SC007 güncellemesi: 8/300 metin revizyonu, 7/300 görselde adla ağız kalibrasyonu. İstasyon/nakliye telefon konuşması, gecikme, adres gönderme ve ailece taksi planı doğal tepki zinciriyle yazıldı. SC008 Li Chen karşılaşması ve SC009 adres sorunu önceden çözülmedi. SC007 ana kadrosu yalnızca production.characters içindeki dört kişidir. SC005 ses işi 37680079039 çalışıyor; SC006–SC007 sonraki mevcut hat paketinde üretilecek. Cihazda balon zamanlaması/dinleme henüz doğrulanmadı. APK başlatılmadı. Sıradaki: HSK1 SC008.


SC007 R2 kast düzeltmesi: CHARACTER_CAST_LOCK_TR, sahne kadrosu dışında aile üyesi eklenmesini bloklar. Önceki görselde eklenmiş Yutong kaldırıldı; app/runtime WebP, metadata ve görsele bağlı dört adlandırılmış ağız yeniden hash eşleşmesiyle doğrulandı. Diyalog metni/ID ve ses düzeni değiştirilmedi. SC008 Li Chen kanonik tabanı (gözlük, kömür rengi ceket, sıcak renkli polo) incelendi; sahne işlemesi sıradadır. APK başlatılmadı.


SC008 güncellemesi: 9/300 metin revizyonu, 8/300 görselde adla ağız kalibrasyonu. Li Chen ile yardım üzerinden doğal tanışma, isim/nereli olma, yeni arkadaşlık, telefon ve taksiye geçiş yazıldı. Dört kişilik kadro ve Li Chen kanonik portresi doğrulandı; Yutong sadece ekran dışında anılır. SC005 ses işi 37680079039 halen çalışıyor; SC006–SC008 sonraki mevcut hat paketinde üretilecek. Dinleme/cihaz zamanlaması bekliyor. APK başlatılmadı. Sıradaki: HSK1 SC009.

Ses durum güncellemesi: 37680079039 başarıyla tamamlandı; HSK1 SC001–SC005 için 500/500 metin/konuşmacı/kast/hash ve Opus başlık eşleşmesi geçti. Ses uygulama entegrasyonu ve dinleme henüz tamamlanmadı. SC006–SC008 yeni metinleri mevcut Kokoro işinde 37685297985 üretiliyor; kaynak a48c00c26dbd899828fbeb2c0b8190e792b978b4. APK/yeni release başlatılmadı.



SC009 güncellemesi: 10/300 metin revizyonu, 9/300 görselde adla ağız kalibrasyonu. Taksi çıkmadan 18/80 yanlış duyma, sağ/sol harita teyidi, rahatlama ve güvenli aile yolculuğu planı yazıldı. Li Chen dört kişilik aileye eşlik ederek araca binmez; istasyonda uğurlar. Büyük bavullar nakliye firmasına teslim edilmiştir. SC010 ev/anahtar olayı sonraya bırakıldı. SC006–SC008 ses işi 37685297985 çalışıyor, SC009 bir sonraki mevcut hat paketinde üretilecek. Dinleme/cihaz zamanlaması bekliyor. APK/yeni release başlatılmadı. Sıradaki: HSK1 SC010.


SC010 güncellemesi: 11/300 metin, 10/300 adla ağız kalibrasyonu. Kapı yanlış anahtarla açılmaz; doğru uzun anahtar bulunur. Aile tepkileri, güvenli giriş, oyuncak tren ve SC011 kutu düzenleme geçişi eşleştirildi. Ses üretimi/entegrasyonu/dinleme ve cihaz zamanlaması bekliyor. APK/yeni release başlatılmadı. Sıradaki HSK1 SC011.


SC011 güncellemesi: 12/300 metin, 11/300 adla ağız kalibrasyonu. Salondaki mutfak kutuları doğru yere taşınır, kitap kutusu kalır. Yardım, hafif şaka, ağır kutu yerine yaşa uygun katkı ve SC012 ilk gece hazırlığı eşleştirildi. Ses entegrasyonu/dinleme ve cihaz zamanlaması bekliyor. APK/yeni release başlatılmadı. Sıradaki HSK1 SC012.


Ses paket birleştirme R1: İlk beş HSK1 sahnesinin 500 ses eşleştirmesi mevcut chinese_course/media/audio/generated/HSK1 ve audio_manifest.json düzeninde altı seviyeli pakete birleştirildi. 29500 diğer mapping/metadata ve ses baytları, ses kastı ve üretim formatı korunarak 30000 mapping doğrulandı. Birleşik ZIP yerelde hazır; uygulamaya kurulum ve dinleme bekliyor. Tamamlanmış ses sahnesi sayısı artırılmadı. SC006–008 işi mevcut tooling kurulum aşamasında sürüyor. Metin sırası HSK1 SC012. APK ve release başlatılmadı.


SC012 güncellemesi: 13/300 metin, 12/300 adla ağız kalibrasyonu. İlk akşam uyku hazırlığı, Mimi’nin görünmemesi, sırayla güvenli arama ve aile içi sakinleştirici tepkiler eşleştirildi. Mimi bulunmadı; SC013 mutfak keşfi korunur. Ses entegrasyonu/dinleme ve cihaz zamanlaması bekliyor. APK/yeni release başlatılmadı. Sıradaki HSK1 SC013.


SC013 güncellemesi: 14/300 metin, 13/300 adla ağız kalibrasyonu. Mimi aynı akşam mutfak dolabı yanında bulunur; endişeden rahatlamaya geçen konuşmalar, kedinin sakin yaklaşması ve ilk gece dinlenme geçişi eşleştirildi. Ses entegrasyonu/dinleme ve cihaz zamanlaması bekliyor. APK/yeni release başlatılmadı. Sıradaki HSK1 SC014.


Ses SC001–SC008: 37685297985 işi başarılı; 800 repliğin normalize metin/konuşmacı/profil/anahtar ve Opus kapsayıcı eşleşmesi doğrulandı. Altı seviyeli mevcut ses paketi biçimine kayıpsız birleştirme, diğer 29200 mapping ve dosya baytları korunarak doğrulandı. Kurulum ve dinleme beklediği için tamamlanan ses sahnesi sayısı artırılmadı. SC009–SC013 ses üretimi 37692980413 başladı; publish_release=false. Otomatik devam 10 dakika. Metin sırası SC014, APK başlatılmadı.


SC014 güncellemesi: 15/300 metin, 14/300 adla ağız kalibrasyonu. Aynı akşam komşu ziyareti, sıcak tanışma, aile/kedi konuşması ve misafiri oturtma işlendi. Komşunun adı uydurulmadı, çay/su SC015 için açık bırakıldı. Ses SC009–SC013 işi çalışıyor; SC014 sonraki üretimde bekliyor. Kurulum/dinleme/cihaz testi bekliyor. APK/yeni release başlatılmadı. Sıradaki HSK1 SC015.


Ses SC001–SC013: 37692980413 işi başarılı, kaynak c447a89ab9e68e96f62859efe1dad739bf59e00c. 1300 repliğin normalize metin, konuşmacı, ses profili, ses anahtarı ve Opus kapsayıcı eşleşmesi doğrulandı. Uygulamaya entegrasyon/dinleme/cihaz testi bekliyor, tamamlanan ses sahnesi sayısı artırılmadı. SC014 sonraki mevcut hat üretiminde bekliyor. Metin sırası SC015; APK/release başlatılmadı.

SC001–SC013 ses paket birleştirmesi: 1300 mapping yenilendi, diğer 28700 mapping ve ses baytları korundu. Mevcut altı seviyeli 30000 mapping biçimi ve Opus kontrolü geçti. Paket yerelde hazır; uygulamaya kurulum ve dinleme bekliyor. APK/release başlatılmadı.

SC015 güncellemesi: 16/300 metin, 15/300 adla ağız kalibrasyonu. Çay/su tercihi, fincan yıkama, sıcak ikram, Lele su tercihi ve komşuyla doğal karşılıklı konuşma eşleştirildi. Aynı akşam kadro ve saç/giysi devamlılığı korundu. SC016 market yol tarifi sonraya bırakıldı. Ses SC014–SC015 üretimi bekliyor; kurulum/dinleme/cihaz testi bekliyor. APK/release başlatılmadı. Sıradaki SC016.

SC014–SC015 sesleri aynı Kokoro iş akışında üretiliyor: https://github.com/uysal23/ChineseHSK-v2/actions/runs/37801632600 (kaynak b3bf50f4fdaafb0ac52df94794d0c91f9a6ab2b1). Üretim, eşleşme denetimi ve uygulama entegrasyonu tamamlanmış sayılmadı. APK ve release başlatılmadı.

SC016 güncellemesi: 17/300 metin, 16/300 adla ağız kalibrasyonu. Ertesi sabah market yönleri, güvenli cadde geçişi, dönüşte yönlerin değişmesi ve küçük rehber rolü doğal karşılıklı konuşmayla işlendi. SC017 market alışverişi sonraki sahnedir. SC014–SC015 ses işi 37801632600 sürüyor, SC016 ses üretimi bekliyor. Kurulum/dinleme/cihaz testi bekliyor. APK/release başlatılmadı.

SC017 güncellemesi: 18/300 metin, 17/300 adla ağız kalibrasyonu. İlk market alışverişi; miktar, ürün fiyatı, liste ve Lele tarafından eklenen fazla atıştırmalık doğal tepki zinciriyle işlendi. Bir paket geri bırakılır, ödeme SC018’e bırakılır. Kanonik anne topuzu ve dört ağız doğrulandı. SC014–SC015 ses işi 37801632600 sürüyor; SC016–SC017 mevcut ses üretimi bekliyor. Kurulum/dinleme/cihaz testi bekliyor. APK/release başlatılmadı.

SC018 güncellemesi: 19/300 metin, 18/300 adla ağız kalibrasyonu. SC017 ürün miktarları korundu; 9+18+6+8+4=45 yuan, 50 ödeme ve 5 para üstü kontrolü işlendi. Çanta ödeme sonrasında doldurulur, SC019 ertesi sabah kahvaltı için bırakılır. Görselde anne topuzu, alışveriş miktarları ve para düzeltildi. Ses/kurulum/dinleme/cihaz testi bekliyor. APK/release başlatılmadı.

Ses SC001–SC015: 37801632600 işi başarılı. 1500 replik normalize metin/konuşmacı/kast/profil/anahtar ve gerçek Opus kapsayıcılarıyla doğrulandı. Kaynak b3bf50f4fdaafb0ac52df94794d0c91f9a6ab2b1. Kurulum/dinleme/cihaz testi bekliyor, tamamlanan ses sahnesi sayısı artırılmadı. SC016–SC018 sonraki mevcut hat üretimi bekliyor. APK/release başlatılmadı.

SC019 güncellemesi: 20/300 metin, 19/300 adla ağız kalibrasyonu. Sakin kahvaltı, yiyecek tercihleri, sıcak çay, kardeş yardımı ve yeni eve alışma doğal karşılıklı konuşmayla işlendi. Gün saati sabaha düzeltildi; Mimi önceki gün değil taşınma günü bulunmuştur. Fotoğraf SC020’ye bırakılır. Ses/kurulum/dinleme/cihaz testi bekliyor. APK/release başlatılmadı.

SC016–SC019 sesleri aynı Kokoro iş akışında üretiliyor: https://github.com/uysal23/ChineseHSK-v2/actions/runs/37813427695 (kaynak 8ff2d98d4e0527baf4f5635289f953d57b05e967). Üretim, eşleşme denetimi ve uygulama entegrasyonu tamamlanmış sayılmadı. APK ve release başlatılmadı.

SC020 güncellemesi: 21/300 metin, 20/300 adla ağız kalibrasyonu. Aile fotoğrafı hazırlığı, Mimi yer değiştirmesi, iki deneme ve doğal aile şakaları işlendi. Kanonik dört aile rolü ve Mimi düzeltildi. Ses/entegrasyon/dinleme/cihaz testi bekliyor. APK/release başlatılmadı. Sıradaki SC021.

SC021: 22/300 metin, 21/300 adla ağız kalibrasyonu. Yanlış binaya yönelme, doğru yolu sorma, ilk gün heyecanı ve karşılıklı yardım doğal diyaloglarla işlendi. Tam dört üretim rolü düzeltildi. Sınıfa tanıtım SC022’de kalır. Ses/entegrasyon/dinleme/cihaz testi bekliyor. APK/release başlatılmadı.
