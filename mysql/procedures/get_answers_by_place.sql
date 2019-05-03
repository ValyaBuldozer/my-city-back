DELIMITER //
DROP PROCEDURE IF EXISTS get_answers_by_place;
CREATE PROCEDURE get_answers_by_place(IN target_place_id INT)
BEGIN 
	SELECT *
    FROM answer
    WHERE place_id = target_place_id;
END;
//