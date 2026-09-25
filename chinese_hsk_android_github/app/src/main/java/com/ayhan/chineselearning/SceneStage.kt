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

@Composable
private fun rememberAssetBitmap(path: String): ImageBitmap? {
    val context = LocalContext.current
    return remember(path) {
        if (path.isBlank()) null
        else try { context.assets.open(path).use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }
        catch (_: Exception) { null }
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
            .height(238.dp)
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
        }

        if (backgroundBitmap == null) {
            Text(
                text = location?.icon ?: "场",
                color = Color.White.copy(alpha = 0.10f),
                fontSize = 116.sp,
                modifier = Modifier.align(Alignment.CenterEnd).padding(end = 22.dp),
                fontWeight = FontWeight.Bold
            )
            Box(
                Modifier
                    .fillMaxWidth()
                    .height(78.dp)
                    .align(Alignment.BottomCenter)
                    .background(Color.Black.copy(alpha = 0.20f))
            )
        }

        Column(Modifier.align(Alignment.TopStart).padding(14.dp)) {
            Surface(color = Color.Black.copy(alpha = 0.42f), shape = RoundedCornerShape(14.dp)) {
                Column(Modifier.padding(horizontal = 12.dp, vertical = 7.dp)) {
                    Text(location?.nameZh ?: scene.production.locationId, color = Color.White, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    Text(location?.nameTr.orEmpty(), color = Color.White.copy(alpha = 0.78f), fontSize = 11.sp)
                }
            }
            if (scene.production.atmosphere.isNotBlank()) {
                Text(
                    scene.production.atmosphere,
                    color = Color.White.copy(alpha = 0.72f),
                    fontSize = 10.sp,
                    modifier = Modifier.padding(top = 6.dp)
                )
            }
        }

        Row(
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .fillMaxWidth()
                .padding(horizontal = 10.dp, vertical = 10.dp),
            horizontalArrangement = Arrangement.SpaceEvenly,
            verticalAlignment = Alignment.Bottom
        ) {
            cast.forEach { name ->
                val profile = characterProfiles[name]
                val isActive = name == activeSpeaker
                val scale by animateFloatAsState(if (isActive) 1.10f else 0.92f, label = "speakerFocus")
                val alpha = if (isActive) 1f else 0.72f
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.widthIn(max = 72.dp).scale(scale)
                ) {
                    Surface(
                        modifier = Modifier.size(if (isActive) 62.dp else 52.dp),
                        shape = CircleShape,
                        color = if (isActive) colors.accent else Color.White.copy(alpha = 0.82f),
                        shadowElevation = if (isActive) 8.dp else 2.dp
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            val portraitBitmap = rememberAssetBitmap(portraitVariantFor(profile, scene.level))
                            if (portraitBitmap != null) {
                                Image(
                                    bitmap = portraitBitmap,
                                    contentDescription = name,
                                    modifier = Modifier.fillMaxSize().clip(CircleShape),
                                    contentScale = ContentScale.Crop
                                )
                            } else {
                                Text(
                                    name.take(1).ifBlank { "人" },
                                    color = Color(0xFF352442).copy(alpha = alpha),
                                    fontSize = if (isActive) 25.sp else 21.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }
                    }
                    Text(
                        name,
                        color = Color.White.copy(alpha = alpha),
                        fontSize = 11.sp,
                        fontWeight = if (isActive) FontWeight.Bold else FontWeight.Medium,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.padding(top = 5.dp)
                    )
                }
            }
        }
    }
}
