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
    # Get values from cookies
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    id_user_artist = request.COOKIES.get('id_user_artist')
    id_user_songwriter = request.COOKIES.get('id_user_songwriter')
    album_id = request.GET.get('album_id') or request.POST.get('album_id')

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
        year_now = '{:04d}'.format(current_datetime.year)
        songwriters = request.POST.getlist('song_writer[]')
        genres = request.POST.getlist('song_genre[]')

        # Handle artist information
        if isArtist == "True":
            id_pemilik_hak_cipta_artist = request.COOKIES.get(
                'idPemilikCiptaArtist')
        else:
            id_user_artist = request.POST.get('song_artist')
            cursor.execute(
                f"SELECT id_pemilik_hak_cipta FROM artist WHERE id = %s", [id_user_artist])
            id_pemilik_hak_cipta_artist = cursor.fetchone()[0]

        # Insert into 'konten' table
        cursor.execute(
            f"INSERT INTO konten VALUES (%s, %s, %s, %s, %s)",
            (id_song, judul, date_now, year_now, durasi)
        )

        # Insert into 'song' table
        cursor.execute(
            f"INSERT INTO song VALUES (%s, %s, %s, 0, 0)",
            (id_song, id_user_artist, album_id)
        )

        # Insert into 'songwriter_write_song' and 'royalti' tables
        for songwriter in songwriters:
            cursor.execute(
                f"SELECT id_pemilik_hak_cipta FROM songwriter WHERE id = %s", [songwriter])
            id_pemilik_hak_cipta_songwriter = cursor.fetchone()[0]
            cursor.execute(
                f"INSERT INTO royalti VALUES (%s, %s, 0)",
                (id_pemilik_hak_cipta_songwriter, id_song)
            )
            cursor.execute(
                f"INSERT INTO songwriter_write_song VALUES (%s, %s)",
                (songwriter, id_song)
            )

        # Insert into 'genre' table
        for genre in genres:
            cursor.execute(
                f"INSERT INTO genre VALUES (%s, %s)",
                (id_song, genre)
            )

        # Insert into 'royalti' table for artist
        cursor.execute(
            f"INSERT INTO royalti VALUES (%s, %s, 0)",
            (id_pemilik_hak_cipta_artist, id_song)
        )

        # Insert into 'royalti' table for label
        cursor.execute(f"SELECT id_label FROM album WHERE id = %s", [album_id])
        id_label = cursor.fetchone()
        if id_label:
            id_label = id_label[0]
            cursor.execute(
                f"SELECT id_pemilik_hak_cipta FROM label WHERE id = %s", [id_label])
            id_pemilik_hak_cipta_label = cursor.fetchone()
            if id_pemilik_hak_cipta_label:
                id_pemilik_hak_cipta_label = id_pemilik_hak_cipta_label[0]
                cursor.execute(
                    f"INSERT INTO royalti VALUES (%s, %s, 0)",
                    (id_pemilik_hak_cipta_label, id_song)
                )

        # Update album information
        cursor.execute(
            f"SELECT jumlah_lagu, total_durasi FROM album WHERE id = %s", [album_id])
        album_saat_ini = cursor.fetchone()
        new_total_durasi = int(album_saat_ini[1]) + int(durasi)
        new_jumlah_lagu = int(album_saat_ini[0]) + 1
        cursor.execute(
            f"UPDATE album SET jumlah_lagu = %s, total_durasi = %s WHERE id = %s",
            (new_jumlah_lagu, new_total_durasi, album_id)
        )

        # Commit changes to the database
        connection.commit()

        return redirect('album_song_royalti:list_album')

    # Fetch artist records for the dropdown
    cursor.execute(f"SELECT id, email_akun, id_pemilik_hak_cipta FROM artist")
    records_artist = cursor.fetchall()
    for i in range(len(records_artist)):
        cursor.execute(
            f"SELECT nama FROM akun WHERE email = %s", [records_artist[i][1]])
        records_artist[i] = records_artist[i] + cursor.fetchone()

    # Fetch songwriter records for the dropdown
    cursor.execute(
        f"SELECT id, email_akun, id_pemilik_hak_cipta FROM songwriter")
    records_songwriter = cursor.fetchall()
    for i in range(len(records_songwriter)):
        cursor.execute(
            f"SELECT nama FROM akun WHERE email = %s", [records_songwriter[i][1]])
        records_songwriter[i] = records_songwriter[i] + cursor.fetchone()

    # Fetch genre records for the dropdown
    cursor.execute(f"SELECT DISTINCT genre FROM genre")
    records_genre = cursor.fetchall()

    # Get album title
    cursor.execute(f"SELECT judul FROM album WHERE id = %s", [album_id])
    judul_album = cursor.fetchone()

    # Get artist name if the user is an artist
    if isArtist == "True":
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

    context = {
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'id_user_artist': id_user_artist,
        'id_user_songwriter': id_user_songwriter,
        'records_artist': records_artist,
        'records_songwriter': records_songwriter,
        'records_genre': records_genre,
        'album_id': album_id,  # Add album ID to context
        'judul_album': judul_album,
        'artist_name': nama_artist,
        'songwriter_name': nama_songwriter,
    }

    return render(request, 'create_songs.html', context)


def list_album_label(request):
    email = request.COOKIES.get('email')
    cursor.execute(
        f'select * from label where email = \'{email}\'')
    label = cursor.fetchmany()
    if len(label) == 1:
        # Cari album yang dimiliki label
        id_label = label[0][0]
        cursor.execute(
            f'select * from album where id_label = \'{id_label}\'')
        records_album = cursor.fetchall()
        context = {
            'role': 'label',
            'status': 'success',
            'id': label[0][0],
            'nama': label[0][1],
            'email': label[0][2],
            'kontak': label[0][4],
            'id_pemilik_hak_cipta': label[0][5],
            'records_album': records_album,
        }
        print(records_album)
        response = render(request, 'list_album_label.html', context)
        response.set_cookie('role', 'label')
        response.set_cookie('email', email)
        response.set_cookie('id', label[0][0])
        response.set_cookie('idPemilikCiptaLabel', label[0][5])
        return response
    return render(request, 'list_album_label.html')


def list_album(request):

    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    records_album = []
    artistHasAlbum = False
    songwriterHasAlbum = False
    album_ids = set()  # Set to track unique album IDs

    # artist
    if isArtist == "True":
        id_artist = request.COOKIES.get('id_user_artist')
        cursor.execute(
            f'SELECT DISTINCT id_album FROM SONG WHERE id_artist = %s', [id_artist])
        list_album_id_artist = cursor.fetchall()

        if list_album_id_artist:
            artistHasAlbum = True
            for id_album in list_album_id_artist:
                album_id = id_album[0]
                if album_id not in album_ids:
                    cursor.execute(
                        f'SELECT id, judul, id_label, jumlah_lagu, total_durasi FROM album WHERE id = %s', [album_id])
                    album_data = cursor.fetchone()
                    if album_data:
                        cursor.execute(
                            f'SELECT nama FROM LABEL WHERE id = %s', [album_data[2]])
                        label_name = cursor.fetchone()
                        if label_name:
                            records_album.append(album_data + label_name)
                            album_ids.add(album_id)

    # songwriter
    if isSongwriter == "True":
        id_songwriter = request.COOKIES.get('id_user_songwriter')
        cursor.execute(
            f'SELECT id_song FROM songwriter_write_song WHERE id_songwriter = %s', [id_songwriter])
        list_song_id_songwriter = cursor.fetchall()
        if list_song_id_songwriter:
            for song in list_song_id_songwriter:
                cursor.execute(
                    f'SELECT id_album FROM SONG WHERE id_konten = %s', [song[0]])
                id_album_songwriter = cursor.fetchone()
                if id_album_songwriter:
                    album_id = id_album_songwriter[0]
                    if album_id not in album_ids:
                        cursor.execute(
                            f'SELECT id, judul, id_label, jumlah_lagu, total_durasi FROM album WHERE id = %s', [album_id])
                        album_data = cursor.fetchone()
                        if album_data:
                            cursor.execute(
                                f'SELECT nama FROM LABEL WHERE id = %s', [album_data[2]])
                            label_name = cursor.fetchone()
                            if label_name:
                                records_album.append(album_data + label_name)
                                album_ids.add(album_id)
                                songwriterHasAlbum = True

    context = {
        'status': 'success',
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'artistHasAlbum': artistHasAlbum,
        'songwriterHasAlbum': songwriterHasAlbum,
        'records_album': records_album,
    }
    response = render(request, 'list_album.html', context)
    return response


def update_album_details(album_id):
    # Calculate the number of songs in the album
    cursor.execute('SELECT COUNT(*) FROM song WHERE id_album = %s', [album_id])
    jumlah_lagu = cursor.fetchone()[0]

    # Calculate the total duration of the songs in the album
    cursor.execute(
        'SELECT SUM(durasi) FROM konten WHERE id IN (SELECT id_konten FROM song WHERE id_album = %s)', [album_id])
    # Ensure total_durasi is 0 if no songs found
    total_durasi = cursor.fetchone()[0] or 0

    # Update the album's details
    cursor.execute('UPDATE album SET jumlah_lagu = %s, total_durasi = %s WHERE id = %s', [
                   jumlah_lagu, total_durasi, album_id])
    connection.commit()


def list_song(request):
    album_id = request.GET.get('id')
    list_songs = []
    cursor.execute(
        f'SELECT id_konten, total_play, total_download from song where id_album = \'{album_id}\'')
    list_songs = cursor.fetchall()
    for i in range(len(list_songs)):
        cursor.execute(
            f'SELECT judul, tanggal_rilis, tahun, durasi from konten where id = \'{list_songs[i][0]}\'')
        list_songs[i] = list_songs[i] + cursor.fetchone()

    # Update album details
    update_album_details(album_id)

    context = {
        'status': 'success',
        'list_songs': list_songs,
    }
    response = render(request, 'list_songs.html', context)
    return response


def delete_song(request):
    # Get the album ID of the song to be deleted
    song_id = request.GET.get('song_id')
    cursor.execute('SELECT id_album FROM song WHERE id_konten = %s', [song_id])
    valid_id = cursor.fetchone()
    if not valid_id:
        return HttpResponse("Invalid song ID")
    album_id = valid_id[0]

    # Delete the references in the related tables first
    cursor.execute(
        'DELETE FROM songwriter_write_song WHERE id_song = %s', [song_id])
    cursor.execute('DELETE FROM downloaded_song WHERE id_song = %s', [song_id])
    cursor.execute('DELETE FROM royalti WHERE id_song = %s', [song_id])
    cursor.execute('DELETE FROM akun_play_song WHERE id_song = %s', [song_id])
    cursor.execute('DELETE FROM playlist_song WHERE id_song = %s', [song_id])

    # Delete the song from the song and konten tables
    cursor.execute('DELETE FROM song WHERE id_konten = %s', [song_id])
    cursor.execute('DELETE FROM genre WHERE id_konten = %s', [song_id])
    cursor.execute('DELETE FROM konten WHERE id = %s', [song_id])

    connection.commit()
    list_songs = []
    cursor.execute(
        'SELECT id_konten, total_play, total_download FROM song WHERE id_album = %s', [album_id])
    list_songs = cursor.fetchall()
    for i in range(len(list_songs)):
        cursor.execute('SELECT judul, tanggal_rilis, tahun, durasi FROM konten WHERE id = %s', [
                       list_songs[i][0]])
        list_songs[i] = list_songs[i] + cursor.fetchone()

    context = {
        'status': 'success',
        'list_songs': list_songs,
    }

    return render(request, 'list_songs.html', context)


def delete_album_label(request):
    # Get the album ID from the request
    album_id = request.GET.get('id')

    # Fetch the album to ensure it exists
    cursor.execute('SELECT * FROM album WHERE id = %s', [album_id])
    album = cursor.fetchone()
    if not album:
        return HttpResponse("Invalid album ID")

    # Fetch all songs in the album
    cursor.execute(
        'SELECT id_konten FROM song WHERE id_album = %s', [album_id])
    songs = cursor.fetchall()

    # Delete references in related tables for each song
    for song in songs:
        song_id = song[0]
        cursor.execute(
            'DELETE FROM songwriter_write_song WHERE id_song = %s', [song_id])
        cursor.execute(
            'DELETE FROM downloaded_song WHERE id_song = %s', [song_id])
        cursor.execute('DELETE FROM royalti WHERE id_song = %s', [song_id])
        cursor.execute(
            'DELETE FROM akun_play_song WHERE id_song = %s', [song_id])
        cursor.execute(
            'DELETE FROM playlist_song WHERE id_song = %s', [song_id])

        # Delete the song from the song and konten tables
        cursor.execute('DELETE FROM song WHERE id_konten = %s', [song_id])
        cursor.execute('DELETE FROM genre WHERE id_konten = %s', [song_id])
        cursor.execute('DELETE FROM konten WHERE id = %s', [song_id])

    # Finally, delete the album itself
    cursor.execute('DELETE FROM album WHERE id = %s', [album_id])
    connection.commit()

    # Return a success response or redirect to the appropriate page
    # Replace with the correct URL or view name
    return redirect('album_song_royalti:list_album_label')


def delete_album_user(request):
    # Get the album ID from the request
    album_id = request.GET.get('id')

    # Fetch the album to ensure it exists
    cursor.execute('SELECT * FROM album WHERE id = %s', [album_id])
    album = cursor.fetchone()
    if not album:
        return HttpResponse("Invalid album ID")

    # Fetch all songs in the album
    cursor.execute(
        'SELECT id_konten FROM song WHERE id_album = %s', [album_id])
    songs = cursor.fetchall()

    # Delete references in related tables for each song
    for song in songs:
        song_id = song[0]
        cursor.execute(
            'DELETE FROM songwriter_write_song WHERE id_song = %s', [song_id])
        cursor.execute(
            'DELETE FROM downloaded_song WHERE id_song = %s', [song_id])
        cursor.execute('DELETE FROM royalti WHERE id_song = %s', [song_id])
        cursor.execute(
            'DELETE FROM akun_play_song WHERE id_song = %s', [song_id])
        cursor.execute(
            'DELETE FROM playlist_song WHERE id_song = %s', [song_id])

        # Delete the song from the song and konten tables
        cursor.execute('DELETE FROM song WHERE id_konten = %s', [song_id])
        cursor.execute('DELETE FROM genre WHERE id_konten = %s', [song_id])
        cursor.execute('DELETE FROM konten WHERE id = %s', [song_id])

    # Finally, delete the album itself
    cursor.execute('DELETE FROM album WHERE id = %s', [album_id])
    connection.commit()

    # Return a success response or redirect to the appropriate page
    # Replace with the correct URL or view name
    return redirect('album_song_royalti:list_album')


def fetch_royalty_data(cursor, id_pemilik_hak_cipta, id_song):

    cursor.execute('SELECT rate_royalti FROM pemilik_hak_cipta WHERE id = %s', [
                   id_pemilik_hak_cipta])
    rate_royalti = cursor.fetchone()

    cursor.execute(
        'SELECT id_album, total_play, total_download FROM song WHERE id_konten = %s', [id_song])
    song_data = cursor.fetchone()

    cursor.execute('SELECT judul FROM album WHERE id = %s', [song_data[0]])
    album_title = cursor.fetchone()

    cursor.execute('SELECT judul FROM konten WHERE id = %s', [id_song])
    song_title = cursor.fetchone()

    return rate_royalti, song_data, album_title, song_title


def update_royalty(cursor, total_royalty, id_pemilik_hak_cipta, id_song):

    cursor.execute('UPDATE royalti SET jumlah = %s WHERE id_pemilik_hak_cipta = %s AND id_song = %s',
                   [total_royalty, id_pemilik_hak_cipta, id_song])
    cursor.connection.commit()


def process_royalties(records_royalti, id_pemilik_hak_cipta):

    for i in range(len(records_royalti)):
        id_song = records_royalti[i][0]
        rate_royalti, song_data, album_title, song_title = fetch_royalty_data(
            cursor, id_pemilik_hak_cipta, id_song)
        total_royalty = rate_royalti[0] * song_data[1]
        update_royalty(cursor, total_royalty, id_pemilik_hak_cipta, id_song)
        records_royalti[i] = (id_song, rate_royalti[0], song_data[0], song_data[1],
                              song_data[2], album_title[0], song_title[0], total_royalty)


def cek_royalti(request):

    role = request.COOKIES.get('role')
    isArtist = request.COOKIES.get('isArtist', "")
    isSongwriter = request.COOKIES.get('isSongwriter', "")
    records_royalti = []

    if role == "label":
        id_pemilik_hak_cipta = request.COOKIES.get('id_pemilik_hak_cipta')
        cursor.execute('SELECT id_song FROM royalti WHERE id_pemilik_hak_cipta = %s', [
                       id_pemilik_hak_cipta])
        records_royalti = cursor.fetchall()
        if records_royalti:
            process_royalties(records_royalti, id_pemilik_hak_cipta)

    elif isArtist == "True":
        idPemilikCiptaArtist = request.COOKIES.get('idPemilikCiptaArtist')
        cursor.execute('SELECT id_song FROM royalti WHERE id_pemilik_hak_cipta = %s', [
                       idPemilikCiptaArtist])
        records_royalti = cursor.fetchall()
        if records_royalti:
            process_royalties(records_royalti, idPemilikCiptaArtist)

    elif isSongwriter == "True":
        idPemilikCiptaSongwriter = request.COOKIES.get(
            'idPemilikCiptaSongwriter')
        cursor.execute('SELECT id_song FROM royalti WHERE id_pemilik_hak_cipta = %s', [
                       idPemilikCiptaSongwriter])
        records_royalti = cursor.fetchall()
        if records_royalti:
            process_royalties(records_royalti, idPemilikCiptaSongwriter)

    context = {
        'status': 'success',
        'role': role,
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'records_royalti': records_royalti,
    }
    return render(request, 'cek_royalti.html', context)
