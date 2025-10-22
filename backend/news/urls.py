from django.urls import path
from .views import HomeNewsView, CategoryNewsView

urlpatterns = [
    path("home/", HomeNewsView.as_view(), name="news-home"),
    path("category/<str:category>/", CategoryNewsView.as_view(), name="news-category"),
]
