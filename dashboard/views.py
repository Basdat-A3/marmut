from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, "dashboard.html")

def dashboard_label(request):
    return render(request, "dashboard_label.html")

def dashboard_artist(request):
    return render(request, "dashboard_artist.html")

def dashboard_podcaster(request):
    return render(request, "dashboard_podcaster.html")

def paket(request):
    return render(request, "paket.html")

def paket_payment(request):
    return render(request, "paket_payment.html")

def riwayat(request):
    return render(request, "riwayat.html")

def search(request):
    return render(request, "search.html")

def downloaded_songs(request):
    return render(request, "downloaded_songs.html")