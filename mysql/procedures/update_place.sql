DELIMITER //
DROP PROCEDURE IF EXISTS update_place;
CREATE PROCEDURE update_place(
	OUT result INT,
    id INT,
	name VARCHAR(200), 
    logo_path VARCHAR(400),
    image_path VARCHAR(400),
    description TEXT,
    question_title VARCHAR(400),
    address VARCHAR(400)
)
BEGIN 
	IF id NOT IN (SELECT place_id FROM places) THEN
		SET result = 1;
	ELSE 
		UPDATE places 
        SET
			place_name = name, 
			place_logo_path = logo_path, 
			place_image_path = image_path, 
			place_description = description, 
			place_question_title = question_title,
			place_address = address
		WHERE place_id = id;
		
		SET result = 0;
	END IF;
END;
//