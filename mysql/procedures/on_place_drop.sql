DELIMITER //
DROP TRIGGER IF EXISTS on_place_drop;
CREATE TRIGGER on_place_drop AFTER DELETE ON places
FOR EACH ROW 
BEGIN
	DELETE FROM route_place WHERE place_id = OLD.place_id;
	DELETE FROM answer WHERE place_id = OLD.place_id;
END;
//