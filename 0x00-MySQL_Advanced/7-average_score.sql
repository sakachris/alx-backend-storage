-- script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE total_score DECIMAL(10, 2);
    DECLARE total_projects INT;

    SELECT SUM(score), COUNT(DISTINCT project_id)
    INTO total_score, total_projects
    FROM corrections
    WHERE corrections.user_id = user_id;

    UPDATE users
    SET users.average_score = IFNULL(total_score / total_projects, 0)
    WHERE users.id = user_id;
END $$

DELIMITER ;
