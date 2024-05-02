from django.shortcuts import render


def play_podcast(request):
    return render(request, 'play_podcast.html')
