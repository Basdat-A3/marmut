from django.shortcuts import render
from http.client import HTTPResponse
from utils.query import *
from function.general import query_result
from kelola_playlist.views import playlist_detail


def song_detail(request, playlist_id, song_id):
    connection, cursor = get_database_cursor()

    # Retrieve playlist details
    cursor.execute("""
    SELECT up.*, a.nama as pembuat
    FROM user_playlist up
    JOIN akun a ON up.email_pembuat = a.email
    WHERE up.id_playlist = %s;
    """, (playlist_id,))
    playlist = cursor.fetchall()

    # Check if playlist exists
    if not playlist:
        return HTTPResponse("Playlist not found", status=404)

    # Retrieve song details
    cursor.execute("""
    SELECT k.judul, g.genre, ak_artist.nama as artist, ak_songwriter.nama as songwriter, k.durasi, k.tanggal_rilis, k.tahun, s.total_play, s.total_download, al.judul as album, s.id_konten
    FROM playlist_song ps
    JOIN song s ON ps.id_song = s.id_konten
    JOIN konten k ON s.id_konten = k.id
    JOIN artist ar ON s.id_artist = ar.id
    JOIN akun ak_artist ON ar.email_akun = ak_artist.email
    JOIN album al ON s.id_album = al.id
    JOIN genre g ON s.id_konten = g.id_konten
    JOIN songwriter_write_song sws ON s.id_konten = sws.id_song
    JOIN songwriter sw ON sws.id_songwriter = sw.id
    JOIN akun ak_songwriter ON sw.email_akun = ak_songwriter.email
    WHERE ps.id_playlist = %s AND ps.id_song = %s;
    """, (playlist_id, song_id))
    song_details = cursor.fetchall()

    # Check if song exists
    if not song_details:
        return HTTPResponse("Song not found", status=404)

    # Get the song detail
    song = song_details[0]

    # Format tanggal rilis
    tanggal_rilis = song[5].strftime("%m/%d/%y")

    context = {
        'playlist': playlist[0],
        'playlist_id' : playlist_id,
        'song_id' : song_id,
        'song': {
            'judul': song[0],
            'genre': song[1], 
            'artist': song[2],
            'songwriters': song[3], 
            'durasi': song[4],
            'tanggal_rilis': tanggal_rilis,
            'tahun': song[6],
            'total_play': song[7],
            'total_download': song[8],
            'album': song[9],
        }
    }

    cursor.close()
    connection.close()

    return render(request, 'detail_song.html', context)

def song_detail_only(request, song_id):
    connection, cursor = get_database_cursor()

    # Retrieve song details
    cursor.execute("""
    SELECT k.judul, g.genre, ak_artist.nama as artist, ak_songwriter.nama as songwriter, k.durasi, k.tanggal_rilis, k.tahun, s.total_play, s.total_download, al.judul as album, s.id_konten
    FROM playlist_song ps
    JOIN song s ON ps.id_song = s.id_konten
    JOIN konten k ON s.id_konten = k.id
    JOIN artist ar ON s.id_artist = ar.id
    JOIN akun ak_artist ON ar.email_akun = ak_artist.email
    JOIN album al ON s.id_album = al.id
    JOIN genre g ON s.id_konten = g.id_konten
    JOIN songwriter_write_song sws ON s.id_konten = sws.id_song
    JOIN songwriter sw ON sws.id_songwriter = sw.id
    JOIN akun ak_songwriter ON sw.email_akun = ak_songwriter.email
    WHERE ps.id_song = %s;
    """, ( [song_id] ))
    song_details = cursor.fetchall()

    # Check if song exists
    if not song_details:
        return HTTPResponse("Song not found", status=404)

    # Get the song detail
    song = song_details[0]

    # Format tanggal rilis
    tanggal_rilis = song[5].strftime("%m/%d/%y")

    context = {
        'song_id' : song_id,
        'song': {
            'judul': song[0],
            'genre': song[1], 
            'artist': song[2],
            'songwriters': song[3], 
            'durasi': song[4],
            'tanggal_rilis': tanggal_rilis,
            'tahun': song[6],
            'total_play': song[7],
            'total_download': song[8],
            'album': song[9],
        }
    }

    cursor.close()
    connection.close()

    return render(request, 'detail_song_only.html', context)

# def add_to_playlist(request, playlist_id, song_id):
#     success_message = None
#     playlist_name = None
#     song_title = None
#     artist_name = None
#     playlists = None

#     email_pengguna = request.COOKIES.get('email')

#     connection, cursor = get_database_cursor()

#     if request.method == 'POST':
#         other_playlist_id = request.POST.get('other_playlist_id')
        
#         cursor.execute("""
#             SELECT k.judul, a.nama AS artist
#             FROM song s
#             JOIN konten k ON s.id_konten = k.id
#             JOIN artist ar ON s.id_artist = ar.id
#             JOIN akun a ON ar.email_akun = a.email
#             WHERE s.id_konten = %s;
#         """, [song_id])
#         song_data = cursor.fetchone()
#         if song_data:
#             song_title, artist_name = song_data

#         cursor.execute("SELECT judul FROM user_playlist WHERE id_playlist = %s", [other_playlist_id])
#         playlist_name_query = cursor.fetchone()
#         if playlist_name_query:
#             playlist_name = playlist_name_query[0]
        
#         cursor.execute("INSERT INTO playlist_song (id_playlist, id_song) VALUES (%s, %s);", 
#                         [other_playlist_id, song_id])
            
#         success_message = f"Berhasil menambahkan Lagu dengan judul '{song_title}' oleh '{artist_name}' ke '{playlist_name}'!"

#     if not playlists:
#         cursor.execute("""
#             SELECT id_playlist, judul 
#             FROM user_playlist 
#             WHERE email_pembuat = %s;
#         """, [email_pengguna])
#         playlists = cursor.fetchall()


#     context = {
#         'playlists': playlists,
#         'playlist_id': playlist_id,
#         'song_id': song_id,
#         'song_title': song_title,
#         'artist_name': artist_name,
#         'success_message': success_message,
#         'playlist_name': playlist_name
#     }

#     cursor.close()
#     connection.close()

#     return render(request, 'add_to_playlist.html', context)

def add_to_playlist_new(request, song_id):
    success_message = None
    playlist_name = None
    song_title = None
    artist_name = None
    playlists = None

    email_pengguna = request.COOKIES.get('email')

    connection, cursor = get_database_cursor()

    if request.method == 'POST':
        other_playlist_id = request.POST.get('other_playlist_id')
        
        cursor.execute("""
            SELECT k.judul, a.nama AS artist
            FROM song s
            JOIN konten k ON s.id_konten = k.id
            JOIN artist ar ON s.id_artist = ar.id
            JOIN akun a ON ar.email_akun = a.email
            WHERE s.id_konten = %s;
        """, [song_id])
        song_data = cursor.fetchone()
        if song_data:
            song_title, artist_name = song_data

        cursor.execute("SELECT judul FROM user_playlist WHERE id_playlist = %s", [other_playlist_id])
        playlist_name_query = cursor.fetchone()
        if playlist_name_query:
            playlist_name = playlist_name_query[0]
        
        cursor.execute("INSERT INTO playlist_song (id_playlist, id_song) VALUES (%s, %s);", 
                        [other_playlist_id, song_id])
            
        success_message = f"Berhasil menambahkan Lagu dengan judul '{song_title}' oleh '{artist_name}' ke '{playlist_name}'!"

    if not playlists:
        cursor.execute("""
            SELECT id_playlist, judul 
            FROM user_playlist 
            WHERE email_pembuat = %s;
        """, [email_pengguna])
        playlists = cursor.fetchall()
    
    cursor.execute(f"""
    SELECT a.nama, k.judul
    FROM song s
    JOIN konten k ON s.id_konten = k.id
    JOIN artist art ON art.id = s.id_artist
    JOIN akun a ON art.email_akun = a.email
    WHERE k.id='{song_id}'
    """)
    artist_name, song_title = cursor.fetchone()

    context = {
        'song_id': song_id,
        'song_title': song_title,
        'artist_name': artist_name,
        'success_message': success_message,
        'playlist_name': playlist_name,
        'playlists' : playlists,
    }

    cursor.close()
    connection.close()

    return render(request, 'add_to_playlist_new.html', context)




