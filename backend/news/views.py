from datetime import date
import requests

from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.db.models import DateField, DateTimeField

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import NewsArticle, NewsConfig

# Newsdata: prefer the /news endpoint (stable)
NEWSDATA_URL = "https://newsdata.io/api/1/news"


# ------ Helpers ------

def _normalize_item(item: dict) -> dict:
    """Convert a NewsData.io item into a consistent dict our frontend expects."""
    return {
        "title": item.get("title"),
        "summary": item.get("description") or item.get("content"),
        "url": item.get("link"),
        "image": item.get("image_url"),
        "source": item.get("source_id"),
        "pubDate": item.get("pubDate"),
        "category": item.get("category") or [],
        "country": item.get("country") or [],
    }


def _serialize_article(a: NewsArticle) -> dict:
    """Serialize DB model -> response dict (same shape as _normalize_item)."""
    return {
        "title": a.title,
        "summary": a.summary,
        "url": a.url,
        "image": a.image,
        "source": a.source,
        "pubDate": a.pubDate.isoformat() if a.pubDate else None,
        "category": [a.category] if a.category else [],
        "country": [a.country] if a.country else [],
    }


def fetch_from_newsdata(categories=None, country=None, language="en"):
    """Call the external Newsdata API once and normalize results."""
    api_key = getattr(settings, "NEWSDATA_API_KEY", None)
    if not api_key:
        return []

    params = {"apikey": api_key, "language": language}
    if categories:
        params["category"] = ",".join(categories) if isinstance(categories, (list, tuple)) else str(categories)
    if country:
        params["country"] = ",".join(country) if isinstance(country, (list, tuple)) else str(country)

    try:
        resp = requests.get(NEWSDATA_URL, params=params, timeout=12)
        data = resp.json()
        if not isinstance(data, dict) or data.get("status") != "success":
            return []
        results = data.get("results") or []
        return [_normalize_item(x) for x in results]
    except Exception:
        return []


def store_news_items(bucket: str, items: list, country: str = "", max_save: int = 24) -> None:
    """Save normalized items to DB under a specific 'bucket' (our section)."""
    count = 0
    for it in items:
        if count >= max_save:
            break
        title = (it.get("title") or "").strip()
        url = (it.get("url") or "").strip() or None
        image = (it.get("image") or "").strip() or None
        source = (it.get("source") or "").strip() or None

        pub_dt = None
        raw_pub = it.get("pubDate")
        if raw_pub:
            pub_dt = parse_datetime(raw_pub)

        lookup = {"url": url} if url else {"title": title, "category": bucket}

        NewsArticle.objects.update_or_create(
            **lookup,
            defaults={
                "title": title or "Untitled",
                "summary": it.get("summary") or "",
                "image": image,
                "source": source,
                "pubDate": pub_dt,
                "category": bucket,
                "country": country or "",
            },
        )
        count += 1


def get_db_section(bucket: str, limit: int = 12) -> list:
    """Read latest items for a given bucket from DB."""
    qs = (
        NewsArticle.objects
        .filter(category=bucket)
        .order_by("-pubDate", "-id")[:limit]
    )
    return [_serialize_article(a) for a in qs]


def _fetched_today(bucket: str) -> bool:
    """Check if this bucket was already fetched today, works with both DateField & DateTimeField."""
    field = NewsArticle._meta.get_field("fetched_at")

    if isinstance(field, DateField) and not isinstance(field, DateTimeField):
        # Fetched_at is a pure DateField
        return NewsArticle.objects.filter(category=bucket, fetched_at=date.today()).exists()

    # Otherwise, DateTimeField
    return NewsArticle.objects.filter(category=bucket, fetched_at__date=date.today()).exists()


# ------ Views ------

class HomeNewsView(APIView):
    """GET /api/news/home/?country=in&language=en"""

    permission_classes = [permissions.AllowAny]

    SECTIONS = {
        "technology": ["technology"],
        "politics": ["politics"],
        "education": ["education"],
        "business": ["business"],
        "sports": ["sports"],
        "health": ["health"],
        "entertainment": ["entertainment"],
        "world": ["world"],
    }

    def get(self, request):
        country = request.query_params.get("country", "us")
        language = request.query_params.get("language", "en")

        config, _ = NewsConfig.objects.get_or_create(id=1)
        payload = {}

        for bucket, api_categories in self.SECTIONS.items():
            if config.fetch_enabled and not _fetched_today(bucket):
                items = fetch_from_newsdata(categories=api_categories, country=country, language=language)
                if items:
                    store_news_items(bucket=bucket, items=items, country=country)
                payload[bucket] = get_db_section(bucket)
            else:
                payload[bucket] = get_db_section(bucket)

        return Response(payload)


class CategoryNewsView(APIView):
    """GET /api/news/category/<category>/?country=in&language=en"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, category: str):
        bucket = category.lower().strip()
        country = request.query_params.get("country", "us")
        language = request.query_params.get("language", "en")

        config, _ = NewsConfig.objects.get_or_create(id=1)

        if config.fetch_enabled and not _fetched_today(bucket):
            items = fetch_from_newsdata(categories=[bucket], country=country, language=language)
            if items:
                store_news_items(bucket=bucket, items=items, country=country)

        data = get_db_section(bucket, limit=20)
        return Response({"category": bucket, "items": data})

    
    
    
# ------ OLD CODE (for reference) ------

# from django.conf import settings
# from django.core.cache import cache
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions
# import requests

# # Use the /latest endpoint instead of /news to avoid pagination errors
# NEWSDATA_URL = "https://newsdata.io/api/1/latest"

# def _normalize(item):
#     """
#     Convert a NewsData.io item into a clean card dictionary.
#     """
#     return {
#         "title": item.get("title"),
#         "summary": item.get("description") or item.get("content"),
#         "url": item.get("link"),
#         "image": item.get("image_url"),
#         "source": item.get("source_id"),
#         "pubDate": item.get("pubDate"),
#         "category": item.get("category", []),
#         "country": item.get("country", []),
#     }

# def fetch_news(categories=None, country=None, language="en", size=12):
#     api_key = getattr(settings, "NEWSDATA_API_KEY", None)
#     if not api_key:
#         print("⚠️ Missing NEWSDATA_API_KEY in settings")
#         return []

#     params = {"apikey": api_key, "language": language}
#     if categories:
#         params["category"] = ",".join(categories) if isinstance(categories, (list, tuple)) else categories
#     if country:
#         params["country"] = ",".join(country) if isinstance(country, (list, tuple)) else country

#     cache_key = f"news:{categories}:{country}:{language}:{size}"
#     cached = cache.get(cache_key)
#     if cached:
#         return cached

#     try:
#         response = requests.get(NEWSDATA_URL, params=params, timeout=10)
#         data = response.json()

#         print("Fetching:", response.url)
#         print("Raw response:", data)

#         # Ensure proper format
#         if not isinstance(data, dict) or data.get("status") != "success":
#             print("⚠️ API returned error:", data)
#             return []

#         results = data.get("results", []) or []
#         normalized = [_normalize(item) for item in results]
#         cache.set(cache_key, normalized, 60 * 10)  # cache 10 minutes
#         return normalized

#     except Exception as e:
#         print("❌ Error fetching news:", e)
#         return []

# class HomeNewsView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request):
#         country = request.query_params.get("country", "us")
#         language = request.query_params.get("language", "en")

#         sections = {
#             "technology": ["technology"],
#             "politics": ["politics"],
#             "education": ["education"],
#             "business": ["business"],
#             "sports": ["sports"],
#             "health": ["health"],
#             "entertainment": ["entertainment"],
#             "world": ["world"],
#         }

#         payload = {key: fetch_news(categories=cats, country=country, language=language) for key, cats in sections.items()}
#         return Response(payload)

# class CategoryNewsView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request, category):
#         country = request.query_params.get("country", "us")
#         language = request.query_params.get("language", "en")
#         items = fetch_news(categories=[category], country=country, language=language)
#         return Response({"category": category, "items": items})
