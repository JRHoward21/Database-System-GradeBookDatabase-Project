# Grade Book Database Project

This repository contains a corrected, GitHub-ready solution for the **Create a Grade Book Database** assignment. The project models students, courses, enrollments, grading categories, assignments, and scores. It includes the database schema, sample data, required SQL tasks, a Python runner, test output, and an ER diagram.

## What was improved

- Added stronger integrity constraints such as `NOT NULL`, `UNIQUE`, and `CHECK`
- Added an ER diagram in `ERD.md` and `ERD.pdf`
- Included the SQL commands for Tasks 4-12
- Kept a larger sample dataset so the queries are more meaningful
- Regenerated test output after corrections

## Project structure

```text
gradebook-database-project/
├── README.md
├── schema.sql
├── sample_data.sql
├── queries.sql
├── run_project.py
├── ERD.md
├── ERD.pdf
├── gradebook.db
└── test_results.txt
```

## Entity overview

- **students**: one row per student
- **courses**: one row per course offering
- **enrollments**: bridge table between students and courses
- **category_weights**: grading categories and percentages for each course
- **assignments**: individual graded items belonging to a course and category
- **scores**: each student's score on each assignment

## Key design choices

1. `enrollments` resolves the many-to-many relationship between students and courses.
2. `category_weights` stores course-specific grading categories.
3. `assignments` belongs to both a course and a grading category.
4. `scores` stores one score per student per assignment.
5. Constraints help protect data quality.

## Assignment Coverage
- The ER diagram with attributes, primary keys, and foreign keys
- The commands for creating tables and inserting values
- The tables with the contents that were inserted
- The SQL commands used for Tasks 4-12
- The source code
- A README with instructions to run the project
- The test cases and results in `test_results.txt`


## How to run

```bash
python run_project.py
```

This creates:
- `gradebook.db`
- `test_results.txt`

## Files for submission
- `schema.sql` - Table creation commands
- `sample_data.sql` - insert statements for sample data
- `queries.sql` - SQL commands for Tasks 4-12
- `run_project.py` - source code used to execute and test the project
- `ERD.md` / `ERD.pdf` - ER diagram
- `test_results.txt` - inserted table contents and query results

## Notes
- Each grading category percentage is stored in `category_weights`.
- Assignment grades are weighted by category percentage and the number of assignments in that category.
- Task 12 computes a student's grade after dropping the lowest score in each category.