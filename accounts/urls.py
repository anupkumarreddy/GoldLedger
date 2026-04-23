from django.urls import path

from .views import HomeRedirectView

app_name = "accounts"

urlpatterns = [
    path("", HomeRedirectView.as_view(), name="home"),
]
