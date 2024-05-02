from django.urls import path

from . import views
app_name = 'kelola_playlist'


urlpatterns = [
    path('playlist/', views.playlist),
    # path('create_podcast/', views.create_podcast),
]