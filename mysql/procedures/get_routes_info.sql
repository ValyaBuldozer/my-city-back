DELIMITER //
DROP PROCEDURE IF EXISTS get_routes_info;
CREATE PROCEDURE get_routes_info()
BEGIN 
	SELECT route_id, route_name, route_logo_path
    FROM routes;
END;
//