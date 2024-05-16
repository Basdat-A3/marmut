from django.shortcuts import render

from django.shortcuts import render
from utils.query import *


def create_podcast(request):
    return render(request, 'create_podcast.html')

def list_podcast(request):
    # belom difilter berdasarkan logged in podcaster
    connection, cursor = get_database_cursor()
    cursor.execute("""
        SELECT K.judul AS "Judul",
                COALESCE(COUNT(E.id_episode), 0) AS "Jumlah Episode",
                COALESCE(SUM(E.durasi), 0) AS "Total Durasi"
        FROM PODCAST P
        LEFT JOIN EPISODE E ON P.id_konten = E.id_konten_podcast
        LEFT JOIN KONTEN K ON P.id_konten = K.id
        GROUP BY K.judul;
    """)
    podcasts = cursor.fetchall()
    
    podcast_data = []
    for podcast in podcasts:
        judul = podcast[0]
        episode_count = podcast[1]
        total_duration = podcast[2]

        podcast_data.append({
            'judul': judul,
            'episode_count': episode_count,
            'total_duration': total_duration
        })

    context = {
        'podcasts': podcast_data
    }
    
    return render(request, 'list_podcast.html', context)

def daftar_episode(request, podcast_id):
    connection, cursor = get_database_cursor()
    cursor.execute("""
        SELECT E.id_episode,
                E.judul AS "Judul Episode",
                E.deskripsi AS "Deskripsi",
                E.durasi AS "Durasi",
                E.tanggal_rilis AS "Tanggal"
        FROM EPISODE E
        JOIN PODCAST P ON E.id_konten_podcast = P.id_konten
        JOIN KONTEN K ON P.id_konten = K.id
        WHERE K.id = %s;
    """, [podcast_id])
    episodes = cursor.fetchall()
    
    episode_data = []
    for episode in episodes:
        episode_id = episode[0]
        judul_episode = episode[1]
        deskripsi = episode[2]
        durasi = episode[3]
        tanggal_rilis = episode[4]

        episode_data.append({
            'episode_id': episode_id,
            'judul_episode': judul_episode,
            'deskripsi': deskripsi,
            'durasi': durasi,
            'tanggal_rilis': tanggal_rilis
        })

    context = {
        'episodes': episode_data
    }
    
    return render(request, 'daftar_episode.html', context)

def create_episode(request):
    return render(request, 'create_episode.html')
