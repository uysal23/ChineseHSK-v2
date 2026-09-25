Media bundle contract (v1.2.0)

The application is fully usable without binary media because Compose visuals and offline Mandarin TTS are fallbacks.
When authored files are added, no scene-code changes are needed.

Background: chinese_course/media/backgrounds/<LOCATION_ID>_DAY.webp
Character:  chinese_course/media/characters/<CHARACTER_ID>/base.webp
Dialogue:   chinese_course/media/audio/dialogues/<DIALOGUE_ID>.opus
Narrator:   chinese_course/media/audio/narrator/<SCENE_ID>.opus
Ambience:   chinese_course/media/ambience/<LOCATION_ID>.opus
Music:      chinese_course/media/music/<SCENE_ID>.opus

All identifiers are declared in characters.json, locations.json, voices.json and media manifests.
