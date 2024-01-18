-- script that creates a function SafeDiv that divides
-- (and returns) the first by the second number or
-- returns 0 if the second number is equal to 0.

DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS DECIMAL(10, 6)
DETERMINISTIC
BEGIN
    DECLARE result DECIMAL(10, 6) DEFAULT 0;

    IF b != 0 THEN
        SET result = a / b;
    END IF;

    RETURN result;
END $$

DELIMITER ;
