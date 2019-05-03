DELIMITER //
DROP PROCEDURE IF EXISTS get_routes_by_place;
CREATE PROCEDURE get_routes_by_place(IN target_place_id INT)
BEGIN 
	SELECT route_id, route_name, route_logo_path
    FROM routes NATURAL JOIN route_place
    WHERE place_id = target_place_id;
END;
//