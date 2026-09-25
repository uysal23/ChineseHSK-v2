# GitHub'dan APK Alma — Teknik Bilgi Gerektirmeyen Yol

Bu proje GitHub'a yüklendikten sonra normal kullanım için kod yazmanız gerekmez.

## İlk APK

1. GitHub'da proje sayfasını açın.
2. Üst menüden **Actions** bölümüne girin.
3. Soldan **Build Personal APK** iş akışını seçin.
4. **Run workflow** düğmesine basın.
5. İşlem yeşil onay ile tamamlandığında aynı çalıştırmanın altındaki **Artifacts** bölümünü açın.
6. `ChineseHSK-personal-apk` paketini indirin.
7. Paketin içinde `ChineseHSK-vX.X.X-personal.apk` dosyası bulunur.
8. APK'yı Android telefona aktarın ve kurun.

## Otomatik build

`main` dalına yeni proje sürümü gönderildiğinde aynı APK build işlemi otomatik çalışır.

## Dosya doğrulama

Artifact içinde APK'nın yanında `.sha256.txt` dosyası da bulunur. Bu dosya APK'nın build sırasında üretilen kontrol özetidir.

## Önemli — kişisel test imzası ve güncellemeler

GitHub Secrets içinde kalıcı Android imzalama anahtarı tanımlanmamışsa workflow **debug APK** üretir. Debug APK kişisel test için uygundur; ancak farklı GitHub build'leri farklı imza kullanırsa Android mevcut uygulamanın üzerine güncelleme kurmayabilir.

Sürekli aynı uygulamanın üzerine güncelleme kurmak istediğiniz aşamada bir defaya mahsus kalıcı imzalama anahtarı ayarlanmalıdır. Workflow bunu desteklemektedir. Gerekli GitHub Secrets:

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

Bu değerler mevcut olduğunda workflow otomatik olarak imzalı **release APK** üretir. Bu anahtar kaybedilmemelidir. Play Store aşamasında ayrıca Google Play App Signing planlanmalıdır.

## Bir build hata verirse

Önce aynı Actions çalıştırmasında **validation-reports** artifact'ını indirin. İçerik doğrulama ve medya raporları burada bulunur.

Uygulamanın kendisinde de Dashboard → **Sistem Kontrolü** ekranı vardır. Offline Mandarin sesi, telaffuz tanıma, bildirim izni ve yerel ses cache'i burada görülebilir.
