-- 10. Safe Divide: Creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0.
 DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT) RETURNS FLOAT
BEGIN
    IF b == 0 THEN
        RETURNS 0
    ELSE
        RETURNS a / b;
    END IF;
END; //
DELIMITER;
