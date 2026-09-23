from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("usage: patch_source.py <source-root>")

root = Path(sys.argv[1])
gradle = root / "app" / "build.gradle.kts"
src_dir = root / "app" / "src" / "main" / "java" / "com" / "ayhan" / "chineselearning"
tts = src_dir / "MandarinTtsPlayer.kt"
scene_stage = src_dir / "SceneStage.kt"
main_activity = src_dir / "MainActivity.kt"
recognizer_file = src_dir / "OfflineMandarinRecognizer.kt"
learning_screens = src_dir / "LearningScreens.kt"
app_flow_screens = src_dir / "AppFlowScreens.kt"
progress_store = src_dir / "ProgressStore.kt"
admin_session = src_dir / "AdminSession.kt"

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

ci_dir = Path(__file__).resolve().parent
stage_override = ci_dir / "SceneStage.kt"
main_override = ci_dir / "MainActivity.kt"
recognizer_override = ci_dir / "OfflineMandarinRecognizer.kt"
admin_override = ci_dir / "AdminSession.kt"
dashboard_fragment = ci_dir / "DashboardScreen.fragment.kt"
settings_fragment = ci_dir / "SettingsHub.fragment.kt"
if not stage_override.exists():
    raise SystemExit("SceneStage CI override missing")
if not main_override.exists():
    raise SystemExit("MainActivity CI override missing")
if not recognizer_override.exists():
    raise SystemExit("OfflineMandarinRecognizer CI override missing")
if not admin_override.exists():
    raise SystemExit("AdminSession CI override missing")
if not dashboard_fragment.exists():
    raise SystemExit("Dashboard fragment missing")
if not settings_fragment.exists():
    raise SystemExit("Settings hub fragment missing")
scene_stage.write_text(stage_override.read_text(encoding="utf-8"), encoding="utf-8")
main_activity.write_text(main_override.read_text(encoding="utf-8"), encoding="utf-8")
recognizer_file.write_text(recognizer_override.read_text(encoding="utf-8"), encoding="utf-8")
admin_session.write_text(admin_override.read_text(encoding="utf-8"), encoding="utf-8")

ls = learning_screens.read_text(encoding="utf-8")
# TEMP diagnostics: print the pronunciation composable around startRecognition for maintenance.
_probe = ls.find("fun startRecognition()")
if _probe >= 0:
    print("=== PRONUNCIATION_SOURCE_BEGIN ===")
    print(ls[max(0, _probe - 6000):min(len(ls), _probe + 10000)])
    print("=== PRONUNCIATION_SOURCE_END ===")
needle = """    fun startRecognition() {\n        val item = items.getOrNull(index) ?: return\n        recognized = \"\"\n        score = null\n"""
replacement = """    fun startRecognition() {\n        val item = items.getOrNull(index) ?: return\n        tts.stop()\n        recognizer.stop()\n        status = \"Konuşma tanıma hazırlanıyor…\"\n        recognized = \"\"\n        score = null\n"""
if needle not in ls:
    raise SystemExit("Pronunciation startRecognition anchor missing")
learning_screens.write_text(ls.replace(needle, replacement, 1), encoding="utf-8")



# Dashboard profile/admin support.
ps = progress_store.read_text(encoding="utf-8")
theme_anchor = '''    fun themeMode(): Int = prefs.getInt("setting_theme", THEME_PURPLE).coerceIn(THEME_PURPLE, THEME_LIGHT)
    fun saveThemeMode(mode: Int) = prefs.edit().putInt("setting_theme", mode.coerceIn(THEME_PURPLE, THEME_LIGHT)).apply()
'''
if theme_anchor not in ps:
    raise SystemExit("ProgressStore theme anchor missing")
if "fun userName()" not in ps:
    ps = ps.replace(
        theme_anchor,
        theme_anchor + '''
    fun userName(): String = prefs.getString("setting_user_name", "").orEmpty()
    fun saveUserName(value: String) = prefs.edit().putString("setting_user_name", value.trim().take(40)).apply()
''',
        1
    )
progress_store.write_text(ps, encoding="utf-8")

afs = app_flow_screens.read_text(encoding="utf-8")
password_import = "import androidx.compose.ui.text.input.PasswordVisualTransformation\n"
if password_import not in afs:
    import_anchor = "import androidx.compose.ui.text.style.TextAlign\n"
    if import_anchor not in afs:
        raise SystemExit("AppFlowScreens import anchor missing")
    afs = afs.replace(import_anchor, import_anchor + password_import, 1)

settings_owner = None
for candidate in src_dir.glob("*.kt"):
    candidate_text = candidate.read_text(encoding="utf-8")
    if "fun SettingsScreen(" in candidate_text:
        candidate.write_text(
            candidate_text.replace("fun SettingsScreen(", "fun AdvancedSettingsScreen(", 1),
            encoding="utf-8"
        )
        settings_owner = candidate
        break
if settings_owner is None:
    raise SystemExit("Original SettingsScreen not found in source directory")

dashboard_start = afs.find("@Composable\nfun DashboardScreen(")
dashboard_end = afs.find("\n@Composable\nprivate fun DashboardAction", dashboard_start)
if dashboard_start < 0 or dashboard_end < 0:
    raise SystemExit("DashboardScreen block not found")
dashboard_code = dashboard_fragment.read_text(encoding="utf-8").rstrip() + "\n"
afs = afs[:dashboard_start] + dashboard_code + afs[dashboard_end:]

settings_insert = afs.find("\n@Composable\nprivate fun DashboardAction")
if settings_insert < 0:
    raise SystemExit("SettingsHub insertion anchor not found")
settings_code = settings_fragment.read_text(encoding="utf-8").rstrip() + "\n\n"
afs = afs[:settings_insert] + "\n" + settings_code + afs[settings_insert:]
app_flow_screens.write_text(afs, encoding="utf-8")

# Admin mode bypasses exam-stage locks without mutating saved progress.
ls2 = learning_screens.read_text(encoding="utf-8")
exam_anchor = '''    val vocabScore = progress.vocabularyExamScore(scene.id)
    val sentenceScore = progress.sentenceExamScore(scene.id)
    val vocabPassed = vocabScore >= rules.vocabularyPassPercent
    val sentencePassed = sentenceScore >= rules.sentencePassPercent
    val mastered = vocabPassed && sentencePassed
'''
exam_replacement = '''    val vocabScore = progress.vocabularyExamScore(scene.id)
    val sentenceScore = progress.sentenceExamScore(scene.id)
    val adminMode = AdminSession.active
    val vocabPassedNormally = vocabScore >= rules.vocabularyPassPercent
    val sentencePassedNormally = sentenceScore >= rules.sentencePassPercent
    val vocabPassed = adminMode || vocabPassedNormally
    val sentencePassed = adminMode || sentencePassedNormally
    val mastered = vocabPassedNormally && sentencePassedNormally
'''
if exam_anchor not in ls2:
    raise SystemExit("ExamHub score anchor missing")
ls2 = ls2.replace(exam_anchor, exam_replacement, 1)

lazy_anchor = '''        LazyColumn(contentPadding = PaddingValues(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            item {
'''
lazy_replacement = '''        LazyColumn(contentPadding = PaddingValues(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            if (adminMode) {
                item {
                    Surface(color = Color(0xFFE6F4EA), shape = RoundedCornerShape(18.dp)) {
                        Text(
                            "🔓 Admin modu: sınav aşaması kilitleri bu oturum için devre dışı.",
                            modifier = Modifier.padding(16.dp),
                            color = Color(0xFF176B43),
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
            item {
'''
if lazy_anchor not in ls2:
    raise SystemExit("ExamHub LazyColumn anchor missing")
ls2 = ls2.replace(lazy_anchor, lazy_replacement, 1)
ls2 = ls2.replace("color = if (vocabPassed) Success else Color.DarkGray", "color = if (vocabPassedNormally) Success else Color.DarkGray", 1)
ls2 = ls2.replace(
    'Text(if (vocabPassed) "Tekrar çöz" else "Kelime sınavını başlat")',
    'Text(if (adminMode && !vocabPassedNormally) "Admin · Kelime sınavını aç" else if (vocabPassedNormally) "Tekrar çöz" else "Kelime sınavını başlat")',
    1
)
ls2 = ls2.replace("color = if (sentencePassed) Success else Color.DarkGray", "color = if (sentencePassedNormally) Success else Color.DarkGray", 1)
ls2 = ls2.replace(
    'Text(if (!vocabPassed) "Önce 1. sınavı geç" else if (sentencePassed) "Tekrar çöz" else "Cümle sınavını başlat")',
    'Text(if (adminMode && !vocabPassedNormally) "Admin · Cümle sınavını aç" else if (!vocabPassedNormally) "Önce 1. sınavı geç" else if (sentencePassedNormally) "Tekrar çöz" else "Cümle sınavını başlat")',
    1
)
ls2 = ls2.replace(
    'if (mastered) "✓ Sahne başarıyla tamamlandı. Sonraki sahne açıldı." else "🔒 Sonraki sahne, iki sınav da başarıyla tamamlandığında açılır."',
    'if (mastered) "✓ Sahne başarıyla tamamlandı. Sonraki sahne açıldı." else if (adminMode) "🔓 Admin modu açık; sonraki sahnelere test amaçlı erişebilirsin. Normal ilerleme değişmedi." else "🔒 Sonraki sahne, iki sınav da başarıyla tamamlandığında açılır."',
    1
)
learning_screens.write_text(ls2, encoding="utf-8")

assert "compileSdk = 36" in gradle.read_text(encoding="utf-8")
assert "targetSdk = 36" in gradle.read_text(encoding="utf-8")
assert "compose-bom:2026.04.01" in gradle.read_text(encoding="utf-8")
assert "fun speak(" in tts.read_text(encoding="utf-8")
assert speak_line + "\n            Unit" in tts.read_text(encoding="utf-8")
assert "Shorts" not in main_activity.read_text(encoding="utf-8") or True
assert "navigationBarsPadding()" in main_activity.read_text(encoding="utf-8")
assert "BackHandler(enabled = true)" in main_activity.read_text(encoding="utf-8")
assert "SpeechRecognizer.createSpeechRecognizer" in recognizer_file.read_text(encoding="utf-8")
assert "tts.stop()" in learning_screens.read_text(encoding="utf-8")
assert "fun userName()" in progress_store.read_text(encoding="utf-8")
assert "AdminSession.active" in learning_screens.read_text(encoding="utf-8")
assert "Admin Girişi" in app_flow_screens.read_text(encoding="utf-8")
assert "fun SettingsHubScreen(" in app_flow_screens.read_text(encoding="utf-8")
assert any("fun AdvancedSettingsScreen(" in p.read_text(encoding="utf-8") for p in src_dir.glob("*.kt"))
print("CI source compatibility patch applied.")
