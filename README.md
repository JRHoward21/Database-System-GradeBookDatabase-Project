# Grade Book Database Project

This repository contains a corrected, GitHub-ready solution for the **Create a Grade Book Database** assignment. The project models students, courses, enrollments, grading categories, assignments, and scores. It includes the database schema, sample data, required SQL tasks, advanced SQL queries, a Python runner, test output, and a LaTeX ER diagram.

## What was improved

- Added stronger integrity constraints such as `NOT NULL`, `UNIQUE`, and `CHECK`
- Added a LaTeX ER diagram in `ERD.tex`
- Included advanced SQL queries using `HAVING`, aggregation, and ranking
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
├── ERD.tex
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

## How to run

```bash
python run_project.py
```

This creates:
- `gradebook.db`
- `test_results.txt`

## LaTeX ER diagram

To compile the ER diagram:

```bash
pdflatex ERD.tex
```

## GitHub commands

```bash
git init
git add .
git commit -m "Add corrected grade book database project"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```
