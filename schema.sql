PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS category_weights;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE CHECK (instr(email, '@') > 1)
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    department TEXT NOT NULL,
    course_number TEXT NOT NULL,
    course_name TEXT NOT NULL,
    semester TEXT NOT NULL,
    year INTEGER NOT NULL CHECK (year >= 2000),
    UNIQUE(department, course_number, semester, year)
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE(student_id, course_id)
);

CREATE TABLE category_weights (
    category_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    category_name TEXT NOT NULL,
    percentage REAL NOT NULL CHECK (percentage >= 0 AND percentage <= 100),
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE(course_id, category_name)
);

CREATE TABLE assignments (
    assignment_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    assignment_name TEXT NOT NULL,
    perfect_score REAL NOT NULL CHECK (perfect_score > 0),
    due_date TEXT CHECK (due_date IS NULL OR length(due_date) = 10),
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category_weights(category_id) ON DELETE CASCADE,
    UNIQUE(course_id, assignment_name)
);

CREATE TABLE scores (
    score_id INTEGER PRIMARY KEY,
    assignment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    score REAL NOT NULL CHECK (score >= 0 AND score <= 100),
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    UNIQUE(assignment_id, student_id)
);
