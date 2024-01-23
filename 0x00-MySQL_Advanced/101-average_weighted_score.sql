-- script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Fetch the user_id from the cursor
    repeat_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE repeat_loop;
        END IF;

        -- Calculate and update the average weighted score for each user
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END $$

DELIMITER ;
