from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('record/', views.record, name='record'), 
    path('script-builder/', views.script_builder, name='script_builder'),
    path('write-script/', views.write_script, name='write_script'),
    path('use-template/', views.use_template, name='use_template'),
    path('video-step/', views.video_step, name='video_step'),

    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'), 
    path("logout/", views.logout, name='logout'),

    path('generate_response/', views.generate_response, name='generate_response'),
]
