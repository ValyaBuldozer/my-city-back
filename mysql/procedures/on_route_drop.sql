DELIMITER //
DROP TRIGGER IF EXISTS on_route_drop;
CREATE TRIGGER on_route_drop AFTER DELETE ON routes
FOR EACH ROW 
BEGIN
	DELETE FROM route_place WHERE route_id = OLD.route_id;
END;
//