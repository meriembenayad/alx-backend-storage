-- 7. Average score: Creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.

DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_score DECIMAL(5,2);

    -- Compute the average score
    SELECT AVG(score) INTO avg_score FROM corrections WHERE corrections.user_id = user_id;

    -- Store the average score
    UPDATE users SET average_score = avg_score WHERE id = user_id;
END; //
DELIMITER;
