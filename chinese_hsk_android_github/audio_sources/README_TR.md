# Ses Kaynakları

Bu klasör APK'ya girecek ham seslerin üretim/teslim alanıdır. Uygulama kaynak klasörünü doğrudan kullanmaz; GitHub Actions `ffmpeg` ile kaynakları optimize edilmiş Opus dosyalarına dönüştürür.

- `dialogues/<DIALOGUE_ID>.wav`: karakter repliği
- `narrator/<SCENE_ID>.wav`: sahne giriş anlatıcısı
- `ambience/<LOCATION_ID>.wav`: tekrar kullanılabilir mekân ambiyansı
- `music/<SCENE_ID>.wav`: isteğe bağlı sahne müziği

Ses kaynağı bulunmazsa APK derlemesi başarısız olmaz. Replik ve anlatıcı için uygulama offline Mandarin TTS fallback kullanır; ambience/müzik eksikse sessiz devam eder.

Önerilen üretim masterı: WAV/PCM. Build aşamasında konuşmalar 24 kHz mono 48 kbps Opus, ambience 48 kHz stereo 64 kbps Opus, müzik 48 kHz stereo 96 kbps Opus olarak paketlenir.
