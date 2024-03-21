-- 5. Email validation to sent: Creates a trigger that resets the attribute valid_email only when the email has been changed

CREATE TRIGGER reset_email
BEFORE UPDATE
ON users FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN SET New.valid_email = 0;
    END IF;
END;
