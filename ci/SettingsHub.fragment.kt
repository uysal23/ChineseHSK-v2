@Composable
fun SettingsHubScreen(
    progress: ProgressStore,
    progressVersion: Int,
    adminMode: Boolean,
    onAdminModeChanged: (Boolean) -> Unit,
    onThemeChanged: (Int) -> Unit,
    onBack: () -> Unit,
    onAdvancedSettings: () -> Unit,
    onSystemCheck: () -> Unit,
    onPlacement: () -> Unit
) {
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

    Column(Modifier.fillMaxSize()) {
        Header("Ayarlar", "Tüm uygulama tercihleri tek yerde", onBack)

        LazyColumn(
            contentPadding = PaddingValues(horizontal = 18.dp, vertical = 4.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item {
                SettingsSectionCard("👤 Kullanıcı Profili") {
                    OutlinedTextField(
                        value = nameDraft,
                        onValueChange = { nameDraft = it.take(40); status = "" },
                        modifier = Modifier.fillMaxWidth(),
                        singleLine = true,
                        label = { Text("Kullanıcı adı") }
                    )
                    Button(
                        onClick = {
                            val clean = nameDraft.trim()
                            progress.saveUserName(clean)
                            savedName = clean
                            status = "Kullanıcı adı kaydedildi"
                        },
                        modifier = Modifier.fillMaxWidth().padding(top = 8.dp)
                    ) { Text("Kaydet") }
                }
            }

            item {
                SettingsSectionCard("🎨 Tema") {
                    Text(
                        "Tema rengini seç. Pastel temalarda metin ve buton kontrastı otomatik korunur.",
                        color = Color(0xFF5F5963),
                        fontSize = 12.sp,
                        modifier = Modifier.padding(bottom = 8.dp)
                    )
                    val themeChoices = listOf(
                        ProgressStore.THEME_PURPLE to "Mor",
                        ProgressStore.THEME_BLUE to "Mavi",
                        ProgressStore.THEME_GREEN to "Yeşil",
                        ProgressStore.THEME_ORANGE to "Turuncu",
                        ProgressStore.THEME_PINK to "Pembe",
                        ProgressStore.THEME_DARK to "Koyu",
                        ProgressStore.THEME_LIGHT to "Açık"
                    )
                    themeChoices.chunked(4).forEach { rowChoices ->
                        Row(
                            Modifier.fillMaxWidth().padding(bottom = 6.dp),
                            horizontalArrangement = Arrangement.spacedBy(6.dp)
                        ) {
                            rowChoices.forEach { (mode, label) ->
                                FilterChip(
                                    selected = themeMode == mode,
                                    onClick = {
                                        themeMode = mode
                                        progress.saveThemeMode(mode)
                                        onThemeChanged(mode)
                                    },
                                    label = {
                                        Text(
                                            label,
                                            fontSize = 11.sp,
                                            fontWeight = if (themeMode == mode) FontWeight.Bold else FontWeight.Medium
                                        )
                                    },
                                    modifier = Modifier.weight(1f)
                                )
                            }
                        }
                    }
                }
            }

            item {
                SettingsSectionCard("字幕 Pinyin ve Türkçe Çeviri") {
                    Text("Pinyin varsayılanı", fontWeight = FontWeight.Bold)
                    SettingsDisplayModeRow(pinyinMode) {
                        pinyinMode = it
                        progress.savePinyinDisplayMode(it)
                    }
                    Spacer(Modifier.height(10.dp))
                    Text("Türkçe çeviri varsayılanı", fontWeight = FontWeight.Bold)
                    SettingsDisplayModeRow(turkishMode) {
                        turkishMode = it
                        progress.saveTurkishDisplayMode(it)
                    }
                }
            }

            item {
                SettingsSectionCard("🔊 Oynatma ve Ses") {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Column(Modifier.weight(1f)) {
                            Text("Otomatik oynat", fontWeight = FontWeight.Bold)
                            Text("Sahne açıldığında replikler otomatik ilerlesin.", color = Color.Gray, fontSize = 12.sp)
                        }
                        Switch(
                            checked = autoplay,
                            onCheckedChange = {
                                autoplay = it
                                progress.saveAutoPlayDefault(it)
                            }
                        )
                    }
                    Spacer(Modifier.height(10.dp))
                    Text("Konuşma hızı: ${"%.2f".format(speed)}x", fontWeight = FontWeight.Bold)
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        listOf(0.75f, 0.85f, 1.0f, 1.15f, 1.25f).forEach { value ->
                            FilterChip(
                                selected = kotlin.math.abs(speed - value) < 0.01f,
                                onClick = {
                                    speed = value
                                    progress.savePlaybackSpeed(value)
                                },
                                label = { Text("${value}x", fontSize = 10.sp) },
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }
            }

            item {
                SettingsSectionCard("🔁 Günlük Tekrar Hedefi") {
                    Text("Günlük $dailyTarget kelime", fontWeight = FontWeight.Bold)
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        listOf(5, 10, 12).forEach { value ->
                            FilterChip(
                                selected = dailyTarget == value,
                                onClick = {
                                    dailyTarget = value
                                    progress.saveDailyReviewTarget(value)
                                },
                                label = { Text("$value") },
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        listOf(15, 20, 30).forEach { value ->
                            FilterChip(
                                selected = dailyTarget == value,
                                onClick = {
                                    dailyTarget = value
                                    progress.saveDailyReviewTarget(value)
                                },
                                label = { Text("$value") },
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }
            }

            item {
                SettingsSectionCard(if (adminMode) "🔓 Admin Modu Aktif" else "🔐 Admin Girişi") {
                    if (adminMode) {
                        Text(
                            "Bu oturumda tüm HSK seviyeleri, 300 sahne ve sınav kilitleri açık. Normal kullanıcı ilerlemesi değiştirilmez.",
                            color = Color(0xFF176B43),
                            fontWeight = FontWeight.SemiBold
                        )
                        Button(
                            onClick = {
                                AdminSession.logout()
                                onAdminModeChanged(false)
                                status = "Admin modu kapatıldı"
                            },
                            modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF7A263A))
                        ) { Text("Admin Modundan Çık") }
                    } else {
                        Text(
                            "Şifre doğruysa admin modu uygulama kapanana kadar açık kalır.",
                            color = Color.Gray,
                            fontSize = 12.sp
                        )
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
                                    onAdminModeChanged(true)
                                    adminPassword = ""
                                    status = "Admin modu açıldı"
                                } else {
                                    status = "Şifre yanlış"
                                }
                            },
                            enabled = adminPassword.isNotBlank(),
                            modifier = Modifier.fillMaxWidth().padding(top = 8.dp)
                        ) { Text("Admin Modunu Aç") }
                    }
                    if (status.isNotBlank()) {
                        Text(
                            status,
                            color = if (AdminSession.active || status.contains("kaydedildi")) FlowSuccess else Color(0xFFB3261E),
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(top = 8.dp)
                        )
                    }
                }
            }

            item {
                SettingsNavigationCard(
                    icon = "🔔",
                    title = "Bildirimler, Yedekleme ve Gelişmiş Ayarlar",
                    subtitle = "Hatırlatıcı saatleri, bildirimler, JSON yedekleme ve veri seçenekleri",
                    onClick = onAdvancedSettings
                )
            }

            item {
                SettingsNavigationCard(
                    icon = "🩺",
                    title = "Sistem Kontrolü",
                    subtitle = "Offline Mandarin sesi, konuşma tanıma, cache ve içerik durumunu kontrol et",
                    onClick = onSystemCheck
                )
            }

            item {
                SettingsNavigationCard(
                    icon = "🎯",
                    title = "Seviye Testini Yenile",
                    subtitle = "Başlangıç HSK seviyeni yeniden belirle",
                    onClick = onPlacement
                )
            }

            item { Spacer(Modifier.height(22.dp)) }
        }
    }
}

@Composable
private fun SettingsSectionCard(
    title: String,
    content: @Composable ColumnScope.() -> Unit
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.97f), contentColor = Color(0xFF231F28)),
        shape = RoundedCornerShape(20.dp)
    ) {
        Column(Modifier.fillMaxWidth().padding(16.dp)) {
            Text(title, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 19.sp)
            Spacer(Modifier.height(10.dp))
            content()
        }
    }
}

@Composable
private fun SettingsDisplayModeRow(selected: Int, onSelect: (Int) -> Unit) {
    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
        listOf(
            ProgressStore.DISPLAY_AUTO to "Otomatik",
            ProgressStore.DISPLAY_ON to "Açık",
            ProgressStore.DISPLAY_OFF to "Kapalı"
        ).forEach { (mode, label) ->
            FilterChip(
                selected = selected == mode,
                onClick = { onSelect(mode) },
                label = { Text(label, fontSize = 11.sp) },
                modifier = Modifier.weight(1f)
            )
        }
    }
}

@Composable
private fun SettingsNavigationCard(
    icon: String,
    title: String,
    subtitle: String,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth().clickable { onClick() },
        colors = CardDefaults.cardColors(containerColor = Color.White.copy(alpha = 0.97f)),
        shape = RoundedCornerShape(20.dp)
    ) {
        Row(
            Modifier.fillMaxWidth().padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(icon, fontSize = 26.sp)
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Text(title, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                Text(subtitle, color = Color.DarkGray, fontSize = 12.sp, modifier = Modifier.padding(top = 3.dp))
            }
            Text("›", color = MaterialTheme.colorScheme.primary, fontSize = 28.sp, fontWeight = FontWeight.Bold)
        }
    }
}
