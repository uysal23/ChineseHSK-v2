from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_source.py <source-root>")

root = Path(sys.argv[1])
gradle = root / "app" / "build.gradle.kts"
tts = root / "app" / "src" / "main" / "java" / "com" / "ayhan" / "chineselearning" / "MandarinTtsPlayer.kt"

g = gradle.read_text(encoding="utf-8")
g = g.replace("compileSdk = 37", "compileSdk = 36")
g = g.replace("targetSdk = 37", "targetSdk = 36")
g = g.replace('compose-bom:2026.09.00', 'compose-bom:2026.04.01')
gradle.write_text(g, encoding="utf-8")

s = tts.read_text(encoding="utf-8")
speak_line = "            tts.speak(text, TextToSpeech.QUEUE_FLUSH, Bundle(), utteranceId)"
if speak_line not in s:
    raise SystemExit("TTS speak anchor not found")
if speak_line + "\n            Unit" not in s:
    s = s.replace(speak_line, speak_line + "\n            Unit", 1)

wrapper = """    fun speak(
        text: String,
        voiceProfileId: String,
        speed: Float,
        onDone: (() -> Unit)? = null
    ) {
        speakDirect(text, voiceProfileId, speed, onDone)
    }

"""
if "    fun speak(\n" not in s:
    anchor = "    private fun playFile"
    if anchor not in s:
        raise SystemExit("TTS playFile anchor not found")
    s = s.replace(anchor, wrapper + anchor, 1)

tts.write_text(s, encoding="utf-8")

assert "compileSdk = 36" in gradle.read_text(encoding="utf-8")
assert "targetSdk = 36" in gradle.read_text(encoding="utf-8")
assert "compose-bom:2026.04.01" in gradle.read_text(encoding="utf-8")
assert "fun speak(" in tts.read_text(encoding="utf-8")
assert speak_line + "\n            Unit" in tts.read_text(encoding="utf-8")
print("CI source compatibility patch applied.")
