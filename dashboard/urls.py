from django.urls import path
from dashboard.views import dashboard, search, downloaded_songs, delete_downloaded_song

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('songs/', downloaded_songs, name='downloaded_songs'),
    path('search/', search, name='search'),
    path('delete-song/', delete_downloaded_song, name='delete'),
]