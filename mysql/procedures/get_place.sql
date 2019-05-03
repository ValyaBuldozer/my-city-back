DELIMITER //
DROP PROCEDURE IF EXISTS get_place;
CREATE PROCEDURE get_place(IN target_place_id INT)
BEGIN 
	SELECT place_id, place_name, place_logo_path, place_image_path, place_description
		, place_question_title, place_address, place_lat, place_lng
    FROM places
    WHERE place_id = target_place_id;
END;
//