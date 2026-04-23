from django.db import models
import django.conf
from apps.news.models import News


class Comment(models.Model):
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username} → {self.news.title[:40]}"
