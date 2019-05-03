DELIMITER //
DROP PROCEDURE IF EXISTS put_place_route;
CREATE PROCEDURE put_place_route(
	OUT result INT,
	id_place INT,
    id_route INT
)
BEGIN 
	IF id_place NOT IN (SELECT place_id FROM places) OR id_route NOT IN (SELECT route_id FROM routes) THEN
		SET result = 1;
	ELSE 
		INSERT INTO place_route (place_id, route_id) 
		VALUES (id_route, id_route);
        SET result = 0;
	END IF;
END;
//