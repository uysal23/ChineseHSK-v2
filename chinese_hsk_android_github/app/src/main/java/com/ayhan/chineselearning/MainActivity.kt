package com.ayhan.chineselearning

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { ChineseJourneyApp() }
    }
}

private val PurpleTop = Color(0xFF4B2B73)
private val PurpleBottom = Color(0xFF211132)
private val Accent = Color(0xFFFFC857)

private enum class SceneMode { STORY, FLASHCARDS, COMPREHENSION, PRONUNCIATION, INTERACTIVE, SENTENCE_PRACTICE, EXAM_HUB, EXAM_VOCAB, EXAM_SENTENCE }

private enum class RootMode { WELCOME, DASHBOARD, LEVELS, PLACEMENT, DAILY_REVIEW, WEAK_WORDS, HABITS, PROGRESS, SETTINGS, SYSTEM_CHECK }

@Composable
fun ChineseJourneyApp() {
    val context = LocalContext.current
    val repo = remember { ContentRepository(context) }
    val progress = remember { ProgressStore(context) }
    val levels = remember { repo.loadLevels() }
    var selectedLevel by remember { mutableStateOf<LevelInfo?>(null) }
    var selectedScene by remember { mutableStateOf<SceneInfo?>(null) }
    var sceneMode by remember { mutableStateOf(SceneMode.STORY) }
    var showFavorites by remember { mutableStateOf(false) }
    var progressVersion by remember { mutableIntStateOf(0) }
    var onboardingComplete by remember { mutableStateOf(progress.isOnboardingComplete()) }
    var themeMode by remember { mutableIntStateOf(progress.themeMode()) }
    var rootMode by remember {
        mutableStateOf(if (progress.isOnboardingComplete()) RootMode.DASHBOARD else RootMode.WELCOME)
    }
    LaunchedEffect(Unit) {
        if (progress.studyReminderEnabled()) {
            StudyReminderScheduler.schedule(context, progress.studyReminderHour(), progress.studyReminderMinute())
        }
    }

    fun openScene(scene: SceneInfo) {
        if (scene.isOpenable && progress.isSceneUnlocked(scene.level, scene.number)) {
            selectedScene = repo.loadScene(scene.level, scene.id)
            progress.saveLastScene(scene.id)
            sceneMode = SceneMode.STORY
        }
    }

    fun continueLearning() {
        val lastId = progress.lastSceneId()
        if (lastId.isNotBlank()) {
            val levelId = lastId.substringAfter("ZH_").substringBefore("_SC")
            val meta = runCatching { repo.loadSceneIndex(levelId).firstOrNull { it.id == lastId } }.getOrNull()
            if (meta != null && progress.isSceneUnlocked(meta.level, meta.number)) {
                openScene(meta)
                return
            }
        }
        val start = progress.placementStartLevel()
        for (levelNo in start..6) {
            val levelId = "HSK$levelNo"
            val candidate = repo.loadSceneIndex(levelId).firstOrNull {
                progress.isSceneUnlocked(levelId, it.number) && !progress.isSceneMastered(it.id)
            }
            if (candidate != null) {
                openScene(candidate)
                return
            }
        }
        val finalScene = repo.loadSceneIndex("HSK6").lastOrNull()
        if (finalScene != null) openScene(finalScene)
    }

    val appColorScheme = when (themeMode) {
        ProgressStore.THEME_DARK -> darkColorScheme(
            primary = Color(0xFF7E57A6), secondary = Accent, background = Color(0xFF121016), surface = Color(0xFF1D1922)
        )
        ProgressStore.THEME_LIGHT -> lightColorScheme(
            primary = PurpleTop, secondary = Color(0xFFE5A900), background = Color(0xFFF7F3FA), surface = Color.White
        )
        else -> darkColorScheme(
            primary = PurpleTop, secondary = Accent, background = PurpleBottom, surface = Color(0xFF2B193C)
        )
    }

    MaterialTheme(colorScheme = appColorScheme) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Brush.verticalGradient(listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.background)))
        ) {
            when {
                !onboardingComplete && rootMode != RootMode.PLACEMENT -> WelcomeScreen(
                    onStartZero = {
                        progress.completeOnboarding(1)
                        onboardingComplete = true
                        rootMode = RootMode.DASHBOARD
                        progressVersion++
                    },
                    onPlacement = { rootMode = RootMode.PLACEMENT }
                )
                rootMode == RootMode.PLACEMENT && selectedScene == null && selectedLevel == null && !showFavorites -> PlacementTestScreen(
                    onBack = { rootMode = if (onboardingComplete) RootMode.DASHBOARD else RootMode.WELCOME },
                    onComplete = { level, score, total ->
                        progress.savePlacementResult(level, score, total)
                        onboardingComplete = true
                        progressVersion++
                        rootMode = RootMode.DASHBOARD
                    }
                )
                rootMode == RootMode.DAILY_REVIEW && selectedScene == null && selectedLevel == null && !showFavorites -> DailyReviewScreen(
                    repo = repo,
                    progress = progress,
                    onBack = { rootMode = RootMode.DASHBOARD }
                )
                rootMode == RootMode.WEAK_WORDS && selectedScene == null && selectedLevel == null && !showFavorites -> WeakWordsScreen(
                    repo = repo,
                    progress = progress,
                    onBack = { rootMode = RootMode.DASHBOARD }
                )
                rootMode == RootMode.HABITS && selectedScene == null && selectedLevel == null && !showFavorites -> StudyHabitsScreen(
                    progress = progress,
                    onBack = { rootMode = RootMode.DASHBOARD }
                )
                rootMode == RootMode.PROGRESS && selectedScene == null && selectedLevel == null && !showFavorites -> ProgressOverviewScreen(
                    progress = progress,
                    onBack = { rootMode = RootMode.DASHBOARD }
                )
                rootMode == RootMode.SYSTEM_CHECK && selectedScene == null && selectedLevel == null && !showFavorites -> SystemCheckScreen(
                    repo = repo,
                    progress = progress,
                    onBack = { rootMode = RootMode.DASHBOARD }
                )
                rootMode == RootMode.SETTINGS && selectedScene == null && selectedLevel == null && !showFavorites -> SettingsScreen(
                    progress = progress,
                    onBack = { rootMode = RootMode.DASHBOARD },
                    onThemeChanged = { mode ->
                        themeMode = mode
                        progressVersion++
                    },
                    onDataChanged = {
                        onboardingComplete = progress.isOnboardingComplete()
                        themeMode = progress.themeMode()
                        progressVersion++
                    }
                )
                showFavorites -> FavoritesScreen(repo, progress) { showFavorites = false }
                selectedScene != null && sceneMode == SceneMode.FLASHCARDS -> FlashCardScreen(
                    title = "Kelime Çalışması · ${selectedScene!!.titleTr}",
                    cards = selectedScene!!.learning.vocabularyCards,
                    progress = progress,
                    onBack = { sceneMode = SceneMode.STORY }
                )
                selectedScene != null && sceneMode == SceneMode.COMPREHENSION -> ComprehensionScreen(
                    scene = selectedScene!!,
                    onBack = { sceneMode = SceneMode.STORY }
                )
                selectedScene != null && sceneMode == SceneMode.PRONUNCIATION -> PronunciationPracticeScreen(
                    scene = selectedScene!!,
                    progress = progress,
                    onBack = { sceneMode = SceneMode.STORY }
                )
                selectedScene != null && sceneMode == SceneMode.INTERACTIVE -> InteractiveDialogueScreen(
                    scene = selectedScene!!,
                    onBack = { sceneMode = SceneMode.STORY }
                )
                selectedScene != null && sceneMode == SceneMode.SENTENCE_PRACTICE -> SentencePracticeScreen(
                    scene = selectedScene!!,
                    onBack = { sceneMode = SceneMode.STORY }
                )
                selectedScene != null && sceneMode == SceneMode.EXAM_HUB -> ExamHubScreen(
                    scene = selectedScene!!,
                    progress = progress,
                    onBack = { sceneMode = SceneMode.STORY },
                    onVocabularyExam = { sceneMode = SceneMode.EXAM_VOCAB },
                    onSentenceExam = { sceneMode = SceneMode.EXAM_SENTENCE }
                )
                selectedScene != null && sceneMode == SceneMode.EXAM_VOCAB -> VocabularyExamScreen(
                    scene = selectedScene!!,
                    progress = progress,
                    onBack = { sceneMode = SceneMode.EXAM_HUB },
                    onProgressChanged = { progressVersion++ }
                )
                selectedScene != null && sceneMode == SceneMode.EXAM_SENTENCE -> SentenceExamScreen(
                    scene = selectedScene!!,
                    progress = progress,
                    onBack = { sceneMode = SceneMode.EXAM_HUB },
                    onProgressChanged = { progressVersion++ }
                )
                selectedScene != null -> SceneScreen(
                    scene = selectedScene!!,
                    progress = progress,
                    progressVersion = progressVersion,
                    onBack = {
                        selectedScene = null
                        sceneMode = SceneMode.STORY
                    },
                    onFlashCards = { sceneMode = SceneMode.FLASHCARDS },
                    onComprehension = { sceneMode = SceneMode.COMPREHENSION },
                    onPronunciation = { sceneMode = SceneMode.PRONUNCIATION },
                    onInteractive = { sceneMode = SceneMode.INTERACTIVE },
                    onSentencePractice = { sceneMode = SceneMode.SENTENCE_PRACTICE },
                    onExam = { sceneMode = SceneMode.EXAM_HUB }
                )
                selectedLevel != null -> SceneListScreen(
                    level = selectedLevel!!,
                    scenes = remember(selectedLevel!!.id) { repo.loadSceneIndex(selectedLevel!!.id) },
                    progress = progress,
                    progressVersion = progressVersion,
                    onBack = { selectedLevel = null },
                    onScene = { item -> openScene(item) }
                )
                rootMode == RootMode.LEVELS -> LevelScreen(
                    levels = levels,
                    onLevel = { selectedLevel = it },
                    onFavorites = { showFavorites = true },
                    onBack = { rootMode = RootMode.DASHBOARD }
                )
                else -> DashboardScreen(
                    levels = levels,
                    progress = progress,
                    progressVersion = progressVersion,
                    onContinue = { continueLearning() },
                    onLevels = { rootMode = RootMode.LEVELS },
                    onFavorites = { showFavorites = true },
                    onDailyReview = { rootMode = RootMode.DAILY_REVIEW },
                    onWeakWords = { rootMode = RootMode.WEAK_WORDS },
                    onHabits = { rootMode = RootMode.HABITS },
                    onProgress = { rootMode = RootMode.PROGRESS },
                    onSettings = { rootMode = RootMode.SETTINGS },
                    onSystemCheck = { rootMode = RootMode.SYSTEM_CHECK },
                    onPlacement = { rootMode = RootMode.PLACEMENT }
                )
            }
        }
    }
}

@Composable
private fun Header(title: String, subtitle: String? = null, onBack: (() -> Unit)? = null) {
    Column(Modifier.fillMaxWidth().padding(20.dp)) {
        if (onBack != null) {
            Text(
                text = "← Geri",
                color = MaterialTheme.colorScheme.secondary,
                modifier = Modifier.clickable { onBack() }.padding(bottom = 12.dp),
                fontWeight = FontWeight.SemiBold
            )
        }
        Text(title, color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
        if (subtitle != null) {
            Spacer(Modifier.height(6.dp))
            Text(subtitle, color = Color.White.copy(alpha = 0.75f), fontSize = 15.sp)
        }
    }
}

@Composable
private fun LevelScreen(levels: List<LevelInfo>, onLevel: (LevelInfo) -> Unit, onFavorites: () -> Unit, onBack: (() -> Unit)? = null) {
    Column(Modifier.fillMaxSize()) {
        Header("Çince Yolculuğu", "HSK1'den HSK6'ya · Basitleştirilmiş Çince · Offline", onBack)
        Button(
            onClick = onFavorites,
            modifier = Modifier.padding(horizontal = 18.dp).fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
        ) {
            Text("★ Favori Kelimelerimi Çalış", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
        }
        Spacer(Modifier.height(8.dp))
        LazyColumn(
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(levels) { level ->
                Card(
                    modifier = Modifier.fillMaxWidth().clickable { onLevel(level) },
                    shape = RoundedCornerShape(20.dp),
                    colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.95f))
                ) {
                    Column(Modifier.padding(18.dp)) {
                        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                            Text(level.title, fontSize = 23.sp, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.weight(1f))
                            Text("${level.completeScenes}/${level.sceneCount} tam", color = Color.DarkGray)
                        }
                        Spacer(Modifier.height(8.dp))
                        Text(level.storyArc, color = Color(0xFF4C4652))
                        if (level.blueprintReadyScenes > 0) {
                            Spacer(Modifier.height(5.dp))
                            Text("${level.blueprintReadyScenes}/${level.sceneCount} sahnenin planı hazır", color = MaterialTheme.colorScheme.primary, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                        }
                        Spacer(Modifier.height(10.dp))
                        LinearProgressIndicator(
                            progress = { if (level.sceneCount == 0) 0f else level.completeScenes.toFloat() / level.sceneCount },
                            modifier = Modifier.fillMaxWidth(),
                            color = MaterialTheme.colorScheme.primary,
                            trackColor = Color(0xFFE7DDF0)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun SceneListScreen(
    level: LevelInfo,
    scenes: List<SceneInfo>,
    progress: ProgressStore,
    progressVersion: Int,
    onBack: () -> Unit,
    onScene: (SceneInfo) -> Unit
) {
    Column(Modifier.fillMaxSize()) {
        Header(level.title, "Sahneler sınav başarısına göre sırayla açılır", onBack)
        LazyColumn(
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(9.dp)
        ) {
            items(scenes) { scene ->
                val unlocked = remember(scene.id, progressVersion) { progress.isSceneUnlocked(scene.level, scene.number) }
                val mastered = remember(scene.id, progressVersion) { progress.isSceneMastered(scene.id) }
                val openable = scene.isOpenable && unlocked
                Card(
                    modifier = Modifier.fillMaxWidth().clickable(enabled = openable) { onScene(scene) },
                    colors = CardDefaults.cardColors(
                        containerColor = if (openable) Color.White else Color.White.copy(alpha = 0.58f)
                    ),
                    shape = RoundedCornerShape(16.dp)
                ) {
                    Row(Modifier.padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Surface(shape = RoundedCornerShape(12.dp), color = if (unlocked) MaterialTheme.colorScheme.primary else Color.Gray) {
                            Text(
                                "%02d".format(scene.number),
                                color = Color.White,
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
                                fontWeight = FontWeight.Bold
                            )
                        }
                        Spacer(Modifier.width(14.dp))
                        Column(Modifier.weight(1f)) {
                            Text(scene.titleZh, fontWeight = FontWeight.Bold, color = Color(0xFF271936))
                            Text(scene.titleTr, color = Color.DarkGray, fontSize = 13.sp)
                        }
                        Text(
                            when {
                                mastered -> "✓ Geçildi"
                                !unlocked -> "🔒 Kilitli"
                                scene.complete -> "Açık"
                                scene.productionStatus == "dialogue_draft" -> "Taslak"
                                scene.productionStatus == "blueprint_ready" -> "Plan hazır"
                                else -> "Planlı"
                            },
                            color = if (mastered) Color(0xFF18794E) else if (unlocked) MaterialTheme.colorScheme.primary else Color.Gray,
                            fontSize = 12.sp,
                            textAlign = TextAlign.End
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun SceneScreen(
    scene: SceneInfo,
    progress: ProgressStore,
    progressVersion: Int,
    onBack: () -> Unit,
    onFlashCards: () -> Unit,
    onComprehension: () -> Unit,
    onPronunciation: () -> Unit,
    onInteractive: () -> Unit,
    onSentencePractice: () -> Unit,
    onExam: () -> Unit
) {
    val context = LocalContext.current
    val repo = remember { ContentRepository(context) }
    val audioPlayer = remember(scene.id) { DialogueAudioPlayer(context) }
    val soundscape = remember(scene.id) { SceneSoundscapePlayer(context) }
    val characterProfiles = remember { repo.loadCharacters().associateBy { it.nameZh } }
    val locationProfiles = remember { repo.loadLocations().associateBy { it.id } }
    val location = remember(scene.id) { locationProfiles[scene.production.locationId] }
    DisposableEffect(scene.id) {
        soundscape.start(scene)
        onDispose {
            audioPlayer.shutdown()
            soundscape.shutdown()
        }
    }

    var showPinyin by remember(scene.id) {
        mutableStateOf(
            when (progress.pinyinDisplayMode()) {
                ProgressStore.DISPLAY_ON -> true
                ProgressStore.DISPLAY_OFF -> false
                else -> scene.learning.defaultSubtitleMode.contains("PINYIN")
            }
        )
    }
    var showTurkish by remember(scene.id) {
        mutableStateOf(
            when (progress.turkishDisplayMode()) {
                ProgressStore.DISPLAY_ON -> true
                ProgressStore.DISPLAY_OFF -> false
                else -> scene.learning.defaultSubtitleMode.contains("TR")
            }
        )
    }
    var currentIndex by remember(scene.id) {
        mutableIntStateOf(
            progress.dialoguePosition(scene.id).coerceIn(0, (scene.dialogues.size - 1).coerceAtLeast(0))
        )
    }
    var autoPlay by remember(scene.id) { mutableStateOf(progress.autoPlayDefault()) }
    var speed by remember(scene.id) {
        mutableFloatStateOf(progress.playbackSpeed(scene.learning.defaultSpeechSpeed))
    }
    var narratorPlaying by remember(scene.id) { mutableStateOf(false) }
    var narratorAutoStarted by remember(scene.id) { mutableStateOf(false) }

    val rules = scene.learning.examRules
    val vocabScore = remember(progressVersion, scene.id) { progress.vocabularyExamScore(scene.id) }
    val sentenceScore = remember(progressVersion, scene.id) { progress.sentenceExamScore(scene.id) }
    val mastered = remember(progressVersion, scene.id) { progress.isSceneMastered(scene.id) }
    val current = scene.dialogues.getOrNull(currentIndex)

    LaunchedEffect(currentIndex, scene.id) {
        progress.saveDialoguePosition(scene.id, currentIndex)
    }

    LaunchedEffect(currentIndex, autoPlay, speed, scene.id) {
        if (autoPlay && current != null) {
            audioPlayer.playDialogue(current, speed) {
                if (currentIndex < scene.dialogues.lastIndex) {
                    currentIndex += 1
                } else {
                    autoPlay = false
                }
            }
        }
    }

    LaunchedEffect(scene.id) {
        val narrator = scene.production.narrator
        if (!narratorAutoStarted && currentIndex == 0 && narrator.zh.isNotBlank()) {
            narratorAutoStarted = true
            narratorPlaying = true
            audioPlayer.playNarrator(scene.id, narrator, 0.90f) {
                narratorPlaying = false
                autoPlay = true
            }
        }
    }

    Column(Modifier.fillMaxSize()) {
        Header(scene.titleZh, scene.titleTr, onBack)

        if (scene.dialogues.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(18.dp), contentAlignment = Alignment.Center) {
                Surface(color = Color.White.copy(alpha = 0.94f), shape = RoundedCornerShape(20.dp)) {
                    Text(
                        "Bu sahnenin tam diyalogları henüz üretim aşamasında.",
                        modifier = Modifier.padding(22.dp),
                        color = MaterialTheme.colorScheme.primary
                    )
                }
            }
            return@Column
        }

        LazyColumn(
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 8.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Card(
                    colors = CardDefaults.cardColors(containerColor = Color(0xFF16111E).copy(alpha = 0.98f)),
                    shape = RoundedCornerShape(24.dp)
                ) {
                    Column(Modifier.padding(18.dp)) {
                        SceneStage(
                            scene = scene,
                            location = location,
                            characterProfiles = characterProfiles,
                            activeSpeaker = current?.speaker.orEmpty()
                        )
                        Spacer(Modifier.height(14.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Surface(
                                shape = RoundedCornerShape(18.dp),
                                color = MaterialTheme.colorScheme.secondary,
                                modifier = Modifier.size(58.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Text(
                                        current?.speaker?.take(1) ?: "中",
                                        color = MaterialTheme.colorScheme.primary,
                                        fontSize = 25.sp,
                                        fontWeight = FontWeight.Bold
                                    )
                                }
                            }
                            Spacer(Modifier.width(13.dp))
                            Column(Modifier.weight(1f)) {
                                Text(current?.speaker.orEmpty(), color = MaterialTheme.colorScheme.secondary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                                Text(
                                    "Replik ${currentIndex + 1} / ${scene.dialogues.size}",
                                    color = Color.White.copy(alpha = 0.65f),
                                    fontSize = 12.sp
                                )
                            }
                            Text(
                                if (autoPlay) "▶ OTOMATİK" else "MANUEL",
                                color = if (autoPlay) MaterialTheme.colorScheme.secondary else Color.White.copy(alpha = 0.55f),
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }

                        Spacer(Modifier.height(18.dp))
                        LinearProgressIndicator(
                            progress = { (currentIndex + 1).toFloat() / scene.dialogues.size.coerceAtLeast(1) },
                            modifier = Modifier.fillMaxWidth(),
                            color = MaterialTheme.colorScheme.secondary,
                            trackColor = Color.White.copy(alpha = 0.14f)
                        )
                        Spacer(Modifier.height(20.dp))

                        Text(
                            current?.zh.orEmpty(),
                            color = Color.White,
                            fontSize = 27.sp,
                            lineHeight = 38.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                        if (showPinyin) {
                            Text(
                                current?.pinyin.orEmpty(),
                                color = Color(0xFFD8C8E8),
                                fontSize = 17.sp,
                                lineHeight = 25.sp,
                                modifier = Modifier.padding(top = 10.dp)
                            )
                        }
                        if (showTurkish) {
                            Text(
                                current?.tr.orEmpty(),
                                color = Color.White.copy(alpha = 0.78f),
                                fontSize = 16.sp,
                                lineHeight = 24.sp,
                                modifier = Modifier.padding(top = 10.dp)
                            )
                        }

                        Spacer(Modifier.height(20.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            OutlinedButton(
                                onClick = {
                                    autoPlay = false
                                    audioPlayer.stop()
                                    if (currentIndex > 0) currentIndex--
                                },
                                enabled = currentIndex > 0,
                                modifier = Modifier.weight(1f)
                            ) { Text("← Önceki") }

                            Button(
                                onClick = {
                                    if (autoPlay) {
                                        autoPlay = false
                                        audioPlayer.stop()
                                    } else {
                                        autoPlay = true
                                    }
                                },
                                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary),
                                modifier = Modifier.weight(1f)
                            ) {
                                Text(if (autoPlay) "⏸ Duraklat" else "▶ Oynat", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            }

                            OutlinedButton(
                                onClick = {
                                    autoPlay = false
                                    audioPlayer.stop()
                                    if (currentIndex < scene.dialogues.lastIndex) currentIndex++
                                },
                                enabled = currentIndex < scene.dialogues.lastIndex,
                                modifier = Modifier.weight(1f)
                            ) { Text("Sonraki →") }
                        }

                        OutlinedButton(
                            onClick = { current?.let { audioPlayer.playDialogue(it, speed) } },
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp)
                        ) {
                            Text(if (current?.let { audioPlayer.hasAuthoredAudio(it) } == true) "🎧 Karakter Sesini Dinle" else "🔊 Repliği Dinle (Offline TTS)")
                        }
                    }
                }
            }

            item {
                val narrator = scene.production.narrator
                if (narrator.zh.isNotBlank() || narrator.tr.isNotBlank()) {
                    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF6DE))) {
                        Column(Modifier.padding(14.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("🎙 Anlatıcı", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                                Spacer(Modifier.weight(1f))
                                if (narratorPlaying) Text("Konuşuyor…", color = MaterialTheme.colorScheme.primary, fontSize = 11.sp)
                            }
                            if (narrator.zh.isNotBlank()) Text(narrator.zh, color = Color(0xFF34233F), modifier = Modifier.padding(top = 7.dp), fontWeight = FontWeight.SemiBold)
                            if (narrator.tr.isNotBlank()) Text(narrator.tr, color = Color.DarkGray, fontSize = 13.sp, modifier = Modifier.padding(top = 5.dp))
                            OutlinedButton(
                                onClick = {
                                    autoPlay = false
                                    audioPlayer.stop()
                                    narratorPlaying = true
                                    audioPlayer.playNarrator(scene.id, narrator, 0.90f) { narratorPlaying = false }
                                },
                                modifier = Modifier.fillMaxWidth().padding(top = 8.dp)
                            ) { Text("🔊 Sahne Girişini Dinle") }
                        }
                    }
                }
            }

            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.96f))) {
                    Column(Modifier.padding(14.dp)) {
                        Text("Altyazı ve Konuşma", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.height(8.dp))
                        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            FilterChip(selected = showPinyin, onClick = { showPinyin = !showPinyin }, label = { Text("Pinyin") })
                            FilterChip(selected = showTurkish, onClick = { showTurkish = !showTurkish }, label = { Text("TR") })
                        }
                        Spacer(Modifier.height(8.dp))
                        Text("Konuşma hızı: ${"%.2f".format(speed)}x", color = Color.DarkGray, fontSize = 13.sp)
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            listOf(0.75f, 0.85f, 1.0f, 1.15f, 1.25f).forEach { value ->
                                FilterChip(
                                    selected = kotlin.math.abs(speed - value) < 0.01f,
                                    onClick = {
                                        speed = value
                                        progress.savePlaybackSpeed(value)
                                        if (autoPlay) {
                                            autoPlay = false
                                            audioPlayer.stop()
                                        }
                                    },
                                    label = { Text("${value}x", fontSize = 11.sp) }
                                )
                            }
                        }
                        Text(
                            "Ses: hazır karakter sesi varsa onu kullanır; yoksa cihazdaki Mandarin sesi ilk kullanımda yerel cache’e alınır ve sonraki dinlemelerde cache’den oynatılır.",
                            color = Color.Gray,
                            fontSize = 11.sp,
                            modifier = Modifier.padding(top = 6.dp)
                        )
                        Text(
                            "Yerel Mandarin sesleri: ${audioPlayer.offlineVoiceCount()} · Cache: ${audioPlayer.cachedTtsCount()} replik",
                            color = Color.Gray,
                            fontSize = 11.sp,
                            modifier = Modifier.padding(top = 3.dp)
                        )
                    }
                }
            }

            item {
                if (scene.miniAdventureTr.isNotBlank()) {
                    Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.94f))) {
                        Column(Modifier.padding(14.dp)) {
                            Text("Sahne özeti", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            Text(scene.miniAdventureTr, color = Color(0xFF4B4B4B), modifier = Modifier.padding(top = 5.dp))
                            if (scene.learning.communicationGoals.isNotEmpty()) {
                                Text(
                                    "İletişim: ${scene.learning.communicationGoals.joinToString(" · ")}",
                                    color = Color(0xFF4B4B4B),
                                    fontSize = 13.sp,
                                    modifier = Modifier.padding(top = 7.dp)
                                )
                            }
                        }
                    }
                }
            }

            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.96f))) {
                    Column(Modifier.padding(14.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("Sahne Çalışmaları", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                            Spacer(Modifier.weight(1f))
                            if (mastered) Text("✓ TAMAMLANDI", color = Color(0xFF18794E), fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        }
                        Spacer(Modifier.height(10.dp))
                        Button(
                            onClick = onFlashCards,
                            enabled = scene.learning.vocabularyCards.isNotEmpty(),
                            modifier = Modifier.fillMaxWidth()
                        ) { Text("🃏 Kelime Flash Kartları (${scene.learning.vocabularyCards.size})") }

                        OutlinedButton(
                            onClick = onComprehension,
                            enabled = scene.learning.comprehensionQuestions.isNotEmpty(),
                            modifier = Modifier.fillMaxWidth().padding(top = 7.dp)
                        ) { Text("🧠 Anlama Çalışması") }

                        OutlinedButton(
                            onClick = onPronunciation,
                            enabled = scene.learning.pronunciationItems.isNotEmpty(),
                            modifier = Modifier.fillMaxWidth().padding(top = 7.dp)
                        ) { Text("🎙 Telaffuz Çalışması") }

                        OutlinedButton(
                            onClick = onInteractive,
                            enabled = scene.learning.interactiveDialogue.isNotEmpty(),
                            modifier = Modifier.fillMaxWidth().padding(top = 7.dp)
                        ) { Text("💬 Seçimli Diyalog") }

                        OutlinedButton(
                            onClick = onSentencePractice,
                            enabled = scene.learning.sentenceExercises.isNotEmpty(),
                            modifier = Modifier.fillMaxWidth().padding(top = 7.dp)
                        ) { Text("✍ Cümle Alıştırmaları") }

                        Button(
                            onClick = onExam,
                            enabled = scene.learning.vocabularyCards.isNotEmpty() && scene.learning.sentenceExercises.isNotEmpty(),
                            modifier = Modifier.fillMaxWidth().padding(top = 7.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                        ) { Text("🎓 İki Seviyeli Sınav", color = MaterialTheme.colorScheme.primary) }

                        Text(
                            "Kelime sınavı: %$vocabScore / gerekli %${rules.vocabularyPassPercent}",
                            fontSize = 12.sp,
                            color = if (vocabScore >= rules.vocabularyPassPercent) Color(0xFF18794E) else Color.DarkGray,
                            modifier = Modifier.padding(top = 8.dp)
                        )
                        Text(
                            "Cümle sınavı: %$sentenceScore / gerekli %${rules.sentencePassPercent}",
                            fontSize = 12.sp,
                            color = if (sentenceScore >= rules.sentencePassPercent) Color(0xFF18794E) else Color.DarkGray
                        )
                        if (!mastered) {
                            Text(
                                "Sonraki sahne, iki sınav da başarıyla tamamlandıktan sonra açılır.",
                                color = Color(0xFF7A3E00),
                                fontSize = 12.sp,
                                modifier = Modifier.padding(top = 6.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}
