package com.ayhan.chineselearning

import android.graphics.BitmapFactory
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private data class StagePalette(val sky: Color, val wall: Color, val floor: Color, val accent: Color)
private data class CartoonStyle(
    val skin: Color,
    val hair: Color,
    val shirt: Color,
    val jacket: Color,
    val trousers: Color,
    val hairStyle: Int,
    val accessory: Int
)

private fun portraitVariantFor(profile: CharacterProfile?, level: String): String {
    if (profile == null) return ""
    return profile.portraitByLevel[level].orEmpty().ifBlank { profile.portraitAsset }
}

private fun palette(theme: String, timeOfDay: String): StagePalette {
    val night = timeOfDay.contains("night", true) || timeOfDay.contains("evening", true)
    if (night) return StagePalette(Color(0xFF17243B), Color(0xFF293954), Color(0xFF171A25), Color(0xFFFFC857))
    return when (theme) {
        "home" -> StagePalette(Color(0xFFCFE6F6), Color(0xFFF1D5BB), Color(0xFF9C765D), Color(0xFFFFC857))
        "cafe" -> StagePalette(Color(0xFFFFE3C7), Color(0xFFC98055), Color(0xFF694534), Color(0xFFFFC857))
        "school" -> StagePalette(Color(0xFFCCE6F6), Color(0xFFF2E9D3), Color(0xFF9D8065), Color(0xFFFFD15C))
        "health" -> StagePalette(Color(0xFFD9F1F0), Color(0xFFF4FAFA), Color(0xFF8DAEB0), Color(0xFF55C2B7))
        "transport" -> StagePalette(Color(0xFFB9D1E4), Color(0xFF65778D), Color(0xFF303845), Color(0xFFFFC857))
        "work" -> StagePalette(Color(0xFFD8E3F0), Color(0xFFB4C1D1), Color(0xFF596677), Color(0xFFFFC857))
        "nature" -> StagePalette(Color(0xFFAED9F3), Color(0xFF78AD63), Color(0xFF567C47), Color(0xFFFFDA70))
        "market" -> StagePalette(Color(0xFFFFD7B0), Color(0xFFE49B69), Color(0xFF8C5C45), Color(0xFFFFC857))
        "hotel" -> StagePalette(Color(0xFFE0D7EF), Color(0xFFAA93BD), Color(0xFF5B4A67), Color(0xFFFFD074))
        "community" -> StagePalette(Color(0xFFD6E4F0), Color(0xFFA5B6C9), Color(0xFF667488), Color(0xFFFFD36B))
        "service" -> StagePalette(Color(0xFFD7E3EC), Color(0xFFA7B7C3), Color(0xFF62717A), Color(0xFFFFD36B))
        else -> StagePalette(Color(0xFFC9DDF0), Color(0xFF9D84B0), Color(0xFF5A4768), Color(0xFFFFC857))
    }
}

private fun styleFor(profile: CharacterProfile?, name: String): CartoonStyle {
    val key = profile?.id ?: name
    val role = profile?.role.orEmpty().lowercase()
    val hash = key.hashCode() and Int.MAX_VALUE
    val skins = listOf(Color(0xFFF0C39B), Color(0xFFE8B58F), Color(0xFFDFA782), Color(0xFFF4CBA8))
    val hairs = listOf(Color(0xFF231E20), Color(0xFF3A2B27), Color(0xFF51382C), Color(0xFF17171A))
    val baseShirts = listOf(Color(0xFF4777B8), Color(0xFFB05D75), Color(0xFF4F9272), Color(0xFF8A68B3), Color(0xFFC27B43))

    var shirt = baseShirts[hash % baseShirts.size]
    var jacket = shirt.copy(alpha = 0.88f)
    var trousers = Color(0xFF374151)
    var accessory = hash % 4

    when {
        profile?.id?.contains("ZHANGWEI") == true -> {
            shirt = Color(0xFF3F6EA8); jacket = Color(0xFF274C7D); trousers = Color(0xFF303A4A); accessory = 1
        }
        profile?.id?.contains("LIUMEI") == true -> {
            shirt = Color(0xFFC86B82); jacket = Color(0xFF944B63); trousers = Color(0xFF4D4552); accessory = 2
        }
        profile?.id?.contains("LICHEN") == true -> {
            shirt = Color(0xFF4D947F); jacket = Color(0xFF2E6758); trousers = Color(0xFF33443F); accessory = 1
        }
        profile?.id?.contains("ZHANGYUTONG") == true -> {
            shirt = Color(0xFF8A67BA); jacket = Color(0xFF684895); trousers = Color(0xFF464052); accessory = 3
        }
        name == "王师傅" -> {
            shirt = Color(0xFF455A64); jacket = Color(0xFF263238); trousers = Color(0xFF343A40); accessory = 0
        }
        role.contains("doctor") || role.contains("nurse") || role.contains("vet") -> {
            shirt = Color(0xFFEEF8F6); jacket = Color(0xFFFFFFFF); trousers = Color(0xFF6C8790); accessory = 3
        }
        role.contains("teacher") || role.contains("mentor") -> {
            shirt = Color(0xFF5D79A8); jacket = Color(0xFF405C8C); accessory = 1
        }
        role.contains("security") -> {
            shirt = Color(0xFF34495E); jacket = Color(0xFF233241); trousers = Color(0xFF222B34); accessory = 0
        }
        role.contains("service") || role.contains("sales") || role.contains("waiter") -> {
            shirt = Color(0xFFD78545); jacket = Color(0xFFAC6332); accessory = 2
        }
        role.contains("volunteer") || role.contains("guide") -> {
            shirt = Color(0xFF4E9A68); jacket = Color(0xFF33724A); accessory = 2
        }
    }

    return CartoonStyle(
        skin = skins[hash % skins.size],
        hair = hairs[(hash / 3) % hairs.size],
        shirt = shirt,
        jacket = jacket,
        trousers = trousers,
        hairStyle = (hash / 7) % 4,
        accessory = accessory
    )
}

@Composable
private fun rememberAssetBitmap(path: String): ImageBitmap? {
    val context = LocalContext.current
    return remember(path) {
        if (path.isBlank()) null
        else try {
            context.assets.open(path).use { BitmapFactory.decodeStream(it)?.asImageBitmap() }
        } catch (_: Exception) {
            null
        }
    }
}

@Composable
private fun SceneDecor(theme: String, p: StagePalette) {
    Box(
        Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(p.sky, p.wall, p.floor)))
    ) {
        when (theme) {
            "home" -> {
                Box(Modifier.width(132.dp).height(178.dp).align(Alignment.TopEnd).padding(top = 74.dp, end = 18.dp)
                    .background(Color(0xFFBCE0F6), RoundedCornerShape(10.dp))) {
                    Box(Modifier.width(4.dp).fillMaxHeight().align(Alignment.Center).background(Color.White.copy(alpha = .75f)))
                    Box(Modifier.height(4.dp).fillMaxWidth().align(Alignment.Center).background(Color.White.copy(alpha = .75f)))
                }
                Box(Modifier.fillMaxWidth(.72f).height(96.dp).align(Alignment.BottomStart).padding(start = 16.dp, bottom = 172.dp)
                    .background(Color(0xFF8E5E4B), RoundedCornerShape(topStart = 30.dp, topEnd = 30.dp)))
                Box(Modifier.width(40.dp).height(112.dp).align(Alignment.CenterStart).padding(start = 18.dp)
                    .background(Color(0xFFD9B46F), RoundedCornerShape(20.dp)))
            }
            "cafe" -> {
                Row(Modifier.align(Alignment.TopCenter).padding(top = 86.dp), horizontalArrangement = Arrangement.spacedBy(54.dp)) {
                    repeat(3) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Box(Modifier.width(2.dp).height(38.dp).background(Color(0xFF5A382A)))
                            Box(Modifier.size(28.dp).background(Color(0xFFFFD27A), CircleShape))
                        }
                    }
                }
                Box(Modifier.fillMaxWidth(.88f).height(106.dp).align(Alignment.BottomCenter).padding(bottom = 164.dp)
                    .background(Color(0xFF6C4030), RoundedCornerShape(topStart = 14.dp, topEnd = 14.dp)))
                Row(Modifier.align(Alignment.Center).padding(top = 78.dp), horizontalArrangement = Arrangement.spacedBy(28.dp)) {
                    repeat(3) { Box(Modifier.size(18.dp).background(Color(0xFFF0E0D2), RoundedCornerShape(5.dp))) }
                }
            }
            "school" -> {
                Box(Modifier.fillMaxWidth(.72f).height(148.dp).align(Alignment.TopCenter).padding(top = 78.dp)
                    .background(Color(0xFF325A4E), RoundedCornerShape(8.dp)))
                Row(Modifier.align(Alignment.BottomCenter).padding(bottom = 176.dp), horizontalArrangement = Arrangement.spacedBy(18.dp)) {
                    repeat(3) { Box(Modifier.width(86.dp).height(48.dp).background(Color(0xFFB98A5D), RoundedCornerShape(8.dp))) }
                }
            }
            "health" -> {
                Box(Modifier.size(62.dp).align(Alignment.TopEnd).padding(top = 90.dp, end = 30.dp)
                    .background(Color.White, RoundedCornerShape(10.dp))) {
                    Box(Modifier.width(14.dp).height(44.dp).align(Alignment.Center).background(Color(0xFFE45353)))
                    Box(Modifier.width(44.dp).height(14.dp).align(Alignment.Center).background(Color(0xFFE45353)))
                }
                Box(Modifier.fillMaxWidth(.68f).height(86.dp).align(Alignment.BottomStart).padding(start = 20.dp, bottom = 174.dp)
                    .background(Color(0xFFEFF8F8), RoundedCornerShape(20.dp)))
            }
            "transport" -> {
                Row(Modifier.align(Alignment.TopCenter).padding(top = 80.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    repeat(3) { Box(Modifier.width(92.dp).height(126.dp).background(Color(0xFF90BDD8), RoundedCornerShape(12.dp))) }
                }
                Row(Modifier.align(Alignment.BottomCenter).padding(bottom = 174.dp), horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                    repeat(3) { Box(Modifier.width(88.dp).height(64.dp).background(Color(0xFF46566C), RoundedCornerShape(16.dp))) }
                }
            }
            "work", "service" -> {
                Row(Modifier.align(Alignment.Center).padding(top = 36.dp), horizontalArrangement = Arrangement.spacedBy(24.dp)) {
                    repeat(2) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Box(Modifier.width(94.dp).height(62.dp).background(Color(0xFF334354), RoundedCornerShape(8.dp)))
                            Box(Modifier.width(122.dp).height(16.dp).background(Color(0xFF7D6653), RoundedCornerShape(5.dp)))
                        }
                    }
                }
            }
            "nature" -> {
                Box(Modifier.size(96.dp).align(Alignment.TopEnd).padding(top = 68.dp, end = 30.dp)
                    .background(Color(0xFFFFE28B), CircleShape))
                Row(Modifier.align(Alignment.BottomCenter).padding(bottom = 150.dp), horizontalArrangement = Arrangement.spacedBy(54.dp)) {
                    repeat(3) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Box(Modifier.size(86.dp).background(Color(0xFF4E8F55), CircleShape))
                            Box(Modifier.width(18.dp).height(70.dp).background(Color(0xFF76543D)))
                        }
                    }
                }
            }
            "market" -> {
                Row(Modifier.align(Alignment.TopCenter).padding(top = 82.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                    repeat(3) { Box(Modifier.width(90.dp).height(38.dp).background(if (it % 2 == 0) Color(0xFFD95959) else Color(0xFFF3D36A))) }
                }
                Row(Modifier.align(Alignment.BottomCenter).padding(bottom = 174.dp), horizontalArrangement = Arrangement.spacedBy(18.dp)) {
                    repeat(3) { Box(Modifier.width(84.dp).height(72.dp).background(Color(0xFF9F714E), RoundedCornerShape(6.dp))) }
                }
            }
            "hotel" -> {
                Box(Modifier.fillMaxWidth(.76f).height(92.dp).align(Alignment.BottomCenter).padding(bottom = 174.dp)
                    .background(Color(0xFF5E476A), RoundedCornerShape(topStart = 18.dp, topEnd = 18.dp)))
                Box(Modifier.width(120.dp).height(164.dp).align(Alignment.TopEnd).padding(top = 82.dp, end = 22.dp)
                    .background(Color(0xFFEEDB9B), RoundedCornerShape(18.dp)))
            }
            else -> {
                Box(Modifier.fillMaxWidth(.72f).height(110.dp).align(Alignment.BottomCenter).padding(bottom = 174.dp)
                    .background(Color.White.copy(alpha = .12f), RoundedCornerShape(24.dp)))
            }
        }

        Box(
            Modifier.fillMaxWidth().height(200.dp).align(Alignment.TopCenter)
                .background(Brush.verticalGradient(listOf(Color.Black.copy(alpha = .16f), Color.Transparent)))
        )
    }
}

@Composable
private fun CartoonCat(name: String, isActive: Boolean, isSpeaking: Boolean, accent: Color) {
    val infinite = rememberInfiniteTransition(label = "catMotion-$name")
    val bob by infinite.animateFloat(-1.5f, 1.5f, infiniteRepeatable(tween(900), RepeatMode.Reverse), label = "catBob")
    val scale by animateFloatAsState(if (isActive) 1.09f else 1f, tween(220), label = "catScale")
    val mouth by infinite.animateFloat(
        initialValue = 3f,
        targetValue = if (isActive && isSpeaking) 12f else 3f,
        animationSpec = infiniteRepeatable(tween(150), RepeatMode.Reverse),
        label = "catMouth"
    )
    Column(
        modifier = Modifier.width(104.dp).height(210.dp).offset(y = bob.dp).scale(scale),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Bottom
    ) {
        Box(Modifier.size(78.dp).background(Color(0xFFD98945), CircleShape)) {
            Box(Modifier.size(26.dp).align(Alignment.TopStart).background(Color(0xFFD98945), RoundedCornerShape(3.dp)).graphicsLayer { rotationZ = 45f })
            Box(Modifier.size(26.dp).align(Alignment.TopEnd).background(Color(0xFFD98945), RoundedCornerShape(3.dp)).graphicsLayer { rotationZ = 45f })
            Row(Modifier.align(Alignment.Center).padding(top = 5.dp), horizontalArrangement = Arrangement.spacedBy(18.dp)) {
                Box(Modifier.size(7.dp).background(Color(0xFF272226), CircleShape))
                Box(Modifier.size(7.dp).background(Color(0xFF272226), CircleShape))
            }
            Box(
                Modifier
                    .width(18.dp)
                    .height(mouth.dp)
                    .align(Alignment.BottomCenter)
                    .padding(bottom = 12.dp)
                    .background(Color(0xFF7A3D35), RoundedCornerShape(6.dp))
            )
        }
        Box(Modifier.width(86.dp).height(96.dp).background(Color(0xFFD98945), RoundedCornerShape(40.dp))) {
            if (isActive) Box(Modifier.width(34.dp).height(5.dp).align(Alignment.TopCenter).padding(top = 12.dp).background(accent, CircleShape))
        }
    }
}

@Composable
private fun CartoonCharacter(name: String, profile: CharacterProfile?, isActive: Boolean, isSpeaking: Boolean, accent: Color) {
    if (profile?.role?.contains("cat", true) == true) {
        CartoonCat(name, isActive, isSpeaking, accent)
        return
    }

    val style = remember(profile?.id, name) { styleFor(profile, name) }
    val infinite = rememberInfiniteTransition(label = "characterMotion-$name")
    val bob by infinite.animateFloat(
        initialValue = -1.2f,
        targetValue = 1.8f,
        animationSpec = infiniteRepeatable(tween(if (isActive) 780 else 1250, easing = FastOutSlowInEasing), RepeatMode.Reverse),
        label = "bob"
    )
    val tilt by infinite.animateFloat(
        initialValue = if (isActive) -0.9f else -0.25f,
        targetValue = if (isActive) 0.9f else 0.25f,
        animationSpec = infiniteRepeatable(tween(if (isActive) 980 else 1600), RepeatMode.Reverse),
        label = "tilt"
    )
    val scale by animateFloatAsState(
        targetValue = if (isActive) 1.09f else 1.00f,
        animationSpec = tween(220),
        label = "speakerScale"
    )
    val opacity = if (isActive) 1f else 0.92f
    val mouth by infinite.animateFloat(
        initialValue = 4f,
        targetValue = if (isActive && isSpeaking) 13f else 4f,
        animationSpec = infiniteRepeatable(tween(135), RepeatMode.Reverse),
        label = "mouth"
    )

    Column(
        modifier = Modifier
            .width(122.dp)
            .height(326.dp)
            .offset(y = bob.dp)
            .graphicsLayer {
                rotationZ = tilt
                shadowElevation = if (isActive) 22f else 8f
            }
            .scale(scale)
            .alpha(opacity),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Bottom
    ) {
        Box(Modifier.width(104.dp).height(64.dp)) {
            Box(
                Modifier.width(18.dp).height(62.dp).align(Alignment.BottomStart).padding(start = 18.dp)
                    .background(style.skin, RoundedCornerShape(10.dp))
                    .graphicsLayer { rotationZ = if (isActive) 5f else 2f }
            )
            Box(
                Modifier.width(18.dp).height(62.dp).align(Alignment.BottomEnd).padding(end = 18.dp)
                    .background(style.skin, RoundedCornerShape(10.dp))
                    .graphicsLayer { rotationZ = if (isActive) -5f else -2f }
            )
        }

        Box(
            Modifier.width(106.dp).height(140.dp)
                .background(
                    Brush.verticalGradient(listOf(style.jacket, style.shirt)),
                    RoundedCornerShape(topStart = 38.dp, topEnd = 38.dp, bottomStart = 16.dp, bottomEnd = 16.dp)
                )
        ) {
            Box(Modifier.width(34.dp).height(8.dp).align(Alignment.TopCenter).padding(top = 13.dp).background(accent.copy(alpha = if (isActive) .95f else .25f), CircleShape))
            if (style.accessory == 1) {
                Box(Modifier.width(10.dp).height(58.dp).align(Alignment.TopCenter).padding(top = 16.dp).background(Color(0xFFE7E0D6), RoundedCornerShape(4.dp)))
            } else if (style.accessory == 2) {
                Box(Modifier.size(22.dp).align(Alignment.TopEnd).padding(top = 18.dp, end = 14.dp).background(Color(0xFFFFD56A), CircleShape))
            } else if (style.accessory == 3) {
                Box(Modifier.width(42.dp).height(12.dp).align(Alignment.TopCenter).padding(top = 18.dp).background(Color(0xFF79C7C0), RoundedCornerShape(6.dp)))
            }
        }

        Box(Modifier.width(72.dp).height(16.dp).background(style.skin, RoundedCornerShape(8.dp)))

        Box(Modifier.size(82.dp).background(style.skin, CircleShape)) {
            when (style.hairStyle) {
                0 -> Box(Modifier.fillMaxWidth().height(30.dp).align(Alignment.TopCenter).background(style.hair, RoundedCornerShape(topStart = 42.dp, topEnd = 42.dp, bottomEnd = 10.dp)))
                1 -> {
                    Box(Modifier.fillMaxWidth().height(25.dp).align(Alignment.TopCenter).background(style.hair, RoundedCornerShape(topStart = 42.dp, topEnd = 42.dp)))
                    Box(Modifier.width(16.dp).height(48.dp).align(Alignment.TopStart).background(style.hair, RoundedCornerShape(8.dp)))
                }
                2 -> {
                    Box(Modifier.fillMaxWidth().height(28.dp).align(Alignment.TopCenter).background(style.hair, RoundedCornerShape(42.dp)))
                    Box(Modifier.size(26.dp).align(Alignment.TopEnd).background(style.hair, CircleShape))
                }
                else -> Box(Modifier.fillMaxWidth().height(34.dp).align(Alignment.TopCenter).background(style.hair, RoundedCornerShape(topStart = 42.dp, topEnd = 42.dp, bottomStart = 14.dp, bottomEnd = 14.dp)))
            }
            Row(Modifier.align(Alignment.Center).padding(top = 9.dp), horizontalArrangement = Arrangement.spacedBy(18.dp)) {
                Box(Modifier.size(6.dp).background(Color(0xFF2A2528), CircleShape))
                Box(Modifier.size(6.dp).background(Color(0xFF2A2528), CircleShape))
            }
            Box(
                Modifier.width(if (isActive) 22.dp else 16.dp).height(mouth.dp).align(Alignment.BottomCenter).padding(bottom = 16.dp)
                    .background(Color(0xFF8E4A50), RoundedCornerShape(8.dp))
            )
        }

        Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Box(Modifier.width(34.dp).height(72.dp).background(style.trousers, RoundedCornerShape(bottomStart = 12.dp, bottomEnd = 12.dp)))
            Box(Modifier.width(34.dp).height(72.dp).background(style.trousers, RoundedCornerShape(bottomStart = 12.dp, bottomEnd = 12.dp)))
        }
    }
}

@Composable
fun SceneStage(
    scene: SceneInfo,
    location: LocationProfile?,
    characterProfiles: Map<String, CharacterProfile>,
    activeSpeaker: String,
    isSpeaking: Boolean,
    dialogueZh: String,
    dialoguePinyin: String,
    dialogueTr: String,
    showPinyin: Boolean,
    showTurkish: Boolean,
    speakerLabel: String,
    modifier: Modifier = Modifier
) {
    val theme = location?.theme ?: "generic"
    val colors = palette(theme, scene.production.timeOfDay)

    // Stable cast order: never truncate speakers.  Truncating the cast used to make any
    // fifth-or-later speaker fall back to slot 0, which put the marker on the wrong person.
    val cast = remember(scene.id) {
        (scene.production.characters + scene.dialogues.map { it.speaker })
            .filter { it.isNotBlank() && it != "旁白" }
            .distinct()
    }

    val activeIndex = cast.indexOf(activeSpeaker)

    Box(modifier.fillMaxSize().background(Color.Black)) {
        val sceneArtPath = "chinese_course/media/scenes/${scene.id}.webp"
        val sceneArtBitmap = rememberAssetBitmap(sceneArtPath)
        val backgroundBitmap = rememberAssetBitmap(location?.backgroundAsset.orEmpty())
        when {
            sceneArtBitmap != null -> {
                Image(
                    bitmap = sceneArtBitmap,
                    contentDescription = scene.titleTr.ifBlank { location?.nameTr ?: "Sahne görseli" },
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
            }
            backgroundBitmap != null -> {
                Image(
                    bitmap = backgroundBitmap,
                    contentDescription = location?.nameTr ?: "Sahne arka planı",
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
            }
            else -> SceneDecor(theme, colors)
        }

        if (sceneArtBitmap == null) {
            Row(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
                    .fillMaxHeight(0.61f)
                    .padding(start = 2.dp, end = 2.dp, bottom = 110.dp),
                horizontalArrangement = Arrangement.SpaceEvenly,
                verticalAlignment = Alignment.Bottom
            ) {
                cast.forEach { name ->
                    val profile = characterProfiles[name]
                    val isActive = name == activeSpeaker
                    val portraitBitmap = rememberAssetBitmap(portraitVariantFor(profile, scene.level))
                    val scale by animateFloatAsState(if (isActive) 1.09f else 1f, tween(220), label = "assetScale-$name")
                    val infinite = rememberInfiniteTransition(label = "assetMotion-$name")
                    val bob by infinite.animateFloat(-1f, 1.5f, infiniteRepeatable(tween(if (isActive) 820 else 1400), RepeatMode.Reverse), label = "assetBob")

                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight(),
                        contentAlignment = Alignment.BottomCenter
                    ) {
                        if (portraitBitmap != null) {
                            val ageScale = when {
                                profile?.id?.contains("ZHANGLELE") == true && scene.level in listOf("HSK1", "HSK2") -> 0.64f
                                profile?.id?.contains("ZHANGLELE") == true && scene.level == "HSK3" -> 0.72f
                                profile?.id?.contains("ZHANGLELE") == true && scene.level == "HSK4" -> 0.82f
                                profile?.id?.contains("ZHANGYUTONG") == true && scene.level in listOf("HSK1", "HSK2") -> 0.82f
                                profile?.id?.contains("ZHANGYUTONG") == true && scene.level == "HSK3" -> 0.88f
                                else -> if (isActive) 0.98f else 0.90f
                            }
                            Image(
                                bitmap = portraitBitmap,
                                contentDescription = name,
                                modifier = Modifier
                                    .fillMaxHeight(ageScale)
                                    .fillMaxWidth()
                                    .offset(y = bob.dp)
                                    .scale(scale)
                                    .alpha(if (isActive) 1f else .92f),
                                contentScale = ContentScale.Fit
                            )
                        } else {
                            CartoonCharacter(name, profile, isActive, isSpeaking, colors.accent)
                        }
                    }
                }
            }

        }
        // Explicit mouth anchors are used for pre-rendered scene art.  They prevent
        // a male/female speaker from being visually associated with the wrong character.
        val sceneArtMouthAnchor: Pair<Float, Float>? = if (sceneArtBitmap != null) when (scene.id) {
            "ZH_HSK1_SC001" -> when (activeSpeaker) {
                "张伟" -> 0.175f to 0.404f
                "刘梅" -> 0.372f to 0.414f
                "张雨桐" -> 0.658f to 0.442f
                "张乐乐" -> 0.489f to 0.483f
                "王师傅" -> 0.886f to 0.404f
                else -> null
            }
            else -> null
        } else null

        // The dialogue text lives in the bottom subtitle panel.  The stage bubble is
        // intentionally empty: it only marks the character whose turn it is to speak.
        // Only show the mouth marker when character positions are actually known.
        // A pre-rendered scene image has no per-character mouth coordinates; guessing from
        // cast order produced misleading markers over the wrong person.
        if (
            dialogueZh.isNotBlank() &&
            activeSpeaker.isNotBlank() &&
            activeIndex >= 0 &&
            (sceneArtBitmap == null || sceneArtMouthAnchor != null)
        ) {
            BoxWithConstraints(Modifier.fillMaxSize()) {
                val mouthXFraction =
                    sceneArtMouthAnchor?.first
                        ?: ((activeIndex + 0.5f) / cast.size.coerceAtLeast(1).toFloat()).coerceIn(0.08f, 0.92f)
                val bubbleWidth = 46.dp
                val bubbleHeight = 28.dp
                val placeOnRight = mouthXFraction <= 0.50f
                val horizontalNudge = if (placeOnRight) 34.dp else (-34).dp
                val bubbleX = (
                    maxWidth * mouthXFraction - bubbleWidth / 2 + horizontalNudge
                ).coerceIn(6.dp, maxWidth - bubbleWidth - 6.dp)
                val mouthYFraction = sceneArtMouthAnchor?.second ?: 0.63f
                val bubbleY = (
                    maxHeight * mouthYFraction - bubbleHeight / 2
                ).coerceIn(92.dp, maxHeight - 220.dp)

                Column(
                    modifier = Modifier.offset(x = bubbleX, y = bubbleY),
                    horizontalAlignment = if (placeOnRight) Alignment.Start else Alignment.End
                ) {
                    Box(
                        Modifier
                            .size(width = bubbleWidth, height = bubbleHeight)
                            .background(
                                Color.White.copy(alpha = 0.12f),
                                RoundedCornerShape(9.dp)
                            )
                            .drawBehind {
                                val stroke = 1.15.dp.toPx()
                                drawRoundRect(
                                    color = Color.White.copy(alpha = 0.90f),
                                    cornerRadius = CornerRadius(9.dp.toPx(), 9.dp.toPx()),
                                    style = Stroke(
                                        width = stroke,
                                        pathEffect = PathEffect.dashPathEffect(
                                            floatArrayOf(5.dp.toPx(), 4.dp.toPx())
                                        )
                                    )
                                )
                            }
                    )
                    Box(
                        Modifier
                            .padding(
                                start = if (placeOnRight) 7.dp else 0.dp,
                                end = if (placeOnRight) 0.dp else 7.dp
                            )
                            .size(7.dp)
                            .graphicsLayer { rotationZ = 45f }
                            .background(Color.White.copy(alpha = 0.10f))
                            .drawBehind {
                                drawRect(
                                    color = Color.White.copy(alpha = 0.86f),
                                    style = Stroke(
                                        width = 1.dp.toPx(),
                                        pathEffect = PathEffect.dashPathEffect(
                                            floatArrayOf(3.dp.toPx(), 2.dp.toPx())
                                        )
                                    )
                                )
                            }
                    )
                }
            }
        }

        if (location != null) {
            Surface(
                modifier = Modifier.align(Alignment.TopEnd).statusBarsPadding().padding(top = 68.dp, end = 12.dp),
                color = Color.Black.copy(alpha = 0.48f),
                contentColor = Color.White,
                shape = RoundedCornerShape(12.dp)
            ) {
                Text(location.nameTr, modifier = Modifier.padding(horizontal = 9.dp, vertical = 5.dp), fontSize = 10.sp, fontWeight = FontWeight.SemiBold)
            }
        }
    }
}
