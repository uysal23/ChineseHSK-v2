## 1.9.0
- Günlük offline çalışma hatırlatıcısı eklendi; saat/dakika ayarı Ayarlar ekranından yapılır.
- Android 13+ POST_NOTIFICATIONS izni yalnızca hatırlatıcı açılırken istenir.
- WorkManager 2.11.2 ile exact-alarm izni gerektirmeyen günlük yeniden zamanlama eklendi.
- Günlük çalışma serisi (current streak), en uzun seri ve son 28 günlük yerel çalışma takvimi eklendi.
- Kelime sınavı hatalarından ve manuel "Zor" işaretinden otomatik Zayıf Kelimeler havuzu oluşturulur.
- Zayıf kelimeler öncelik puanına göre ayrı ekranda tekrar çalışılabilir.
- Günlük tekrar kuyruğu artık önce zayıf kelimeleri, sonra favorileri, ardından son sahne kelimelerini getirir.
- Flash-card ekranına "Zor İşaretle" seçeneği eklendi.
- Yedek sistemi yeni seri, hatırlatıcı ve zayıf-kelime verilerini otomatik olarak içerir.
- App-flow validator yeni hatırlatıcı, seri/takvim ve zayıf-kelime özelliklerini zorunlu olarak kontrol eder.
- versionName 1.9.0 / versionCode 19 yapıldı.

## 1.7.0

- Added first-run onboarding: Start from Zero or Placement Test.
- Added offline 12-question HSK placement test and persistent starting-level result.
- Added main dashboard with Continue, HSK levels, Favorites, Daily Review and placement retest.
- Placement may unlock the first scene of the recommended level, while all subsequent scenes remain mastery-gated.
- Added persistent last-scene resume behavior.
- Added daily review deck from favorites and the most recently studied scene.

# v1.5.0

- Added deterministic audio production queue derived from the canonical 300-scene course.
- Added 30,000 dialogue audio targets, 63 reusable ambience targets and 300 optional scene-music targets.
- Added `audio_sources/` master-audio drop area and human-readable CSV worklist.
- Added ffmpeg-based authored-audio preparation to Opus runtime assets.
- Added ffprobe validation for codec, sample rate and channel count.
- Added media-readiness JSON/text reports that separate authored binaries from fallbacks.
- GitHub Actions now builds/validates both visual and audio media pipelines before strict content validation and APK build.
- Missing dialogue/narrator authored audio continues to use offline Mandarin TTS; optional ambience/music can remain silent.
- versionName 1.5.0 / versionCode 15.

# v1.4.0

- Added deterministic visual production pipeline: `visual_sources` → WebP optimizer → Android assets.
- Added 93-asset visual queue (33 core-character base/age variants + 60 core-location DAY/NIGHT/RAIN/HOLIDAY variants).
- Added automatic 768×1152 transparent WebP character preparation and 1280×720 WebP background preparation.
- Added visual binary validation for format, dimensions and character alpha channels.
- Added data-driven HSK-level portrait mapping so core characters visibly age across the six levels without changing identity.
- Added GitHub Actions steps for Pillow setup, visual queue generation, WebP preparation and runtime/binary validation.
- Added human-readable visual production CSV and source drop-area documentation.
- No real generated binary art is bundled yet; missing assets still use Compose fallbacks.
- versionName 1.4.0 / versionCode 14.

# v1.2.0

- Added reusable Visual Novel / Theatre stage layer driven by scene `locationId` and production cast metadata.
- Added active-speaker focus animation and location-aware Compose fallback backgrounds.
- Added asset-aware WebP background and character portrait loading without adding a third-party image library.
- Added media catalog generator with 83 character/role profiles, 63 locations and 84 voice profiles.
- Added authored-audio-first `DialogueAudioPlayer`: packaged dialogue/narrator Opus assets are used when present, otherwise offline Mandarin TTS remains the fallback.
- Added optional scene ambience/music player using location/scene ID conventions.
- Added automatic narrator intro and narrator replay control.
- Subtitle defaults now follow each scene's `defaultSubtitleMode`; users can still toggle Pinyin/TR manually.
- Added visual/audio manifests and stable future media paths so binary assets can be inserted without changing scene code.
- GitHub Actions now regenerates media catalogs before strict validation/build.
- Validator now checks character, location, voice and media catalog references.
- versionName 1.2.0 / versionCode 12.

# v1.1.0

- Added single-dialogue visual-novel scene player with previous/next navigation.
- Added Pinyin and Turkish subtitle toggles.
- Added persistent dialogue resume position and persistent playback speed.
- Added scene auto-play and per-line Mandarin TTS fallback with speed controls.
- Added TTS playback to scene vocabulary and Favorites flash cards.
- Added comprehension practice screen.
- Added pronunciation practice using Android on-device Mandarin SpeechRecognizer when available; no network recognizer fallback is used.
- Added local recognized-text similarity score and persistent best pronunciation practice score.
- Added interactive/choice-dialogue practice screen.
- Added RECORD_AUDIO permission and Android 11+ package-visibility queries for speech recognition/TTS services.
- Existing 90% vocabulary + 85% sentence exam gating remains unchanged.

# Changelog
## 1.0.0
- HSK6 50/50 sahne veri-tam duruma getirildi; kurs HSK1–HSK6 genelinde **300/300 tam sahneye** ulaştı.
- HSK6 için 5.000 diyalog ve 400 flash-card eklendi; toplam durum **30.000 diyalog** ve **2.400 flash-card** oldu.
- HSK6 içeriği evlilikler, telif/mesleki sınırlar, emeklilik, torunlar, kentleşme, mentorluk, kültürel miras, afet dayanışması, sağlık, aidiyet ve yaşamın anlamı temalarıyla genişletildi.
- HSK6 gramer/pragmatik hedefleri: çok katmanlı bağlı cümleler, ima ve dolaylı anlatım, ödünleme/karşı argüman, soyut nedensellik, retorik/pragmatik kullanım ve resmî/gündelik register geçişleri.
- HSK6 sahnelerinde kelime sınavı >= %90 ve cümle sınavı >= %85 sahne kilidi korunur.
- Tüm kurs için `validate_content.py --strict` geçti; quality audit 300 complete sahnenin tamamını kontrol etti.
- Normal GitHub APK build workflow'u artık strict 300/300 içerik kontrolü yapar.
- 300 sahnenin tamamında native/editoryal Mandarin kontrol bayrağı bilinçli olarak korunur.
- versionName 1.0.0 / versionCode 10 yapıldı.

## 0.9.0
- HSK5 50/50 sahne veri-tam duruma getirildi.
- HSK5 için 5.000 diyalog ve 400 benzersiz flash-card eklendi; toplam durum 250/300 tam sahne, 25.000 diyalog ve 2.000 flash-card oldu.
- HSK5 içeriği öz değerlendirme, iş etiği, kanıt/kaynak doğrulama, profesyonel müzakere, çevre, maliyet-fiyat dengesi, kariyer tercihleri, yaşlı bakımı ve soyut yaşam değerleriyle genişletildi.
- HSK5 gramer hedefleri: 尽管…仍然…, 之所以…是因为…, 无论…都…, 不仅…还…, 从…来看 ve 与…相比.
- HSK5 sahnelerinde tekrar eden flash-card yüzeyleri temizlendi; bazı fiiller için mekanik genel şablon yerine bağlama özel Mandarin cümleleri eklendi.
- Zorunlu kelime >= %90 ve cümle >= %85 sahne kilidi sistemi HSK5 için de korunuyor.
- Validation ve quality audit geçti; native/editoryal Mandarin kontrol bayrağı korunuyor.
- versionName 0.9.0 / versionCode 9 yapıldı.

## 0.8.0
- HSK4 50/50 sahne veri-tam duruma getirildi.
- HSK4 için 5.000 diyalog, 400 flash-card, kelime sıralama, boşluk doldurma, cümle düzeltme, anlama, telaffuz ve interaktif diyalog verileri eklendi.
- HSK4 gramer hedefleri: 既然…就…, 不但…而且…, 即使…也…, 一方面…另一方面…, 与其…不如… ve 把/被字句综合.
- HSK4 karakter rolleri sahne bağlamına göre ayrıntılandırıldı; flash-card içinde tekrar eden kelimeler temizlendi.
- Toplam durum 200/300 tam sahne, 20.000 diyalog ve 1.600 flash-card oldu.
- Validation ve quality audit geçti; native/editoryal Mandarin kontrol bayrağı korunuyor.
- versionName 0.8.0 / versionCode 8 yapıldı.

## 0.7.0
- HSK3 50/50 sahne veri-tam duruma getirildi.
- HSK3 için 5.000 diyalog, 400 flash-card, cümle alıştırmaları, anlama, telaffuz ve interaktif diyalog verileri eklendi.
- HSK3 üreticisinde sahneye özel kelime havuzu, kategori duyarlı cümle kalıpları ve HSK3 bağlaçları kullanıldı.
- Toplam durum 150/300 tam sahne, 15.000 diyalog ve 1.200 flash-card oldu.
- Validation ve quality audit geçti; native/editoryal Mandarin kontrol bayrağı korunuyor.


## 0.6.0
- HSK2 50/50 sahne tek kaynak authoring içinde tam veri seviyesine çıkarıldı.
- HSK2 toplam 5.000 diyalog turu eklendi; her replikte Basitleştirilmiş Çince, ton işaretli Hanyu Pinyin ve offline Türkçe alanı bulunur.
- HSK2 sahnelerinin tamamında sahneye özel flash-card, favori uyumlu kelime verisi, kelime sıralama, boşluk doldurma, cümle düzeltme, anlama, telaffuz ve interaktif diyalog modülleri bulunur.
- Zorunlu sınav eşikleri HSK2 için de sabitlendi: kelime >= %90, cümle >= %85; iki aşama geçilmeden sonraki sahne açılmaz.
- HSK2 üreticisi zaman/bağlaç/soyut kelimeleri tek bir nesne şablonuna sokmayacak şekilde semantik kategorilere ayrıldı; örnekleme sırasında bulunan yapay kalıplar düzeltildi.
- HSK2 diyalog tepki çeşitliliği artırıldı; kalite auditinde complete sahnelerde ortalama unique-ZH oranı yükseltildi.
- content_status artık bir sonraki eksik seviyeyi otomatik olarak production target olarak belirler.
- Proje toplam durumu: 300/300 blueprint, 100/300 veri-tam sahne, 10.000 diyalog.
- versionName 0.6.0 / versionCode 6 yapıldı.

## 0.5.0
- HSK1 50/50 sahne için tek kaynak authoring üretimi eklendi.
- HSK1 toplam 5.000 diyalog turuna çıkarıldı; her replikte Basitleştirilmiş Çince, ton işaretli Pinyin ve Türkçe katmanı var.
- HSK1 sahnelerinin tamamında flash-card, favori uyumlu kelime verisi, üç tür cümle alıştırması, anlama soruları, telaffuz öğeleri ve interaktif diyalog eklendi.
- İki aşamalı sınav kuralları tüm HSK1 sahnelerinde sabitlendi: kelime >= %90, cümle >= %85.
- HSK1 sahnelerine minimal prodüksiyon/visual-novel metadata eklendi.
- compile_authoring.py artık authoring içindeki tam diyalogları gerçek Single Source of Truth olarak derliyor.
- Validator complete sahnelerde comprehension, pronunciation, interactive dialogue ve production verisini de zorunlu kılıyor.
- İçerik statüsü native/editoryal inceleme ihtiyacını teknik tamlıktan ayrı takip ediyor.
- versionName 0.5.0 / versionCode 5 yapıldı.

## 0.4.0
- Sahneye özel flash-card kelime çalışma ekranı eklendi.
- İleri/geri kart navigasyonu ve kalıcı favori kelimeler eklendi.
- Favori kelimeleri bağımsız çalışma ekranı eklendi.
- Kelime sıralama, boşluk doldurma ve yanlış sırayı düzeltme cümle alıştırmaları eklendi.
- İki seviyeli zorunlu sahne sınavı eklendi: kelime %90, cümle %85.
- 2. sınav 1. sınav geçilmeden açılamaz; sonraki sahne iki sınav geçilmeden kilitli kalır.
- Favoriler ve en iyi sınav skorları cihazda offline SharedPreferences ile kalıcı saklanır.
- Validator, complete sahnelerde bu öğrenme modüllerini ve eşikleri zorunlu kılar.
- HSK1-S01 için örnek 10 flash kart + 7 cümle alıştırması veri sözleşmesi eklendi.
- versionName 0.4.0 / versionCode 4 yapıldı.

## 0.3.0
- HSK3–HSK6 için toplam 200 gerçek scene blueprint eklendi.
- HSK1–HSK6 toplam 300/300 blueprint-ready duruma getirildi.
- İleri dönem hikâyesi için tekrar kullanılabilir location manifest genişletildi.
- HSK3–HSK6 seviye bazlı kelime yoğunluğu, varsayılan konuşma hızı, altyazı, gramer ve telaffuz metadata'sı eklendi.
- AGP 9.x built-in Kotlin ile daha güvenli uyum için Compose compiler plugin 2.2.10'a hizalandı ve gereksiz harici KGP override kaldırıldı.
- Uygulama versionName 0.3.0 / versionCode 3 yapıldı.

## 0.2.0
- HSK1 ve HSK2 için 100 blueprint hazırlandı.
- Blueprint / draft / complete durumları ayrıldı.
- Authoring → compile → validation akışı eklendi.

## 1.3.0
- Added locked visual identity system for 9 core characters and 15 high-reuse locations.
- Added `media/visual_bible.json` and 24 deterministic image-generation prompt files.
- Added age-variant rules and location continuity/variant rules.
- Added visual asset validation to GitHub Actions.
- Binary WebP assets remain optional; Compose fallback stays active until generated media is bundled.

## 1.6.0
- Added deterministic per-character binding to locally installed offline Mandarin TTS voices.
- Added persistent on-device TTS audio cache for dialogue and narrator lines.
- Cached synthesis is reused at all playback speeds; speed is applied during playback.
- Added automatic ~350 MB LRU-style cache pruning.
- Authored audio still has priority over generated local TTS cache.
- Added runtime voice/cache status in the scene audio panel.

## 1.8.0
- Dashboard'a Ayarlar ve İlerlemem ekranları eklendi.
- Pinyin ve Türkçe altyazı varsayılanı artık Seviyeye göre / Her zaman açık / Kapalı seçilebilir.
- Otomatik oynatma, konuşma hızı ve günlük tekrar hedefi kalıcı ayarlara bağlandı.
- Mor / Koyu / Açık görünüm seçenekleri eklendi.
- Genel ve seviye bazlı ilerleme, kelime/cümle sınav ortalamaları, placement sonucu ve favori sayısı için ilerleme ekranı eklendi.
- Android dosya seçicisi üzerinden depolama izni istemeden tek JSON yedek dışa aktarma ve geri yükleme eklendi.
- Günlük tekrar kart sayısı kullanıcı hedefine bağlandı.
- App-flow doğrulaması ayarlar ve yerel yedek özelliklerini de kontrol ediyor.

## 2.0.0
- Added in-app System Check for offline TTS, on-device recognition, notification permission, content status and TTS cache.
- Added user-friendly GitHub APK packaging with versioned APK name, SHA-256 and validation-report artifacts.
- Added optional GitHub Secrets based stable release signing; falls back to personal debug APK when signing is not configured.
- Added Turkish GitHub build/signing guides.
