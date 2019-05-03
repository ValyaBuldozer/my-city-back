DELIMITER //
DROP PROCEDURE IF EXISTS get_places_info;
CREATE PROCEDURE get_places_info()
BEGIN 
	SELECT place_id, place_name, place_logo_path, place_lat, place_lng
    FROM places;
END;
//