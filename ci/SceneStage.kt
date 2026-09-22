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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

private data class StagePalette(val top: Color, val bottom: Color, val accent: Color)

private fun portraitVariantFor(profile: CharacterProfile?, level: String): String {
    if (profile == null) return ""
    return profile.portraitByLevel[level].orEmpty().ifBlank { profile.portraitAsset }
}

private fun palette(theme: String, timeOfDay: String): StagePalette {
    val night = timeOfDay.contains("night", ignoreCase = true) || timeOfDay.contains("evening", ignoreCase = true)
    if (night) return StagePalette(Color(0xFF152238), Color(0xFF080D18), Color(0xFF8FB9FF))
    return when (theme) {
        "home" -> StagePalette(Color(0xFFD8B58A), Color(0xFF7E5A45), Color(0xFFFFE0B2))
        "cafe" -> StagePalette(Color(0xFFB06E46), Color(0xFF4B2A24), Color(0xFFFFD59A))
        "school" -> StagePalette(Color(0xFF6E91B5), Color(0xFF314C6D), Color(0xFFD6EDFF))
        "health" -> StagePalette(Color(0xFF77AFA5), Color(0xFF315D59), Color(0xFFD5FFF7))
        "transport" -> StagePalette(Color(0xFF6C7280), Color(0xFF2F3440), Color(0xFFFFD17C))
        "work" -> StagePalette(Color(0xFF73809A), Color(0xFF333D52), Color(0xFFD7E0FF))
        "nature" -> StagePalette(Color(0xFF6E9C66), Color(0xFF2D5B38), Color(0xFFD5F4B5))
        "market" -> StagePalette(Color(0xFFB57A5F), Color(0xFF604536), Color(0xFFFFD8B5))
        "hotel" -> StagePalette(Color(0xFF8E7AAE), Color(0xFF44375B), Color(0xFFE9D9FF))
        "community" -> StagePalette(Color(0xFF7E8FB0), Color(0xFF394A68), Color(0xFFE1E8FF))
        "service" -> StagePalette(Color(0xFF7D8EA0), Color(0xFF364553), Color(0xFFDCEBFA))
        else -> StagePalette(Color(0xFF755B8B), Color(0xFF32243F), Color(0xFFE9D5FF))
    }
}

private fun fallbackBodyColor(name: String): Color {
    val colors = listOf(
        Color(0xFF496DDB), Color(0xFFB95C75), Color(0xFF4D9A77),
        Color(0xFFB77C39), Color(0xFF7B63B6), Color(0xFF3F879B),
        Color(0xFFA75C45), Color(0xFF6D7D45)
    )
    return colors[(name.hashCode() and Int.MAX_VALUE) % colors.size]
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
private fun FallbackSceneDecor(theme: String, colors: StagePalette) {
    Box(Modifier.fillMaxSize()) {
        Box(
            Modifier
                .fillMaxWidth()
                .fillMaxHeight(0.38f)
                .align(Alignment.BottomCenter)
                .background(Color.Black.copy(alpha = 0.16f))
        )

        // Window / light panel
        Box(
            Modifier
                .width(88.dp)
                .height(72.dp)
                .align(Alignment.TopEnd)
                .padding(top = 18.dp, end = 18.dp)
                .clip(RoundedCornerShape(12.dp))
                .background(colors.accent.copy(alpha = 0.20f))
        )

        when (theme) {
            "home", "hotel" -> {
                Box(
                    Modifier
                        .width(120.dp)
                        .height(44.dp)
                        .align(Alignment.BottomStart)
                        .padding(start = 18.dp, bottom = 24.dp)
                        .clip(RoundedCornerShape(14.dp))
                        .background(Color.White.copy(alpha = 0.15f))
                )
            }
            "cafe", "market" -> {
                Box(
                    Modifier
                        .width(136.dp)
                        .height(18.dp)
                        .align(Alignment.BottomCenter)
                        .padding(bottom = 34.dp)
                        .clip(RoundedCornerShape(9.dp))
                        .background(Color.White.copy(alpha = 0.18f))
                )
            }
            "school", "work", "service" -> {
                Box(
                    Modifier
                        .width(138.dp)
                        .height(64.dp)
                        .align(Alignment.CenterEnd)
                        .padding(end = 18.dp)
                        .clip(RoundedCornerShape(10.dp))
                        .background(Color.White.copy(alpha = 0.12f))
                )
            }
            "nature" -> {
                Box(
                    Modifier
                        .size(72.dp)
                        .align(Alignment.TopEnd)
                        .padding(top = 18.dp, end = 26.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFFFF1A8).copy(alpha = 0.22f))
                )
            }
        }
    }
}

@Composable
private fun FallbackCharacter(
    name: String,
    isActive: Boolean,
    accent: Color,
    alpha: Float
) {
    val bodyColor = fallbackBodyColor(name)
    val bodyWidth = if (isActive) 62.dp else 54.dp
    val bodyHeight = if (isActive) 60.dp else 52.dp
    val headSize = if (isActive) 42.dp else 36.dp

    Box(
        modifier = Modifier
            .width(if (isActive) 72.dp else 62.dp)
            .height(if (isActive) 100.dp else 88.dp),
        contentAlignment = Alignment.BottomCenter
    ) {
        Surface(
            modifier = Modifier
                .width(bodyWidth)
                .height(bodyHeight)
                .align(Alignment.BottomCenter),
            shape = RoundedCornerShape(topStart = 26.dp, topEnd = 26.dp, bottomStart = 12.dp, bottomEnd = 12.dp),
            color = bodyColor.copy(alpha = alpha),
            shadowElevation = if (isActive) 9.dp else 2.dp
        ) {
            Box(contentAlignment = Alignment.Center) {
                if (isActive) {
                    Box(
                        Modifier
                            .width(30.dp)
                            .height(4.dp)
                            .align(Alignment.TopCenter)
                            .padding(top = 8.dp)
                            .clip(CircleShape)
                            .background(accent.copy(alpha = 0.9f))
                    )
                }
            }
        }

        Surface(
            modifier = Modifier
                .size(headSize)
                .align(Alignment.TopCenter),
            shape = CircleShape,
            color = Color(0xFFF2C6A0).copy(alpha = alpha),
            shadowElevation = if (isActive) 7.dp else 2.dp
        ) {
            Box(contentAlignment = Alignment.Center) {
                Box(
                    Modifier
                        .fillMaxWidth()
                        .height(if (isActive) 15.dp else 13.dp)
                        .align(Alignment.TopCenter)
                        .background(Color(0xFF2E2430).copy(alpha = alpha))
                )
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.padding(top = 7.dp)
                ) {
                    Box(Modifier.size(3.dp).clip(CircleShape).background(Color(0xFF3A2B2E).copy(alpha = alpha)))
                    Box(Modifier.size(3.dp).clip(CircleShape).background(Color(0xFF3A2B2E).copy(alpha = alpha)))
                }
            }
        }

        Surface(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 6.dp),
            shape = RoundedCornerShape(8.dp),
            color = Color.Black.copy(alpha = if (isActive) 0.48f else 0.30f)
        ) {
            Text(
                name.take(2).ifBlank { "人" },
                color = Color.White.copy(alpha = alpha),
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(horizontal = 7.dp, vertical = 2.dp)
            )
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
    }.distinct().take(5)

    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(286.dp)
            .clip(RoundedCornerShape(24.dp))
            .background(Brush.verticalGradient(listOf(colors.top, colors.bottom)))
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
            FallbackSceneDecor(theme, colors)
            Text(
                text = location?.icon ?: "场",
                color = Color.White.copy(alpha = 0.08f),
                fontSize = 116.sp,
                modifier = Modifier.align(Alignment.CenterEnd).padding(end = 22.dp),
                fontWeight = FontWeight.Bold
            )
        }

        Box(
            Modifier
                .fillMaxWidth()
                .height(112.dp)
                .align(Alignment.BottomCenter)
                .background(
                    Brush.verticalGradient(
                        listOf(Color.Transparent, Color.Black.copy(alpha = 0.58f))
                    )
                )
        )

        Column(Modifier.align(Alignment.TopStart).padding(14.dp)) {
            Surface(color = Color.Black.copy(alpha = 0.48f), shape = RoundedCornerShape(14.dp)) {
                Column(Modifier.padding(horizontal = 12.dp, vertical = 7.dp)) {
                    Text(
                        location?.nameZh ?: scene.production.locationId,
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp
                    )
                    Text(location?.nameTr.orEmpty(), color = Color.White.copy(alpha = 0.82f), fontSize = 11.sp)
                }
            }
            if (scene.production.atmosphere.isNotBlank()) {
                Text(
                    scene.production.atmosphere,
                    color = Color.White.copy(alpha = 0.78f),
                    fontSize = 10.sp,
                    modifier = Modifier.padding(top = 6.dp)
                )
            }
        }

        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .padding(horizontal = 8.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.Bottom
        ) {
            cast.forEach { name ->
                val profile = characterProfiles[name]
                val isActive = name == activeSpeaker
                val scale by animateFloatAsState(if (isActive) 1.08f else 0.90f, label = "speakerFocus")
                val alpha = if (isActive) 1f else 0.72f
                val portraitBitmap = rememberAssetBitmap(portraitVariantFor(profile, scene.level))

                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier
                        .widthIn(min = 58.dp, max = 78.dp)
                        .scale(scale)
                ) {
                    if (portraitBitmap != null) {
                        // Real character art is a transparent full-body/bust asset.
                        // Never crop it into a circle.
                        Box(
                            modifier = Modifier
                                .width(if (isActive) 78.dp else 68.dp)
                                .height(if (isActive) 116.dp else 102.dp),
                            contentAlignment = Alignment.BottomCenter
                        ) {
                            Image(
                                bitmap = portraitBitmap,
                                contentDescription = name,
                                modifier = Modifier.fillMaxSize(),
                                contentScale = ContentScale.Fit
                            )
                        }
                    } else {
                        FallbackCharacter(name, isActive, colors.accent, alpha)
                    }

                    Surface(
                        color = if (isActive) colors.accent.copy(alpha = 0.92f) else Color.Black.copy(alpha = 0.36f),
                        shape = RoundedCornerShape(9.dp),
                        modifier = Modifier.padding(top = 3.dp)
                    ) {
                        Text(
                            name,
                            color = if (isActive) Color(0xFF302238) else Color.White.copy(alpha = alpha),
                            fontSize = 10.sp,
                            fontWeight = if (isActive) FontWeight.Bold else FontWeight.Medium,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                        )
                    }
                }
            }
        }
    }
}
