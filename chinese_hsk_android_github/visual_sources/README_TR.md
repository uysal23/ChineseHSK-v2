# Görsel Kaynak Drop Alanı

Bu klasör, üretilen yüksek kaliteli karakter ve mekân görsellerinin kaynak alanıdır. Normal kullanıcı bu klasörle uğraşmaz.

- `scripts/build_visual_asset_queue.py` gerekli dosya adlarını üretir.
- `visual_asset_queue.csv` hangi görselin hangi hedefe gideceğini gösterir.
- Karakter kaynakları PNG ve şeffaf arka planlı olmalıdır.
- Mekân kaynakları PNG/JPG/WebP olabilir; derleme sırasında 1280×720 WebP'ye dönüştürülür.
- `scripts/prepare_visual_assets.py` kaynakları optimize ederek `app/src/main/assets/chinese_course/media/...` altına taşır.
- Kaynak görsel yoksa uygulama Compose fallback kullanmaya devam eder; build kırılmaz.

Amaç: görsel üretimi ile Android kodunu birbirinden ayırmak ve yeni görseller geldiğinde kod değiştirmeden APK'ya dahil etmektir.
