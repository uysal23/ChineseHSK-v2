package com.ayhan.chineselearning

import android.content.Context
import android.media.MediaPlayer
import android.media.MediaRecorder
import android.os.Build
import java.io.File

class UserVoiceRecorder(context: Context) {
    private val appContext = context.applicationContext
    private val audioFile = File(appContext.cacheDir, "pronunciation_user_voice.m4a")
    private var recorder: MediaRecorder? = null
    private var player: MediaPlayer? = null
    private var recording = false

    fun start(): Boolean {
        stop()
        releasePlayer()
        try { audioFile.delete() } catch (_: Throwable) { }

        val next = try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                MediaRecorder(appContext)
            } else {
                @Suppress("DEPRECATION")
                MediaRecorder()
            }
        } catch (_: Throwable) {
            null
        } ?: return false

        return try {
            next.setAudioSource(MediaRecorder.AudioSource.MIC)
            next.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            next.setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            next.setAudioSamplingRate(44_100)
            next.setAudioEncodingBitRate(128_000)
            next.setOutputFile(audioFile.absolutePath)
            next.prepare()
            next.start()
            recorder = next
            recording = true
            true
        } catch (_: Throwable) {
            try { next.reset() } catch (_: Throwable) { }
            try { next.release() } catch (_: Throwable) { }
            recorder = null
            recording = false
            try { audioFile.delete() } catch (_: Throwable) { }
            false
        }
    }

    fun stop(): Boolean {
        val active = recorder
        if (active != null) {
            if (recording) {
                try {
                    active.stop()
                } catch (_: Throwable) {
                    try { audioFile.delete() } catch (_: Throwable) { }
                }
            }
            try { active.reset() } catch (_: Throwable) { }
            try { active.release() } catch (_: Throwable) { }
        }
        recorder = null
        recording = false
        return hasRecording()
    }

    fun hasRecording(): Boolean =
        audioFile.exists() && audioFile.isFile && audioFile.length() > 512L

    fun play(onFinished: () -> Unit = {}): Boolean {
        stop()
        releasePlayer()
        if (!hasRecording()) return false

        return try {
            val next = MediaPlayer()
            next.setDataSource(audioFile.absolutePath)
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
        stop()
        releasePlayer()
        try { audioFile.delete() } catch (_: Throwable) { }
    }

    fun release() {
        stop()
        releasePlayer()
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
}
