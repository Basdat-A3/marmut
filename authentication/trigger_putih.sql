SET search_path to marmut;
-- Membuat Function untuk cek email
CREATE OR REPLACE FUNCTION cek_email_terdaftar(email_input VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    email_count INT;
BEGIN
    -- Mengecek apakah email sudah ada di tabel AKUN
    SELECT COUNT(*) INTO email_count
    FROM AKUN
    WHERE email = email_input;

    IF email_count > 0 THEN
        RETURN TRUE;
    END IF;

    -- Mengecek apakah email sudah ada di tabel LABEL
    SELECT COUNT(*) INTO email_count
    FROM LABEL
    WHERE email = email_input;

    IF email_count > 0 THEN
        RETURN TRUE;
    END IF;

    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Membuat Trigger Function untuk AKUN
CREATE OR REPLACE FUNCTION trigger_cek_email_akun()
RETURNS TRIGGER AS $$
BEGIN
    IF cek_email_terdaftar(NEW.email) THEN
        RAISE EXCEPTION 'Email sudah terdaftar di tabel AKUN atau LABEL';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Membuat Trigger Function untuk LABEL
CREATE OR REPLACE FUNCTION trigger_cek_email_label()
RETURNS TRIGGER AS $$
BEGIN
    IF cek_email_terdaftar(NEW.email) THEN
        RAISE EXCEPTION 'Email sudah terdaftar di tabel AKUN atau LABEL';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Membuat Trigger untuk AKUN
CREATE TRIGGER sebelum_insert_akun
BEFORE INSERT ON AKUN
FOR EACH ROW
EXECUTE FUNCTION trigger_cek_email_akun();

-- Membuat Trigger untuk LABEL
CREATE TRIGGER sebelum_insert_label
BEFORE INSERT ON LABEL
FOR EACH ROW
EXECUTE FUNCTION trigger_cek_email_label();

SET search_path to marmut;
-- Membuat Function untuk Insert ke NONPREMIUM
CREATE OR REPLACE FUNCTION insert_ke_nonpremium()
RETURNS TRIGGER AS $$
BEGIN
    -- Menyisipkan email baru ke tabel NONPREMIUM
    INSERT INTO NONPREMIUM (email)
    VALUES (NEW.email);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Membuat Trigger untuk AKUN
CREATE TRIGGER setelah_insert_akun
AFTER INSERT ON AKUN
FOR EACH ROW
EXECUTE FUNCTION insert_ke_nonpremium();

SET search_path to marmut;
CREATE OR REPLACE FUNCTION cek_dan_pindahkan_email(email_input VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    email_should_be_moved BOOLEAN := FALSE;
BEGIN
    -- Mengecek apakah semua transaksi dengan email tersebut sudah berakhir
    IF NOT EXISTS (
        SELECT 1
        FROM TRANSACTION
        WHERE email = email_input
        AND timestamp_berakhir >= CURRENT_TIMESTAMP
    ) THEN
        -- Jika tidak ada transaksi yang masih berlaku, hapus dari tabel premium
        DELETE FROM premium WHERE email = email_input;

        -- Tambahkan email ke tabel nonpremium
        INSERT INTO nonpremium (email)
        VALUES (email_input)
        ON CONFLICT (email) DO NOTHING;

        email_should_be_moved := TRUE;
    END IF;
    RETURN email_should_be_moved;
END;
$$ LANGUAGE plpgsql;

