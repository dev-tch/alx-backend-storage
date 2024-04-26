--  creates a view need_meeting that lists all students that have a score under 80 (strict) and no last_meeting or more than 1 month.
CREATE VIEW need_meeting AS
SELECT students.name
FROM students
LEFT JOIN meetings ON students.id = meetings.student_id
GROUP BY students.id
HAVING MAX(meetings.date) IS NULL OR DATEDIFF(CURDATE(), MAX(meetings.date)) > 30
OR MAX(meetings.score) < 80;
