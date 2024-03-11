from django.urls import path
from .views import restrictArea

urlpatterns = [
    path("restricted-area/",restrictArea),
    ]