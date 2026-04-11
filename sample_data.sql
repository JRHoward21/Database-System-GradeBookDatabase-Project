INSERT INTO students (student_id, first_name, last_name, email) VALUES
(1, 'David', 'Mack', 'david.mack@example.com'),
(2, 'Aisha', 'Quinn', 'aisha.quinn@example.com'),
(3, 'Marcus', 'Cole', 'marcus.cole@example.com'),
(4, 'Nia', 'Brown', 'nia.brown@example.com');

INSERT INTO courses (course_id, department, course_number, course_name, semester, year) VALUES
(1, 'CSCI', '340', 'Database Systems', 'Spring', 2026),
(2, 'CSCI', '350', 'Structure of Programming Languages', 'Spring', 2026);

INSERT INTO enrollments (enrollment_id, student_id, course_id) VALUES
(1, 1, 1), (2, 2, 1), (3, 3, 1), (4, 4, 1),
(5, 1, 2), (6, 2, 2), (7, 4, 2);

INSERT INTO category_weights (category_id, course_id, category_name, percentage) VALUES
(1, 1, 'Participation', 10),
(2, 1, 'Homework', 20),
(3, 1, 'Tests', 50),
(4, 1, 'Projects', 20),
(5, 2, 'Homework', 40),
(6, 2, 'Exams', 60);

INSERT INTO assignments (assignment_id, course_id, category_id, assignment_name, perfect_score, due_date) VALUES
(1, 1, 1, 'Participation', 100, '2026-02-01'),
(2, 1, 2, 'Homework 1', 100, '2026-02-08'),
(3, 1, 2, 'Homework 2', 100, '2026-02-15'),
(4, 1, 2, 'Homework 3', 100, '2026-02-22'),
(5, 1, 2, 'Homework 4', 100, '2026-03-01'),
(6, 1, 2, 'Homework 5', 100, '2026-03-08'),
(7, 1, 3, 'Test 1', 100, '2026-03-20'),
(8, 1, 3, 'Test 2', 100, '2026-04-10'),
(9, 1, 4, 'Project 1', 100, '2026-04-25'),
(10, 2, 5, 'HW A', 100, '2026-02-10'),
(11, 2, 5, 'HW B', 100, '2026-03-10'),
(12, 2, 6, 'Midterm', 100, '2026-03-25');

INSERT INTO scores (score_id, assignment_id, student_id, score) VALUES
(1, 1, 1, 100), (2, 1, 2, 95), (3, 1, 3, 88), (4, 1, 4, 91),
(5, 2, 1, 96), (6, 2, 2, 85), (7, 2, 3, 77), (8, 2, 4, 90),
(9, 3, 1, 92), (10, 3, 2, 88), (11, 3, 3, 80), (12, 3, 4, 93),
(13, 4, 1, 100), (14, 4, 2, 82), (15, 4, 3, 76), (16, 4, 4, 95),
(17, 5, 1, 94), (18, 5, 2, 86), (19, 5, 3, 79), (20, 5, 4, 89),
(21, 6, 1, 98), (22, 6, 2, 90), (23, 6, 3, 84), (24, 6, 4, 92),
(25, 7, 1, 87), (26, 7, 2, 75), (27, 7, 3, 81), (28, 7, 4, 88),
(29, 8, 1, 91), (30, 8, 2, 84), (31, 8, 3, 78), (32, 8, 4, 90),
(33, 9, 1, 95), (34, 9, 2, 89), (35, 9, 3, 83), (36, 9, 4, 94),
(37, 10, 1, 93), (38, 10, 2, 85), (39, 10, 4, 97),
(40, 11, 1, 90), (41, 11, 2, 88), (42, 11, 4, 96),
(43, 12, 1, 92), (44, 12, 2, 80), (45, 12, 4, 94);
