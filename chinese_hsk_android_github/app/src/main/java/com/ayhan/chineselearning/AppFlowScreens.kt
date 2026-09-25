package com.ayhan.chineselearning

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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private val FlowSuccess = Color(0xFF18794E)

@Composable
fun WelcomeScreen(onStartZero: () -> Unit, onPlacement: () -> Unit) {
    Box(
        Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.background))),
        contentAlignment = Alignment.Center
    ) {
        Column(
            Modifier.fillMaxWidth().padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text("中文生活", color = MaterialTheme.colorScheme.secondary, fontSize = 42.sp, fontWeight = FontWeight.Bold)
            Text("Çince Yolculuğu", color = Color.White, fontSize = 29.sp, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(12.dp))
            Text(
                "HSK1'den HSK6'ya · 300 sahne · tamamen offline öğrenme",
                color = Color.White.copy(alpha = 0.78f),
                textAlign = TextAlign.Center
            )
            Spacer(Modifier.height(38.dp))
            Button(
                onClick = onStartZero,
                modifier = Modifier.fillMaxWidth().height(58.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
            ) {
                Text("Sıfırdan Başla", color = MaterialTheme.colorScheme.primary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            }
            Spacer(Modifier.height(14.dp))
            OutlinedButton(onClick = onPlacement, modifier = Modifier.fillMaxWidth().height(58.dp)) {
                Text("Seviyemi Belirle", color = Color.White, fontSize = 18.sp)
            }
            Spacer(Modifier.height(24.dp))
            Text(
                "İlerleme, favoriler ve sınav sonuçları yalnızca bu telefonda saklanır.",
                color = Color.White.copy(alpha = 0.58f),
                textAlign = TextAlign.Center,
                fontSize = 12.sp
            )
        }
    }
}

private data class PlacementQuestion(
    val level: Int,
    val prompt: String,
    val options: List<String>,
    val correct: Int
)

private val placementQuestions = listOf(
    PlacementQuestion(1, "你好 ne demektir?", listOf("Merhaba", "Teşekkürler", "Yarın"), 0),
    PlacementQuestion(1, "我叫李明。 cümlesinin anlamı?", listOf("Ben Li Ming'im.", "Li Ming nerede?", "Li Ming öğretmen."), 0),
    PlacementQuestion(2, "我已经吃饭了。", listOf("Henüz yemek yemedim.", "Yemeğimi zaten yedim.", "Yemek yapmak istiyorum."), 1),
    PlacementQuestion(2, "今天比昨天冷。", listOf("Bugün dün kadar sıcak.", "Bugün dünden daha soğuk.", "Yarın daha soğuk."), 1),
    PlacementQuestion(3, "因为下雨，所以我们没去公园。", listOf("Yağmur yağdığı için parka gitmedik.", "Parka gittikten sonra yağmur yağdı.", "Yağmur yağmazsa parka gideriz."), 0),
    PlacementQuestion(3, "虽然很忙，但是他还是来帮忙了。", listOf("Meşgul olmadığı için geldi.", "Çok meşguldü, yine de yardıma geldi.", "Yardım etmek istemedi."), 1),
    PlacementQuestion(4, "既然决定了，就别再犹豫。", listOf("Karar verdiğimize göre artık tereddüt etme.", "Karar vermeden önce bekle.", "Karar yanlış olduğu için vazgeç."), 0),
    PlacementQuestion(4, "与其抱怨，不如想办法解决。", listOf("Şikâyet etmek en iyi çözüm.", "Şikâyet etmek yerine çözüm düşünmek daha iyi.", "Çözümü başkasına bırak."), 1),
    PlacementQuestion(5, "这个结论缺乏足够的证据支持。", listOf("Bu sonuç yeterli kanıtla desteklenmiyor.", "Bu sonuç kesinlikle doğru.", "Kanıt artık gerekli değil."), 0),
    PlacementQuestion(5, "从长远来看，这个选择更符合我们的目标。", listOf("Kısa vadede bu daha ucuz.", "Uzun vadede bu seçim hedeflerimize daha uygun.", "Bu seçimin hedeflerle ilgisi yok."), 1),
    PlacementQuestion(6, "真正留下来的，往往不是东西，而是人与人之间的联系。", listOf("Asıl kalan çoğu zaman eşyalar değil, insanlar arasındaki bağlardır.", "Eşyalar insanlardan daha değerlidir.", "Geçmişi tamamen unutmak gerekir."), 0),
    PlacementQuestion(6, "回过头看，那些看似偶然的选择，后来都成了人生的一部分。", listOf("Geçmişteki tesadüfi görünen seçimler zamanla hayatın parçası oldu.", "Bütün seçimler önemsizdi.", "Gelecek geçmişten tamamen bağımsızdır."), 0)
)

@Composable
fun PlacementTestScreen(onBack: () -> Unit, onComplete: (level: Int, score: Int, total: Int) -> Unit) {
    var index by remember { mutableIntStateOf(0) }
    var score by remember { mutableIntStateOf(0) }
    var answered by remember { mutableStateOf<Int?>(null) }
    var finished by remember { mutableStateOf(false) }

    Box(Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.background)))) {
        Column(Modifier.fillMaxSize()) {
            Text("← Geri", color = MaterialTheme.colorScheme.secondary, modifier = Modifier.clickable { onBack() }.padding(20.dp), fontWeight = FontWeight.Bold)
            if (finished) {
                val level = when (score) {
                    in 0..2 -> 1
                    in 3..4 -> 2
                    in 5..6 -> 3
                    in 7..8 -> 4
                    in 9..10 -> 5
                    else -> 6
                }
                Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                    Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(28.dp)) {
                        Column(Modifier.padding(28.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                            Text("Seviye Sonucu", color = MaterialTheme.colorScheme.primary, fontSize = 25.sp, fontWeight = FontWeight.Bold)
                            Text("HSK$level", color = MaterialTheme.colorScheme.secondary, fontSize = 48.sp, fontWeight = FontWeight.Black, modifier = Modifier.padding(vertical = 16.dp))
                            Text("$score / ${placementQuestions.size} doğru", color = Color.DarkGray)
                            Spacer(Modifier.height(20.dp))
                            Button(onClick = { onComplete(level, score, placementQuestions.size) }, colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)) {
                                Text("Bu Seviyeden Başla")
                            }
                        }
                    }
                }
            } else {
                val q = placementQuestions[index]
                Column(Modifier.padding(horizontal = 20.dp)) {
                    Text("Seviye Tespit Sınavı", color = Color.White, fontSize = 28.sp, fontWeight = FontWeight.Bold)
                    Text("${index + 1} / ${placementQuestions.size}", color = Color.White.copy(alpha = 0.7f), modifier = Modifier.padding(top = 4.dp))
                    LinearProgressIndicator(
                        progress = { (index + 1).toFloat() / placementQuestions.size },
                        modifier = Modifier.fillMaxWidth().padding(vertical = 18.dp),
                        color = MaterialTheme.colorScheme.secondary
                    )
                    Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(22.dp)) {
                        Column(Modifier.padding(20.dp)) {
                            Text(q.prompt, color = MaterialTheme.colorScheme.primary, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                            Spacer(Modifier.height(18.dp))
                            q.options.forEachIndexed { optionIndex, option ->
                                val selected = answered == optionIndex
                                val correct = answered != null && optionIndex == q.correct
                                OutlinedButton(
                                    onClick = {
                                        if (answered == null) {
                                            answered = optionIndex
                                            if (optionIndex == q.correct) score++
                                        }
                                    },
                                    modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                                    colors = ButtonDefaults.outlinedButtonColors(
                                        containerColor = when {
                                            correct -> Color(0xFFE6F4EA)
                                            selected -> Color(0xFFFFE8E6)
                                            else -> Color.Transparent
                                        }
                                    )
                                ) { Text(option, color = MaterialTheme.colorScheme.primary) }
                            }
                            if (answered != null) {
                                Button(
                                    onClick = {
                                        if (index < placementQuestions.lastIndex) {
                                            index++
                                            answered = null
                                        } else finished = true
                                    },
                                    modifier = Modifier.fillMaxWidth().padding(top = 14.dp),
                                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                                ) { Text(if (index < placementQuestions.lastIndex) "Sonraki" else "Sonucu Gör", color = MaterialTheme.colorScheme.primary) }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun DashboardScreen(
    levels: List<LevelInfo>,
    progress: ProgressStore,
    progressVersion: Int,
    onContinue: () -> Unit,
    onLevels: () -> Unit,
    onFavorites: () -> Unit,
    onDailyReview: () -> Unit,
    onWeakWords: () -> Unit,
    onHabits: () -> Unit,
    onProgress: () -> Unit,
    onSettings: () -> Unit,
    onSystemCheck: () -> Unit,
    onPlacement: () -> Unit
) {
    val mastered = remember(progressVersion) { progress.masteredCount() }
    val startLevel = progress.placementStartLevel()
    val favoriteCount = progress.favoriteIds().size
    val weakCount = progress.weakWordIds().size
    val streak = progress.currentStreak()
    Column(Modifier.fillMaxSize()) {
        Column(Modifier.padding(20.dp)) {
            Text("中文生活", color = MaterialTheme.colorScheme.secondary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
            Text("Ana Dashboard", color = Color.White, fontSize = 30.sp, fontWeight = FontWeight.Bold)
            Text("Başlangıç noktası: HSK$startLevel", color = Color.White.copy(alpha = 0.72f), modifier = Modifier.padding(top = 4.dp))
        }
        LazyColumn(
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 4.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(22.dp)) {
                    Column(Modifier.padding(18.dp)) {
                        Text("Kurs İlerlemesi", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                        Text("$mastered / 300 sahne tamamlandı", color = Color.DarkGray, modifier = Modifier.padding(top = 6.dp))
                        LinearProgressIndicator(
                            progress = { mastered / 300f },
                            modifier = Modifier.fillMaxWidth().padding(top = 12.dp),
                            color = FlowSuccess,
                            trackColor = Color(0xFFE8E1ED)
                        )
                    }
                }
            }
            item {
                Button(
                    onClick = onContinue,
                    modifier = Modifier.fillMaxWidth().height(58.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                ) { Text("▶ Kaldığım Yerden Devam Et", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold) }
            }
            item { DashboardAction("📚", "HSK Seviyeleri", "300 sahneyi seviye bazında gör", onLevels) }
            item { DashboardAction("★", "Favorilerim", "$favoriteCount favori kelime", onFavorites) }
            item { DashboardAction("🔁", "Günlük Tekrar", "Zayıf kelimeler öncelikli · hedef ${progress.dailyReviewTarget()} kelime", onDailyReview) }
            item { DashboardAction("⚑", "Zayıf Kelimeler", "$weakCount kelime tekrar bekliyor", onWeakWords) }
            item { DashboardAction("🔥", "Seri ve Takvim", "Mevcut seri: $streak gün", onHabits) }
            item { DashboardAction("📊", "İlerlemem", "Sınav ortalamaları ve seviye ilerlemesi", onProgress) }
            item { DashboardAction("⚙", "Ayarlar ve Yedek", "Altyazı, hız, tema ve yerel yedek", onSettings) }
            item { DashboardAction("🩺", "Sistem Kontrolü", "Offline ses, telaffuz ve içerik durumunu kontrol et", onSystemCheck) }
            item { DashboardAction("🎯", "Seviye Testini Yenile", "Başlangıç seviyeni yeniden belirle", onPlacement) }
            item {
                Text("Seviye Durumu", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 6.dp, bottom = 2.dp))
            }
            items(levels) { level ->
                val levelNo = level.id.removePrefix("HSK").toIntOrNull() ?: 1
                val count = remember(level.id, progressVersion) { progress.masteredCount(levelNo) }
                Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.94f))) {
                    Row(Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(level.title, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.weight(1f))
                        Text("$count / 50", color = if (count == 50) FlowSuccess else Color.Gray)
                    }
                }
            }
            item { Spacer(Modifier.height(20.dp)) }
        }
    }
}

@Composable
private fun DashboardAction(icon: String, title: String, subtitle: String, onClick: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth().clickable { onClick() },
        colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.96f)),
        shape = RoundedCornerShape(18.dp)
    ) {
        Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Text(icon, fontSize = 27.sp)
            Spacer(Modifier.width(14.dp))
            Column(Modifier.weight(1f)) {
                Text(title, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
                Text(subtitle, color = Color.Gray, fontSize = 13.sp)
            }
            Text("›", color = MaterialTheme.colorScheme.primary, fontSize = 28.sp)
        }
    }
}

@Composable
fun DailyReviewScreen(repo: ContentRepository, progress: ProgressStore, onBack: () -> Unit) {
    val cards = remember {
        val all = repo.loadAllVocabularyCards()
        val favoriteIds = progress.favoriteIds()
        val weakIds = progress.weakWordIds()
        val target = progress.dailyReviewTarget()
        val weak = all.filter { weakIds.contains(it.card.id) }
            .sortedByDescending { progress.weakWordPriority(it.card.id) }
            .take(target)
        val favorites = all.filter { favoriteIds.contains(it.card.id) && !weakIds.contains(it.card.id) }.take(target)
        val lastScene = progress.lastSceneId()
        val recent = all.filter { it.sceneId == lastScene && !favoriteIds.contains(it.card.id) && !weakIds.contains(it.card.id) }.take(target)
        (weak + favorites + recent).distinctBy { it.card.id }.take(target).ifEmpty { all.take(target) }
    }
    LaunchedEffect(Unit) { progress.recordStudyActivity() }
    var index by remember { mutableIntStateOf(0) }
    var flipped by remember(index) { mutableStateOf(false) }

    Box(Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.background)))) {
        Column(Modifier.fillMaxSize()) {
            Text("← Geri", color = MaterialTheme.colorScheme.secondary, modifier = Modifier.clickable { onBack() }.padding(20.dp), fontWeight = FontWeight.Bold)
            Text("Günlük Tekrar", color = Color.White, fontSize = 29.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 20.dp))
            Text("Bugünkü hedef: ${progress.dailyReviewTarget()} kelime", color = Color.White.copy(alpha = 0.7f), modifier = Modifier.padding(horizontal = 20.dp, vertical = 5.dp))
            if (cards.isEmpty()) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { Text("Tekrar kartı bulunamadı.", color = Color.White) }
            } else {
                if (index >= cards.size) index = cards.lastIndex
                val item = cards[index]
                Card(
                    Modifier.fillMaxWidth().weight(1f).padding(20.dp).clickable { flipped = !flipped },
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    shape = RoundedCornerShape(28.dp)
                ) {
                    Box(Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text(item.card.zh, color = MaterialTheme.colorScheme.primary, fontSize = 46.sp, fontWeight = FontWeight.Bold)
                            if (flipped) {
                                Text(item.card.pinyin, color = Color.Gray, fontSize = 22.sp, modifier = Modifier.padding(top = 16.dp))
                                Text(item.card.tr, fontSize = 22.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 8.dp))
                                if (item.card.exampleZh.isNotBlank()) Text(item.card.exampleZh, textAlign = TextAlign.Center, modifier = Modifier.padding(top = 18.dp))
                            } else {
                                Text("Anlamı görmek için karta dokun", color = Color.Gray, modifier = Modifier.padding(top = 16.dp))
                            }
                            Text("${item.levelId} · ${item.sceneTitleTr}", color = Color.Gray, fontSize = 12.sp, modifier = Modifier.padding(top = 24.dp))
                        }
                    }
                }
                Row(Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 12.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    OutlinedButton(onClick = { if (index > 0) index-- }, enabled = index > 0, modifier = Modifier.weight(1f)) { Text("← Önceki") }
                    Button(onClick = { if (index < cards.lastIndex) index++ }, enabled = index < cards.lastIndex, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)) { Text("Sonraki →", color = MaterialTheme.colorScheme.primary) }
                }
            }
        }
    }
}
