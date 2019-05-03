DELIMITER //
DROP PROCEDURE IF EXISTS put_new_route;
CREATE PROCEDURE put_new_route(OUT result INT, IN name VARCHAR(200), logo_path VARCHAR(400), description TEXT)
BEGIN 
	INSERT INTO routes (route_name, route_logo_path, route_description) 
	VALUES (name, logo_path, description);
    
    SET result = 0;
END;
//