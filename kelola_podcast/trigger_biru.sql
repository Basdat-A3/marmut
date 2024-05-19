SET search_path to marmut;

-- Sudah dijalankan pada database

-- asumsi trigger pada fitur biru seharusnya memperbarui total_play saat lagu di play (ada data baru di tabel AKUN_PLAY_SONG)
CREATE OR REPLACE FUNCTION increment_total_play()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE SONG
    SET total_play = total_play + 1
    WHERE id_konten = NEW.id_song;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER play_song_add_trigger
AFTER INSERT ON AKUN_PLAY_SONG
FOR EACH ROW
EXECUTE FUNCTION increment_total_play();


CREATE OR REPLACE FUNCTION increment_total_download()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE SONG
    SET total_download = total_download + 1
    WHERE id_konten = NEW.id_song;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER downloaded_song_add_trigger
AFTER INSERT ON DOWNLOADED_SONG
FOR EACH ROW
EXECUTE FUNCTION increment_total_download();



CREATE OR REPLACE FUNCTION decrement_total_download()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE SONG
    SET total_download = total_download - 1
    WHERE id_konten = OLD.id_song;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER downloaded_song_delete_trigger
AFTER DELETE ON DOWNLOADED_SONG
FOR EACH ROW
EXECUTE FUNCTION decrement_total_download();