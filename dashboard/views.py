import uuid
from django.shortcuts import redirect, render
from utils.query import get_database_cursor
from datetime import datetime, timedelta

# Create your views here.
def dashboard(request):
    return render(request, "dashboard.html")

def dashboard_label(request):
    return render(request, "dashboard_label.html")

def dashboard_artist(request):
    return render(request, "dashboard_artist.html")

def dashboard_podcaster(request):
    return render(request, "dashboard_podcaster.html")

def search(request):
    return render(request, "search.html")

def downloaded_songs(request):
    return render(request, "downloaded_songs.html")