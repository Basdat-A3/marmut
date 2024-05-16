from django.shortcuts import render
from utils.query import *

def playlist(request):
    connection, cursor = get_database_cursor()
    
    # close connection
    cursor.close()
    connection.close()

    
    return render(request, 'playlist.html')

def playlist_detail(request):
    connection, cursor = get_database_cursor()


    # close connection
    cursor.close()
    connection.close()


    return render(request, 'playlist_detail.html')

def tambah_lagu(request):
    connection, cursor = get_database_cursor()


    # close connection
    cursor.close()
    connection.close()


    return render(request, 'tambah_lagu.html')

def tambah_playlist(request):
    connection, cursor = get_database_cursor()


    # close connection
    cursor.close()
    connection.close()


    return render(request, 'tambah_playlist.html')
