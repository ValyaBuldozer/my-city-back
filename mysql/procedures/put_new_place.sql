DELIMITER //
DROP PROCEDURE IF EXISTS put_new_place;
CREATE PROCEDURE put_new_place(
	OUT result INT,
    OUT ID INT,
	name VARCHAR(200), 
    logo_path VARCHAR(400),
    image_path VARCHAR(400),
    description TEXT,
    question_title VARCHAR(400),
    address VARCHAR(400),
    lat DECIMAL(10, 8),
    lng DECIMAL(11,8))
BEGIN 
	INSERT INTO places (
        place_name, 
        place_logo_path, 
        place_image_path, 
        place_description, 
        place_question_title,
        place_address,
        place_lat,
        place_lng ) 
	VALUES (name, logo_path, image_path, description, question_title, address, lat, lng);
    
    SET ID = LAST_INSERT_ID();
    SET result = 0;
END;
//