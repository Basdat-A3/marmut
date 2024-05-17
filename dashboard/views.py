import uuid
from django.shortcuts import redirect, render
from utils.query import get_database_cursor
from datetime import datetime, timedelta

# Create your views here.
def get_playlist(email):
    connection, cursor = get_database_cursor()
    query = f"select * from user_playlist where email_pembuat='{email}'"
    cursor.execute(query)
    playlists = cursor.fetchall()
    return playlists

def get_podcast(email):
    connection, cursor = get_database_cursor()
    query = f"""
    select * from podcast p
    join konten k on k.id = p.id_konten
    where email_podcaster='{email}'
    """
    cursor.execute(query)
    podcasts = cursor.fetchall()
    return podcasts

def get_song(id_artist):
    connection, cursor = get_database_cursor()
    query = f"""
    select k.judul, k.id, k.tahun from song s
    join konten k on k.id = s.id_konten
    where id_artist='{id_artist}'
    """
    cursor.execute(query)
    songs = cursor.fetchall()
    return songs

def dashboard(request):
    role = request.COOKIES.get('role')
    email = request.COOKIES.get('email')
    id_user_artist = request.COOKIES.get('id_user_artist')
    id_user_songwriter = request.COOKIES.get('id_user_songwriter')
    id_pemilik_hak_cipta_artist = request.COOKIES.get('idPemilikCiptaArtist')
    id_pemilik_hak_cipta_songwriter = request.COOKIES.get('idPemilikCiptaSongwriter')
    status_langganan = request.COOKIES.get('status_langganan')
    isArtist = request.COOKIES.get('isArtist')=='True'
    isSongwriter = request.COOKIES.get('isSongwriter')=='True'
    isPodcaster = request.COOKIES.get('isPodcaster')=='True'
    
    song, podcast, playlist = [], [], []
    connection, cursor = get_database_cursor()
    
    playlist = get_playlist(email)
    if isArtist or isSongwriter:
        song = get_song(id_user_artist)
    if isPodcaster:
        podcast = get_podcast(email)



    query = f"SELECT * FROM AKUN WHERE EMAIL='{email}'"
    cursor.execute(query)
    user = cursor.fetchone()
    print(song)
    print(podcast)
    print(playlist)

    context = {
        'role': role,
        'status_langganan': status_langganan,
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'isPodcaster': isPodcaster,
        'email': email,
        'user' : user,
        'song' : song,
        'podcast' : podcast,
        'playlist' : playlist,
    }

    return render(request, "dashboard.html", context)


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

            SELECT 'User Playlist' AS Tipe, up.judul AS Judul, a.nama AS Oleh, up.id_playlist as ID
            FROM user_playlist up
            JOIN akun a ON up.email_pembuat = a.email
            WHERE LOWER(up.judul) LIKE LOWER('%{keyword}%')
            """
        cursor.execute(query)
        contents = cursor.fetchall()
        message = f"Hasil pencarian untuk \"{keyword}\""
        print(contents)
        if len(contents) == 0:
            message = f"Maaf, pencarian untuk \"{keyword}\" tidak ditemukan"

        context = {
            "contents": contents,
            "message" : message
        }

        # close connection
        cursor.close()
        connection.close()
        # print(paket)
        return render(request, "search.html", context)
    return render(request, "search.html")

def downloaded_songs(request):
    connection, cursor = get_database_cursor()
    email = request.COOKIES.get('email')

    cursor.execute(f"""
        select k.judul, a.nama from downloaded_song d
        JOIN konten k ON d.id_song = k.id
        JOIN song s ON d.id_song = s.id_konten
        JOIN artist art ON s.id_artist = art.id
        JOIN akun a ON art.email_akun = a.email
        WHERE d.email_downloader = '{email}'
    """
    )
    songs = cursor.fetchall()
    context = {
        "songs": songs
    }
    print(songs)

    # close connection
    cursor.close()
    connection.close()
    return render(request, "downloaded_songs.html", context)
