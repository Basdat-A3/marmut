import uuid
from django.shortcuts import redirect, render
from utils.query import *
from datetime import datetime
# Create your views here.
from django.http import HttpResponse


def create_album(request):
    connection, cursor = get_database_cursor()
    if request.method == 'POST' and not request.method == 'GET':
        judul = request.POST.get('album-title')
        label = request.POST.get('album-label')
        id_album = str(uuid.uuid4())
        cursor.execute(
            f'insert into album values (\'{id_album}\', \'{judul}\', 0, \'{label}\', 0)')
        connection.commit()
        return redirect('album_song_royalti:list_album')

    cursor.execute(
        f'select id, nama from label')
    list_label = cursor.fetchall()
    context = {
        'list_label': list_label
    }
    return render(request, 'create_album.html', context)


def create_song_artist(request):
    connection, cursor = get_database_cursor()
    return render(request, 'create_songs_artist.html')


def create_song(request):
    connection, cursor = get_database_cursor()
    return render(request, 'create_songs.html')


def list_album_label(request):
    connection, cursor = get_database_cursor()
    email = request.COOKIES.get('email')

    cursor.execute(
        f'select * from label where email = \'{email}\'')
    label = cursor.fetchmany()
    print(label)
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
    connection, cursor = get_database_cursor()
    isArtist = request.COOKIES.get('isArtist')
    isSongwriter = request.COOKIES.get('isSongwriter')
    records_album = []
    artistHasAlbum = False
    songwriterHasAlbum = False
    album_ids = set()  # Set to track unique album IDs

    # kalau dia artist, list album dia sebagai artist
    if isArtist == "True":
        id_artist = request.COOKIES.get('id_user_artist')
        cursor.execute(
            f'SELECT DISTINCT id_album FROM SONG WHERE id_artist = %s', [id_artist])
        list_album_id_artist = cursor.fetchall()
        print(list_album_id_artist)
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

    # kalau dia songwriter, list album dia sebagai songwriter
    if isSongwriter == "True":
        id_songwriter = request.COOKIES.get('id_user_songwriter')
        cursor.execute(
            f'SELECT id_song FROM songwriter_write_song WHERE id_songwriter = %s', [id_songwriter])
        list_song_id_songwriter = cursor.fetchall()
        print(list_song_id_songwriter)
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
    print(records_album)
    response = render(request, 'list_album.html', context)
    return response


def list_song(request):
    print(request.GET, "INI REQUEST")
    connection, cursor = get_database_cursor()
    album_id = request.GET.get('id')
    records_song = []

    cursor.execute(
        f'SELECT id_konten, total_play, total_download from song where id_album = \'{album_id}\'')
    records_song = cursor.fetchall()
    for i in range(len(records_song)):
        cursor.execute(
            f'SELECT judul, tanggal_rilis, tahun, durasi from konten where id = \'{records_song[i][0]}\'')
        records_song[i] = records_song[i] + cursor.fetchone()

    context = {
        'status': 'success',
        'records_song': records_song,
    }
    response = render(request, 'list_songs.html', context)
    return response


def fetch_royalty_data(cursor, id_pemilik_hak_cipta, id_song):
    connection, cursor = get_database_cursor()
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
    connection, cursor = get_database_cursor()
    cursor.execute('UPDATE royalti SET jumlah = %s WHERE id_pemilik_hak_cipta = %s AND id_song = %s',
                   [total_royalty, id_pemilik_hak_cipta, id_song])
    cursor.connection.commit()


def process_royalties(records_royalti, id_pemilik_hak_cipta):
    connection, cursor = get_database_cursor()
    for i in range(len(records_royalti)):
        id_song = records_royalti[i][0]
        rate_royalti, song_data, album_title, song_title = fetch_royalty_data(
            cursor, id_pemilik_hak_cipta, id_song)
        total_royalty = rate_royalti[0] * song_data[1]
        update_royalty(cursor, total_royalty, id_pemilik_hak_cipta, id_song)
        records_royalti[i] = (id_song, rate_royalti[0], song_data[0], song_data[1],
                              song_data[2], album_title[0], song_title[0], total_royalty)


def cek_royalti(request):
    connection, cursor = get_database_cursor()
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
