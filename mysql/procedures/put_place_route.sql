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
		INSERT INTO route_place (route_id, place_id) 
		VALUES (id_route, id_place);
        SET result = 0;
	END IF;
END;
//