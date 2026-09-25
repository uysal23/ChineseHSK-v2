package com.ayhan.chineselearning

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
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

private val StudyTop = Color(0xFF4B2B73)
private val StudyBottom = Color(0xFF211132)
private val StudyAccent = Color(0xFFFFC857)
private val Success = Color(0xFF18794E)
private val Danger = Color(0xFFB42318)

@Composable
private fun StudyShell(title: String, subtitle: String? = null, onBack: () -> Unit, content: @Composable ColumnScope.() -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(StudyTop, StudyBottom)))
    ) {
        Column(Modifier.fillMaxWidth().padding(20.dp)) {
            Text(
                "← Geri",
                color = StudyAccent,
                modifier = Modifier.clickable { onBack() }.padding(bottom = 12.dp),
                fontWeight = FontWeight.SemiBold
            )
            Text(title, color = Color.White, fontSize = 27.sp, fontWeight = FontWeight.Bold)
            if (!subtitle.isNullOrBlank()) {
                Spacer(Modifier.height(5.dp))
                Text(subtitle, color = Color.White.copy(alpha = 0.78f), fontSize = 14.sp)
            }
        }
        content()
    }
}

@Composable
fun FlashCardScreen(
    title: String,
    cards: List<VocabularyCard>,
    progress: ProgressStore,
    onBack: () -> Unit
) {
    var index by remember(cards.size) { mutableIntStateOf(0) }
    var flipped by remember(index) { mutableStateOf(false) }
    var favoriteVersion by remember { mutableIntStateOf(0) }
    val context = LocalContext.current
    val tts = remember { MandarinTtsPlayer(context) }
    DisposableEffect(Unit) { onDispose { tts.shutdown() } }
    LaunchedEffect(Unit) { progress.recordStudyActivity() }

    StudyShell(title, "Kartı çevir · ileri/geri git · favorile", onBack) {
        if (cards.isEmpty()) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("Bu sahne için kelime kartları henüz hazırlanmadı.", color = Color.White)
            }
            return@StudyShell
        }
        if (index >= cards.size) index = cards.lastIndex
        val card = cards[index]
        val isFavorite = remember(card.id, favoriteVersion) { progress.isFavorite(card.id) }
        val isDifficult = remember(card.id, favoriteVersion) { progress.isWordDifficult(card.id) }

        Column(
            Modifier.fillMaxSize().padding(horizontal = 18.dp, vertical = 8.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("${index + 1} / ${cards.size}", color = Color.White.copy(alpha = 0.8f))
            Spacer(Modifier.height(10.dp))
            Card(
                modifier = Modifier.fillMaxWidth().weight(1f).clickable { flipped = !flipped },
                shape = RoundedCornerShape(28.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White)
            ) {
                Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(card.zh, fontSize = 44.sp, fontWeight = FontWeight.Bold, color = StudyTop, textAlign = TextAlign.Center)
                        if (flipped) {
                            Spacer(Modifier.height(18.dp))
                            Text(card.pinyin, fontSize = 22.sp, color = Color(0xFF62546B), textAlign = TextAlign.Center)
                            Spacer(Modifier.height(8.dp))
                            Text(card.tr, fontSize = 21.sp, fontWeight = FontWeight.SemiBold, textAlign = TextAlign.Center)
                            if (card.exampleZh.isNotBlank()) {
                                HorizontalDivider(Modifier.padding(vertical = 18.dp))
                                Text(card.exampleZh, fontSize = 21.sp, textAlign = TextAlign.Center)
                                if (card.examplePinyin.isNotBlank()) Text(card.examplePinyin, color = Color.Gray, textAlign = TextAlign.Center)
                                if (card.exampleTr.isNotBlank()) Text(card.exampleTr, color = Color.DarkGray, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 5.dp))
                            }
                        } else {
                            Spacer(Modifier.height(14.dp))
                            Text("Anlam ve örnek için karta dokun", color = Color.Gray)
                        }
                    }
                }
            }
            Spacer(Modifier.height(14.dp))
            OutlinedButton(
                onClick = { tts.speak(card.zh, "VOCAB", 0.82f) },
                modifier = Modifier.fillMaxWidth()
            ) { Text("🔊 Kelimeyi Dinle") }
            Spacer(Modifier.height(8.dp))
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { progress.toggleFavorite(card.id); favoriteVersion++ },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = if (isFavorite) StudyAccent else Color.White.copy(alpha = 0.18f))
                ) {
                    Text(if (isFavorite) "★ Favori" else "☆ Favorile", color = if (isFavorite) StudyTop else Color.White)
                }
                Button(
                    onClick = { progress.markWordDifficult(card.id, !isDifficult); favoriteVersion++ },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = if (isDifficult) Color(0xFFFFD7D2) else Color.White.copy(alpha = 0.18f))
                ) {
                    Text(if (isDifficult) "⚑ Zor" else "⚐ Zor İşaretle", color = if (isDifficult) Danger else Color.White)
                }
            }
            Spacer(Modifier.height(10.dp))
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedButton(
                    onClick = { if (index > 0) index-- },
                    enabled = index > 0,
                    modifier = Modifier.weight(1f)
                ) { Text("← Önceki") }
                Button(
                    onClick = { if (index < cards.lastIndex) index++ },
                    enabled = index < cards.lastIndex,
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)
                ) { Text("Sonraki →", color = StudyTop) }
            }
            Spacer(Modifier.height(14.dp))
        }
    }
}

@Composable
fun FavoritesScreen(repo: ContentRepository, progress: ProgressStore, onBack: () -> Unit) {
    var version by remember { mutableIntStateOf(0) }
    val favorites = remember(version) {
        val ids = progress.favoriteIds()
        repo.loadAllVocabularyCards().filter { ids.contains(it.card.id) }
    }
    var index by remember(favorites.size) { mutableIntStateOf(0) }
    var flipped by remember(index) { mutableStateOf(false) }
    val context = LocalContext.current
    val tts = remember { MandarinTtsPlayer(context) }
    DisposableEffect(Unit) { onDispose { tts.shutdown() } }

    StudyShell("Favorilerim", "Kaydettiğin kelimeleri istediğin zaman tekrar çalış", onBack) {
        if (favorites.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                Text("Henüz favori kelimen yok. Kelime kartında ☆ simgesine dokunarak ekleyebilirsin.", color = Color.White, textAlign = TextAlign.Center)
            }
            return@StudyShell
        }
        if (index >= favorites.size) index = favorites.lastIndex
        val item = favorites[index]
        val card = item.card
        Column(Modifier.fillMaxSize().padding(horizontal = 18.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text("${item.levelId} · ${item.sceneTitleTr}", color = Color.White.copy(alpha = 0.8f))
            Text("${index + 1} / ${favorites.size}", color = Color.White.copy(alpha = 0.7f), modifier = Modifier.padding(top = 3.dp))
            Spacer(Modifier.height(10.dp))
            Card(
                Modifier.fillMaxWidth().weight(1f).clickable { flipped = !flipped },
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(28.dp)
            ) {
                Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(card.zh, fontSize = 44.sp, fontWeight = FontWeight.Bold, color = StudyTop)
                        if (flipped) {
                            Text(card.pinyin, fontSize = 22.sp, color = Color.Gray, modifier = Modifier.padding(top = 14.dp))
                            Text(card.tr, fontSize = 21.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(top = 6.dp))
                            if (card.exampleZh.isNotBlank()) Text(card.exampleZh, fontSize = 20.sp, modifier = Modifier.padding(top = 18.dp), textAlign = TextAlign.Center)
                            if (card.exampleTr.isNotBlank()) Text(card.exampleTr, color = Color.DarkGray, modifier = Modifier.padding(top = 5.dp), textAlign = TextAlign.Center)
                        }
                    }
                }
            }
            Spacer(Modifier.height(12.dp))
            OutlinedButton(
                onClick = { tts.speak(card.zh, "VOCAB", 0.82f) },
                modifier = Modifier.fillMaxWidth()
            ) { Text("🔊 Kelimeyi Dinle") }
            TextButton(onClick = {
                progress.toggleFavorite(card.id)
                version++
                if (index > 0) index--
            }) { Text("★ Favorilerden çıkar", color = StudyAccent) }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedButton(onClick = { if (index > 0) index-- }, enabled = index > 0, modifier = Modifier.weight(1f)) { Text("← Önceki") }
                Button(onClick = { if (index < favorites.lastIndex) index++ }, enabled = index < favorites.lastIndex, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)) { Text("Sonraki →", color = StudyTop) }
            }
            Spacer(Modifier.height(14.dp))
        }
    }
}

@Composable
fun ComprehensionScreen(scene: SceneInfo, onBack: () -> Unit) {
    val questions = scene.learning.comprehensionQuestions
    var index by remember(scene.id) { mutableIntStateOf(0) }
    var selected by remember(index) { mutableStateOf<Int?>(null) }
    var correctCount by remember(scene.id) { mutableIntStateOf(0) }
    var finished by remember(scene.id) { mutableStateOf(false) }

    StudyShell("Anlama · ${scene.titleTr}", "Sahneyi gerçekten anlayıp anlamadığını kontrol et", onBack) {
        if (questions.isEmpty()) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("Bu sahne için anlama soruları bulunmuyor.", color = Color.White)
            }
            return@StudyShell
        }
        if (finished) {
            Box(Modifier.fillMaxSize().padding(20.dp), contentAlignment = Alignment.Center) {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(24.dp)) {
                    Column(Modifier.padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                        val score = ((correctCount.toFloat() / questions.size) * 100).toInt()
                        Text("Anlama sonucu", color = StudyTop, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                        Text("%$score", color = if (score >= 70) Success else Danger, fontSize = 42.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(vertical = 14.dp))
                        Button(onClick = { index = 0; selected = null; correctCount = 0; finished = false }) { Text("Tekrar Çalış") }
                    }
                }
            }
            return@StudyShell
        }
        val q = questions[index]
        Column(Modifier.fillMaxSize().padding(18.dp)) {
            Text("${index + 1} / ${questions.size}", color = Color.White.copy(alpha = 0.75f))
            Card(
                Modifier.fillMaxWidth().padding(top = 10.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(22.dp)
            ) {
                Column(Modifier.padding(18.dp)) {
                    Text(q.questionTr, color = StudyTop, fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(14.dp))
                    q.optionsTr.forEachIndexed { optionIndex, option ->
                        val chosen = selected == optionIndex
                        val correct = selected != null && optionIndex == q.correctIndex
                        OutlinedButton(
                            onClick = { if (selected == null) { selected = optionIndex; if (optionIndex == q.correctIndex) correctCount++ } },
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            colors = ButtonDefaults.outlinedButtonColors(
                                containerColor = when {
                                    correct -> Color(0xFFE6F4EA)
                                    chosen -> Color(0xFFFFE8E6)
                                    else -> Color.Transparent
                                }
                            )
                        ) { Text(option, color = StudyTop) }
                    }
                    if (selected != null) {
                        Text(
                            if (selected == q.correctIndex) "✓ Doğru" else "Doğru cevap: ${q.optionsTr.getOrElse(q.correctIndex) { "" }}",
                            color = if (selected == q.correctIndex) Success else Danger,
                            modifier = Modifier.padding(top = 10.dp),
                            fontWeight = FontWeight.SemiBold
                        )
                        Button(
                            onClick = {
                                if (index < questions.lastIndex) { index++; selected = null } else finished = true
                            },
                            modifier = Modifier.fillMaxWidth().padding(top = 12.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)
                        ) { Text(if (index < questions.lastIndex) "Sonraki Soru" else "Sonucu Gör", color = StudyTop) }
                    }
                }
            }
        }
    }
}

@Composable
fun PronunciationPracticeScreen(scene: SceneInfo, progress: ProgressStore, onBack: () -> Unit) {
    val context = LocalContext.current
    val items = scene.learning.pronunciationItems
    var index by remember(scene.id) { mutableIntStateOf(0) }
    var recognized by remember(index) { mutableStateOf("") }
    var score by remember(index) { mutableStateOf<Int?>(null) }
    var status by remember(index) { mutableStateOf("") }
    val tts = remember { MandarinTtsPlayer(context) }
    val recognizer = remember { OfflineMandarinRecognizer(context) }
    DisposableEffect(Unit) { onDispose { tts.shutdown(); recognizer.destroy() } }

    fun startRecognition() {
        val item = items.getOrNull(index) ?: return
        recognized = ""
        score = null
        recognizer.start(
            onListening = { status = "Dinliyorum…" },
            onResult = { text ->
                recognized = text
                val value = chineseTextSimilarity(item.zh, text)
                score = value
                progress.savePronunciationBest(item.id, value)
                status = ""
            },
            onError = { message -> status = message }
        )
    }

    val permissionLauncher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) startRecognition() else status = "Mikrofon izni verilmedi."
    }

    StudyShell("Telaffuz · ${scene.titleTr}", "Dinle → tekrar et → çevrimdışı tanıt → karşılaştır", onBack) {
        if (items.isEmpty()) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text("Telaffuz hedefi bulunmuyor.", color = Color.White) }
            return@StudyShell
        }
        if (index >= items.size) index = items.lastIndex
        val item = items[index]
        val best = progress.pronunciationBest(item.id)
        Column(Modifier.fillMaxSize().padding(18.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text("${index + 1} / ${items.size} · En iyi %$best", color = Color.White.copy(alpha = 0.8f))
            Card(
                Modifier.fillMaxWidth().weight(1f).padding(vertical = 10.dp),
                colors = CardDefaults.cardColors(containerColor = Color.White),
                shape = RoundedCornerShape(26.dp)
            ) {
                Column(Modifier.fillMaxSize().padding(22.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center) {
                    Text(item.zh, color = StudyTop, fontSize = 34.sp, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
                    Text(item.pinyin, color = Color(0xFF65566C), fontSize = 20.sp, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 10.dp))
                    Text(item.tr, color = Color.DarkGray, fontSize = 17.sp, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 8.dp))
                    Spacer(Modifier.height(22.dp))
                    Button(onClick = { tts.speak(item.zh, "PRONUNCIATION", 0.78f) }, colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)) {
                        Text("🔊 Dinle", color = StudyTop, fontWeight = FontWeight.Bold)
                    }
                    Spacer(Modifier.height(8.dp))
                    OutlinedButton(onClick = {
                        if (ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED) startRecognition()
                        else permissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
                    }) { Text("🎙 Söyle ve Karşılaştır") }
                    if (status.isNotBlank()) Text(status, color = Danger, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 12.dp))
                    if (recognized.isNotBlank()) {
                        Text("Algılanan: $recognized", color = Color.DarkGray, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 14.dp))
                    }
                    if (score != null) {
                        Text("Metin eşleşmesi: %${score!!}", color = if (score!! >= 60) Success else Danger, fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 8.dp))
                        Text("Not: Bu puan ton analizi değil; cihazın çevrimdışı konuşma tanımasının metin eşleşmesidir.", color = Color.Gray, fontSize = 11.sp, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 5.dp))
                    }
                }
            }
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                OutlinedButton(onClick = { if (index > 0) index-- }, enabled = index > 0, modifier = Modifier.weight(1f)) { Text("← Önceki") }
                Button(onClick = { if (index < items.lastIndex) index++ }, enabled = index < items.lastIndex, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)) { Text("Sonraki →", color = StudyTop) }
            }
        }
    }
}

@Composable
fun InteractiveDialogueScreen(scene: SceneInfo, onBack: () -> Unit) {
    val items = scene.learning.interactiveDialogue
    var index by remember(scene.id) { mutableIntStateOf(0) }
    var selected by remember(index) { mutableStateOf<Int?>(null) }
    var correctCount by remember(scene.id) { mutableIntStateOf(0) }
    val context = LocalContext.current
    val tts = remember { MandarinTtsPlayer(context) }
    DisposableEffect(Unit) { onDispose { tts.shutdown() } }

    StudyShell("Seçimli Diyalog · ${scene.titleTr}", "Doğal ve bağlama uygun cevabı seç", onBack) {
        if (items.isEmpty()) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text("Etkileşimli diyalog bulunmuyor.", color = Color.White) }
            return@StudyShell
        }
        if (index >= items.size) index = items.lastIndex
        val item = items[index]
        val correctIndex = item.options.indexOfFirst { it.correct }
        Column(Modifier.fillMaxSize().padding(18.dp)) {
            Text("${index + 1} / ${items.size} · Doğru: $correctCount", color = Color.White.copy(alpha = 0.8f))
            Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(22.dp), modifier = Modifier.fillMaxWidth().padding(top = 10.dp)) {
                Column(Modifier.padding(18.dp)) {
                    Text(item.promptZh, color = StudyTop, fontSize = 27.sp, fontWeight = FontWeight.Bold)
                    Text(item.promptPinyin, color = Color.Gray, modifier = Modifier.padding(top = 5.dp))
                    Text(item.promptTr, color = Color.DarkGray, modifier = Modifier.padding(top = 5.dp))
                    OutlinedButton(onClick = { tts.speak(item.promptZh, "DIALOGUE_PROMPT", 0.88f) }, modifier = Modifier.padding(top = 8.dp)) { Text("🔊 Soruyu Dinle") }
                    Spacer(Modifier.height(12.dp))
                    item.options.forEachIndexed { optionIndex, option ->
                        val chosen = selected == optionIndex
                        val revealCorrect = selected != null && option.correct
                        OutlinedButton(
                            onClick = { if (selected == null) { selected = optionIndex; if (option.correct) correctCount++ } },
                            modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                            colors = ButtonDefaults.outlinedButtonColors(containerColor = when { revealCorrect -> Color(0xFFE6F4EA); chosen -> Color(0xFFFFE8E6); else -> Color.Transparent })
                        ) {
                            Column(Modifier.fillMaxWidth()) {
                                Text(option.zh, color = StudyTop, fontSize = 18.sp, fontWeight = FontWeight.SemiBold)
                                Text(option.tr, color = Color.Gray, fontSize = 13.sp)
                            }
                        }
                    }
                    if (selected != null) {
                        Text(if (selected == correctIndex) "✓ Uygun cevap" else "En uygun cevap yukarıda yeşil gösterildi.", color = if (selected == correctIndex) Success else Danger, modifier = Modifier.padding(top = 9.dp))
                        Button(
                            onClick = { if (index < items.lastIndex) { index++; selected = null } else { index = 0; selected = null; correctCount = 0 } },
                            modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)
                        ) { Text(if (index < items.lastIndex) "Sonraki Diyalog" else "Baştan Çalış", color = StudyTop) }
                    }
                }
            }
        }
    }
}

@Composable
private fun OrderingEditor(exercise: SentenceExercise, onAnswerReady: (Boolean?) -> Unit) {
    val selectedIndices = remember(exercise.id) { mutableStateListOf<Int>() }
    val selectedTokens = selectedIndices.map { exercise.tokens[it] }
    LaunchedEffect(selectedIndices.toList()) {
        onAnswerReady(if (selectedIndices.size == exercise.tokens.size) selectedTokens == exercise.answerTokens else null)
    }
    if (selectedTokens.isNotEmpty()) {
        Surface(color = Color(0xFFF0EAF5), shape = RoundedCornerShape(14.dp), modifier = Modifier.fillMaxWidth()) {
            Text(selectedTokens.joinToString(" "), modifier = Modifier.padding(14.dp), fontSize = 21.sp, fontWeight = FontWeight.SemiBold)
        }
        Spacer(Modifier.height(12.dp))
    }
    LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        items(exercise.tokens.indices.toList()) { tokenIndex ->
            AssistChip(
                onClick = { if (!selectedIndices.contains(tokenIndex)) selectedIndices.add(tokenIndex) },
                enabled = !selectedIndices.contains(tokenIndex),
                label = { Text(exercise.tokens[tokenIndex], fontSize = 17.sp) }
            )
        }
    }
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
        TextButton(onClick = { if (selectedIndices.isNotEmpty()) selectedIndices.removeAt(selectedIndices.lastIndex); onAnswerReady(null) }) { Text("Geri al") }
        TextButton(onClick = { selectedIndices.clear(); onAnswerReady(null) }) { Text("Sıfırla") }
    }
}

@Composable
private fun FillBlankEditor(exercise: SentenceExercise, onAnswerReady: (Boolean?) -> Unit) {
    var selected by remember(exercise.id) { mutableStateOf<String?>(null) }
    Text(exercise.blankSentenceZh, fontSize = 25.sp, fontWeight = FontWeight.Bold, color = StudyTop)
    Spacer(Modifier.height(12.dp))
    exercise.options.forEach { option ->
        OutlinedButton(
            onClick = { selected = option; onAnswerReady(option == exercise.answer) },
            modifier = Modifier.fillMaxWidth().padding(vertical = 3.dp),
            colors = ButtonDefaults.outlinedButtonColors(containerColor = if (selected == option) Color(0xFFEFE7F5) else Color.Transparent)
        ) { Text(option, fontSize = 18.sp) }
    }
}

@Composable
private fun ExerciseEditor(exercise: SentenceExercise, onAnswerReady: (Boolean?) -> Unit) {
    Text(
        when (exercise.type) {
            "word_order" -> "Kelime sıralama"
            "fill_blank" -> "Boşluk doldurma"
            "sentence_repair" -> "Yanlış sırayı düzelt"
            else -> "Cümle alıştırması"
        },
        color = StudyTop,
        fontWeight = FontWeight.Bold
    )
    Text(exercise.promptTr, color = Color.DarkGray, modifier = Modifier.padding(top = 4.dp, bottom = 12.dp))
    when (exercise.type) {
        "fill_blank" -> FillBlankEditor(exercise, onAnswerReady)
        else -> OrderingEditor(exercise, onAnswerReady)
    }
}

@Composable
fun SentencePracticeScreen(scene: SceneInfo, onBack: () -> Unit) {
    val exercises = scene.learning.sentenceExercises
    var index by remember { mutableIntStateOf(0) }
    var answerCorrect by remember(index) { mutableStateOf<Boolean?>(null) }
    var checked by remember(index) { mutableStateOf(false) }

    StudyShell("Cümle Alıştırması", "${scene.titleTr} · sıralama, boşluk doldurma, düzeltme", onBack) {
        if (exercises.isEmpty()) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text("Bu sahnenin cümle alıştırmaları henüz hazırlanmadı.", color = Color.White) }
            return@StudyShell
        }
        val exercise = exercises[index]
        Card(Modifier.fillMaxWidth().padding(18.dp), colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(22.dp)) {
            Column(Modifier.padding(18.dp)) {
                Text("${index + 1} / ${exercises.size}", color = Color.Gray)
                Spacer(Modifier.height(10.dp))
                key(exercise.id) {
                    ExerciseEditor(exercise) { answerCorrect = it; checked = false }
                }
                if (checked) {
                    Text(
                        if (answerCorrect == true) "✓ Doğru" else "✗ Tekrar dene",
                        color = if (answerCorrect == true) Success else Danger,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(top = 12.dp)
                    )
                }
                Spacer(Modifier.height(10.dp))
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedButton(onClick = { if (index > 0) index-- }, enabled = index > 0, modifier = Modifier.weight(1f)) { Text("← Geri") }
                    Button(onClick = { checked = true }, enabled = answerCorrect != null, modifier = Modifier.weight(1f)) { Text("Kontrol") }
                    Button(onClick = { if (index < exercises.lastIndex) index++ }, enabled = index < exercises.lastIndex && answerCorrect == true, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)) { Text("İleri →", color = StudyTop) }
                }
            }
        }
    }
}

@Composable
fun ExamHubScreen(
    scene: SceneInfo,
    progress: ProgressStore,
    onBack: () -> Unit,
    onVocabularyExam: () -> Unit,
    onSentenceExam: () -> Unit
) {
    val rules = scene.learning.examRules
    val vocabScore = progress.vocabularyExamScore(scene.id)
    val sentenceScore = progress.sentenceExamScore(scene.id)
    val vocabPassed = vocabScore >= rules.vocabularyPassPercent
    val sentencePassed = sentenceScore >= rules.sentencePassPercent
    val mastered = vocabPassed && sentencePassed

    StudyShell("Sahne Sınavı", scene.titleTr, onBack) {
        LazyColumn(contentPadding = PaddingValues(18.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(20.dp)) {
                    Column(Modifier.padding(18.dp)) {
                        Text("1. Seviye · Kelime", fontSize = 21.sp, fontWeight = FontWeight.Bold, color = StudyTop)
                        Text("Başarı şartı: %${rules.vocabularyPassPercent}", color = Color.DarkGray)
                        Text("En iyi sonuç: %$vocabScore", color = if (vocabPassed) Success else Color.DarkGray, modifier = Modifier.padding(top = 6.dp))
                        Button(onClick = onVocabularyExam, modifier = Modifier.fillMaxWidth().padding(top = 12.dp)) { Text(if (vocabPassed) "Tekrar çöz" else "Kelime sınavını başlat") }
                    }
                }
            }
            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(20.dp)) {
                    Column(Modifier.padding(18.dp)) {
                        Text("2. Seviye · Cümle", fontSize = 21.sp, fontWeight = FontWeight.Bold, color = StudyTop)
                        Text("Kelime sıralama · boşluk doldurma · yanlış sırayı düzeltme", color = Color.DarkGray)
                        Text("Başarı şartı: %${rules.sentencePassPercent}", color = Color.DarkGray)
                        Text("En iyi sonuç: %$sentenceScore", color = if (sentencePassed) Success else Color.DarkGray, modifier = Modifier.padding(top = 6.dp))
                        Button(onClick = onSentenceExam, enabled = vocabPassed, modifier = Modifier.fillMaxWidth().padding(top = 12.dp)) {
                            Text(if (!vocabPassed) "Önce 1. sınavı geç" else if (sentencePassed) "Tekrar çöz" else "Cümle sınavını başlat")
                        }
                    }
                }
            }
            item {
                Surface(color = if (mastered) Color(0xFFE6F4EA) else Color.White.copy(alpha = 0.92f), shape = RoundedCornerShape(18.dp)) {
                    Text(
                        if (mastered) "✓ Sahne başarıyla tamamlandı. Sonraki sahne açıldı." else "🔒 Sonraki sahne, iki sınav da başarıyla tamamlandığında açılır.",
                        modifier = Modifier.padding(18.dp),
                        color = if (mastered) Success else StudyTop,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    }
}

private data class VocabularyQuestion(val card: VocabularyCard, val options: List<String>)

private fun buildVocabularyQuestions(cards: List<VocabularyCard>): List<VocabularyQuestion> {
    if (cards.isEmpty()) return emptyList()
    return List(10) { i ->
        val card = cards[i % cards.size]
        val distractors = cards.filter { it.id != card.id }.map { it.tr }.distinct()
        val raw = (listOf(card.tr) + distractors.drop(i % maxOf(1, distractors.size)).plus(distractors).distinct()).take(4)
        val shift = if (raw.isEmpty()) 0 else i % raw.size
        val rotated = if (raw.isEmpty()) emptyList() else List(raw.size) { raw[(it + shift) % raw.size] }
        VocabularyQuestion(card, rotated)
    }
}

@Composable
fun VocabularyExamScreen(scene: SceneInfo, progress: ProgressStore, onBack: () -> Unit, onProgressChanged: () -> Unit) {
    val rules = scene.learning.examRules
    val questions = remember(scene.id) { buildVocabularyQuestions(scene.learning.vocabularyCards) }
    var index by remember { mutableIntStateOf(0) }
    var correct by remember { mutableIntStateOf(0) }
    var selected by remember(index) { mutableStateOf<String?>(null) }
    var finishedScore by remember { mutableStateOf<Int?>(null) }

    StudyShell("1. Seviye · Kelime Sınavı", "Geçme notu %${rules.vocabularyPassPercent}", onBack) {
        if (questions.isEmpty()) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text("Kelime sınavı henüz hazır değil.", color = Color.White) }
            return@StudyShell
        }
        if (finishedScore != null) {
            val passed = finishedScore!! >= rules.vocabularyPassPercent
            Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(24.dp)) {
                    Column(Modifier.padding(26.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("%${finishedScore}", fontSize = 48.sp, fontWeight = FontWeight.Bold, color = if (passed) Success else Danger)
                        Text(if (passed) "Başarılı! 2. seviye sınav açıldı." else "%${rules.vocabularyPassPercent} gerekiyor. Tekrar çalışıp yeniden deneyebilirsin.", textAlign = TextAlign.Center, modifier = Modifier.padding(top = 10.dp))
                        Button(onClick = onBack, modifier = Modifier.padding(top = 18.dp)) { Text("Sınav ekranına dön") }
                    }
                }
            }
            return@StudyShell
        }
        val q = questions[index]
        Card(Modifier.fillMaxWidth().padding(18.dp), colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(22.dp)) {
            Column(Modifier.padding(18.dp)) {
                Text("Soru ${index + 1} / ${questions.size}", color = Color.Gray)
                Text(q.card.zh, fontSize = 38.sp, fontWeight = FontWeight.Bold, color = StudyTop, modifier = Modifier.padding(vertical = 14.dp))
                Text("Bu kelimenin Türkçe anlamı hangisi?", fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.height(10.dp))
                q.options.forEach { option ->
                    OutlinedButton(onClick = { selected = option }, modifier = Modifier.fillMaxWidth().padding(vertical = 3.dp), colors = ButtonDefaults.outlinedButtonColors(containerColor = if (selected == option) Color(0xFFEFE7F5) else Color.Transparent)) { Text(option) }
                }
                Button(
                    onClick = {
                        val answerCorrect = selected == q.card.tr
                        progress.recordWordAnswer(q.card.id, answerCorrect)
                        val newCorrect = correct + if (answerCorrect) 1 else 0
                        if (index == questions.lastIndex) {
                            val score = ((newCorrect.toDouble() / questions.size) * 100).toInt()
                            progress.saveVocabularyExam(scene.id, score, rules.vocabularyPassPercent)
                            onProgressChanged()
                            correct = newCorrect
                            finishedScore = score
                        } else {
                            correct = newCorrect
                            index++
                        }
                    },
                    enabled = selected != null,
                    modifier = Modifier.fillMaxWidth().padding(top = 12.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)
                ) { Text(if (index == questions.lastIndex) "Sınavı bitir" else "Sonraki soru", color = StudyTop) }
            }
        }
    }
}

@Composable
fun SentenceExamScreen(scene: SceneInfo, progress: ProgressStore, onBack: () -> Unit, onProgressChanged: () -> Unit) {
    val rules = scene.learning.examRules
    val source = scene.learning.sentenceExercises
    val questions = remember(scene.id) { if (source.isEmpty()) emptyList() else List(7) { source[it % source.size] } }
    var index by remember { mutableIntStateOf(0) }
    var correct by remember { mutableIntStateOf(0) }
    var currentCorrect by remember(index) { mutableStateOf<Boolean?>(null) }
    var finishedScore by remember { mutableStateOf<Int?>(null) }

    StudyShell("2. Seviye · Cümle Sınavı", "Geçme notu %${rules.sentencePassPercent}", onBack) {
        if (!progress.vocabularyExamPassed(scene.id, rules.vocabularyPassPercent)) {
            Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) { Text("Önce kelime sınavından %${rules.vocabularyPassPercent} almalısın.", color = Color.White, textAlign = TextAlign.Center) }
            return@StudyShell
        }
        if (questions.isEmpty()) {
            Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text("Cümle sınavı henüz hazır değil.", color = Color.White) }
            return@StudyShell
        }
        if (finishedScore != null) {
            val passed = finishedScore!! >= rules.sentencePassPercent
            Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(24.dp)) {
                    Column(Modifier.padding(26.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                        Text("%${finishedScore}", fontSize = 48.sp, fontWeight = FontWeight.Bold, color = if (passed) Success else Danger)
                        Text(if (passed) "Başarılı! Sonraki sahne açıldı." else "%${rules.sentencePassPercent} gerekiyor. Cümle alıştırmasına dönüp tekrar deneyebilirsin.", textAlign = TextAlign.Center, modifier = Modifier.padding(top = 10.dp))
                        Button(onClick = onBack, modifier = Modifier.padding(top = 18.dp)) { Text("Sınav ekranına dön") }
                    }
                }
            }
            return@StudyShell
        }
        val exercise = questions[index]
        Card(Modifier.fillMaxWidth().padding(18.dp), colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(22.dp)) {
            Column(Modifier.padding(18.dp)) {
                Text("Soru ${index + 1} / ${questions.size}", color = Color.Gray)
                Spacer(Modifier.height(10.dp))
                key("exam_${index}_${exercise.id}") {
                    ExerciseEditor(exercise) { currentCorrect = it }
                }
                Button(
                    onClick = {
                        val newCorrect = correct + if (currentCorrect == true) 1 else 0
                        if (index == questions.lastIndex) {
                            val score = ((newCorrect.toDouble() / questions.size) * 100).toInt()
                            progress.saveSentenceExam(scene.id, score, rules.vocabularyPassPercent, rules.sentencePassPercent)
                            onProgressChanged()
                            correct = newCorrect
                            finishedScore = score
                        } else {
                            correct = newCorrect
                            index++
                        }
                    },
                    enabled = currentCorrect != null,
                    modifier = Modifier.fillMaxWidth().padding(top = 14.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = StudyAccent)
                ) { Text(if (index == questions.lastIndex) "Sınavı bitir" else "Cevabı kaydet ve ilerle", color = StudyTop) }
            }
        }
    }
}
