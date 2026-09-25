# Kalıcı APK İmzası

Kişisel test döneminde debug APK yeterlidir. Aynı APK'yı telefonda veri kaybetmeden sürüm sürüm güncellemek için kalıcı bir signing key kullanmak daha doğrudur.

Proje signing key'i repoya koymaz. Bu bilinçli bir güvenlik kararıdır.

GitHub Actions dört Secret tanımlandığında release imzasını otomatik kullanır:

- ANDROID_KEYSTORE_BASE64
- ANDROID_KEYSTORE_PASSWORD
- ANDROID_KEY_ALIAS
- ANDROID_KEY_PASSWORD

Bu bilgiler yoksa build otomatik olarak debug APK'ya döner.

Ticarileştirme aşamasında kişisel/test anahtarı yerine ayrı release süreci ve Google Play App Signing kullanılmalıdır.
