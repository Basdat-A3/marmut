from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def cek_royalti(request):
    return render(request, 'cek_royalti.html')


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
