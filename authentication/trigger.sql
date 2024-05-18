-- Pengecekan Email:
CREATE OR REPLACE FUNCTION check_email_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM AKUN WHERE email = NEW.email) THEN
        RAISE EXCEPTION 'Email % is already registered.', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_akun_insert
BEFORE INSERT ON AKUN
FOR EACH ROW
EXECUTE FUNCTION check_email_exists();



CREATE OR REPLACE FUNCTION check_label_email_exists()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM AKUN WHERE email = NEW.email) THEN
        RAISE EXCEPTION 'Email % is already registered.', NEW.email;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_label_insert
BEFORE INSERT ON LABEL
FOR EACH ROW
EXECUTE FUNCTION check_label_email_exists();


--Pendaftaran Pengguna Baru:

--Memeriksa status langganan Pengguna: