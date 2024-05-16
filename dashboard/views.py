import uuid
from django.shortcuts import redirect, render
from utils.query import get_database_cursor
from datetime import datetime, timedelta

# Create your views here.


def dashboard(request):
    # role_verif = request.COOKIES.get('role')
    # email = request.COOKIES.get('email')
    # id_user_artist = request.COOKIES.get('id_user_artist')
    # id_user_songwriter = request.COOKIES.get('id_user_songwriter')
    # id_pemilik_hak_cipta_artist = request.COOKIES.get('idPemilikCiptaArtist')
    # id_pemilik_hak_cipta_songwriter = request.COOKIES.get('idPemilikCiptaSongwriter')
    # status_langganan = request.COOKIES.get('status_langganan')
    # isArtist = request.COOKIES.get('isArtist')
    # isSongwriter = request.COOKIES.get('isSongwriter')
    # isPodcaster = request.COOKIES.get('isPodcaster')

    # context = {
    #     'role': role_verif,
    #     'status_langganan': status_langganan,
    #     'isArtist': isArtist,
    #     'isSongwriter': isSongwriter,
    #     'isPodcaster': isPodcaster,
    #     'email': email,
    # }

    return render(request, "dashboard.html")


def dashboard_label(request):
    return render(request, "dashboard_label.html")


def dashboard_artist(request):
    return render(request, "dashboard_artist.html")


def dashboard_podcaster(request):
    return render(request, "dashboard_podcaster.html")

def search(request):
    return render(request, "search.html")


def downloaded_songs(request):
    return render(request, "downloaded_songs.html")
