from django.urls import path
from paket.views import paket, paket_payment, riwayat

app_name = 'paket'

urlpatterns = [
    path('', paket, name='paket'),
    path('riwayat/', riwayat, name='riwayat'),
    path('<str:nama_paket>/', paket_payment, name='paket_payment'),
]