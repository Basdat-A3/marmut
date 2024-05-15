from django.shortcuts import render
import uuid
from django.shortcuts import redirect, render
from utils.query import *
from datetime import datetime
# Create your views here.
from django.http import HttpResponse


def create_album(request):
    return render(request, 'create_album.html')


def create_song_artist(request):
    return render(request, 'create_songs_artist.html')


def create_song(request):
    return render(request, 'create_songs.html')


def list_album_label(request):
    return render(request, 'list_album_label.html')


def list_album(request):
    return render(request, 'list_album.html')


def list_song(request):
    return render(request, 'list_songs.html')


def cek_royalti(request):
    role = 'label'
    isArtist = ""
    isSongwriter = ""
    records_royalti_label = []
    records_royalti_artist = []
    records_royalti_songwriter = []

    if role == "label":
        idPemilikCiptaLabel = '772674b1-db75-4354-a51e-78de4d7c9e13'
        cursor.execute(
            f'select id_song, jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaLabel}\'')
        records_royalti_label = cursor.fetchall()
        if len(records_royalti_label) != 0:
            for i in range(len(records_royalti_label)):
                cursor.execute(
                    f'select id_album, total_play, total_download from song where id_konten = \'{records_royalti_label[i][0]}\'')
                records_royalti_label[i] = records_royalti_label[i] + \
                    cursor.fetchone()
                cursor.execute(
                    f'select judul from album where id = \'{records_royalti_label[i][2]}\'')
                records_royalti_label[i] = records_royalti_label[i] + \
                    cursor.fetchone()
                cursor.execute(
                    f'select judul from konten where id = \'{records_royalti_label[i][0]}\'')
                records_royalti_label[i] = records_royalti_label[i] + \
                    cursor.fetchone()
    else:
        isArtist = request.COOKIES.get('isArtist')
        isSongwriter = request.COOKIES.get('isSongwriter')

        if isArtist == "True":
            idPemilikCiptaArtist = request.COOKIES.get('idPemilikCiptaArtist')
            cursor.execute(
                f'select id_song, jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaArtist}\'')
            records_royalti_artist = cursor.fetchall()
            if len(records_royalti_artist) != 0:
                for i in range(len(records_royalti_artist)):
                    cursor.execute(
                        f'select id_album, total_play, total_download from song where id_konten = \'{records_royalti_artist[i][0]}\'')
                    records_royalti_artist[i] = records_royalti_artist[i] + \
                        cursor.fetchone()
                    cursor.execute(
                        f'select judul from album where id = \'{records_royalti_artist[i][2]}\'')
                    records_royalti_artist[i] = records_royalti_artist[i] + \
                        cursor.fetchone()
                    cursor.execute(
                        f'select judul from konten where id = \'{records_royalti_artist[i][0]}\'')
                    records_royalti_artist[i] = records_royalti_artist[i] + \
                        cursor.fetchone()
        else:
            idPemilikCiptaSongwriter = request.COOKIES.get(
                'idPemilikCiptaSongwriter')
            cursor.execute(
                f'select id_song, jumlah from royalti where id_pemilik_hak_cipta = \'{idPemilikCiptaSongwriter}\'')
            records_royalti_songwriter = cursor.fetchall()
            if len(records_royalti_songwriter) != 0:
                for i in range(len(records_royalti_songwriter)):
                    cursor.execute(
                        f'select id_album, total_play, total_download from song where id_konten = \'{records_royalti_songwriter[i][0]}\'')
                    records_royalti_songwriter[i] = records_royalti_songwriter[i] + \
                        cursor.fetchone()
                    cursor.execute(
                        f'select judul from album where id = \'{records_royalti_songwriter[i][2]}\'')
                    records_royalti_songwriter[i] = records_royalti_songwriter[i] + \
                        cursor.fetchone()
                    cursor.execute(
                        f'select judul from konten where id = \'{records_royalti_songwriter[i][0]}\'')
                    records_royalti_songwriter[i] = records_royalti_songwriter[i] + \
                        cursor.fetchone()

    context = {
        'status': 'success',
        'role': role,
        'isArtist': isArtist,
        'isSongwriter': isSongwriter,
        'records_royalti_label': records_royalti_label,
        'records_royalti_artist': records_royalti_artist,
        'records_royalti_songwriter': records_royalti_songwriter,
    }
    response = render(request, 'cek_royalti.html', context)
    return response
