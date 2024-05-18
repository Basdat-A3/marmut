from http.client import HTTPResponse
from pyexpat.errors import messages
from utils.query import *
from django.db import connection
from function.general import query_result
from django.http import HttpResponseRedirect
from django.core import serializers
from kelola_playlist.forms import AddUserPlaylistForm, EditUserPlaylistForm
from django.urls import reverse
from django.db import connection
import datetime
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_protect


def playlist(request):
    connection, cursor = get_database_cursor()
    email = request.COOKIES.get('email')
    cursor.execute(f"""
            SELECT * FROM user_playlist where email_pembuat = '{email}';
        """)
    playlists = cursor.fetchall()

    context = {'playlists': playlists}
    cursor.close()
    connection.close()
    return render(request, 'playlist.html', context)

def convert_to_hours_minutes(total_minutes):
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return hours, minutes

def playlist_detail(request, idPlaylist):
    connection, cursor = get_database_cursor()
    cursor.execute("""
            SELECT UP.judul, UP.deskripsi, UP.tanggal_dibuat, A.nama AS pembuat_playlist, 
                   COUNT(PS.id_song) AS jumlah_lagu, COALESCE(SUM(K.durasi), 0) AS total_durasi
            FROM marmut.user_playlist AS UP
            JOIN marmut.akun AS A ON UP.email_pembuat = A.email
            LEFT JOIN marmut.playlist_song AS PS ON UP.id_playlist = PS.id_playlist
            LEFT JOIN marmut.konten AS K ON PS.id_song = K.id
            WHERE UP.id_playlist = %s
            GROUP BY UP.judul, UP.deskripsi, UP.tanggal_dibuat, A.nama, UP.total_durasi;
        """, [idPlaylist])
    playlist = cursor.fetchone()

    cursor.execute("""
            SELECT K.judul, K.durasi, K.tanggal_rilis, A.nama AS oleh, K.id
            FROM marmut.playlist_song AS PS
            JOIN marmut.konten AS K ON K.id = PS.id_song
            JOIN marmut.song AS S ON S.id_konten = K.id
            JOIN marmut.artist AS AT ON AT.id = S.id_artist
            JOIN marmut.akun AS A ON A.email = AT.email_akun
            WHERE PS.id_playlist = %s;
        """, [idPlaylist])
    songs = cursor.fetchall()

    if not playlist:
        return HTTPResponse("Playlist not found", status=404)

    total_minutes = playlist[5]
    hours, minutes = convert_to_hours_minutes(total_minutes)

    context = {
        'playlist': {
            'judul': playlist[0],
            'deskripsi': playlist[1],
            'tanggal_dibuat': playlist[2],
            'pembuat_playlist': playlist[3],
            'jumlah_lagu': playlist[4],
            'total_durasi_hours': hours,
            'total_durasi_minutes': minutes,
            'idPlaylist' : idPlaylist,

        },
        'songs': [
            {
                'judul': song[0],
                'oleh': song[3],
                'durasi': song[1],
                'id' : song[4]
            }
            for song in songs
        ],
    }

    cursor.close()
    connection.close()
    
    return render(request, 'playlist_detail.html', context)

def delete_playlist(request, idPlaylist):
    connection, cursor = get_database_cursor()

    try:
        # Check if the playlist exists
        cursor.execute("""
            SELECT id_playlist 
            FROM user_playlist 
            WHERE id_playlist = %s;
        """, [idPlaylist])

        playlist = cursor.fetchone()

        if playlist:
            # Fetch songs associated with the playlist
            cursor.execute("""
                SELECT id_song 
                FROM playlist_song 
                WHERE id_playlist = %s;
            """, [idPlaylist])

            songs = cursor.fetchall()

            # Delete each song associated with the playlist
            for song in songs:
                song_id = song[0]
                cursor.execute("""
                    DELETE FROM playlist_song 
                    WHERE id_playlist = %s AND id_song = %s;
                """, [idPlaylist, song_id])

            # Now delete the playlist
            cursor.execute("""
                DELETE FROM user_playlist 
                WHERE id_playlist = %s;
            """, [idPlaylist])

            connection.commit()
        else:
            return HttpResponseForbidden("The playlist does not exist.")
    finally:
        cursor.close()
        connection.close()

    # Redirect to the list_playlist page after successful deletion
    return redirect('kelola_playlist:playlist')

def edit_playlist(request, idPlaylist):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM marmut.user_playlist WHERE id_playlist = '{idPlaylist}';")
        playlist = cursor.fetchone()
        
        if not playlist:
            return HTTPResponse("Playlist not found", status=404)

        if request.method == 'POST':
            form = EditUserPlaylistForm(request.POST)
            if form.is_valid():
                judul = form.cleaned_data['judul']
                deskripsi = form.cleaned_data['deskripsi']
                
                cursor.execute("""
                UPDATE marmut.user_playlist
                SET judul = %s, deskripsi = %s
                WHERE id_playlist = %s;
                """, [judul, deskripsi, idPlaylist])
                
                return redirect('kelola_playlist:playlist')
        else:
            form = EditUserPlaylistForm(initial={'judul': playlist[2], 'deskripsi': playlist[3]})
    
    context = {'form': form, 'playlist_id': idPlaylist}
    return render(request, 'edit_playlist.html', context)

def tambah_playlist(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')

        # Generate UUID baru
        id_playlist = str(uuid.uuid4())
        connection, cursor = get_database_cursor()

        # Insert playlist baru
        cursor.execute("INSERT INTO playlist (id) VALUES (%s);", [id_playlist])

        # Insert data ke "user_playlist" 
        email_pembuat = request.COOKIES.get('email')  
        jumlah_lagu = 0
        tanggal_dibuat = datetime.date.today()  
        id_user_playlist = str(uuid.uuid4())  
        total_durasi = 0

        cursor.execute("""
            INSERT INTO user_playlist 
            (email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_user_playlist, id_playlist, total_durasi) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            [email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_user_playlist, id_playlist, total_durasi])
        
        context = {
            'email_pembuat' : email_pembuat
        }
        
        connection.commit()
        cursor.close()
        connection.close()

        # sukses
        return redirect('kelola_playlist:playlist')
    else:
        email_pembuat = request.COOKIES.get('email') 
        context = {
            'email_pembuat' : email_pembuat
        }
        return render(request, 'tambah_playlist.html', context)
    
def tambah_lagu(request, idPlaylist):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')

        # Pastikan song_id tidak kosong atau None
        if song_id:
            # Dapatkan koneksi dan kursor sebelum melakukan operasi database
            connection, cursor = get_database_cursor()
            cursor.execute("INSERT INTO playlist_song (id_playlist, id_song) VALUES (%s, %s);", [idPlaylist, song_id])
            connection.commit()
            cursor.close()
            connection.close()

            return redirect(reverse('kelola_playlist:playlist_detail', args=[idPlaylist]))
        else:
            # Berikan pesan kesalahan jika song_id kosong
            error_message = "Silakan pilih lagu sebelum menambahkan."

    else:
        error_message = None

    # Dapatkan koneksi dan kursor sebelum melakukan operasi database
    connection, cursor = get_database_cursor()
    cursor.execute("""
        SELECT s.id_konten, k.judul, a.nama as artist
        FROM song s
        JOIN konten k ON s.id_konten = k.id 
        JOIN artist ar ON s.id_artist = ar.id
        JOIN akun a ON ar.email_akun = a.email;
    """)
    songs = cursor.fetchall()
    cursor.close()
    connection.close()

    return render(request, 'tambah_lagu.html', {'songs': songs, 'playlist_id': idPlaylist, 'error_message': error_message})

def delete_song(request, playlist_id, song_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM marmut.playlist_song WHERE id_playlist = %s AND id_song = %s;", 
                        [playlist_id, song_id])

    return redirect(reverse('kelola_playlist:playlist_detail', args=[playlist_id]))

