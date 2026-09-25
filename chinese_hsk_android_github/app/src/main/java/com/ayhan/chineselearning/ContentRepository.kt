package com.ayhan.chineselearning

import android.content.Context
import org.json.JSONObject

data class LevelInfo(
    val id: String,
    val title: String,
    val sceneCount: Int,
    val completeScenes: Int,
    val blueprintReadyScenes: Int,
    val storyArc: String
)

data class DialogueLine(
    val id: String,
    val speaker: String,
    val zh: String,
    val pinyin: String,
    val tr: String,
    val emotion: String = "neutral",
    val actionTr: String = "",
    val audioAsset: String = "",
    val sfxAsset: String = ""
)

data class CharacterProfile(
    val id: String,
    val nameZh: String,
    val pinyin: String = "",
    val role: String = "supporting",
    val portraitAsset: String = "",
    val portraitVariants: Map<String, String> = emptyMap(),
    val portraitByLevel: Map<String, String> = emptyMap(),
    val voiceProfileId: String = ""
)

data class LocationProfile(
    val id: String,
    val nameZh: String,
    val nameTr: String,
    val theme: String = "generic",
    val icon: String = "场",
    val backgroundAsset: String = ""
)

data class VoiceProfile(
    val id: String,
    val characterId: String,
    val language: String = "zh-CN",
    val style: String = "natural",
    val authoredAudioPreferred: Boolean = true
)

data class NarratorInfo(
    val profileId: String = "NARRATOR_ZH_001",
    val zh: String = "",
    val pinyin: String = "",
    val tr: String = "",
    val audioAsset: String = ""
)

data class ProductionInfo(
    val locationId: String = "",
    val timeOfDay: String = "day",
    val atmosphere: String = "",
    val characters: List<String> = emptyList(),
    val visualStyle: String = "visual_novel_theatre",
    val animationLevel: String = "minimal",
    val speakerFocus: Boolean = true,
    val narrator: NarratorInfo = NarratorInfo(),
    val ambienceAsset: String = "",
    val musicAsset: String = ""
)

data class VocabularyCard(
    val id: String,
    val zh: String,
    val pinyin: String,
    val tr: String,
    val exampleZh: String = "",
    val examplePinyin: String = "",
    val exampleTr: String = "",
    val kind: String = "active"
)

data class SentenceExercise(
    val id: String,
    val type: String,
    val promptTr: String,
    val tokens: List<String> = emptyList(),
    val answerTokens: List<String> = emptyList(),
    val blankSentenceZh: String = "",
    val options: List<String> = emptyList(),
    val answer: String = ""
)

data class ComprehensionQuestion(
    val id: String,
    val questionTr: String,
    val optionsTr: List<String>,
    val correctIndex: Int
)

data class PronunciationItem(
    val id: String,
    val zh: String,
    val pinyin: String,
    val tr: String
)

data class InteractiveOption(
    val zh: String,
    val tr: String,
    val correct: Boolean
)

data class InteractiveDialogueItem(
    val id: String,
    val promptZh: String,
    val promptPinyin: String,
    val promptTr: String,
    val options: List<InteractiveOption>
)

data class ExamRules(
    val vocabularyPassPercent: Int = 90,
    val sentencePassPercent: Int = 85,
    val lockNextSceneUntilPassed: Boolean = true
)

data class LearningInfo(
    val communicationGoals: List<String> = emptyList(),
    val vocabularyTheme: String = "",
    val grammarTheme: String = "",
    val pronunciationTheme: String = "",
    val defaultSpeechSpeed: Float = 1.0f,
    val defaultSubtitleMode: String = "ZH_PINYIN_TR",
    val vocabularyCards: List<VocabularyCard> = emptyList(),
    val sentenceExercises: List<SentenceExercise> = emptyList(),
    val comprehensionQuestions: List<ComprehensionQuestion> = emptyList(),
    val pronunciationItems: List<PronunciationItem> = emptyList(),
    val interactiveDialogue: List<InteractiveDialogueItem> = emptyList(),
    val examRules: ExamRules = ExamRules()
)

data class SceneInfo(
    val id: String,
    val level: String,
    val number: Int,
    val titleZh: String,
    val titleTr: String,
    val complete: Boolean,
    val productionStatus: String,
    val miniAdventureTr: String = "",
    val learning: LearningInfo = LearningInfo(),
    val production: ProductionInfo = ProductionInfo(),
    val dialogues: List<DialogueLine>
) {
    val isOpenable: Boolean
        get() = productionStatus != "planned"
}

data class VocabularyStudyItem(
    val levelId: String,
    val sceneId: String,
    val sceneTitleTr: String,
    val card: VocabularyCard
)

class ContentRepository(private val context: Context) {
    private fun readAsset(path: String): String =
        context.assets.open(path).bufferedReader(Charsets.UTF_8).use { it.readText() }

    private fun jsonArrayToStrings(obj: JSONObject, key: String): List<String> {
        val arr = obj.optJSONArray(key) ?: return emptyList()
        return buildList {
            for (i in 0 until arr.length()) add(arr.optString(i))
        }
    }

    private fun parseVocabularyCards(learning: JSONObject): List<VocabularyCard> {
        val arr = learning.optJSONArray("vocabularyCards") ?: return emptyList()
        return buildList {
            for (i in 0 until arr.length()) {
                val item = arr.getJSONObject(i)
                add(
                    VocabularyCard(
                        id = item.getString("id"),
                        zh = item.getString("zh"),
                        pinyin = item.getString("pinyin"),
                        tr = item.getString("tr"),
                        exampleZh = item.optString("exampleZh", ""),
                        examplePinyin = item.optString("examplePinyin", ""),
                        exampleTr = item.optString("exampleTr", ""),
                        kind = item.optString("kind", "active")
                    )
                )
            }
        }
    }

    private fun parseSentenceExercises(learning: JSONObject): List<SentenceExercise> {
        val arr = learning.optJSONArray("sentenceExercises") ?: return emptyList()
        return buildList {
            for (i in 0 until arr.length()) {
                val item = arr.getJSONObject(i)
                add(
                    SentenceExercise(
                        id = item.getString("id"),
                        type = item.getString("type"),
                        promptTr = item.optString("promptTr", ""),
                        tokens = jsonArrayToStrings(item, "tokens"),
                        answerTokens = jsonArrayToStrings(item, "answerTokens"),
                        blankSentenceZh = item.optString("blankSentenceZh", ""),
                        options = jsonArrayToStrings(item, "options"),
                        answer = item.optString("answer", "")
                    )
                )
            }
        }
    }

    private fun parseComprehension(learning: JSONObject): List<ComprehensionQuestion> {
        val arr = learning.optJSONArray("comprehensionQuestions") ?: return emptyList()
        return buildList {
            for (i in 0 until arr.length()) {
                val item = arr.getJSONObject(i)
                add(ComprehensionQuestion(
                    id = item.getString("id"),
                    questionTr = item.optString("questionTr", ""),
                    optionsTr = jsonArrayToStrings(item, "optionsTr"),
                    correctIndex = item.optInt("correctIndex", 0)
                ))
            }
        }
    }

    private fun parsePronunciation(learning: JSONObject): List<PronunciationItem> {
        val arr = learning.optJSONArray("pronunciationItems") ?: return emptyList()
        return buildList {
            for (i in 0 until arr.length()) {
                val item = arr.getJSONObject(i)
                add(PronunciationItem(
                    id = item.getString("id"),
                    zh = item.optString("zh", ""),
                    pinyin = item.optString("pinyin", ""),
                    tr = item.optString("tr", "")
                ))
            }
        }
    }

    private fun parseInteractiveDialogue(learning: JSONObject): List<InteractiveDialogueItem> {
        val arr = learning.optJSONArray("interactiveDialogue") ?: return emptyList()
        return buildList {
            for (i in 0 until arr.length()) {
                val item = arr.getJSONObject(i)
                val optionsJson = item.optJSONArray("options")
                val options = buildList {
                    if (optionsJson != null) {
                        for (j in 0 until optionsJson.length()) {
                            val option = optionsJson.getJSONObject(j)
                            add(InteractiveOption(
                                zh = option.optString("zh", ""),
                                tr = option.optString("tr", ""),
                                correct = option.optBoolean("correct", false)
                            ))
                        }
                    }
                }
                add(InteractiveDialogueItem(
                    id = item.getString("id"),
                    promptZh = item.optString("promptZh", ""),
                    promptPinyin = item.optString("promptPinyin", ""),
                    promptTr = item.optString("promptTr", ""),
                    options = options
                ))
            }
        }
    }

    private fun parseLearning(learningJson: JSONObject): LearningInfo {
        val examJson = learningJson.optJSONObject("examRules") ?: JSONObject()
        return LearningInfo(
            communicationGoals = jsonArrayToStrings(learningJson, "communicationGoals"),
            vocabularyTheme = learningJson.optString("vocabularyTheme", ""),
            grammarTheme = learningJson.optString("grammarTheme", ""),
            pronunciationTheme = learningJson.optString("pronunciationTheme", ""),
            defaultSpeechSpeed = learningJson.optDouble("defaultSpeechSpeed", 1.0).toFloat(),
            defaultSubtitleMode = learningJson.optString("defaultSubtitleMode", "ZH_PINYIN_TR"),
            vocabularyCards = parseVocabularyCards(learningJson),
            sentenceExercises = parseSentenceExercises(learningJson),
            comprehensionQuestions = parseComprehension(learningJson),
            pronunciationItems = parsePronunciation(learningJson),
            interactiveDialogue = parseInteractiveDialogue(learningJson),
            examRules = ExamRules(
                vocabularyPassPercent = examJson.optInt("vocabularyPassPercent", 90),
                sentencePassPercent = examJson.optInt("sentencePassPercent", 85),
                lockNextSceneUntilPassed = examJson.optBoolean("lockNextSceneUntilPassed", true)
            )
        )
    }


    private fun parseProduction(sceneJson: JSONObject): ProductionInfo {
        val production = sceneJson.optJSONObject("production") ?: JSONObject()
        val visual = production.optJSONObject("visual") ?: JSONObject()
        val animation = production.optJSONObject("animation") ?: JSONObject()
        val audio = production.optJSONObject("audio") ?: JSONObject()
        val characters = jsonArrayToStrings(production, "characters")
        val narratorJson = sceneJson.optJSONObject("narrator") ?: JSONObject()
        val titleZh = sceneJson.optString("titleZh", "")
        val titleTr = sceneJson.optString("titleTr", "")
        val miniAdventureTr = sceneJson.optString("miniAdventureTr", "")
        val narrator = NarratorInfo(
            profileId = narratorJson.optString("profileId", audio.optString("narratorProfile", "NARRATOR_ZH_001")),
            zh = narratorJson.optString("zh", if (titleZh.isBlank()) "" else "这一场是《${titleZh}》。让我们继续看看这一家人的故事。"),
            pinyin = narratorJson.optString("pinyin", ""),
            tr = narratorJson.optString("tr", listOf("Bu sahne: $titleTr.", miniAdventureTr).filter { it.isNotBlank() }.joinToString(" ")),
            audioAsset = narratorJson.optString("audioAsset", "")
        )
        return ProductionInfo(
            locationId = sceneJson.optString("locationId", production.optString("locationId", "")),
            timeOfDay = production.optString("timeOfDay", "day"),
            atmosphere = production.optString("atmosphere", ""),
            characters = characters,
            visualStyle = visual.optString("style", "visual_novel_theatre"),
            animationLevel = animation.optString("level", "minimal"),
            speakerFocus = animation.optBoolean("speakerFocus", true),
            narrator = narrator,
            ambienceAsset = audio.optString("ambienceAsset", ""),
            musicAsset = audio.optString("musicAsset", "")
        )
    }

    fun loadCharacters(): List<CharacterProfile> {
        val root = JSONObject(readAsset("chinese_course/characters.json"))
        val items = root.optJSONArray("characters") ?: return emptyList()
        return buildList {
            for (i in 0 until items.length()) {
                val item = items.getJSONObject(i)
                val variantJson = item.optJSONObject("portraitVariants")
                val variants = mutableMapOf<String, String>()
                if (variantJson != null) {
                    val keys = variantJson.keys()
                    while (keys.hasNext()) {
                        val key = keys.next()
                        variants[key] = variantJson.optString(key, "")
                    }
                }
                val byLevelJson = item.optJSONObject("portraitByLevel")
                val byLevel = mutableMapOf<String, String>()
                if (byLevelJson != null) {
                    val keys = byLevelJson.keys()
                    while (keys.hasNext()) {
                        val key = keys.next()
                        byLevel[key] = byLevelJson.optString(key, "")
                    }
                }
                add(CharacterProfile(
                    id = item.getString("id"),
                    nameZh = item.getString("nameZh"),
                    pinyin = item.optString("pinyin", ""),
                    role = item.optString("role", "supporting"),
                    portraitAsset = item.optString("portraitAsset", ""),
                    portraitVariants = variants,
                    portraitByLevel = byLevel,
                    voiceProfileId = item.optString("voiceProfileId", "")
                ))
            }
        }
    }

    fun loadLocations(): List<LocationProfile> {
        val root = JSONObject(readAsset("chinese_course/locations.json"))
        val items = root.optJSONArray("locations") ?: return emptyList()
        return buildList {
            for (i in 0 until items.length()) {
                val item = items.getJSONObject(i)
                add(LocationProfile(
                    id = item.getString("id"),
                    nameZh = item.optString("nameZh", item.getString("id")),
                    nameTr = item.optString("nameTr", item.getString("id")),
                    theme = item.optString("theme", "generic"),
                    icon = item.optString("icon", "场"),
                    backgroundAsset = item.optString("backgroundAsset", "")
                ))
            }
        }
    }

    fun loadVoiceProfiles(): List<VoiceProfile> {
        return try {
            val root = JSONObject(readAsset("chinese_course/voices.json"))
            val items = root.optJSONArray("voices") ?: return emptyList()
            buildList {
                for (i in 0 until items.length()) {
                    val item = items.getJSONObject(i)
                    add(VoiceProfile(
                        id = item.getString("id"),
                        characterId = item.optString("characterId", ""),
                        language = item.optString("language", "zh-CN"),
                        style = item.optString("style", "natural"),
                        authoredAudioPreferred = item.optBoolean("authoredAudioPreferred", true)
                    ))
                }
            }
        } catch (_: Exception) { emptyList() }
    }

    fun loadLevels(): List<LevelInfo> {
        val root = JSONObject(readAsset("chinese_course/manifest.json"))
        val levels = root.getJSONArray("levels")
        return buildList {
            for (i in 0 until levels.length()) {
                val item = levels.getJSONObject(i)
                add(
                    LevelInfo(
                        id = item.getString("id"),
                        title = item.getString("title"),
                        sceneCount = item.getInt("sceneCount"),
                        completeScenes = item.optInt("completeScenes", 0),
                        blueprintReadyScenes = item.optInt("blueprintReadyScenes", 0),
                        storyArc = item.getString("storyArc")
                    )
                )
            }
        }
    }

    fun loadSceneIndex(levelId: String): List<SceneInfo> {
        val root = JSONObject(readAsset("chinese_course/levels/$levelId/index.json"))
        val scenes = root.getJSONArray("scenes")
        return buildList {
            for (i in 0 until scenes.length()) {
                val item = scenes.getJSONObject(i)
                add(
                    SceneInfo(
                        id = item.getString("id"),
                        level = levelId,
                        number = item.getInt("number"),
                        titleZh = item.optString("titleZh", "第${i + 1}场"),
                        titleTr = item.optString("titleTr", "Sahne ${i + 1}"),
                        complete = item.optBoolean("complete", false),
                        productionStatus = item.optString("productionStatus", "planned"),
                        dialogues = emptyList()
                    )
                )
            }
        }
    }

    fun loadScene(levelId: String, sceneId: String): SceneInfo {
        val json = JSONObject(readAsset("chinese_course/levels/$levelId/scenes/$sceneId.json"))
        val dialoguesJson = json.optJSONArray("dialogues")
        val dialogues = buildList {
            if (dialoguesJson != null) {
                for (i in 0 until dialoguesJson.length()) {
                    val d = dialoguesJson.getJSONObject(i)
                    add(
                        DialogueLine(
                            id = d.getString("id"),
                            speaker = d.getString("speaker"),
                            zh = d.getString("zh"),
                            pinyin = d.getString("pinyin"),
                            tr = d.getString("tr"),
                            emotion = d.optString("emotion", "neutral"),
                            actionTr = d.optString("actionTr", ""),
                            audioAsset = d.optString("audioAsset", ""),
                            sfxAsset = d.optString("sfxAsset", "")
                        )
                    )
                }
            }
        }
        val learningJson = json.optJSONObject("learning") ?: JSONObject()
        return SceneInfo(
            id = json.getString("id"),
            level = json.getString("level"),
            number = json.getInt("number"),
            titleZh = json.getString("titleZh"),
            titleTr = json.getString("titleTr"),
            complete = json.optBoolean("complete", false),
            productionStatus = json.optString("productionStatus", "planned"),
            miniAdventureTr = json.optString("miniAdventureTr", ""),
            learning = parseLearning(learningJson),
            production = parseProduction(json),
            dialogues = dialogues
        )
    }

    fun loadAllVocabularyCards(): List<VocabularyStudyItem> {
        val result = mutableListOf<VocabularyStudyItem>()
        for (level in loadLevels()) {
            for (sceneMeta in loadSceneIndex(level.id)) {
                val scene = loadScene(level.id, sceneMeta.id)
                scene.learning.vocabularyCards.forEach { card ->
                    result += VocabularyStudyItem(level.id, scene.id, scene.titleTr, card)
                }
            }
        }
        return result
    }
}
