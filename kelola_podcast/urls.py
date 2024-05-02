from django.urls import path
from . import views

app_name = 'kelola_podcast'

urlpatterns = [
    path('create_podcast/', views.create_podcast),
    path('list_podcast/', views.list_podcast),
    path('create_episode/', views.create_episode),
    path('daftar_episode/', views.daftar_episode),
    path('daftar_episode_sebuah_podcast/', views.daftar_episode_sebuah_podcast),
]
