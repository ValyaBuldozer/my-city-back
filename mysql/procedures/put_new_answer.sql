DELIMITER //
DROP PROCEDURE IF EXISTS put_new_answer;
CREATE PROCEDURE put_new_answer(
	OUT result INT,
    OUT ID INT,
	ans_place_id INT,
    title VARCHAR(200),
    is_right TINYINT(1),
    description TEXT
)
BEGIN
	IF ans_place_id NOT IN (SELECT place_id FROM places) THEN 
		SET result = 1;
    ELSE 
		SET result = 0;
		INSERT INTO answer (
			place_id,
			answer_title,
			answer_is_right,
			answer_description) 
		VALUES (ans_place_id, title, is_right, description);
        
		SET ID = LAST_INSERT_ID();
	END IF;
END;
//