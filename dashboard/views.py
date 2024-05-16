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
    keyword = request.GET.get('q', None)
    connection, cursor = get_database_cursor()
    if keyword:
        query = f"""
            SELECT 'Podcast' AS Tipe, k.judul AS Judul, a.nama AS Oleh, k.id as ID
            FROM podcast p
            JOIN konten k ON p.id_konten = k.id
            JOIN akun a ON p.email_podcaster = a.email
            WHERE LOWER(k.judul) LIKE LOWER('%{keyword}%')

            UNION

            SELECT 'Song' AS Tipe, k.judul AS Judul, a.nama AS Oleh, k.id as ID
            FROM song s
            JOIN konten k ON s.id_konten = k.id
            JOIN artist art ON s.id_artist = art.id
            JOIN akun a ON art.email_akun = a.email
            WHERE LOWER(k.judul) LIKE LOWER('%{keyword}%')

            UNION

            SELECT 'User Playlist' AS Tipe, up.judul AS Judul, a.nama AS Oleh, up.id_user_playlist as ID
            FROM user_playlist up
            JOIN akun a ON up.email_pembuat = a.email
            WHERE LOWER(up.judul) LIKE LOWER('%{keyword}%')
            """
        cursor.execute(query)
        contents = cursor.fetchall()
        print(contents)

        context = {
            "contents": contents,
            "keyword" : keyword
        }
        # print(paket)
        return render(request, "search.html", context)
    return render(request, "search.html")

def downloaded_songs(request):
    return render(request, "downloaded_songs.html")
