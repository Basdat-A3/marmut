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

-- total download (kuning)
CREATE OR REPLACE FUNCTION increment_total_download()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE song
    SET total_download = total_download + 1
    WHERE id_konten = NEW.id_konten;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER increment_total_download_trigger
AFTER INSERT ON akun_play_user_playlist
FOR EACH ROW
EXECUTE FUNCTION increment_total_download();
