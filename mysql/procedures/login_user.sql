DELIMITER //
DROP PROCEDURE IF EXISTS login_user;
CREATE PROCEDURE login_user(
	OUT result INT,
	name VARCHAR(40),
    pass VARCHAR(40)
)
BEGIN 
	IF NOT exists(SELECT user_name, user_password FROM users WHERE name = user_name) THEN
		SET result = 1;
	ELSE 
		IF NOT EXISTS(SELECT user_name, user_password FROM users WHERE name = user_name and pass = user_password) THEN
			SET result = 2;
		ELSE 
			SET result = 0;
		END IF;
	END IF;
END;
//