
CREATE OR REPLACE FUNCTION update_podcast_duration_after_insert()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE KONTEN
    SET durasi = (
        SELECT COALESCE(SUM(durasi), 0)
        FROM EPISODE
        WHERE id_konten_podcast = NEW.id_konten_podcast
    )
    WHERE id = NEW.id_konten_podcast;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_podcast_duration_after_insert
AFTER INSERT ON EPISODE
FOR EACH ROW
EXECUTE FUNCTION update_podcast_duration_after_insert();

CREATE OR REPLACE FUNCTION update_podcast_duration_after_delete()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE KONTEN
    SET durasi = (
        SELECT COALESCE(SUM(durasi), 0)
        FROM EPISODE
        WHERE id_konten_podcast = OLD.id_konten_podcast
    )
    WHERE id = OLD.id_konten_podcast;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_update_podcast_duration_after_delete
AFTER DELETE ON EPISODE
FOR EACH ROW
EXECUTE FUNCTION update_podcast_duration_after_delete();


CREATE OR REPLACE FUNCTION update_album_after_insert_song()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE ALBUM
    SET total_durasi = (
        SELECT COALESCE(SUM(KONTEN.durasi), 0)
        FROM SONG
        JOIN KONTEN ON SONG.id_konten = KONTEN.id
        WHERE SONG.id_album = NEW.id_album
    ),
    jumlah_lagu = (
        SELECT COUNT(*)
        FROM SONG
        WHERE SONG.id_album = NEW.id_album
    )
    WHERE id = NEW.id_album;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_update_album_after_insert_song
AFTER INSERT ON SONG
FOR EACH ROW
EXECUTE FUNCTION update_album_after_insert_song();


CREATE OR REPLACE FUNCTION update_album_after_delete_song()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE ALBUM
    SET total_durasi = (
        SELECT COALESCE(SUM(KONTEN.durasi), 0)
        FROM SONG
        JOIN KONTEN ON SONG.id_konten = KONTEN.id
        WHERE SONG.id_album = OLD.id_album
    ),
    jumlah_lagu = (
        SELECT COUNT(*)
        FROM SONG
        WHERE SONG.id_album = OLD.id_album
    )
    WHERE id = OLD.id_album;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_update_album_after_delete_song
AFTER DELETE ON SONG
FOR EACH ROW
EXECUTE FUNCTION update_album_after_delete_song();
