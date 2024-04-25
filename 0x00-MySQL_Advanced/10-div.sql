-- creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0
DELIMITER $$
CREATE FUNCTION SafeDiv (IN a INT, IN b INT) RETURNS FLOAT
BEGIN
    DECLARE res_div FLOAT; 
    IF b = 0 THEN
        SET res_div = 0;
    ELSE
        SET res_div = a / b;
    END IF;  
    RETURN res_div;
END;
$$
DELIMITER ;
