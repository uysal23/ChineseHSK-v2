package com.ayhan.chineselearning

import android.content.Context
import org.json.JSONObject

/**
 * Resolves the visible Chinese speaker name to the stable Voice Bible profile id.
 * This keeps the same character attached to the same local TTS voice across app launches.
 */
class VoiceIdentityResolver(context: Context) {
    private val speakerToProfile: Map<String, String> = run {
        try {
            val text = context.assets.open("chinese_course/characters.json")
                .bufferedReader(Charsets.UTF_8).use { it.readText() }
            val root = JSONObject(text)
            val array = root.optJSONArray("characters")
            buildMap {
                if (array != null) {
                    for (i in 0 until array.length()) {
                        val item = array.optJSONObject(i) ?: continue
                        val name = item.optString("nameZh")
                        val profile = item.optString("voiceProfileId")
                        if (name.isNotBlank() && profile.isNotBlank()) put(name, profile)
                    }
                }
            }
        } catch (_: Exception) {
            emptyMap()
        }
    }

    fun profileForSpeaker(speaker: String): String =
        speakerToProfile[speaker] ?: "VOICE_ZH_GENERIC_${speaker.hashCode().toUInt().toString(16).uppercase()}"
}
