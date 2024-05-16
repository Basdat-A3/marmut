from django.urls import path
from dashboard.views import dashboard, \
    dashboard_label, dashboard_artist,\
        dashboard_podcaster, \
        search, downloaded_songs

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('label/', dashboard_label, name='dashboard_label'),
    path('artist/', dashboard_artist, name='dashboard_artist'),
    path('podcaster/', dashboard_podcaster, name='dashboard_podcaster'),
    path('songs/', downloaded_songs, name='downloaded_songs'),
    path('search/', search, name='search'),
]