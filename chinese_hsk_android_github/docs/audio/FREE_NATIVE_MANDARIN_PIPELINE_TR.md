# Ücretsiz Native Mandarin Ses Üretim Hattı

Bu proje için ana ses üretim yolu ücretli API kullanmaz.

## Kilitli üretim yaklaşımı

- Ana TTS: Kokoro-82M Mandarin
- Dil: zh-CN / lang_code=z
- G2P: Misaki Chinese
- Kodlama: FFmpeg, mono 24 kHz Opus 24 kbps VBR
- Karakter eşleme: `ci/voice_cast_manifest.json`
- Diyalog kaynağı: `ci/dialogue_final_v5/HSK1..HSK6`
- Android fallback: cihazdaki Mandarin TTS korunur
- Ücretli bulut API anahtarı: kullanılmaz

Kokoro'nun Mandarin sesleri:
- kadın: zf_xiaobei, zf_xiaoni, zf_xiaoxiao, zf_xiaoyi
- erkek: zm_yunjian, zm_yunxi, zm_yunxia, zm_yunyang

Aynı karakter bütün seviyelerde aynı temel ses kimliğini korur. HSK seviyesi
ilerledikçe hız ve çok küçük pitch/energy değişiklikleri uygulanır. Aşırı
pitch-shift Mandarin tonlarını bozabileceği için üretici script DSP pitch
değişimini +/-1.75 semitone ile sınırlar.

## Neden Kokoro ana motor?

Küçük ve CPU'da çalışabilen bir modeldir. Mandarin dil hattı vardır ve proje
zaten 83 karakteri sekiz Mandarin base voice'a deterministik biçimde
eşleştirmiştir. Bu nedenle 30.000 repliği ücretli API olmadan toplu üretmek
mümkündür.

## CosyVoice seçeneği

Fun-CosyVoice 3 açık kaynak/Apache-2.0 bir üst kalite seçeneğidir ve duygu,
hız, ses yüksekliği gibi instruction kontrolleri sunar. Ancak 0.5B sınıfı
olduğu için 30.000 repliği CPU'da üretmek Kokoro'ya göre çok daha ağırdır.
Bu projede ana toplu üretim Kokoro'dur; CosyVoice yalnızca seçilmiş kritik
sahneler için opsiyonel stüdyo katmanı olarak düşünülür.

## Yerel üretim

Python 3.11, ffmpeg ve espeak-ng kurulduktan sonra:

```bash
pip install "kokoro>=0.9.4" "misaki[zh]>=0.9.4" soundfile numpy
python ci/validate_voice_cast.py
python ci/generate_voice_audio.py --level HSK1 --out voice-HSK1
```

Tüm seviyeler aynı komutla HSK1..HSK6 için sırayla üretilebilir. Üretim
dosyaları hash ile deduplicate edilir: aynı metin + aynı etkili ses profili
yalnızca bir kez sentezlenir.

## GitHub Actions güvenliği

`.github/workflows/generate-voice-audio.yml` artık push ile otomatik
30.000 replik üretmez. Yalnızca manuel `workflow_dispatch` ile çalışır.

- SMOKE: 12 benzersiz replik
- HSK1..HSK6: tek seviye
- ALL: altı seviye
- max_items=0: seçilen seviyenin tamamı
- publish_release=false: varsayılan; release'e otomatik yazmaz

Bu düzen özel repoda GitHub Actions dakika kotasının yanlışlıkla
tüketilmesini önler. Gerçek anlamda sınırsız ücret gerektirmeyen yol yerel
PC veya kendi self-hosted runner'ında üretimdir.

## Doğallık kuralları

1. Ses dosyasına giden metin yeniden yazılmaz; sadece Unicode ve Çince
   noktalama normalizasyonu yapılır.
2. Karakterin temel ses kimliği değişmez.
3. Yaş geçişleri esas olarak konuşma hızıyla yapılır.
4. Aşırı DSP pitch uygulanmaz.
5. Soru, ünlem, virgül ve doğal dolgu sözcükleri authored Mandarin metinde
   korunur; Kokoro bunların prosodisini işler.
6. Her final dosya mono 24 kHz Opus olur.
7. Native/editoryal Mandarin kontrolü, ses üretiminden önceki diyalog QA'nın
   yerini tutmaz; 300 sahnenin metin kalite kontrolü ayrıca korunur.

## Mevcut durum

Ses cast'i hazırdır; gerçek authored/generate edilmiş 30.000 dialogue Opus
paketi henüz repoya gömülü değildir. Bu hat, bunları ücretsiz olarak
üretmek için canonical üretim yoludur.
