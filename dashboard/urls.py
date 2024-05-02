from django.urls import path
from dashboard.views import dashboard, \
    dashboard_label, dashboard_artist,\
        dashboard_podcaster, paket, \
        search, paket_payment, riwayat, \
        downloaded_songs

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('label/', dashboard_label, name='dashboard_label'),
    path('artist/', dashboard_artist, name='dashboard_artist'),
    path('podcaster/', dashboard_podcaster, name='dashboard_podcaster'),
    path('paket/', paket, name='paket'),
    path('paket/riwayat/', riwayat, name='riwayat'),
    path('paket/pay/', paket_payment, name='paket_payment'),
    path('songs/', downloaded_songs, name='downloaded_songs'),
    path('search/', search, name='search'),
]