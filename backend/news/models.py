from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    pubDate = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    fetched_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title[:50]


class NewsConfig(models.Model):
    fetch_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"News Config (fetch_enabled={self.fetch_enabled})"

    def save(self, *args, **kwargs):
        # Always force this to be the only row (id=1)
        self.pk = 1
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "News Config"
        verbose_name_plural = "News Config"
