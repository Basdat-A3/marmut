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
    playlists = query_result(f"""
    SELECT * FROM marmut.user_playlist;
    """)
    context = {'playlists':playlists}
    return render(request, 'playlist.html', context)

def playlist_detail(request, idPlaylist):
    playlist = query_result(f"""
    SELECT UP.*, A.nama AS pembuat_playlist
    FROM marmut.user_playlist AS UP, marmut.akun AS A
    WHERE UP.email_pembuat = A.email
    AND UP.id_playlist = '{idPlaylist}';
    """)

    songs = query_result(f"""
    SELECT K.judul, K.durasi, K.tanggal_rilis, A.nama AS oleh
    FROM marmut.playlist_song AS PS, marmut.konten AS K, marmut.song AS S, marmut.artist AS AT, marmut.akun AS A
    WHERE K.id = PS.id_song
    AND S.id_konten = K.id
    AND AT.id = S.id_artist
    AND A.email = AT.email_akun
    AND PS.id_playlist = '{idPlaylist}';
    """)

    if not playlist:
        return HTTPResponse("Playlist not found", status=404)

    context = {
        'playlist': playlist[0],
        'songs': songs,
    }
    
    return render(request, 'playlist_detail.html', context)

def delete_playlist(request, idPlaylist):
    # # Hapus user playlist berdasarkan id_playlist
    # with connection.cursor() as cursor:
    #     cursor.execute("DELETE FROM marmut.user_playlist WHERE id_playlist = %s;", [idPlaylist])
    
    # # Hapus playlist berdasarkan id_playlist
    # with connection.cursor() as cursor:
    #     cursor.execute("DELETE FROM marmut.playlist WHERE id = %s;", [idPlaylist])
    
    # # Redirect ke halaman show_user_playlist setelah berhasil menghapus
    # return redirect('kelola_playlist:playlist')
    # connection, cursor = get_database_cursor()

    # # Delete records from referencing table (akun_play_user_playlist)
    # cursor.execute("DELETE FROM akun_play_user_playlist WHERE id_user_playlist = %s;", [idPlaylist])
        
    # # Delete user playlist based on id_playlist
    # cursor.execute("DELETE FROM user_playlist WHERE id_playlist = %s;", [idPlaylist])
        
    # # Delete playlist based on id_playlist
    # cursor.execute("DELETE FROM playlist WHERE id = %s;", [idPlaylist])
    # #playlist = cursor.fetchone()

    # cursor.close()
    # connection.close()
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

def tambah_lagu(request):
    connection, cursor = get_database_cursor()


    # close connection
    cursor.close()
    connection.close()


    return render(request, 'tambah_lagu.html')

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
        email_pembuat = "john.doe@example.com"  
        jumlah_lagu = 0
        tanggal_dibuat = datetime.date.today()  
        id_user_playlist = str(uuid.uuid4())  
        total_durasi = 0

        cursor.execute("""
            INSERT INTO user_playlist 
            (email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_user_playlist, id_playlist, total_durasi) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            [email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_user_playlist, id_playlist, total_durasi])
        
        cursor.close()
        connection.close()

        # sukses
        return redirect('kelola_playlist:playlist')
    else:
        return render(request, 'tambah_playlist.html')
