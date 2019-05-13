DELIMITER //
DROP PROCEDURE IF EXISTS update_route;
CREATE PROCEDURE update_route(OUT result INT, id INT, title VARCHAR(200), logo_path VARCHAR(400))
BEGIN 
	IF id NOT IN (SELECT route_id FROM routes) THEN
		SET result = 1;
    ELSE 
		UPDATE routes
        SET route_name = title, route_logo_path = logo_path
        WHERE route_id = id;
        
        SET result = 0;
	END IF;
END;
//