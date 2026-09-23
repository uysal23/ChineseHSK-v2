package com.ayhan.chineselearning

import android.content.Context
import android.media.AudioFormat
import android.media.AudioRecord
import android.media.MediaPlayer
import android.media.MediaRecorder
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.os.ParcelFileDescriptor
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import kotlin.math.sqrt

class UserVoiceRecorder(context: Context) {
    companion object {
        const val SAMPLE_RATE = 16_000
        const val CHANNEL_COUNT = 1
        const val ENCODING = AudioFormat.ENCODING_PCM_16BIT

        private const val MAX_CAPTURE_MS = 15_000L
        private const val NO_SPEECH_TIMEOUT_MS = 6_000L
        private const val MIN_CAPTURE_MS = 900L
        private const val END_SILENCE_MS = 950L
        private const val VOICE_RMS_THRESHOLD = 520.0
    }

    private val appContext = context.applicationContext
    private val main = Handler(Looper.getMainLooper())

    @Volatile private var sessionId = 0
    @Volatile private var stopRequested = false
    @Volatile private var recording = false

    private var audioRecord: AudioRecord? = null
    private var captureThread: Thread? = null
    private var player: MediaPlayer? = null
    private var pcmFile: File? = null
    private var wavFile: File? = null

    fun start(onFinished: (Boolean) -> Unit): Boolean {
        clear()
        releasePlayer()

        val id = ++sessionId
        stopRequested = false

        val minBuffer = AudioRecord.getMinBufferSize(
            SAMPLE_RATE,
            AudioFormat.CHANNEL_IN_MONO,
            ENCODING
        )
        if (minBuffer <= 0) return false

        val next = try {
            AudioRecord(
                MediaRecorder.AudioSource.VOICE_RECOGNITION,
                SAMPLE_RATE,
                AudioFormat.CHANNEL_IN_MONO,
                ENCODING,
                maxOf(minBuffer * 2, 4096)
            )
        } catch (_: Throwable) {
            null
        } ?: return false

        if (next.state != AudioRecord.STATE_INITIALIZED) {
            try { next.release() } catch (_: Throwable) { }
            return false
        }

        val pcm = File(appContext.cacheDir, "pronunciation_user_voice_$id.pcm")
        val wav = File(appContext.cacheDir, "pronunciation_user_voice_$id.wav")
        pcmFile = pcm
        wavFile = wav

        return try {
            next.startRecording()
            audioRecord = next
            recording = true

            val thread = Thread({
                var heardSpeech = false
                var lastVoiceAt = 0L
                val startedAt = android.os.SystemClock.elapsedRealtime()
                val buffer = ByteArray(maxOf(minBuffer, 2048))

                try {
                    FileOutputStream(pcm).use { out ->
                        while (!stopRequested && id == sessionId) {
                            val count = try {
                                next.read(buffer, 0, buffer.size)
                            } catch (_: Throwable) {
                                break
                            }
                            if (count <= 0) continue

                            out.write(buffer, 0, count)

                            val now = android.os.SystemClock.elapsedRealtime()
                            val elapsed = now - startedAt
                            val rms = pcm16Rms(buffer, count)

                            if (rms >= VOICE_RMS_THRESHOLD) {
                                heardSpeech = true
                                lastVoiceAt = now
                            }

                            if (heardSpeech && elapsed >= MIN_CAPTURE_MS && now - lastVoiceAt >= END_SILENCE_MS) {
                                break
                            }
                            if (!heardSpeech && elapsed >= NO_SPEECH_TIMEOUT_MS) {
                                break
                            }
                            if (elapsed >= MAX_CAPTURE_MS) {
                                break
                            }
                        }
                    }
                } finally {
                    try { next.stop() } catch (_: Throwable) { }
                    try { next.release() } catch (_: Throwable) { }
                    if (audioRecord === next) audioRecord = null
                    recording = false

                    if (id == sessionId && pcm.exists() && pcm.length() > 0L) {
                        try {
                            writeWav(pcm, wav)
                        } catch (_: Throwable) {
                            try { wav.delete() } catch (_: Throwable) { }
                        }
                        main.post {
                            if (id == sessionId) onFinished(heardSpeech)
                        }
                    } else {
                        try { pcm.delete() } catch (_: Throwable) { }
                        try { wav.delete() } catch (_: Throwable) { }
                    }
                }
            }, "PronunciationVoiceCapture-$id")

            captureThread = thread
            thread.start()
            true
        } catch (_: Throwable) {
            recording = false
            try { next.release() } catch (_: Throwable) { }
            audioRecord = null
            try { pcm.delete() } catch (_: Throwable) { }
            try { wav.delete() } catch (_: Throwable) { }
            false
        }
    }

    fun stop() {
        stopRequested = true
        val active = audioRecord
        if (active != null) {
            try { active.stop() } catch (_: Throwable) { }
        }
    }

    fun isRecording(): Boolean = recording

    fun hasRecording(): Boolean {
        val file = wavFile
        return file != null && file.exists() && file.length() > 48L
    }

    fun openRecognitionSource(): ParcelFileDescriptor? {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) return null
        val file = pcmFile ?: return null
        if (!file.exists() || file.length() <= 0L) return null
        return try {
            ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
        } catch (_: Throwable) {
            null
        }
    }

    fun play(onFinished: () -> Unit = {}): Boolean {
        releasePlayer()
        val file = wavFile ?: return false
        if (!file.exists() || file.length() <= 48L) return false

        return try {
            val next = MediaPlayer()
            next.setDataSource(file.absolutePath)
            next.setOnCompletionListener {
                releasePlayer()
                onFinished()
            }
            next.setOnErrorListener { _, _, _ ->
                releasePlayer()
                onFinished()
                true
            }
            next.prepare()
            next.start()
            player = next
            true
        } catch (_: Throwable) {
            releasePlayer()
            false
        }
    }

    fun stopPlayback() {
        releasePlayer()
    }

    fun clear() {
        sessionId += 1
        stopRequested = true

        val active = audioRecord
        if (active != null) {
            try { active.stop() } catch (_: Throwable) { }
            try { active.release() } catch (_: Throwable) { }
        }
        audioRecord = null
        recording = false
        captureThread = null
        releasePlayer()

        try { pcmFile?.delete() } catch (_: Throwable) { }
        try { wavFile?.delete() } catch (_: Throwable) { }
        pcmFile = null
        wavFile = null
    }

    fun release() {
        clear()
    }

    private fun releasePlayer() {
        val active = player
        if (active != null) {
            try {
                if (active.isPlaying) active.stop()
            } catch (_: Throwable) { }
            try { active.reset() } catch (_: Throwable) { }
            try { active.release() } catch (_: Throwable) { }
        }
        player = null
    }

    private fun pcm16Rms(buffer: ByteArray, count: Int): Double {
        if (count < 2) return 0.0
        var sum = 0.0
        var samples = 0
        var i = 0
        while (i + 1 < count) {
            val lo = buffer[i].toInt() and 0xFF
            val hi = buffer[i + 1].toInt()
            val sample = ((hi shl 8) or lo).toShort().toInt()
            sum += sample.toDouble() * sample.toDouble()
            samples++
            i += 2
        }
        return if (samples == 0) 0.0 else sqrt(sum / samples)
    }

    private fun writeWav(pcm: File, wav: File) {
        val audioLength = pcm.length()
        val byteRate = SAMPLE_RATE * CHANNEL_COUNT * 16 / 8
        FileOutputStream(wav).use { out ->
            val header = ByteArray(44)
            val totalDataLength = audioLength + 36

            header[0] = 'R'.code.toByte()
            header[1] = 'I'.code.toByte()
            header[2] = 'F'.code.toByte()
            header[3] = 'F'.code.toByte()
            writeIntLE(header, 4, totalDataLength.toInt())
            header[8] = 'W'.code.toByte()
            header[9] = 'A'.code.toByte()
            header[10] = 'V'.code.toByte()
            header[11] = 'E'.code.toByte()
            header[12] = 'f'.code.toByte()
            header[13] = 'm'.code.toByte()
            header[14] = 't'.code.toByte()
            header[15] = ' '.code.toByte()
            writeIntLE(header, 16, 16)
            writeShortLE(header, 20, 1)
            writeShortLE(header, 22, CHANNEL_COUNT)
            writeIntLE(header, 24, SAMPLE_RATE)
            writeIntLE(header, 28, byteRate)
            writeShortLE(header, 32, CHANNEL_COUNT * 2)
            writeShortLE(header, 34, 16)
            header[36] = 'd'.code.toByte()
            header[37] = 'a'.code.toByte()
            header[38] = 't'.code.toByte()
            header[39] = 'a'.code.toByte()
            writeIntLE(header, 40, audioLength.toInt())
            out.write(header)

            FileInputStream(pcm).use { input ->
                val copyBuffer = ByteArray(8192)
                while (true) {
                    val n = input.read(copyBuffer)
                    if (n <= 0) break
                    out.write(copyBuffer, 0, n)
                }
            }
        }
    }

    private fun writeIntLE(target: ByteArray, offset: Int, value: Int) {
        target[offset] = (value and 0xFF).toByte()
        target[offset + 1] = ((value shr 8) and 0xFF).toByte()
        target[offset + 2] = ((value shr 16) and 0xFF).toByte()
        target[offset + 3] = ((value shr 24) and 0xFF).toByte()
    }

    private fun writeShortLE(target: ByteArray, offset: Int, value: Int) {
        target[offset] = (value and 0xFF).toByte()
        target[offset + 1] = ((value shr 8) and 0xFF).toByte()
    }
}
