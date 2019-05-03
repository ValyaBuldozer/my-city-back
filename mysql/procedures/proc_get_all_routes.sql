DELIMITER //
DROP PROCEDURE IF EXISTS get_all_routes;
CREATE PROCEDURE get_all_routes()
BEGIN 
	SELECT *
    FROM routes;
END;
//