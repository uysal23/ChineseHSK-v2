from pathlib import Path

main = Path('app/src/main/java/com/ayhan/chineselearning/MainActivity.kt').read_text(encoding='utf-8')
flow = Path('app/src/main/java/com/ayhan/chineselearning/AppFlowScreens.kt').read_text(encoding='utf-8')
progress = Path('app/src/main/java/com/ayhan/chineselearning/ProgressStore.kt').read_text(encoding='utf-8')
settings = Path('app/src/main/java/com/ayhan/chineselearning/SettingsAndProgressScreens.kt').read_text(encoding='utf-8')
habit = Path('app/src/main/java/com/ayhan/chineselearning/HabitScreens.kt').read_text(encoding='utf-8')
reminder = Path('app/src/main/java/com/ayhan/chineselearning/StudyReminder.kt').read_text(encoding='utf-8')
system_check = Path('app/src/main/java/com/ayhan/chineselearning/SystemCheckScreen.kt').read_text(encoding='utf-8')
required = {
    'welcome screen': 'WelcomeScreen',
    'placement test': 'PlacementTestScreen',
    'dashboard': 'DashboardScreen',
    'daily review': 'DailyReviewScreen',
    'progress overview': 'ProgressOverviewScreen',
    'settings': 'SettingsScreen',
    'local backup export': 'exportBackupJson',
    'local backup import': 'importBackupJson',
    'pinyin default setting': 'pinyinDisplayMode',
    'turkish default setting': 'turkishDisplayMode',
    'autoplay default setting': 'autoPlayDefault',
    'daily review target': 'dailyReviewTarget',
    'weak word review': 'WeakWordsScreen',
    'study streak calendar': 'StudyHabitsScreen',
    'study activity tracking': 'recordStudyActivity',
    'weak word scoring': 'weakWordPriority',
    'daily reminder scheduling': 'StudyReminderScheduler',
    'system diagnostics': 'SystemCheckScreen',
    'offline Mandarin voice diagnostics': 'offlineVoiceCount',
    'offline recognition diagnostics': 'recognizer.isAvailable',
    'notification permission': 'POST_NOTIFICATIONS',
    'resume': 'lastSceneId',
    'placement persistence': 'savePlacementResult',
    'vocabulary threshold': 'VOCAB_PASS = 90',
    'sentence threshold': 'SENTENCE_PASS = 85',
}
combined = main + '\n' + flow + '\n' + progress + '\n' + settings + '\n' + habit + '\n' + reminder + '\n' + system_check + '\n' + Path('app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
missing = [name for name, token in required.items() if token not in combined]
if missing:
    raise SystemExit('App-flow validation failed: ' + ', '.join(missing))
print('App-flow validation passed.')
print('Checked:', ', '.join(required))
