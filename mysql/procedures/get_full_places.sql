DELIMITER //
DROP PROCEDURE IF EXISTS get_full_places;
CREATE PROCEDURE get_full_places()
BEGIN 
	SELECT * FROM places;
END;
//