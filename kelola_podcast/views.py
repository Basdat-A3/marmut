from django.shortcuts import render

def create_podcast(request):
    return render(request, 'create_podcast.html')

def list_podcast(request):
    return render(request, 'list_podcast.html')

def create_episode(request):
    return render(request, 'create_episode.html')

def daftar_episode(request):
    return render(request, 'daftar_episode.html')

def daftar_episode_sebuah_podcast(request):
    return render(request, 'daftar_episode_sebuah_podcast.html')
