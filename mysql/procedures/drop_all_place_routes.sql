DELIMITER //
DROP PROCEDURE IF EXISTS drop_all_place_routes;
CREATE PROCEDURE drop_all_place_routes(
	OUT result INT,
	id_place INT
)
BEGIN 
	IF id_place NOT IN (SELECT place_id FROM places) THEN
		SET result = 1;
	ELSE 
		DELETE FROM route_place WHERE place_id = id_place;
        SET result = 0;
	END IF;
END;
//