-- Task 4: Compute the average/highest/lowest score of an assignment
SELECT 
    a.assignment_name,
    ROUND(AVG(s.score), 2) AS average_score,
    MAX(s.score) AS highest_score,
    MIN(s.score) AS lowest_score
FROM assignments a
JOIN scores s ON a.assignment_id = s.assignment_id
WHERE a.assignment_name = 'Homework 1' AND a.course_id = 1;

-- Task 5: List all students in a given course
SELECT st.student_id, st.first_name, st.last_name, st.email
FROM students st
JOIN enrollments e ON st.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
WHERE c.department = 'CSCI' AND c.course_number = '340' AND c.semester = 'Spring' AND c.year = 2026
ORDER BY st.last_name, st.first_name;

-- Task 6: List all students in a course and all of their scores on every assignment
SELECT 
    st.student_id,
    st.first_name,
    st.last_name,
    a.assignment_name,
    s.score,
    a.perfect_score
FROM students st
JOIN enrollments e ON st.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
JOIN assignments a ON c.course_id = a.course_id
LEFT JOIN scores s ON s.assignment_id = a.assignment_id AND s.student_id = st.student_id
WHERE c.course_id = 1
ORDER BY st.last_name, st.first_name, a.assignment_id;

-- Task 7: Add an assignment to a course
INSERT INTO assignments (assignment_id, course_id, category_id, assignment_name, perfect_score, due_date)
VALUES (13, 1, 4, 'Project 2', 100, '2026-05-05');

-- Task 8: Change the percentages of the categories for a course
UPDATE category_weights
SET percentage = CASE category_name
    WHEN 'Participation' THEN 5
    WHEN 'Homework' THEN 25
    WHEN 'Tests' THEN 45
    WHEN 'Projects' THEN 25
END
WHERE course_id = 1;

-- Task 9: Add 2 points to the score of each student on an assignment
UPDATE scores
SET score = MIN(score + 2, 100)
WHERE assignment_id = 2;

-- Task 10: Add 2 points just to those students whose last name contains a 'Q'
UPDATE scores
SET score = MIN(score + 2, 100)
WHERE assignment_id = 3
  AND student_id IN (
      SELECT student_id
      FROM students
      WHERE last_name LIKE '%Q%' OR last_name LIKE '%q%'
  );

-- Task 11: Compute the grade for a student
WITH assignment_breakdown AS (
    SELECT 
        a.assignment_id,
        a.course_id,
        cw.category_name,
        cw.percentage,
        COUNT(*) OVER (PARTITION BY a.course_id, a.category_id) AS assignments_in_category,
        sc.student_id,
        sc.score,
        a.perfect_score
    FROM assignments a
    JOIN category_weights cw ON a.category_id = cw.category_id
    JOIN scores sc ON sc.assignment_id = a.assignment_id
    WHERE a.course_id = 1 AND sc.student_id = 1
)
SELECT 
    student_id,
    ROUND(SUM((score / perfect_score) * (percentage / assignments_in_category)), 2) AS final_grade
FROM assignment_breakdown
GROUP BY student_id;

-- Task 12: Compute the grade for a student, dropping the lowest score in each category
WITH ranked_scores AS (
    SELECT 
        a.assignment_id,
        a.course_id,
        cw.category_name,
        cw.percentage,
        sc.student_id,
        sc.score,
        a.perfect_score,
        ROW_NUMBER() OVER (
            PARTITION BY a.course_id, cw.category_name, sc.student_id
            ORDER BY (sc.score * 1.0 / a.perfect_score) ASC
        ) AS rn,
        COUNT(*) OVER (
            PARTITION BY a.course_id, cw.category_name, sc.student_id
        ) AS category_count
    FROM assignments a
    JOIN category_weights cw ON a.category_id = cw.category_id
    JOIN scores sc ON sc.assignment_id = a.assignment_id
    WHERE a.course_id = 1 AND sc.student_id = 1
),
kept_scores AS (
    SELECT *
    FROM ranked_scores
    WHERE category_count = 1 OR rn > 1
),
weighted AS (
    SELECT 
        student_id,
        category_name,
        percentage,
        COUNT(*) AS kept_assignments,
        SUM(score / perfect_score) AS sum_ratios
    FROM kept_scores
    GROUP BY student_id, category_name, percentage
)
SELECT 
    student_id,
    ROUND(SUM((sum_ratios / kept_assignments) * percentage), 2) AS final_grade_drop_lowest
FROM weighted
GROUP BY student_id;

-- Advanced Query 1: Top student in Database Systems
SELECT 
    st.student_id,
    st.first_name,
    st.last_name,
    ROUND(AVG(s.score), 2) AS average_score
FROM students st
JOIN scores s ON st.student_id = s.student_id
JOIN assignments a ON s.assignment_id = a.assignment_id
WHERE a.course_id = 1
GROUP BY st.student_id, st.first_name, st.last_name
ORDER BY average_score DESC
LIMIT 1;

-- Advanced Query 2: Students averaging at least 90 in a course
SELECT 
    st.student_id,
    st.first_name,
    st.last_name,
    ROUND(AVG(s.score), 2) AS average_score
FROM students st
JOIN scores s ON st.student_id = s.student_id
JOIN assignments a ON s.assignment_id = a.assignment_id
WHERE a.course_id = 1
GROUP BY st.student_id, st.first_name, st.last_name
HAVING AVG(s.score) >= 90
ORDER BY average_score DESC;

-- Advanced Query 3: Assignment count by category for a course
SELECT 
    cw.category_name,
    COUNT(a.assignment_id) AS assignments_in_category
FROM category_weights cw
LEFT JOIN assignments a ON cw.category_id = a.category_id
WHERE cw.course_id = 1
GROUP BY cw.category_name
ORDER BY assignments_in_category DESC, cw.category_name;

-- Validation: category percentages per course should total 100
SELECT
    c.course_id,
    c.department,
    c.course_number,
    c.semester,
    c.year,
    SUM(cw.percentage) AS total_percentage
FROM courses c
JOIN category_weights cw ON c.course_id = cw.course_id
GROUP BY c.course_id, c.department, c.course_number, c.semester, c.year;