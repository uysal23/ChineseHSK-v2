package com.ayhan.chineselearning

import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer

class OfflineMandarinRecognizer(context: Context) {
    private val appContext = context.applicationContext
    private val main = Handler(Looper.getMainLooper())
    private var recognizer: SpeechRecognizer? = null
    private var runId = 0

    fun isAvailable(): Boolean =
        SpeechRecognizer.isRecognitionAvailable(appContext) ||
            (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S &&
                SpeechRecognizer.isOnDeviceRecognitionAvailable(appContext))

    fun start(
        onListening: () -> Unit,
        onResult: (String) -> Unit,
        onError: (String) -> Unit
    ) {
        runId += 1
        val id = runId
        main.post {
            destroyNow()
            val onDevice = Build.VERSION.SDK_INT >= Build.VERSION_CODES.S &&
                SpeechRecognizer.isOnDeviceRecognitionAvailable(appContext)
            startEngine(id, onDevice, true, onListening, onResult, onError)
        }
    }

    private fun startEngine(
        id: Int,
        onDevice: Boolean,
        allowFallback: Boolean,
        onListening: () -> Unit,
        onResult: (String) -> Unit,
        onError: (String) -> Unit
    ) {
        if (id != runId) return

        val sr = try {
            if (onDevice && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                SpeechRecognizer.createOnDeviceSpeechRecognizer(appContext)
            } else {
                if (!SpeechRecognizer.isRecognitionAvailable(appContext)) {
                    onError("Telefonda konuşma tanıma hizmeti bulunamadı.")
                    return
                }
                SpeechRecognizer.createSpeechRecognizer(appContext)
            }
        } catch (_: Throwable) {
            if (onDevice && allowFallback) {
                main.postDelayed({
                    startEngine(id, false, false, onListening, onResult, onError)
                }, 200)
            } else {
                onError("Konuşma tanıma motoru başlatılamadı.")
            }
            return
        }

        recognizer = sr
        sr.setRecognitionListener(object : RecognitionListener {
            override fun onReadyForSpeech(params: Bundle?) = onListening()
            override fun onBeginningOfSpeech() = Unit
            override fun onRmsChanged(rmsdB: Float) = Unit
            override fun onBufferReceived(buffer: ByteArray?) = Unit
            override fun onEndOfSpeech() = Unit
            override fun onPartialResults(partialResults: Bundle?) = Unit
            override fun onEvent(eventType: Int, params: Bundle?) = Unit

            override fun onError(error: Int) {
                if (id != runId) return
                val fallbackErrors = setOf(
                    SpeechRecognizer.ERROR_CLIENT,
                    SpeechRecognizer.ERROR_RECOGNIZER_BUSY,
                    SpeechRecognizer.ERROR_SERVER,
                    SpeechRecognizer.ERROR_SERVER_DISCONNECTED,
                    SpeechRecognizer.ERROR_LANGUAGE_NOT_SUPPORTED,
                    SpeechRecognizer.ERROR_LANGUAGE_UNAVAILABLE
                )
                if (onDevice && allowFallback && error in fallbackErrors) {
                    destroyNow()
                    main.postDelayed({
                        startEngine(id, false, false, onListening, onResult, onError)
                    }, 300)
                } else {
                    onError(messageFor(error))
                }
            }

            override fun onResults(results: Bundle?) {
                val best = results
                    ?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                    ?.firstOrNull()
                    .orEmpty()
                if (best.isBlank()) onError("Konuşma algılanamadı. Tekrar deneyin.")
                else onResult(best)
            }
        })

        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, "zh-CN")
            putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false)
            putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE, true)
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 5)
        }

        try {
            sr.startListening(intent)
        } catch (_: SecurityException) {
            destroyNow()
            onError("Mikrofon izni verilmemiş.")
        } catch (_: Throwable) {
            destroyNow()
            if (onDevice && allowFallback) {
                main.postDelayed({
                    startEngine(id, false, false, onListening, onResult, onError)
                }, 300)
            } else {
                onError("Konuşma tanıma başlatılamadı. Tekrar deneyin.")
            }
        }
    }

    private fun messageFor(error: Int): String = when (error) {
        SpeechRecognizer.ERROR_AUDIO -> "Mikrofon kullanılamıyor."
        SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "Mikrofon izni verilmemiş."
        SpeechRecognizer.ERROR_NO_MATCH -> "Konuşma anlaşılmadı. Tekrar deneyin."
        SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "Ses algılanmadı. Düğmeden sonra konuşun."
        SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "Konuşma tanıyıcı meşgul. Tekrar deneyin."
        SpeechRecognizer.ERROR_LANGUAGE_NOT_SUPPORTED -> "Mandarin tanıma desteklenmiyor."
        SpeechRecognizer.ERROR_LANGUAGE_UNAVAILABLE -> "Mandarin konuşma modeli telefonda hazır değil."
        SpeechRecognizer.ERROR_NETWORK,
        SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "Çevrimdışı model bulunamadı ve bağlantı kullanılamadı."
        else -> "Konuşma tanıma hatası ($error). Tekrar deneyin."
    }

    fun stop() {
        runId += 1
        main.post {
            try { recognizer?.stopListening() } catch (_: Throwable) { }
            destroyNow()
        }
    }

    fun destroy() {
        runId += 1
        main.post { destroyNow() }
    }

    private fun destroyNow() {
        try { recognizer?.cancel() } catch (_: Throwable) { }
        try { recognizer?.destroy() } catch (_: Throwable) { }
        recognizer = null
    }
}

fun chineseTextSimilarity(target: String, recognized: String): Int {
    fun normalize(s: String): String = s
        .replace(Regex("[\\s，。！？、,.!?;；:'\"“”‘’（）()\\-]"), "")
        .trim()

    val a = normalize(target)
    val b = normalize(recognized)
    if (a.isEmpty() && b.isEmpty()) return 100
    if (a.isEmpty() || b.isEmpty()) return 0

    val prev = IntArray(b.length + 1) { it }
    val cur = IntArray(b.length + 1)
    for (i in 1..a.length) {
        cur[0] = i
        for (j in 1..b.length) {
            val cost = if (a[i - 1] == b[j - 1]) 0 else 1
            cur[j] = minOf(cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + cost)
        }
        for (j in prev.indices) prev[j] = cur[j]
    }
    val distance = prev[b.length]
    val maxLen = maxOf(a.length, b.length)
    return (((maxLen - distance).toFloat() / maxLen) * 100).toInt().coerceIn(0, 100)
}
