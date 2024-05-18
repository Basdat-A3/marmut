import datetime
from django.shortcuts import render
from utils.query import *

def chart_list(request):
    connection, cursor = get_database_cursor()
    
    # close connection
    cursor.close()
    connection.close()

    
    return render(request, 'chart_list.html')

def chart_detail(request, id_chart):
    connection, cursor = get_database_cursor()
    # Get the type of chart from the chart ID
    cursor.execute("""
        SELECT tipe
        FROM CHART
        WHERE id_playlist = %s;
    """, [id_chart])
    tipe_chart = cursor.fetchone()
    
    if not tipe_chart:
        return render(request, 'chart_detail.html', {'error': 'Chart not found'})

    tipe_chart = tipe_chart[0]

    # Determine the time range
    now = datetime.datetime.now()
    if tipe_chart == 'Daily Top 20':
        start_time = now - datetime.timedelta(days=1)
    elif tipe_chart == 'Weekly Top 20':
        start_time = now - datetime.timedelta(weeks=1)
    elif tipe_chart == 'Monthly Top 20':
        start_time = now - datetime.timedelta(days=30)
    elif tipe_chart == 'Yearly Top 20':
        start_time = now - datetime.timedelta(days=365)
    else:
        return render(request, 'chart_detail.html', {'error': 'Invalid chart type'})
    
    # Clear existing songs from the chart
    cursor.execute("""
        DELETE FROM PLAYLIST_SONG
        WHERE id_playlist = %s;
    """, [id_chart])

    connection.commit()

    # Query to get the top 20 songs and their artists based on play count within the specified time range
    cursor.execute("""
        SELECT s.id_konten, k.judul, k.tanggal_rilis, k.durasi, COUNT(*) AS play_count, akun.nama AS artist_name
        FROM AKUN_PLAY_SONG aps
        JOIN SONG s ON aps.id_song = s.id_konten
        JOIN KONTEN k ON s.id_konten = k.id
        JOIN ARTIST a ON s.id_artist = a.id
        JOIN AKUN akun ON a.email_akun = akun.email
        WHERE aps.waktu >= %s
        GROUP BY s.id_konten, k.judul, k.tanggal_rilis, k.durasi, akun.nama
        ORDER BY play_count DESC, k.judul ASC
        LIMIT 20;
    """, [start_time])

    songs = cursor.fetchall()
    


    list_song = []
    for song in songs:
        id_konten = song[0]
        judul = song[1]
        tanggal_rilis = song[2]
        durasi = song[3]
        play_count = song[4]
        artist_name = song[5]

        song_duration_hours = durasi // 60
        song_duration_minutes = durasi % 60

        list_song.append({
            'id': id_konten,
            'judul': judul,
            'tanggal_rilis': tanggal_rilis,
            'durasi': durasi,
            'play_count': play_count,
            'artist_name': artist_name,
            'song_duration_hours': song_duration_hours,
            'song_duration_minutes': song_duration_minutes
        })

    context = {
        'tipe_chart': tipe_chart,
        'songs': list_song
    }

    # print(list_song)

    for song in list_song:
        id_konten = song['id']
        try:
            cursor.execute("""
                INSERT INTO playlist_song
                VALUES (%s, %s);
            """, [id_chart, id_konten])
            connection.commit()
        except Exception as e:
            print(f"Error inserting song {id_konten} into chart {id_chart}: {e}")

    # Close connection
    cursor.close()
    connection.close()

    
    return render(request, 'chart_detail.html', context)
