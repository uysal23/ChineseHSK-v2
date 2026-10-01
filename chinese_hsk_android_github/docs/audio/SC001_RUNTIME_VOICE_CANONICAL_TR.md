# SC001 Runtime Ses Sistemi — CANONICAL

Bu projede normal uygulama oynatımı için canonical Mandarin ses sistemi
ZH_HSK1_SC001'de kullanılan mevcut Android offline TTS tekniğidir.

## Kilit

- Ana çalışma motoru: cihazda kurulu offline Mandarin Android TTS.
- İnternet gerekmez.
- Ücretli API gerekmez.
- Her karakterin kimliği `characters.json -> voiceProfileId` ile sabittir.
- `VoiceIdentityResolver` görünür Çince konuşmacı adını bu profile çözer.
- `MandarinTtsPlayer` profile göre cihazdaki local zh voice'u deterministik seçer.
- İlk seçim `offline_mandarin_voice_bindings` SharedPreferences içinde saklanır.
- Aynı cihazda sonraki açılışlarda aynı karakter aynı local voice ile konuşur.
- Replik ilk oynatıldığında yerel WAV cache'e sentezlenir; sonraki oynatmalarda yeniden sentezlenmeden cache çalınır.
- Sahne konuşma hızı ilgili sahnenin `defaultSpeechSpeed` değerinden gelir.
- Karaktere özgü pitch profile ID'den deterministik ve sabit üretilir.

## Kapsam

83/83 karakterin `voiceProfileId` eşlemesi vardır.
83/83 voice cast karakter adı `characters.json` ile birebir eşleşmektedir.
Bu nedenle HSK1-HSK6 toplam 30.000 sahne diyaloğunda generic voice'a düşmek zorunda olan tanımlı bir karakter yoktur.

Anlatıcı `NARRATOR_ZH_001` profiline kilitlidir.
Kelime kartı, telaffuz, interaktif soru ve seviye tespit konuşmaları da
`MandarinTtsPlayer.speak()` üzerinden aynı local voice-binding ve persistent
cache mekanizmasını kullanır; bunlar karakter diyaloğu olmadığından sabit
öğrenme profilleri (VOCAB, PRONUNCIATION, DIALOGUE_PROMPT, PLACEMENT) kullanır.

## Cihazlar arası not

Aynı telefonda karakter sesi kalıcı olarak sabittir. Uygulama güncellemesi
SharedPreferences ve app data korunduğu sürece sesi değiştirmez.

Başka bir telefonda kurulu offline Mandarin TTS voice listesi farklıysa
birebir aynı timbre garanti edilemez. Ancak aynı voice-profile kimliği ve
deterministik seçim mantığı korunur. Bütün cihazlarda birebir aynı timbre
istenirse ayrıca packaged authored audio veya bundled TTS model gerekir.

## Kokoro

Kokoro smoke/paket üretim hattı silinmez, fakat canonical runtime ses motoru
değildir. İstenirse ileride seçilmiş içerikler için prebuilt offline ses paketi
üretmekte kullanılabilir. Normal uygulama çalışması Kokoro dosyalarına bağlı
değildir.
