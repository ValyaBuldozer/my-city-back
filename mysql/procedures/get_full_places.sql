DELIMITER //
DROP PROCEDURE IF EXISTS get_full_places;
CREATE PROCEDURE get_full_places()
BEGIN 
	SELECT place_id, place_name, place_logo_path, place_image_path, place_description, place_question_title, place_address
    FROM places;
END;
//