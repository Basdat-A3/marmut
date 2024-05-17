from http.client import HTTPResponse
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


def playlist(request):
    connection, cursor = get_database_cursor()
    cursor.execute("""
            SELECT * FROM user_playlist;
        """)
    playlists = cursor.fetchall()

    column_names = [col[0] for col in cursor.description]
    playlists = [
        dict(zip(column_names, row))
        for row in playlists
    ]

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
                   COUNT(PS.id_song) AS jumlah_lagu, UP.total_durasi
            FROM marmut.user_playlist AS UP
            JOIN marmut.akun AS A ON UP.email_pembuat = A.email
            LEFT JOIN marmut.playlist_song AS PS ON UP.id_playlist = PS.id_playlist
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

    # Delete records from referencing table (akun_play_user_playlist)
    cursor.execute("DELETE FROM akun_play_user_playlist WHERE id_user_playlist = %s;", [idPlaylist])
        
    # Delete user playlist based on id_playlist
    cursor.execute("DELETE FROM user_playlist WHERE id_playlist = %s;", [idPlaylist])
        
    # Delete playlist based on id_playlist
    cursor.execute("DELETE FROM playlist WHERE id = %s;", [idPlaylist])
    #playlist = cursor.fetchone()

    cursor.close()
    connection.close()
    # # Redirect to the show_user_playlist page after successful deletion
    return redirect('kelola_playlist:playlist')

def edit_playlist(request, idPlaylist):
    connection, cursor = get_database_cursor()
    cursor.execute("SELECT * FROM user_playlist WHERE id_playlist = %s;", [idPlaylist])
    playlist = cursor.fetchone()

    if not playlist:
            return HTTPResponse("Playlist not found", status=404)

    if request.method == 'POST':
            form = EditUserPlaylistForm(request.POST)
            if form.is_valid():
                judul = form.cleaned_data['judul']
                deskripsi = form.cleaned_data['deskripsi']
                
                cursor.execute("""
                UPDATE user_playlist
                SET judul = %s, deskripsi = %s
                WHERE id_playlist = %s;
                """, [judul, deskripsi, idPlaylist])
                
                return redirect('kelola_playlist:playlist')
    else:
            form = EditUserPlaylistForm(initial={'judul': playlist[2], 'deskripsi': playlist[3]})
        
    context = {'form': form, 'playlist_id': idPlaylist}
    
    cursor.close()
    connection.close()
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

        # Check if the song is already in the playlist
        # existing_song = query_result(f"""
        #     SELECT s.* FROM marmut.user_playlist up
        #     JOIN marmut.playlist_song ps ON ps.id_playlist = up.id_playlist
        #     JOIN marmut.song s ON ps.id_song = s.id_konten
        #     WHERE up.id_playlist = '{playlist_id}' AND s.id_konten = '{song_id}';
        # """)
        # if existing_song:
        #     return HttpResponse("Lagu sudah ada di dalam playlist", status=400)

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO marmut.playlist_song (id_playlist, id_song) VALUES (%s, %s);", 
                           [idPlaylist, song_id])

        return redirect(reverse('kelola_playlist:playlist_detail', args=[idPlaylist]))

    # Get the list of all songs for the dropdown
    songs = query_result(f"""
        SELECT s.id_konten, k.judul, a.nama as artist
        FROM marmut.song s
        JOIN marmut.konten k ON s.id_konten = k.id 
        JOIN marmut.artist ar ON s.id_artist = ar.id
        JOIN marmut.akun a ON ar.email_akun = a.email;
    """)

    return render(request, 'tambah_lagu.html', {'songs': songs, 'playlist_id': idPlaylist})
