@Composable
fun DashboardScreen(
    levels: List<LevelInfo>,
    progress: ProgressStore,
    progressVersion: Int,
    adminMode: Boolean,
    onAdminModeChanged: (Boolean) -> Unit,
    onThemeChanged: (Int) -> Unit,
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

    var savedName by remember(progressVersion) { mutableStateOf(progress.userName()) }
    var nameDraft by remember(savedName) { mutableStateOf(savedName) }
    var themeMode by remember(progressVersion) { mutableIntStateOf(progress.themeMode()) }
    var pinyinMode by remember(progressVersion) { mutableIntStateOf(progress.pinyinDisplayMode()) }
    var turkishMode by remember(progressVersion) { mutableIntStateOf(progress.turkishDisplayMode()) }
    var autoplay by remember(progressVersion) { mutableStateOf(progress.autoPlayDefault()) }
    var speed by remember(progressVersion) { mutableFloatStateOf(progress.playbackSpeed(1.0f)) }
    var dailyTarget by remember(progressVersion) { mutableIntStateOf(progress.dailyReviewTarget()) }
    var adminPassword by remember { mutableStateOf("") }
    var status by remember(adminMode) { mutableStateOf("") }

    val greeting = savedName.trim().takeIf { it.isNotEmpty() }?.let { "Merhaba, $it" } ?: "Merhaba"

    Column(Modifier.fillMaxSize()) {
        Column(Modifier.padding(20.dp)) {
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text("中文生活", color = MaterialTheme.colorScheme.secondary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Text(greeting, color = Color.White, fontSize = 30.sp, fontWeight = FontWeight.Bold)
                    Text("Ana Dashboard · Başlangıç HSK$startLevel", color = Color.White.copy(alpha = 0.72f))
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
                DashboardSettingsCard("👤 Profil") {
                    OutlinedTextField(
                        value = nameDraft,
                        onValueChange = { nameDraft = it.take(40); status = "" },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        label = { Text("Kullanıcı adı") }
                    )
                    Button(onClick = {
                        val clean = nameDraft.trim()
                        progress.saveUserName(clean)
                        savedName = clean
                        status = "Kullanıcı adı kaydedildi"
                    }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp)) { Text("Kaydet") }
                }
            }

            item {
                DashboardSettingsCard("🎨 Tema") {
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        listOf(
                            ProgressStore.THEME_PURPLE to "Mor",
                            ProgressStore.THEME_DARK to "Koyu",
                            ProgressStore.THEME_LIGHT to "Açık"
                        ).forEach { (mode, label) ->
                            FilterChip(
                                selected = themeMode == mode,
                                onClick = { themeMode = mode; progress.saveThemeMode(mode); onThemeChanged(mode) },
                                label = { Text(label) },
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }
            }

            item {
                DashboardSettingsCard("字幕 Pinyin ve Türkçe") {
                    Text("Pinyin", fontWeight = FontWeight.Bold)
                    DashboardDisplayModeRow(pinyinMode) { pinyinMode = it; progress.savePinyinDisplayMode(it) }
                    Spacer(Modifier.height(10.dp))
                    Text("Türkçe çeviri", fontWeight = FontWeight.Bold)
                    DashboardDisplayModeRow(turkishMode) { turkishMode = it; progress.saveTurkishDisplayMode(it) }
                }
            }

            item {
                DashboardSettingsCard("🔊 Oynatma") {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text("Otomatik oynat", fontWeight = FontWeight.Bold)
                            Text("Sahne açıldığında replikleri otomatik ilerlet.", color = Color.Gray, fontSize = 12.sp)
                        }
                        Switch(checked = autoplay, onCheckedChange = { autoplay = it; progress.saveAutoPlayDefault(it) })
                    }
                    Spacer(Modifier.height(8.dp))
                    Text("Konuşma hızı: ${"%.2f".format(speed)}x", fontWeight = FontWeight.Bold)
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        listOf(0.75f, 0.85f, 1.0f, 1.15f, 1.25f).forEach { value ->
                            FilterChip(
                                selected = kotlin.math.abs(speed - value) < 0.01f,
                                onClick = { speed = value; progress.savePlaybackSpeed(value) },
                                label = { Text("${value}x", fontSize = 10.sp) },
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }
            }

            item {
                DashboardSettingsCard("🔁 Günlük tekrar hedefi") {
                    Text("$dailyTarget kelime", fontWeight = FontWeight.Bold)
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        listOf(5, 10, 12).forEach { value ->
                            FilterChip(selected = dailyTarget == value, onClick = { dailyTarget = value; progress.saveDailyReviewTarget(value) }, label = { Text("$value") }, modifier = Modifier.weight(1f))
                        }
                    }
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        listOf(15, 20, 30).forEach { value ->
                            FilterChip(selected = dailyTarget == value, onClick = { dailyTarget = value; progress.saveDailyReviewTarget(value) }, label = { Text("$value") }, modifier = Modifier.weight(1f))
                        }
                    }
                }
            }

            item {
                DashboardSettingsCard(if (adminMode) "🔓 Admin Modu Aktif" else "🔐 Admin Girişi") {
                    if (adminMode) {
                        Text(
                            "Tüm HSK seviyeleri, 300 sahne ve sınav kilitleri bu oturum için açıktır. Normal kullanıcı ilerlemesi değiştirilmez.",
                            color = Color(0xFF176B43),
                            fontWeight = FontWeight.SemiBold
                        )
                        Button(
                            onClick = { AdminSession.logout(); onAdminModeChanged(false); status = "Admin modu kapatıldı" },
                            modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF7A263A))
                        ) { Text("Admin Modundan Çık") }
                    } else {
                        Text("Şifreyi girince kilitler uygulama kapanana kadar açılır.", color = Color.Gray, fontSize = 12.sp)
                        OutlinedTextField(
                            value = adminPassword,
                            onValueChange = { adminPassword = it; status = "" },
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                            singleLine = true,
                            label = { Text("Admin şifresi") },
                            visualTransformation = PasswordVisualTransformation()
                        )
                        Button(
                            onClick = {
                                if (AdminSession.login(adminPassword)) {
                                    status = "Admin modu açıldı"
                                    onAdminModeChanged(true)
                                    adminPassword = ""
                                } else status = "Şifre yanlış"
                            },
                            enabled = adminPassword.isNotBlank(),
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp)
                        ) { Text("Admin Modunu Aç") }
                    }
                    if (status.isNotBlank()) {
                        Text(status, color = if (AdminSession.active || status.contains("kaydedildi")) FlowSuccess else Color(0xFFB3261E), fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 8.dp))
                    }
                }
            }

            item {
                Card(colors = CardDefaults.cardColors(containerColor = Color.White), shape = RoundedCornerShape(22.dp)) {
                    Column(Modifier.padding(18.dp)) {
                        Text("Kurs İlerlemesi", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 20.sp)
                        Text("$mastered / 300 sahne tamamlandı", color = Color.DarkGray, modifier = Modifier.padding(top = 6.dp))
                        LinearProgressIndicator(progress = { mastered / 300f }, modifier = Modifier.fillMaxWidth().padding(top = 12.dp), color = FlowSuccess, trackColor = Color(0xFFE8E1ED))
                        if (adminMode) Text("Admin görünümü ilerlemeyi değiştirmeden tüm içeriği açar.", color = Color(0xFF176B43), fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
                    }
                }
            }

            item {
                Button(onClick = onContinue, modifier = Modifier.fillMaxWidth().height(58.dp), colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)) {
                    Text("▶ Kaldığım Yerden Devam Et", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                }
            }
            item { DashboardAction("📚", "HSK Seviyeleri", if (adminMode) "ADMIN: 300 sahnenin tamamı açık" else "300 sahneyi seviye bazında gör", onLevels) }
            item { DashboardAction("★", "Favorilerim", "$favoriteCount favori kelime", onFavorites) }
            item { DashboardAction("🔁", "Günlük Tekrar", "Zayıf kelimeler öncelikli · hedef ${progress.dailyReviewTarget()} kelime", onDailyReview) }
            item { DashboardAction("⚑", "Zayıf Kelimeler", "$weakCount kelime tekrar bekliyor", onWeakWords) }
            item { DashboardAction("🔥", "Seri ve Takvim", "Mevcut seri: $streak gün", onHabits) }
            item { DashboardAction("📊", "İlerlemem", "Sınav ortalamaları ve seviye ilerlemesi", onProgress) }
            item { DashboardAction("⚙", "Gelişmiş Ayarlar ve Yedek", "Bildirim, yedekleme ve diğer sistem seçenekleri", onSettings) }
            item { DashboardAction("🩺", "Sistem Kontrolü", "Offline ses, telaffuz ve içerik durumunu kontrol et", onSystemCheck) }
            item { DashboardAction("🎯", "Seviye Testini Yenile", "Başlangıç seviyeni yeniden belirle", onPlacement) }

            item { Text("Seviye Durumu", color = Color.White, fontSize = 20.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(top = 6.dp)) }
            items(levels) { level ->
                val levelNo = level.id.removePrefix("HSK").toIntOrNull() ?: 1
                val count = remember(level.id, progressVersion) { progress.masteredCount(levelNo) }
                Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.94f))) {
                    Row(Modifier.fillMaxWidth().padding(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(level.title, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.weight(1f))
                        Text(if (adminMode) "🔓 $count / 50" else "$count / 50", color = if (adminMode || count == 50) FlowSuccess else Color.Gray)
                    }
                }
            }
            item { Spacer(Modifier.height(20.dp)) }
        }
    }
}

@Composable
private fun DashboardSettingsCard(title: String, content: @Composable ColumnScope.() -> Unit) {
    Card(colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.97f)), shape = RoundedCornerShape(20.dp)) {
        Column(Modifier.fillMaxWidth().padding(16.dp)) {
            Text(title, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 19.sp)
            Spacer(Modifier.height(10.dp))
            content()
        }
    }
}

@Composable
private fun DashboardDisplayModeRow(selected: Int, onSelect: (Int) -> Unit) {
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        listOf(
            ProgressStore.DISPLAY_AUTO to "Otomatik",
            ProgressStore.DISPLAY_ON to "Açık",
            ProgressStore.DISPLAY_OFF to "Kapalı"
        ).forEach { (mode, label) ->
            FilterChip(selected = selected == mode, onClick = { onSelect(mode) }, label = { Text(label, fontSize = 11.sp) }, modifier = Modifier.weight(1f))
        }
    }
}
