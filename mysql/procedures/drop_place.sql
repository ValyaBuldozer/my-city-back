DELIMITER //
DROP PROCEDURE IF EXISTS drop_place;
CREATE PROCEDURE drop_place(OUT result INT, id INT)
BEGIN 
	IF ID NOT IN (SELECT place_id FROM places) THEN
		SET result = 1;
    ELSE 
		DELETE FROM places WHERE place_id = id;
		SET result = 0;
	END IF;
END;
//