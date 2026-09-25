package com.ayhan.chineselearning

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
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
import java.time.LocalDate
import java.time.YearMonth

@Composable
fun StudyHabitsScreen(progress: ProgressStore, onBack: () -> Unit) {
    val today = remember { LocalDate.now() }
    val month = remember { YearMonth.now() }
    val current = remember { progress.currentStreak(today) }
    val longest = remember { progress.longestStreak() }
    val monthDays = remember { progress.studyDaysInMonth(month) }
    val recentDays = remember {
        (27 downTo 0).map { today.minusDays(it.toLong()) }
    }

    Box(Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.background)))) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(18.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Text("← Geri", color = MaterialTheme.colorScheme.secondary, fontWeight = FontWeight.Bold,
                    modifier = Modifier.clickable { onBack() }.padding(vertical = 4.dp))
                Text("Seri ve Çalışma Takvimi", color = Color.White, fontSize = 29.sp, fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(top = 8.dp))
                Text("Çalıştığın günler yalnızca bu telefonda tutulur.", color = Color.White.copy(alpha = 0.72f), modifier = Modifier.padding(top = 4.dp))
            }
            item {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    HabitMetric("🔥", "$current gün", "Mevcut seri", Modifier.weight(1f))
                    HabitMetric("🏆", "$longest gün", "En uzun seri", Modifier.weight(1f))
                    HabitMetric("📅", "$monthDays gün", "Bu ay", Modifier.weight(1f))
                }
            }
            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.97f)), shape = RoundedCornerShape(22.dp)) {
                    Column(Modifier.fillMaxWidth().padding(16.dp)) {
                        Text("Son 28 Gün", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                        Text("Dolu günler en az bir çalışma etkinliği yaptığın günlerdir.", color = Color.Gray, fontSize = 12.sp, modifier = Modifier.padding(top = 3.dp, bottom = 12.dp))
                        recentDays.chunked(7).forEach { week ->
                            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                week.forEach { date ->
                                    val active = progress.studiedOn(date)
                                    Surface(
                                        shape = RoundedCornerShape(14.dp),
                                        color = if (active) MaterialTheme.colorScheme.secondary else Color(0xFFEDE7F1),
                                        modifier = Modifier.size(42.dp)
                                    ) {
                                        Box(contentAlignment = Alignment.Center) {
                                            Text(
                                                date.dayOfMonth.toString(),
                                                color = if (active) MaterialTheme.colorScheme.primary else Color.Gray,
                                                fontWeight = if (active) FontWeight.Bold else FontWeight.Normal,
                                                fontSize = 13.sp
                                            )
                                        }
                                    }
                                }
                            }
                            Spacer(Modifier.height(8.dp))
                        }
                    }
                }
            }
            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.96f)), shape = RoundedCornerShape(20.dp)) {
                    Column(Modifier.padding(16.dp)) {
                        Text("Seri Kuralı", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        Text(
                            "Bir sahne çalışmak, kelime kartı kullanmak, telaffuz yapmak veya sınav çözmek o günü çalışma günü olarak işaretler. Bir gün ara verilirse mevcut seri sıfırlanır; en uzun seri kaybolmaz.",
                            color = Color.DarkGray, fontSize = 13.sp, modifier = Modifier.padding(top = 6.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun HabitMetric(icon: String, value: String, label: String, modifier: Modifier = Modifier) {
    Card(modifier = modifier, colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(18.dp)) {
        Column(Modifier.padding(vertical = 15.dp, horizontal = 8.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(icon, fontSize = 25.sp)
            Text(value, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 19.sp, modifier = Modifier.padding(top = 3.dp))
            Text(label, color = Color.Gray, fontSize = 11.sp, textAlign = TextAlign.Center)
        }
    }
}

@Composable
fun WeakWordsScreen(repo: ContentRepository, progress: ProgressStore, onBack: () -> Unit) {
    var version by remember { mutableIntStateOf(0) }
    val items = remember(version) {
        val weak = progress.weakWordIds()
        repo.loadAllVocabularyCards()
            .filter { weak.contains(it.card.id) }
            .sortedByDescending { progress.weakWordPriority(it.card.id) }
    }
    var index by remember(items.size, version) { mutableIntStateOf(0) }
    var flipped by remember(index) { mutableStateOf(false) }
    val context = LocalContext.current
    val tts = remember { MandarinTtsPlayer(context) }
    DisposableEffect(Unit) { onDispose { tts.shutdown() } }

    Box(Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.background)))) {
        Column(Modifier.fillMaxSize()) {
            Text("← Geri", color = MaterialTheme.colorScheme.secondary, fontWeight = FontWeight.Bold,
                modifier = Modifier.clickable { onBack() }.padding(20.dp))
            Text("Zayıf Kelimeler", color = Color.White, fontSize = 29.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 20.dp))
            Text("Sınav hataları ve 'zor' işaretlediğin kartlardan otomatik oluşur.", color = Color.White.copy(alpha = 0.72f), modifier = Modifier.padding(horizontal = 20.dp, vertical = 5.dp))

            if (items.isEmpty()) {
                Box(Modifier.fillMaxSize().padding(26.dp), contentAlignment = Alignment.Center) {
                    Text("Şimdilik zayıf kelime yok. Kelime kartlarında 'Zor' işaretleyebilir veya sınavlara devam edebilirsin.", color = Color.White, textAlign = TextAlign.Center)
                }
                return@Column
            }
            if (index >= items.size) index = items.lastIndex
            val item = items[index]
            val card = item.card
            val priority = progress.weakWordPriority(card.id)
            Column(Modifier.fillMaxSize().padding(18.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text("${item.levelId} · ${item.sceneTitleTr} · öncelik $priority", color = Color.White.copy(alpha = 0.78f), fontSize = 12.sp)
                Text("${index + 1} / ${items.size}", color = Color.White.copy(alpha = 0.7f), modifier = Modifier.padding(top = 3.dp))
                Card(
                    modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 10.dp).clickable { flipped = !flipped },
                    colors = CardDefaults.cardColors(containerColor = Color.White),
                    shape = RoundedCornerShape(26.dp)
                ) {
                    Box(Modifier.fillMaxSize().padding(22.dp), contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text(card.zh, color = MaterialTheme.colorScheme.primary, fontSize = 43.sp, fontWeight = FontWeight.Bold, textAlign = TextAlign.Center)
                            if (flipped) {
                                Text(card.pinyin, color = Color.Gray, fontSize = 21.sp, modifier = Modifier.padding(top = 12.dp), textAlign = TextAlign.Center)
                                Text(card.tr, fontSize = 20.sp, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(top = 7.dp), textAlign = TextAlign.Center)
                                if (card.exampleZh.isNotBlank()) Text(card.exampleZh, fontSize = 19.sp, modifier = Modifier.padding(top = 18.dp), textAlign = TextAlign.Center)
                                if (card.exampleTr.isNotBlank()) Text(card.exampleTr, color = Color.DarkGray, modifier = Modifier.padding(top = 5.dp), textAlign = TextAlign.Center)
                            } else {
                                Text("Anlam için karta dokun", color = Color.Gray, modifier = Modifier.padding(top = 14.dp))
                            }
                        }
                    }
                }
                OutlinedButton(onClick = { tts.speak(card.zh, "WEAK_VOCAB", 0.82f) }, modifier = Modifier.fillMaxWidth()) { Text("🔊 Dinle") }
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedButton(
                        onClick = { progress.recordWordAnswer(card.id, false); progress.markWordDifficult(card.id, true); version++ },
                        modifier = Modifier.weight(1f)
                    ) { Text("↺ Tekrar Et") }
                    Button(
                        onClick = {
                            progress.recordWordAnswer(card.id, true)
                            progress.markWordDifficult(card.id, false)
                            version++
                        },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                    ) { Text("✓ Hatırladım", color = MaterialTheme.colorScheme.primary) }
                }
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedButton(onClick = { if (index > 0) index-- }, enabled = index > 0, modifier = Modifier.weight(1f)) { Text("← Önceki") }
                    OutlinedButton(onClick = { if (index < items.lastIndex) index++ }, enabled = index < items.lastIndex, modifier = Modifier.weight(1f)) { Text("Sonraki →") }
                }
                Spacer(Modifier.height(8.dp))
            }
        }
    }
}
