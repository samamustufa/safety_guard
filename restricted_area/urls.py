from django.urls import path
from . import views

urlpatterns = [
    path("restricted-area/",views.restrictArea, name= 'restricted_area'),
    path('restricted_area_detection/', views.restricted_area_detection, name='restricted_area_detection'),
    path('define_area/<str:video_path>/<str:first_frame_path>/', views.define_area, name='define_area'),
    path('process_restricted_area/', views.process_restricted_area, name='process_restricted_area'),
    path('restricted_area_result/', views.restricted_area_result, name='restricted_area_result'),
    ]