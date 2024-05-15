from django.shortcuts import render
from utils.query import *
#
#
# durasi episode belom diformat
#
#durasi episode belom diformat
#
#
#
def play_podcast(request, podcast_id):
    connection, cursor = get_database_cursor()
    cursor.execute("""
        SELECT K.judul AS "Judul",
            array_agg(G.genre) AS "Genre",
            AKUN.nama AS "Podcaster",
            COALESCE(EP.total_durasi, 0) AS "Total Durasi",
            K.tanggal_rilis AS "Tanggal Rilis",
            K.tahun AS "Tahun"
        FROM KONTEN K
        LEFT JOIN PODCAST P ON K.id = P.id_konten
        LEFT JOIN GENRE G ON K.id = G.id_konten
        LEFT JOIN AKUN ON P.email_podcaster = AKUN.email
        LEFT JOIN (
            SELECT id_konten_podcast, SUM(durasi) AS total_durasi
            FROM EPISODE
            GROUP BY id_konten_podcast
        ) AS EP ON P.id_konten = EP.id_konten_podcast
        WHERE K.id = %s
        GROUP BY K.judul, AKUN.nama, K.tanggal_rilis, K.tahun, EP.total_durasi;
    """, [podcast_id])
    podcast_detail = cursor.fetchone()

    # Get episodes for the specified podcast ID
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
        # durasi episode belom dibeenrin
        episode_data.append({
            'id': episode_id,
            'judul': judul_episode,
            'deskripsi': deskripsi,
            'durasi': durasi,
            'tanggal_rilis': tanggal_rilis
        })
    
    total_duration_minutes = podcast_detail[3]
    total_hours = total_duration_minutes // 60
    total_minutes = total_duration_minutes % 60

    print(total_duration_minutes)

    context = {
        'podcast_detail': {
            'judul': podcast_detail[0],
            'genre': podcast_detail[1],
            'podcaster': podcast_detail[2],
            'total_durasi_hours': total_hours,
            'total_durasi_minutes': total_minutes,
            'tanggal_rilis': podcast_detail[4],
            'tahun': podcast_detail[5],
        },
        'episodes': episode_data
    }

    return render(request, 'play_podcast.html', context)
#
# durasi episode belom diformat
#
# durasi episode belom diformat
#