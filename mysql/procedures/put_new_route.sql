DELIMITER //
DROP PROCEDURE IF EXISTS put_new_route;
CREATE PROCEDURE put_new_route(OUT result INT, IN name VARCHAR(200), logo_path VARCHAR(400))
BEGIN 
	INSERT INTO routes (route_name, route_logo_path) 
	VALUES (name, logo_path);
    
    SET result = 0;
END;
//