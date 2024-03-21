from django.urls import path
from .views import loginaction,loginPage,Welcomepage

urlpatterns = [
    path("",loginPage,name="loginPage"),
    path("welcome-page/",loginaction,name='welcome-page'),
    path("welcome/",Welcomepage,name='welcome'),
    ]