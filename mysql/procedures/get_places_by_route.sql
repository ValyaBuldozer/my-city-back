DELIMITER //
DROP PROCEDURE IF EXISTS get_places_by_route;
CREATE PROCEDURE get_places_by_route(IN target_route_id INT)
BEGIN 
	SELECT place_id, place_name, place_logo_path, place_lat, place_lng
    FROM route_place NATURAL JOIN places
    WHERE route_id = target_route_id;
END;
//