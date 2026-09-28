# Offline Mandarin Telaffuz Tanıma

Bu proje Mandarin telaffuz alıştırmalarında Android/Google SpeechRecognizer servisine bağımlı değildir.

## Motor

- Motor: Vosk Android 0.3.75
- Model: vosk-model-small-cn-0.22
- Model boyutu: yaklaşık 42 MB arşiv
- Örnekleme: 16 kHz, mono, PCM 16-bit
- Lisans: Apache-2.0
- Resmî model kaynağı: https://alphacephei.com/vosk/models
- Model SHA-256: `3af8b0e7e0f835ae9d414ce5df580237a3cfb08d586c9fbbb0f7ff29ad5b14ba`

Build sırasında model indirilir, SHA-256 doğrulanır ve APK assets içine gömülür. Kurulumdan sonra konuşma tanıma için internet gerekmez.

## Puanlama

Ekrandaki yüzde, Vosk tarafından tanınan Mandarin metin ile hedef Mandarin metin arasındaki normalize karakter düzenleme benzerliğidir:

- %100: tanınan metin hedefle aynı.
- Daha düşük oran: eksik, fazla veya farklı tanınan karakterler vardır.
- Noktalama ve boşluklar puana dahil edilmez.

Bu değer pratik bir **telaffuz/anlaşılabilirlik benzeşme puanıdır**. Ayrı bir laboratuvar tipi ton-konturu veya fonem spektrogram ölçümü değildir.

## Tasarım kararı

Vosk'un büyük Çince modeli daha yüksek doğruluk sunabilir ancak yaklaşık 1.3 GB boyutundadır ve mobil APK için uygun değildir. Küçük 0.22 model, Vosk'un Android/RPi için önerdiği mobil Mandarin modelidir ve uygulamanın tam çevrimdışı hedefi için seçilmiştir.
