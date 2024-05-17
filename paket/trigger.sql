-- langganan paket (kuning)
CREATE OR REPLACE FUNCTION check_active_subscription() 
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM transaction
        WHERE email = NEW.email
          AND timestamp_dimulai <= NOW()
          AND timestamp_berakhir >= NOW()
    ) THEN
        RAISE EXCEPTION 'User already has an active subscription';
    ELSE
        INSERT INTO premium (email)
        VALUES (NEW.email)
        ON CONFLICT (email) DO NOTHING;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_subscription_before_insert
BEFORE INSERT ON transaction
FOR EACH ROW
EXECUTE FUNCTION check_active_subscription();

--- akun play song
CREATE OR REPLACE FUNCTION create_akun_play_song_entries()
RETURNS TRIGGER AS $$
DECLARE
    song_record RECORD;
BEGIN
    -- Loop melalui setiap lagu dalam playlist yang baru ditambahkan
    FOR song_record IN
        SELECT id_song
        FROM USER_PLAYLIST_SONGS
        WHERE id_user_playlist = NEW.id_user_playlist AND email_pembuat = NEW.email_pembuat
    LOOP
        -- Insert entri baru ke dalam tabel AKUN_PLAY_SONG
        INSERT INTO AKUN_PLAY_SONG (email_pemain, id_song, waktu)
        VALUES (NEW.email_pemain, song_record.id_song, NEW.waktu);
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Buat trigger
CREATE TRIGGER after_insert_akun_play_user_playlist
AFTER INSERT ON AKUN_PLAY_USER_PLAYLIST
FOR EACH ROW
EXECUTE FUNCTION create_akun_play_song_entries();

