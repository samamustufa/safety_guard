from django.urls import path
from .views import upload_video, test


urlpatterns = [
    path("uploadvideo/",upload_video),
    path("testvideo/",test),

    ]