from utils.query import get_database_cursor
from django.shortcuts import render, redirect
from django.shortcuts import render
import uuid
from django.shortcuts import redirect, render
from utils.query import *
from datetime import datetime
# Create your views here.
from django.http import HttpResponse


def create_album(request):
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    id_user_artist = request.COOKIES.get('id_user_artist')
    id_user_songwriter = request.COOKIES.get('id_user_songwriter')

    if isArtist == "True":
        print(1)
        cursor.execute(
            f"SELECT email_akun FROM artist WHERE id = %s", [id_user_artist])
        email_artist = cursor.fetchone()
        cursor.execute(
            f"SELECT nama FROM akun WHERE email = %s", [email_artist[0]])
        nama_artist = cursor.fetchone()

    # Get songwriter name if the user is a songwriter
    if isSongwriter == "True":
        cursor.execute(
            f"SELECT email_akun FROM songwriter WHERE id = %s", [id_user_songwriter])
        email_songwriter = cursor.fetchone()
        cursor.execute(
            f"SELECT nama FROM akun WHERE email = %s", [email_songwriter[0]])
        nama_songwriter = cursor.fetchone()

    if request.method == 'POST':
        # Album creation part
        judul_album = request.POST.get('album-title')
        label = request.POST.get('album-label')
        id_album = str(uuid.uuid4())

        cursor.execute(
            'INSERT INTO album VALUES (%s, %s, 0, %s, 0)', (id_album, judul_album, label))
        connection.commit()

        # Check if song details are provided
        if 'song-title' in request.POST:
            judul_song = request.POST.get('song-title')
            durasi = request.POST.get('song-duration')
            songwriters = request.POST.getlist('song_writer[]')
            genres = request.POST.getlist('song_genre[]')
            id_song = str(uuid.uuid4())
            current_datetime = datetime.now()
            date_now = current_datetime.strftime('%Y-%m-%d')
            year_now = '{:04d}'.format(current_datetime.year)

            # Handle artist information
            if isArtist == "True":
                id_pemilik_hak_cipta_artist = request.COOKIES.get(
                    'idPemilikCiptaArtist')
            else:
                id_user_artist = request.POST.get('song_artist')
                cursor.execute(
                    "SELECT id_pemilik_hak_cipta FROM artist WHERE id = %s", [id_user_artist])
                id_pemilik_hak_cipta_artist = cursor.fetchone()[0]

            # Insert into 'konten' table
            cursor.execute(
                "INSERT INTO konten VALUES (%s, %s, %s, %s, %s)",
                (id_song, judul_song, date_now, year_now, durasi)
            )

            # Insert into 'song' table
            cursor.execute(
                "INSERT INTO song VALUES (%s, %s, %s, 0, 0)",
                (id_song, id_user_artist, id_album)
            )

            # Insert into 'songwriter_write_song' and 'royalti' tables
            for songwriter in songwriters:
                cursor.execute(
                    "SELECT id_pemilik_hak_cipta FROM songwriter WHERE id = %s", [songwriter])
                id_pemilik_hak_cipta_songwriter = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO royalti VALUES (%s, %s, 0)",
                    (id_pemilik_hak_cipta_songwriter, id_song)
                )
                cursor.execute(
                    "INSERT INTO songwriter_write_song VALUES (%s, %s)",
                    (songwriter, id_song)
                )

            # Insert into 'genre' table
            for genre in genres:
                cursor.execute(
                    "INSERT INTO genre VALUES (%s, %s)",
                    (id_song, genre)
                )

            # Insert into 'royalti' table for artist
            cursor.execute(
                "INSERT INTO royalti VALUES (%s, %s, 0)",
                (id_pemilik_hak_cipta_artist, id_song)
            )

            # Insert into 'royalti' table for label
            cursor.execute(
                "SELECT id_label FROM album WHERE id = %s", [id_album])
            id_label = cursor.fetchone()
            if id_label:
                id_label = id_label[0]
                cursor.execute(
                    "SELECT id_pemilik_hak_cipta FROM label WHERE id = %s", [id_label])
                id_pemilik_hak_cipta_label = cursor.fetchone()
                if id_pemilik_hak_cipta_label:
                    id_pemilik_hak_cipta_label = id_pemilik_hak_cipta_label[0]
                    cursor.execute(
                        "INSERT INTO royalti VALUES (%s, %s, 0)",
                        (id_pemilik_hak_cipta_label, id_song)
                    )

            # Update album information
            cursor.execute(
                "SELECT jumlah_lagu, total_durasi FROM album WHERE id = %s", [id_album])
            album_saat_ini = cursor.fetchone()
            new_total_durasi = int(album_saat_ini[1]) + int(durasi)
            new_jumlah_lagu = int(album_saat_ini[0]) + 1
            cursor.execute(
                "UPDATE album SET jumlah_lagu = %s, total_durasi = %s WHERE id = %s",
                (new_jumlah_lagu, new_total_durasi, id_album)
            )

            # Commit changes to the database
            connection.commit()
            update_album_details(id_album)
            return redirect('album_song_royalti:list_album')

    cursor.execute('SELECT id, nama FROM label')
    list_label = cursor.fetchall()

    cursor.execute("SELECT id, email_akun, id_pemilik_hak_cipta FROM artist")
    records_artist = cursor.fetchall()
    for i in range(len(records_artist)):
        cursor.execute("SELECT nama FROM akun WHERE email = %s",
                       [records_artist[i][1]])
        records_artist[i] = records_artist[i] + cursor.fetchone()

    cursor.execute(
        "SELECT id, email_akun, id_pemilik_hak_cipta FROM songwriter")
    records_songwriter = cursor.fetchall()
    for i in range(len(records_songwriter)):
        cursor.execute("SELECT nama FROM akun WHERE email = %s",
                       [records_songwriter[i][1]])
        records_songwriter[i] = records_songwriter[i] + cursor.fetchone()

    cursor.execute("SELECT DISTINCT genre FROM genre")
    records_genre = cursor.fetchall()

    context = {
        'list_label': list_label,
        'records_artist': records_artist,
        'records_songwriter': records_songwriter,
        'records_genre': records_genre,
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'id_user_artist': id_user_artist,
        'id_user_songwriter': id_user_songwriter,
        'artist_name': nama_artist,
        'songwriter_name': nama_songwriter,
    }

    return render(request, 'create_album.html', context)


def create_song(request):
    connection, cursor = get_database_cursor()
    # Get values from cookies
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    id_user_artist = request.COOKIES.get('id_user_artist')
    id_user_songwriter = request.COOKIES.get('id_user_songwriter')
    album_id = request.GET.get('id') or request.POST.get('id')

    # Initialize names
    nama_artist = ""
    nama_songwriter = ""

    if request.method == 'POST':
        album_id = request.POST.get('album_id')
        if not album_id:
            return HttpResponse("Album ID is required", status=400)

        # Get POST data
        judul = request.POST.get('song-title')
        id_song = str(uuid.uuid4())
        durasi = request.POST.get('song-duration')
        current_datetime = datetime.now()
        date_now = current_datetime.strftime('%Y-%m-%d')
        year_now = current_datetime.year
        songwriters = request.POST.getlist('song_writer[]')
        genres = request.POST.getlist('song_genre[]')

        # Handle artist information
        if isArtist == "True":
            id_pemilik_hak_cipta_artist = request.COOKIES.get(
                'idPemilikCiptaArtist')
        else:
            id_user_artist = request.POST.get('song_artist')
            cursor.execute("SELECT id_pemilik_hak_cipta FROM artist WHERE id = %s", [
                           id_user_artist])
            id_pemilik_hak_cipta_artist = cursor.fetchone()[0]

        # Insert song and related data
        cursor.execute(
            "INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi) VALUES (%s, %s, %s, %s, %s)",
            (id_song, judul, date_now, year_now, durasi)
        )
        cursor.execute(
            "INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download) VALUES (%s, %s, %s, 0, 0)",
            (id_song, id_user_artist, album_id)
        )
        cursor.executemany(
            "INSERT INTO songwriter_write_song (id_songwriter, id_song) VALUES (%s, %s)",
            [(songwriter, id_song) for songwriter in songwriters]
        )
        cursor.executemany(
            "INSERT INTO genre (id_konten, genre) VALUES (%s, %s)",
            [(id_song, genre) for genre in genres]
        )
        cursor.executemany(
            "INSERT INTO royalti (id_pemilik_hak_cipta, id_song, jumlah) VALUES (%s, %s, 0)",
            [(id_pemilik_hak_cipta_artist, id_song)] +
            [(cursor.execute("SELECT id_pemilik_hak_cipta FROM songwriter WHERE id = %s", [
              songwriter]).fetchone()[0], id_song) for songwriter in songwriters]
        )

        cursor.execute("SELECT id_label FROM album WHERE id = %s", [album_id])
        id_label = cursor.fetchone()
        if id_label:
            id_label = id_label[0]
            cursor.execute(
                "SELECT id_pemilik_hak_cipta FROM label WHERE id = %s", [id_label])
            id_pemilik_hak_cipta_label = cursor.fetchone()
            if id_pemilik_hak_cipta_label:
                cursor.execute(
                    "INSERT INTO royalti (id_pemilik_hak_cipta, id_song, jumlah) VALUES (%s, %s, 0)",
                    (id_pemilik_hak_cipta_label[0], id_song)
                )

        cursor.execute(
            "UPDATE album SET jumlah_lagu = jumlah_lagu + 1, total_durasi = total_durasi + %s WHERE id = %s",
            (durasi, album_id)
        )
        connection.commit()

        return redirect('album_song_royalti:list_album')

    # Fetch artist records for the dropdown
    cursor.execute(
        "SELECT artist.id, artist.email_akun, artist.id_pemilik_hak_cipta, akun.nama FROM artist JOIN akun ON artist.email_akun = akun.email")
    records_artist = cursor.fetchall()

    # Fetch songwriter records for the dropdown
    cursor.execute("SELECT songwriter.id, songwriter.email_akun, songwriter.id_pemilik_hak_cipta, akun.nama FROM songwriter JOIN akun ON songwriter.email_akun = akun.email")
    records_songwriter = cursor.fetchall()

    # Fetch genre records for the dropdown
    cursor.execute("SELECT DISTINCT genre FROM genre")
    records_genre = cursor.fetchall()

    # Get album title
    cursor.execute("SELECT judul FROM album WHERE id = %s", [album_id])
    judul_album = cursor.fetchone()

    # Get artist name if the user is an artist
    if isArtist == "True":
        cursor.execute("SELECT nama FROM akun WHERE email = (SELECT email_akun FROM artist WHERE id = %s)", [
                       id_user_artist])
        nama_artist = cursor.fetchone()

    # Get songwriter name if the user is a songwriter
    if isSongwriter == "True":
        cursor.execute("SELECT nama FROM akun WHERE email = (SELECT email_akun FROM songwriter WHERE id = %s)", [
                       id_user_songwriter])
        nama_songwriter = cursor.fetchone()

    context = {
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'id_user_artist': id_user_artist,
        'id_user_songwriter': id_user_songwriter,
        'records_artist': records_artist,
        'records_songwriter': records_songwriter,
        'records_genre': records_genre,
        'album_id': album_id,
        'judul_album': judul_album,
        'artist_name': nama_artist,
        'songwriter_name': nama_songwriter,
    }

    cursor.close()
    connection.close()
    return render(request, 'create_songs.html', context)


def list_album_label(request):
    connection, cursor = get_database_cursor()
    email = request.COOKIES.get('email')

    # Fetch label details and albums in a single query
    cursor.execute(
        '''
        SELECT 
            label.id, label.nama, label.email, label.kontak, label.id_pemilik_hak_cipta, 
            album.id, album.judul, album.jumlah_lagu, album.total_durasi
        FROM 
            label 
        LEFT JOIN 
            album 
        ON 
            label.id = album.id_label 
        WHERE 
            label.email = %s
        ORDER BY
            album.judul ASC
        ''', [email]
    )

    results = cursor.fetchall()
    if results:
        # Extract label details and album records
        label = results[0]
        list_albums = [
            record[5:] for record in results if record[5] is not None
        ]

        context = {
            'role': 'label',
            'status': 'success',
            'id': label[0],
            'nama': label[1],
            'email': label[2],
            'kontak': label[3],
            'id_pemilik_hak_cipta': label[4],
            'list_albums': list_albums,
        }

        response = render(request, 'list_album_label.html', context)
        response.set_cookie('role', 'label')
        response.set_cookie('email', email)
        response.set_cookie('id', label[0])
        response.set_cookie('idPemilikCiptaLabel', label[4])
        return response

    cursor.close()
    connection.close()
    return render(request, 'list_album_label.html')


def list_album(request):
    connection, cursor = get_database_cursor()
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    id_user_artist = request.COOKIES.get('id_user_artist')
    id_user_songwriter = request.COOKIES.get('id_user_songwriter')

    list_albums = []
    album_ids = set()  # Set to track unique album IDs

    # Fetch albums for artist
    if isArtist == "True" and id_user_artist:
        cursor.execute(
            '''
            SELECT DISTINCT album.id, album.judul, album.id_label, album.jumlah_lagu, album.total_durasi, label.nama 
            FROM album
            JOIN song ON album.id = song.id_album
            JOIN label ON album.id_label = label.id
            WHERE song.id_artist = %s
            ''', [id_user_artist]
        )
        artist_records = cursor.fetchall()
        for record in artist_records:
            if record[0] not in album_ids:
                list_albums.append(record)
                album_ids.add(record[0])

    # Fetch albums for songwriter
    if isSongwriter == "True" and id_user_songwriter:
        cursor.execute(
            '''
            SELECT DISTINCT album.id, album.judul, album.id_label, album.jumlah_lagu, album.total_durasi, label.nama 
            FROM album
            JOIN song ON album.id = song.id_album
            JOIN songwriter_write_song ON song.id_konten = songwriter_write_song.id_song
            JOIN label ON album.id_label = label.id
            WHERE songwriter_write_song.id_songwriter = %s
            ''', [id_user_songwriter]
        )
        songwriter_records = cursor.fetchall()
        for record in songwriter_records:
            if record[0] not in album_ids:
                list_albums.append(record)
                album_ids.add(record[0])

    # Sort the combined list_albums list alphabetically by album title
    list_albums.sort(key=lambda x: x[1])

    artistHasAlbum = bool(artist_records) if isArtist == "True" else False
    songwriterHasAlbum = bool(
        songwriter_records) if isSongwriter == "True" else False

    context = {
        'status': 'success',
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'artistHasAlbum': artistHasAlbum,
        'songwriterHasAlbum': songwriterHasAlbum,
        'list_albums': list_albums,
    }

    cursor.close()
    connection.close()
    response = render(request, 'list_album.html', context)
    return response


def update_album_details(album_id):
    connection, cursor = get_database_cursor()
    # Calculate the number of songs and the total duration of the songs in the album
    cursor.execute(
        '''
        SELECT COUNT(id), COALESCE(SUM(konten.durasi), 0) 
        FROM song 
        JOIN konten ON id_konten = konten.id 
        WHERE id_album = %s
        ''', [album_id]
    )
    jumlah_lagu, total_durasi = cursor.fetchone()

    # Update the album's details
    cursor.execute(
        '''
        UPDATE album 
        SET jumlah_lagu = %s, total_durasi = %s 
        WHERE id = %s
        ''', [jumlah_lagu, total_durasi, album_id]
    )
    connection.commit()
    cursor.close()
    connection.close()


def list_song(request):
    connection, cursor = get_database_cursor()
    role = request.COOKIES.get('role')
    album_id = request.GET.get('id')
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    id_user_artist = request.COOKIES.get('id_user_artist')
    id_user_songwriter = request.COOKIES.get('id_user_songwriter')

    if not album_id:
        return HttpResponse("Album ID is required", status=400)

    list_songs = []
    song_ids = set()  # Set to track unique song IDs

    # Query to fetch songs related to the logged-in artist
    if isArtist == "True" and id_user_artist:
        cursor.execute(
            '''
            SELECT song.id_konten, song.total_play, song.total_download, 
                   konten.judul, konten.tanggal_rilis, konten.tahun, konten.durasi
            FROM song
            JOIN konten ON song.id_konten = konten.id
            WHERE song.id_album = %s AND song.id_artist = %s
            ''', [album_id, id_user_artist]
        )
        artist_songs = cursor.fetchall()
        for song in artist_songs:
            if song[0] not in song_ids:
                list_songs.append(song)
                song_ids.add(song[0])

    # Query to fetch songs related to the logged-in songwriter
    if isSongwriter == "True" and id_user_songwriter:
        cursor.execute(
            '''
            SELECT song.id_konten, song.total_play, song.total_download, 
                   konten.judul, konten.tanggal_rilis, konten.tahun, konten.durasi
            FROM song
            JOIN konten ON song.id_konten = konten.id
            JOIN songwriter_write_song ON song.id_konten = songwriter_write_song.id_song
            WHERE song.id_album = %s AND songwriter_write_song.id_songwriter = %s
            ''', [album_id, id_user_songwriter]
        )
        songwriter_songs = cursor.fetchall()
        for song in songwriter_songs:
            if song[0] not in song_ids:
                list_songs.append(song)
                song_ids.add(song[0])

    if role == "label":
        cursor.execute(
            '''
            SELECT song.id_konten, song.total_play, song.total_download, 
                   konten.judul, konten.tanggal_rilis, konten.tahun, konten.durasi
            FROM song
            JOIN konten ON song.id_konten = konten.id
            WHERE song.id_album = %s
            ''', [album_id]
        )
        label_songs = cursor.fetchall()
        for song in label_songs:
            if song[0] not in song_ids:
                list_songs.append(song)
                song_ids.add(song[0])

    update_album_details(album_id)
    # playlkist_id = req()
    context = {
        'status': 'success',
        'list_songs': list_songs,
        # 'playlist_id': playlist_id,  # Ensure this is added

    }
    cursor.close()
    connection.close()
    return render(request, 'list_songs.html', context)


def delete_song(request):
    connection, cursor = get_database_cursor()

    role = request.COOKIES.get('role')
    song_id = request.GET.get('song_id')
    cursor.execute('SELECT id_album FROM song WHERE id_konten = %s', [song_id])
    valid_id = cursor.fetchone()
    if not valid_id:
        return HttpResponse("Invalid song ID")

    # Delete the references in  related tables
    cursor.execute(
        '''
        DELETE FROM songwriter_write_song WHERE id_song = %s;
        DELETE FROM downloaded_song WHERE id_song = %s;
        DELETE FROM royalti WHERE id_song = %s;
        DELETE FROM akun_play_song WHERE id_song = %s;
        DELETE FROM playlist_song WHERE id_song = %s;
        DELETE FROM song WHERE id_konten = %s;
        DELETE FROM genre WHERE id_konten = %s;
        DELETE FROM konten WHERE id = %s;
        ''', [song_id, song_id, song_id, song_id, song_id, song_id, song_id, song_id]
    )

    connection.commit()

    cursor.close()
    connection.close()
    # Redirect to the list_album page
    if role == "label":
        return redirect(f'/list-album-label/')
    return redirect(f'/list-album/')


def delete_album_label(request):
    connection, cursor = get_database_cursor()
    # Get the album ID from the request
    album_id = request.GET.get('id')

    # Fetch the album to ensure it exists
    cursor.execute('SELECT id FROM album WHERE id = %s', [album_id])
    album = cursor.fetchone()
    if not album:
        return HttpResponse("Invalid album ID")

    # Fetch all songs in the album
    cursor.execute(
        'SELECT id_konten FROM song WHERE id_album = %s', [album_id])
    songs = cursor.fetchall()

    # Delete references in related tables for all songs in the album
    song_ids = [song[0] for song in songs]
    if song_ids:
        format_strings = ','.join(['%s'] * len(song_ids))
        cursor.execute(
            f'DELETE FROM songwriter_write_song WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM downloaded_song WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM royalti WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM akun_play_song WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM playlist_song WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM song WHERE id_konten IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM genre WHERE id_konten IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM konten WHERE id IN ({format_strings})', song_ids)

    # Finally, delete the album itself
    cursor.execute('DELETE FROM album WHERE id = %s', [album_id])
    connection.commit()

    cursor.close()
    connection.close()
    # Redirect to the list of albums
    return redirect('album_song_royalti:list_album_label')


def delete_album_user(request):
    connection, cursor = get_database_cursor()
    # Get the album ID from the request
    album_id = request.GET.get('id')

    # Fetch the album to ensure it exists
    cursor.execute('SELECT id FROM album WHERE id = %s', [album_id])
    album = cursor.fetchone()
    if not album:
        return HttpResponse("Invalid album ID")

    # Fetch all songs in the album
    cursor.execute(
        'SELECT id_konten FROM song WHERE id_album = %s', [album_id])
    songs = cursor.fetchall()

    # Delete references in related tables for all songs in the album
    song_ids = [song[0] for song in songs]
    if song_ids:
        format_strings = ','.join(['%s'] * len(song_ids))
        cursor.execute(
            f'DELETE FROM songwriter_write_song WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM downloaded_song WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM royalti WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM akun_play_song WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM playlist_song WHERE id_song IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM song WHERE id_konten IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM genre WHERE id_konten IN ({format_strings})', song_ids)
        cursor.execute(
            f'DELETE FROM konten WHERE id IN ({format_strings})', song_ids)

    # Finally, delete the album itself
    cursor.execute('DELETE FROM album WHERE id = %s', [album_id])
    connection.commit()

    cursor.close()
    connection.close()
    # Redirect to the list of albums
    return redirect('album_song_royalti:list_album')


def fetch_royalty_data(id_pemilik_hak_cipta, id_song):
    connection, cursor = get_database_cursor()
    cursor.execute('SELECT rate_royalti FROM pemilik_hak_cipta WHERE id = %s', [
                   id_pemilik_hak_cipta])
    rate_royalti = cursor.fetchone()

    cursor.execute(
        '''
        SELECT song.id_album, song.total_play, song.total_download, album.judul, konten.judul
        FROM song
        JOIN album ON song.id_album = album.id
        JOIN konten ON song.id_konten = konten.id
        WHERE song.id_konten = %s
        ''', [id_song]
    )
    song_data = cursor.fetchone()

    if not rate_royalti or not song_data:
        return None, None, None, None

    album_title = song_data[3]
    song_title = song_data[4]
    cursor.close()
    connection.close()
    return rate_royalti, song_data, album_title, song_title


def update_royalty(total_royalty, id_pemilik_hak_cipta, id_song):
    connection, cursor = get_database_cursor()
    cursor.execute(
        '''
        UPDATE royalti 
        SET jumlah = %s 
        WHERE id_pemilik_hak_cipta = %s AND id_song = %s
        ''', [total_royalty, id_pemilik_hak_cipta, id_song]
    )
    cursor.connection.commit()
    cursor.close()
    connection.close()


def process_royalties(all_royalti, id_pemilik_hak_cipta):
    connection, cursor = get_database_cursor()
    detailed_records = []
    for record in all_royalti:
        id_song = record[0]
        rate_royalti, song_data, album_title, song_title = fetch_royalty_data(
            id_pemilik_hak_cipta, id_song)
        if rate_royalti and song_data:
            total_royalty = rate_royalti[0] * song_data[1]
            update_royalty(total_royalty,
                           id_pemilik_hak_cipta, id_song)
            detailed_record = (
                id_song, song_title, album_title, song_data[1], song_data[2], total_royalty
            )
            detailed_records.append(detailed_record)
    cursor.close()
    connection.close()
    return detailed_records


def fetch_records(id_pemilik_hak_cipta):
    connection, cursor = get_database_cursor()
    cursor.execute('SELECT id_song FROM royalti WHERE id_pemilik_hak_cipta = %s', [
                   id_pemilik_hak_cipta])
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return records


def fetch_records_for_label(id_label):
    connection, cursor = get_database_cursor()
    cursor.execute(
        '''
        SELECT song.id_konten, song.id_album, song.total_play, song.total_download, konten.judul, album.judul
        FROM song
        JOIN konten ON song.id_konten = konten.id
        JOIN album ON song.id_album = album.id
        WHERE album.id_label = %s
        ''', [id_label]
    )
    cursor.close()
    connection.close()
    return cursor.fetchall()


def cek_royalti(request):
    connection, cursor = get_database_cursor()
    role = request.COOKIES.get('role')
    isArtist = request.COOKIES.get('isArtist', "")
    isSongwriter = request.COOKIES.get('isSongwriter', "")
    all_royalti = []

    id_pemilik_hak_cipta_set = set()

    if role == "label":
        id_label = request.COOKIES.get('id')
        label_records = fetch_records_for_label(id_label)
        for record in label_records:
            song_id = record[0]
            cursor.execute(
                '''
                SELECT rate_royalti 
                FROM pemilik_hak_cipta 
                JOIN royalti ON pemilik_hak_cipta.id = royalti.id_pemilik_hak_cipta
                WHERE royalti.id_song = %s
                ''', [song_id]
            )
            rate_royalti = cursor.fetchone()
            if rate_royalti:
                total_royalty = rate_royalti[0] * record[2]
                detailed_record = (
                    song_id, record[4], record[5], record[2], record[3], total_royalty
                )
                all_royalti.append(detailed_record)
    else:
        if isArtist == "True":
            id_pemilik_hak_cipta_set.add(
                request.COOKIES.get('idPemilikCiptaArtist'))
        if isSongwriter == "True":
            id_pemilik_hak_cipta_set.add(
                request.COOKIES.get('idPemilikCiptaSongwriter'))

        for id_pemilik_hak_cipta in id_pemilik_hak_cipta_set:
            if id_pemilik_hak_cipta:
                records = fetch_records(id_pemilik_hak_cipta)
                if records:
                    all_royalti.extend(process_royalties(
                        records, id_pemilik_hak_cipta))

    context = {
        'status': 'success',
        'role': role,
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'all_royalti': all_royalti,
    }
    cursor.close()
    connection.close()
    return render(request, 'cek_royalti.html', context)


def song_detail(request):
    connection, cursor = get_database_cursor()
    song_id = request.GET.get('song_id')
    print(song_id)
    # Retrieve song details
    cursor.execute("""
    SELECT k.judul, g.genre, ak_artist.nama as artist, ak_songwriter.nama as songwriter, k.durasi, k.tanggal_rilis, k.tahun, s.total_play, s.total_download, al.judul as album, s.id_konten
    FROM song s
    JOIN konten k ON s.id_konten = k.id
    JOIN artist ar ON s.id_artist = ar.id
    JOIN akun ak_artist ON ar.email_akun = ak_artist.email
    JOIN album al ON s.id_album = al.id
    JOIN genre g ON s.id_konten = g.id_konten
    JOIN songwriter_write_song sws ON s.id_konten = sws.id_song
    JOIN songwriter sw ON sws.id_songwriter = sw.id
    JOIN akun ak_songwriter ON sw.email_akun = ak_songwriter.email
    WHERE s.id_konten = %s;
    """, (song_id,))
    song_details = cursor.fetchall()
    print(song_details)
    # Check if song exists
    if not song_details:
        return HttpResponse("Song not found", status=404)

    # Get the song detail
    song = song_details[0]

    # Format tanggal rilis
    tanggal_rilis = song[5].strftime("%m/%d/%y")

    context = {
        'song_id': song_id,
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
