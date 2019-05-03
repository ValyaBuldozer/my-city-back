DELIMITER //
DROP PROCEDURE IF EXISTS drop_route;
CREATE PROCEDURE drop_route(OUT result INT, id INT)
BEGIN 
	IF ID NOT IN (SELECT route_id FROM routes) THEN
		SET result = 1;
    ELSE 
		DELETE FROM routes WHERE route_id = ID;
        DELETE FROM route_place WHERE route_id = ID;
		SET result = 0;
	END IF;
END;
//