from django.contrib import admin
from .models import NewsConfig, NewsArticle


@admin.register(NewsConfig)
class NewsConfigAdmin(admin.ModelAdmin):
    list_display = ("fetch_enabled",)

    def has_add_permission(self, request):
        # Prevent creating new configs if one already exists
        return not NewsConfig.objects.exists()

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "pubDate", "fetched_at")
    list_filter = ("category", "fetched_at")
    search_fields = ("title", "summary", "url")
