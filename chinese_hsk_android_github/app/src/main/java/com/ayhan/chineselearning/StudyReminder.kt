package com.ayhan.chineselearning

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.Worker
import androidx.work.WorkerParameters
import java.time.Duration
import java.time.ZonedDateTime
import java.util.concurrent.TimeUnit

object StudyReminderScheduler {
    private const val UNIQUE_WORK = "daily_chinese_study_reminder"

    fun schedule(context: Context, hour: Int, minute: Int) {
        val now = ZonedDateTime.now()
        var next = now.withHour(hour.coerceIn(0, 23)).withMinute(minute.coerceIn(0, 59)).withSecond(0).withNano(0)
        if (!next.isAfter(now)) next = next.plusDays(1)
        val delayMs = Duration.between(now, next).toMillis().coerceAtLeast(1_000L)
        val request = OneTimeWorkRequestBuilder<StudyReminderWorker>()
            .setInitialDelay(delayMs, TimeUnit.MILLISECONDS)
            .build()
        WorkManager.getInstance(context).enqueueUniqueWork(UNIQUE_WORK, ExistingWorkPolicy.REPLACE, request)
    }

    fun cancel(context: Context) {
        WorkManager.getInstance(context).cancelUniqueWork(UNIQUE_WORK)
    }
}

class StudyReminderWorker(appContext: Context, params: WorkerParameters) : Worker(appContext, params) {
    override fun doWork(): Result {
        val progress = ProgressStore(applicationContext)
        if (!progress.studyReminderEnabled()) return Result.success()

        val channelId = "study_reminder"
        val manager = applicationContext.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            manager.createNotificationChannel(
                NotificationChannel(channelId, "Çince çalışma hatırlatıcısı", NotificationManager.IMPORTANCE_DEFAULT).apply {
                    description = "Günlük Çince çalışma ve tekrar hatırlatmaları"
                }
            )
        }

        val allowed = Build.VERSION.SDK_INT < 33 ||
            ContextCompat.checkSelfPermission(applicationContext, Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED
        if (allowed) {
            val intent = Intent(applicationContext, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
            }
            val pending = PendingIntent.getActivity(
                applicationContext, 41, intent,
                PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
            )
            val mastered = progress.masteredCount()
            val weakCount = progress.weakWordIds().size
            val body = if (weakCount > 0) {
                "Bugünkü tekrarını yap: $weakCount zayıf kelime seni bekliyor."
            } else {
                "Bugünkü Çince sahnen ve kelime tekrarların hazır."
            }
            val notification = NotificationCompat.Builder(applicationContext, channelId)
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentTitle("中文生活 · Çalışma zamanı")
                .setContentText(body)
                .setStyle(NotificationCompat.BigTextStyle().bigText("$body Kurs ilerlemen: $mastered / 300 sahne."))
                .setContentIntent(pending)
                .setAutoCancel(true)
                .build()
            manager.notify(4101, notification)
        }

        StudyReminderScheduler.schedule(applicationContext, progress.studyReminderHour(), progress.studyReminderMinute())
        return Result.success()
    }
}
