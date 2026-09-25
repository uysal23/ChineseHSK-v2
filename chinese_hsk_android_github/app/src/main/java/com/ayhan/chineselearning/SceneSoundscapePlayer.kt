package com.ayhan.chineselearning

import android.content.Context
import android.media.MediaPlayer

/** Optional ambience/music layer. Missing assets are silently ignored. */
class SceneSoundscapePlayer(private val context: Context) {
    private var ambience: MediaPlayer? = null
    private var music: MediaPlayer? = null

    private fun assetExists(path: String): Boolean = try {
        if (path.isBlank()) false else { context.assets.open(path).close(); true }
    } catch (_: Exception) { false }

    private fun loopAsset(path: String, volume: Float): MediaPlayer? {
        if (!assetExists(path)) return null
        return try {
            val afd = context.assets.openFd(path)
            MediaPlayer().apply {
                setDataSource(afd.fileDescriptor, afd.startOffset, afd.length)
                afd.close()
                isLooping = true
                setVolume(volume, volume)
                setOnPreparedListener { it.start() }
                prepareAsync()
            }
        } catch (_: Exception) { null }
    }

    fun start(scene: SceneInfo) {
        stop()
        val ambiencePath = scene.production.ambienceAsset.ifBlank {
            if (scene.production.locationId.isBlank()) ""
            else "chinese_course/media/ambience/${scene.production.locationId}.opus"
        }
        val musicPath = scene.production.musicAsset.ifBlank {
            "chinese_course/media/music/${scene.id}.opus"
        }
        ambience = loopAsset(ambiencePath, 0.20f)
        music = loopAsset(musicPath, 0.10f)
    }

    fun stop() {
        for (player in listOf(ambience, music)) {
            try { player?.stop() } catch (_: Exception) { }
            try { player?.release() } catch (_: Exception) { }
        }
        ambience = null
        music = null
    }

    fun shutdown() = stop()
}
