@Composable
fun DashboardScreen(
    levels: List<LevelInfo>,
    progress: ProgressStore,
    progressVersion: Int,
    adminMode: Boolean,
    onContinue: () -> Unit,
    onLevels: () -> Unit,
    onFavorites: () -> Unit,
    onDailyReview: () -> Unit,
    onProgress: () -> Unit,
    onSettings: () -> Unit
) {
    val mastered = remember(progressVersion) { progress.masteredCount() }
    val startLevel = progress.placementStartLevel()
    val favoriteCount = progress.favoriteIds().size
    val streak = progress.currentStreak()
    val userName = remember(progressVersion) { progress.userName() }
    val greeting = userName.trim().takeIf { it.isNotEmpty() }?.let { "Merhaba, $it" } ?: "Merhaba"

    Column(Modifier.fillMaxSize()) {
        Column(Modifier.padding(horizontal = 20.dp, vertical = 18.dp)) {
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text("中文生活", color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.92f), fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Text(greeting, color = MaterialTheme.colorScheme.onPrimary, fontSize = 30.sp, fontWeight = FontWeight.Bold)
                    Text("Çince öğrenme yolculuğun · HSK$startLevel", color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.82f))
                }
                if (adminMode) {
                    Surface(color = Color(0xFF1B7F4C), contentColor = Color.White, shape = RoundedCornerShape(14.dp)) {
                        Text("ADMIN", modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp), fontWeight = FontWeight.Black)
                    }
                }
            }
        }

        LazyColumn(
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 4.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White, contentColor = Color(0xFF231F28)), shape = RoundedCornerShape(22.dp)) {
                    Column(Modifier.padding(18.dp)) {
                        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                            Column(Modifier.weight(1f)) {
                                Text("Kurs İlerlemesi", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                                Text("$mastered / 300 sahne tamamlandı", color = Color.DarkGray, modifier = Modifier.padding(top = 4.dp))
                            }
                            Text("🔥 $streak", color = Color(0xFFD2691E), fontWeight = FontWeight.Bold)
                        }
                        LinearProgressIndicator(
                            progress = { mastered / 300f },
                            modifier = Modifier.fillMaxWidth().padding(top = 12.dp),
                            color = FlowSuccess,
                            trackColor = Color(0xFFE8E1ED)
                        )
                        if (adminMode) {
                            Text(
                                "Admin modu açık: tüm sahneler bu oturum için erişilebilir.",
                                color = Color(0xFF176B43),
                                fontSize = 12.sp,
                                fontWeight = FontWeight.SemiBold,
                                modifier = Modifier.padding(top = 8.dp)
                            )
                        }
                    }
                }
            }

            item {
                Button(
                    onClick = onContinue,
                    modifier = Modifier.fillMaxWidth().height(60.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary),
                    shape = RoundedCornerShape(18.dp)
                ) {
                    Text("▶ Kaldığım Yerden Devam Et", color = MaterialTheme.colorScheme.onSecondary, fontWeight = FontWeight.Black)
                }
            }

            item {
                DashboardAction(
                    "📚",
                    "HSK Seviyeleri",
                    if (adminMode) "ADMIN · 300 sahnenin tamamı açık" else "HSK1–HSK6 · 300 sahne",
                    onLevels
                )
            }
            item { DashboardAction("🔁", "Günlük Tekrar", "Bugünkü kelime tekrarlarını çalış", onDailyReview) }
            item { DashboardAction("★", "Favorilerim", "$favoriteCount favori kelime", onFavorites) }
            item { DashboardAction("📊", "İlerlemem", "Sınavlar, seri ve seviye durumun", onProgress) }

            item {
                Button(
                    onClick = onSettings,
                    modifier = Modifier.fillMaxWidth().height(58.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color.White.copy(alpha = 0.96f),
                        contentColor = MaterialTheme.colorScheme.primary
                    ),
                    shape = RoundedCornerShape(18.dp)
                ) {
                    Text("⚙  Ayarlar", fontWeight = FontWeight.Black, fontSize = 17.sp)
                }
            }

            item {
                Text(
                    "Seviye Durumu",
                    color = MaterialTheme.colorScheme.onBackground,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(top = 4.dp)
                )
            }
            items(levels) { level ->
                val levelNo = level.id.removePrefix("HSK").toIntOrNull() ?: 1
                val count = remember(level.id, progressVersion) { progress.masteredCount(levelNo) }
                Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.94f), contentColor = Color(0xFF231F28))) {
                    Row(Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(level.title, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.weight(1f))
                        Text(
                            if (adminMode) "🔓 $count / 50" else "$count / 50",
                            color = if (adminMode || count == 50) FlowSuccess else Color.Gray
                        )
                    }
                }
            }
            item { Spacer(Modifier.height(20.dp)) }
        }
    }
}
