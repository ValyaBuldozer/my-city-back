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
    address VARCHAR(400))
BEGIN 
	INSERT INTO places (
        place_name, 
        place_logo_path, 
        place_image_path, 
        place_description, 
        place_question_title,
        place_address ) 
	VALUES (name, logo_path, image_path, description, question_title, address);
    
    SET ID = LAST_INSERT_ID();
    SET result = 0;
END;
//