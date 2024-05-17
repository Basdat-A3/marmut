import datetime
import uuid
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from django.shortcuts import render
from utils.query import *


def create_podcast(request):
    connection, cursor = get_database_cursor()
    isPodcaster = request.COOKIES.get('isPodcaster')

    if request.method == 'POST' and isPodcaster == 'True':
        judul = request.POST.get('judul')
        genre_list = request.POST.getlist('genre')
        email_podcaster = request.COOKIES.get('email')
        # email_podcaster = 'william.martin@countermail.com'  # Temporary email for testing
        print(email_podcaster)

        # Generate unique IDs
        id_konten = str(uuid.uuid4())
        
        # Insert into KONTEN table
        cursor.execute(
            f"INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi) VALUES ('{id_konten}', '{judul}', CURRENT_TIMESTAMP, EXTRACT(YEAR FROM CURRENT_TIMESTAMP), 0)"
        )
        
        # Insert into PODCAST table
        cursor.execute(
            f"INSERT INTO PODCAST (id_konten, email_podcaster) VALUES ('{id_konten}', '{email_podcaster}')"
        )
        
        # Insert into GENRE table
        for genre in genre_list:
            cursor.execute(
                f"INSERT INTO GENRE (id_konten, genre) VALUES ('{id_konten}', '{genre}')"
            )

        # Commit the transaction
        connection.commit()
        
        # Redirect to list podcast page
        return HttpResponseRedirect('/list-podcast/')
    
    context = {
        'genres': ['Technology', 'Education', 'Sports', 'History', 'Comedy', 'Mystery']
    }

    # close connection
    cursor.close()
    connection.close()
    
    return render(request, 'create_podcast.html', context)




def list_podcast(request):
    email_podcaster = request.COOKIES.get('email')
    isPodcaster = request.COOKIES.get('isPodcaster')

    if isPodcaster == 'True':
        connection, cursor = get_database_cursor()
        

        cursor.execute("""
        SELECT P.id_konten,  -- Select id_konten
               K.judul AS "Judul",
               COALESCE(COUNT(E.id_episode), 0) AS "Jumlah Episode",
               COALESCE(SUM(E.durasi), 0) AS "Total Durasi"
        FROM PODCAST P
        LEFT JOIN EPISODE E ON P.id_konten = E.id_konten_podcast
        LEFT JOIN KONTEN K ON P.id_konten = K.id
        JOIN PODCASTER POD ON POD.email = P.email_podcaster
        WHERE POD.email = %s
        GROUP BY P.id_konten, K.judul;
        """, [email_podcaster])

        podcasts = cursor.fetchall()
        
        podcast_data = []
        for podcast in podcasts:
            id_konten = podcast[0]  # Get the id_konten
            judul = podcast[1]
            episode_count = podcast[2]
            total_duration = podcast[3]

            podcast_data.append({
                'id_konten': id_konten,  # Add id_konten to the dictionary
                'judul': judul,
                'episode_count': episode_count,
                'total_duration': total_duration
            })
            print(id_konten)  # Optional: print id_konten for debugging

        context = {
            'podcasts': podcast_data
        }

        # close connection
        cursor.close()
        connection.close()
    
    return render(request, 'list_podcast.html', context)

def daftar_episode(request, podcast_id):
    isPodcaster = request.COOKIES.get('isPodcaster')

    if isPodcaster == 'True':
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

        # close connection
        cursor.close()
        connection.close()
    
    return render(request, 'daftar_episode.html', context)



def create_episode(request, podcast_id):
    isPodcaster = request.COOKIES.get('isPodcaster')

    if isPodcaster == 'True':
        connection, cursor = get_database_cursor()
        if request.method == 'POST':
            judul = request.POST.get('judul')
            deskripsi = request.POST.get('deskripsi')
            durasi = int(request.POST.get('durasi'))
            # tanggal_rilis = request.POST.get('tanggal_rilis')

            id_episode = str(uuid.uuid4())

            # Insert into EPISODE table
            cursor.execute(
                """
                INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """,
                [id_episode, podcast_id, judul, deskripsi, durasi]
            )
            
            # Update total duration in KONTEN table
            cursor.execute(
                """
                UPDATE KONTEN
                SET durasi = COALESCE(durasi, 0) + %s
                WHERE id = %s
                """,
                [durasi, podcast_id]
            )

            connection.commit()
            # close connection
            cursor.close()
            connection.close()        
            return HttpResponseRedirect('/daftar-episode/' + str(podcast_id) + '/')
        
        # Fetch podcast title for display purposes
        cursor.execute(
            """
            SELECT K.judul
            FROM KONTEN K
            JOIN PODCAST P ON K.id = P.id_konten
            WHERE P.id_konten = %s
            """,
            [podcast_id]
        )
        podcast = cursor.fetchone()
        
        context = {
            'podcast_id': podcast_id,
            'podcast_title': podcast[0] if podcast else 'Unknown Podcast'
        }

        # close connection
        cursor.close()
        connection.close()
    
    return render(request, 'create_episode.html', context)
