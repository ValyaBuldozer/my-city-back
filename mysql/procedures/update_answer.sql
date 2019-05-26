DELIMITER //
DROP PROCEDURE IF EXISTS update_answer;
CREATE PROCEDURE update_answer(
	OUT result INT,
    INOUT id int,
    IN ans_place_id INT,
    IN title VARCHAR(200),
    IN is_right TINYINT(1),
    IN description TEXT
)
BEGIN 
	IF id IN (SELECT answer_id FROM answer) THEN
		UPDATE answer 
        SET place_id = ans_place_id, answer_title = title, answer_is_right = is_right, answer_description = description
        WHERE answer_id = id;
        SET result = 0;
    ELSE 
		INSERT INTO answer (place_id, answer_title, answer_is_right, answer_description)
        VALUES (ans_place_id, title, is_right, description);
        SET id = LAST_INSERT_ID();
        SET result = 0;
    END IF;
END
//