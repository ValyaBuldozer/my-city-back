DELIMITER //
DROP PROCEDURE IF EXISTS register_user;
CREATE PROCEDURE register_user(
	OUT result INT,
	name VARCHAR(40),
    pass VARCHAR(40)
)
BEGIN 
	IF name IN (SELECT user_name FROM users) THEN
		SET result = 1;
	ELSE 
		INSERT INTO users (user_name, user_password)
        VALUES(name, pass);
		SET result = 0;
	END IF;
END;
//