package com.ayhan.chineselearning

import android.graphics.BitmapFactory
import androidx.compose.animation.core.animateFloatAsState
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
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private data class StagePalette(val top: Color, val middle: Color, val bottom: Color, val accent: Color)

private fun portraitVariantFor(profile: CharacterProfile?, level: String): String {
    if (profile == null) return ""
    return profile.portraitByLevel[level].orEmpty().ifBlank { profile.portraitAsset }
}

private fun palette(theme: String, timeOfDay: String): StagePalette {
    val night = timeOfDay.contains("night", ignoreCase = true) || timeOfDay.contains("evening", ignoreCase = true)
    if (night) return StagePalette(
        Color(0xFF172033),
        Color(0xFF28364B),
        Color(0xFF090B10),
        Color(0xFFFFC857)
    )
    return when (theme) {
        "home" -> StagePalette(Color(0xFFD7B08A), Color(0xFF9A6D52), Color(0xFF4A322A), Color(0xFFFFD09A))
        "cafe" -> StagePalette(Color(0xFFC38761), Color(0xFF7D4B36), Color(0xFF351F1A), Color(0xFFFFC857))
        "school" -> StagePalette(Color(0xFF9AB7D2), Color(0xFF5F7E9A), Color(0xFF263849), Color(0xFFFFD67E))
        "health" -> StagePalette(Color(0xFFA9D4CA), Color(0xFF699A92), Color(0xFF27443F), Color(0xFFFFFFFF))
        "transport" -> StagePalette(Color(0xFF9BA2AF), Color(0xFF626B79), Color(0xFF242A32), Color(0xFFFFC857))
        "work" -> StagePalette(Color(0xFF9AA6BC), Color(0xFF657187), Color(0xFF2B3445), Color(0xFFFFC857))
        "nature" -> StagePalette(Color(0xFF9FC18E), Color(0xFF5D8B59), Color(0xFF29462E), Color(0xFFFFE18A))
        "market" -> StagePalette(Color(0xFFD5A17E), Color(0xFF9C684E), Color(0xFF4E342A), Color(0xFFFFC857))
        "hotel" -> StagePalette(Color(0xFFB5A5C9), Color(0xFF7D6A94), Color(0xFF342B42), Color(0xFFFFD88B))
        "community" -> StagePalette(Color(0xFFA5B0C8), Color(0xFF6C7894), Color(0xFF313B50), Color(0xFFFFD36B))
        "service" -> StagePalette(Color(0xFFAAB8C4), Color(0xFF6C7D8B), Color(0xFF2E3A44), Color(0xFFFFD36B))
        else -> StagePalette(Color(0xFF8E729F), Color(0xFF624A75), Color(0xFF241B2C), Color(0xFFFFC857))
    }
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
private fun CinematicFallbackBackground(theme: String, colors: StagePalette) {
    Box(
        Modifier
            .fillMaxSize()
            .background(Brush.verticalGradient(listOf(colors.top, colors.middle, colors.bottom)))
    ) {
        Box(
            Modifier
                .fillMaxWidth()
                .fillMaxHeight(0.42f)
                .align(Alignment.BottomCenter)
                .background(Color.Black.copy(alpha = 0.18f))
        )

        when (theme) {
            "home", "hotel" -> {
                Box(
                    Modifier
                        .fillMaxWidth(0.64f)
                        .fillMaxHeight(0.16f)
                        .align(Alignment.BottomStart)
                        .padding(start = 18.dp, bottom = 116.dp)
                        .background(Color.White.copy(alpha = 0.08f), RoundedCornerShape(22.dp))
                )
                Box(
                    Modifier
                        .width(120.dp)
                        .height(150.dp)
                        .align(Alignment.CenterEnd)
                        .padding(end = 20.dp)
                        .background(colors.accent.copy(alpha = 0.12f), RoundedCornerShape(28.dp))
                )
            }
            "cafe", "market" -> {
                Box(
                    Modifier
                        .fillMaxWidth(0.86f)
                        .height(26.dp)
                        .align(Alignment.BottomCenter)
                        .padding(bottom = 144.dp)
                        .background(Color.White.copy(alpha = 0.10f), RoundedCornerShape(13.dp))
                )
                Row(
                    Modifier.align(Alignment.Center).padding(top = 90.dp),
                    horizontalArrangement = Arrangement.spacedBy(24.dp)
                ) {
                    repeat(3) {
                        Box(
                            Modifier
                                .width(56.dp)
                                .height(98.dp)
                                .background(Color.Black.copy(alpha = 0.10f), RoundedCornerShape(12.dp))
                        )
                    }
                }
            }
            "school", "work", "service", "health" -> {
                Box(
                    Modifier
                        .fillMaxWidth(0.76f)
                        .fillMaxHeight(0.22f)
                        .align(Alignment.CenterEnd)
                        .padding(end = 18.dp)
                        .background(Color.White.copy(alpha = 0.09f), RoundedCornerShape(18.dp))
                )
            }
            "nature" -> {
                Box(
                    Modifier
                        .size(150.dp)
                        .align(Alignment.TopEnd)
                        .padding(top = 64.dp, end = 28.dp)
                        .background(Color(0xFFFFF0A0).copy(alpha = 0.16f), CircleShape)
                )
            }
        }

        Box(
            Modifier
                .fillMaxWidth()
                .fillMaxHeight(0.25f)
                .align(Alignment.TopCenter)
                .background(
                    Brush.verticalGradient(
                        listOf(Color.Black.copy(alpha = 0.16f), Color.Transparent)
                    )
                )
        )
    }
}

@Composable
private fun FallbackSilhouette(
    name: String,
    isActive: Boolean,
    accent: Color
) {
    val scale by animateFloatAsState(if (isActive) 1.05f else 0.92f, label = "fallbackCharacterScale")
    val opacity = if (isActive) 1f else 0.72f
    val cloth = when ((name.hashCode() and Int.MAX_VALUE) % 6) {
        0 -> Color(0xFF4E6FA8)
        1 -> Color(0xFF8D5B6C)
        2 -> Color(0xFF567E67)
        3 -> Color(0xFF8A6A49)
        4 -> Color(0xFF675987)
        else -> Color(0xFF4F747D)
    }

    Column(
        modifier = Modifier
            .width(112.dp)
            .height(300.dp)
            .scale(scale)
            .alpha(opacity),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Bottom
    ) {
        Box(
            modifier = Modifier
                .size(70.dp)
                .background(Color(0xFFE4B891), CircleShape)
        ) {
            Box(
                Modifier
                    .fillMaxWidth()
                    .height(26.dp)
                    .align(Alignment.TopCenter)
                    .background(Color(0xFF2B2528), RoundedCornerShape(topStart = 36.dp, topEnd = 36.dp))
            )
        }
        Box(
            modifier = Modifier
                .width(if (isActive) 104.dp else 94.dp)
                .height(if (isActive) 190.dp else 174.dp)
                .background(
                    if (isActive) cloth else cloth.copy(alpha = 0.9f),
                    RoundedCornerShape(topStart = 46.dp, topEnd = 46.dp, bottomStart = 16.dp, bottomEnd = 16.dp)
                )
        ) {
            if (isActive) {
                Box(
                    Modifier
                        .width(38.dp)
                        .height(5.dp)
                        .align(Alignment.TopCenter)
                        .padding(top = 14.dp)
                        .background(accent, CircleShape)
                )
            }
        }
    }
}

@Composable
fun SceneStage(
    scene: SceneInfo,
    location: LocationProfile?,
    characterProfiles: Map<String, CharacterProfile>,
    activeSpeaker: String,
    modifier: Modifier = Modifier
) {
    val theme = location?.theme ?: "generic"
    val colors = palette(theme, scene.production.timeOfDay)
    val baseCast = scene.production.characters.ifEmpty {
        scene.dialogues.map { it.speaker }.filter { it.isNotBlank() && it != "旁白" }.distinct()
    }
    val cast = buildList {
        if (activeSpeaker.isNotBlank() && activeSpeaker != "旁白") add(activeSpeaker)
        addAll(baseCast.filter { it != activeSpeaker && it != "旁白" })
    }.distinct().take(4)

    Box(
        modifier = modifier
            .fillMaxSize()
            .background(Color.Black)
    ) {
        val backgroundBitmap = rememberAssetBitmap(location?.backgroundAsset.orEmpty())
        if (backgroundBitmap != null) {
            Image(
                bitmap = backgroundBitmap,
                contentDescription = location?.nameTr ?: "Sahne arka planı",
                modifier = Modifier.fillMaxSize(),
                contentScale = ContentScale.Crop
            )
        } else {
            CinematicFallbackBackground(theme, colors)
        }

        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .fillMaxHeight(0.58f)
                .padding(horizontal = 6.dp, bottom = 116.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.Bottom
        ) {
            cast.forEach { name ->
                val profile = characterProfiles[name]
                val isActive = name == activeSpeaker
                val portraitBitmap = rememberAssetBitmap(portraitVariantFor(profile, scene.level))
                val scale by animateFloatAsState(if (isActive) 1.07f else 0.93f, label = "speakerScale")
                val alpha = if (isActive) 1f else 0.74f

                if (portraitBitmap != null) {
                    Image(
                        bitmap = portraitBitmap,
                        contentDescription = name,
                        modifier = Modifier
                            .fillMaxHeight(if (isActive) 0.98f else 0.88f)
                            .widthIn(min = 92.dp, max = 170.dp)
                            .scale(scale)
                            .alpha(alpha),
                        contentScale = ContentScale.Fit
                    )
                } else {
                    FallbackSilhouette(name, isActive, colors.accent)
                }
            }
        }

        if (location != null) {
            Surface(
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .statusBarsPadding()
                    .padding(top = 68.dp, end = 12.dp),
                color = Color.Black.copy(alpha = 0.52f),
                contentColor = Color.White,
                shape = RoundedCornerShape(12.dp)
            ) {
                Text(
                    location.nameTr,
                    modifier = Modifier.padding(horizontal = 9.dp, vertical = 5.dp),
                    fontSize = 10.sp,
                    fontWeight = FontWeight.SemiBold
                )
            }
        }
    }
}
