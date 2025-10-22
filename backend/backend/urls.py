from django.urls import path, include


from django.contrib import admin
from django.urls import path
from .views import GoogleLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),

    path("api/users/google/", GoogleLoginView.as_view(), name="google_login"),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),  # for normal login/logout
    path("api/news/", include("news.urls")),   
]