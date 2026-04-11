"""Builds the SQLite database, runs the required queries, and saves test output."""
from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "gradebook.db"
SCHEMA_PATH = ROOT / "schema.sql"
DATA_PATH = ROOT / "sample_data.sql"
OUTPUT_PATH = ROOT / "test_results.txt"


def execute_script(cursor: sqlite3.Cursor, path: Path) -> None:
    cursor.executescript(path.read_text(encoding="utf-8"))


def fetch_rows(cursor: sqlite3.Cursor, query: str) -> list[tuple]:
    cursor.execute(query)
    return cursor.fetchall()


def format_rows(title: str, headers: list[str], rows: list[tuple]) -> str:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))
    line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
    sep = "-+-".join("-" * widths[i] for i in range(len(headers)))
    body = "\n".join(" | ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)) for row in rows)
    return f"{title}\n{line}\n{sep}\n{body}\n"


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    execute_script(cur, SCHEMA_PATH)
    execute_script(cur, DATA_PATH)

    outputs: list[str] = []

    # Show inserted contents
    for table in ["students", "courses", "enrollments", "category_weights", "assignments", "scores"]:
        rows = fetch_rows(cur, f"SELECT * FROM {table};")
        headers = [desc[0] for desc in cur.description]
        outputs.append(format_rows(f"Contents of {table}", headers, rows))

    # Task 4
    rows = fetch_rows(
        cur,
        """
        SELECT a.assignment_name, ROUND(AVG(s.score), 2), MAX(s.score), MIN(s.score)
        FROM assignments a
        JOIN scores s ON a.assignment_id = s.assignment_id
        WHERE a.assignment_name = 'Homework 1' AND a.course_id = 1;
        """,
    )
    outputs.append(format_rows("Task 4 - Avg/Highest/Lowest for Homework 1", [d[0] for d in cur.description], rows))

    # Task 5
    rows = fetch_rows(
        cur,
        """
        SELECT st.student_id, st.first_name, st.last_name, st.email
        FROM students st
        JOIN enrollments e ON st.student_id = e.student_id
        WHERE e.course_id = 1
        ORDER BY st.last_name, st.first_name;
        """,
    )
    outputs.append(format_rows("Task 5 - Students in CSCI 340", [d[0] for d in cur.description], rows))

    # Task 6
    rows = fetch_rows(
        cur,
        """
        SELECT st.student_id, st.first_name, st.last_name, a.assignment_name, COALESCE(s.score, 'NULL') AS score
        FROM students st
        JOIN enrollments e ON st.student_id = e.student_id
        JOIN assignments a ON a.course_id = e.course_id
        LEFT JOIN scores s ON s.assignment_id = a.assignment_id AND s.student_id = st.student_id
        WHERE e.course_id = 1
        ORDER BY st.last_name, st.first_name, a.assignment_id;
        """,
    )
    outputs.append(format_rows("Task 6 - Every student and every assignment score", [d[0] for d in cur.description], rows))

    # Task 7
    cur.execute(
        "INSERT INTO assignments (assignment_id, course_id, category_id, assignment_name, perfect_score, due_date) VALUES (13, 1, 4, 'Project 2', 100, '2026-05-05');"
    )
    rows = fetch_rows(cur, "SELECT assignment_id, assignment_name, category_id, due_date FROM assignments WHERE assignment_id = 13;")
    outputs.append(format_rows("Task 7 - Added assignment", [d[0] for d in cur.description], rows))

    # Task 8
    cur.executescript(
        """
        UPDATE category_weights
        SET percentage = CASE category_name
            WHEN 'Participation' THEN 5
            WHEN 'Homework' THEN 25
            WHEN 'Tests' THEN 45
            WHEN 'Projects' THEN 25
        END
        WHERE course_id = 1;
        """
    )
    rows = fetch_rows(cur, "SELECT category_name, percentage FROM category_weights WHERE course_id = 1 ORDER BY category_id;")
    outputs.append(format_rows("Task 8 - Updated category percentages", [d[0] for d in cur.description], rows))

    # Restore original weights for grade computations
    cur.executescript(
        """
        UPDATE category_weights
        SET percentage = CASE category_name
            WHEN 'Participation' THEN 10
            WHEN 'Homework' THEN 20
            WHEN 'Tests' THEN 50
            WHEN 'Projects' THEN 20
        END
        WHERE course_id = 1;
        """
    )

    # Task 9
    cur.execute("UPDATE scores SET score = MIN(score + 2, 100) WHERE assignment_id = 2;")
    rows = fetch_rows(cur, "SELECT student_id, score FROM scores WHERE assignment_id = 2 ORDER BY student_id;")
    outputs.append(format_rows("Task 9 - Homework 1 after +2 points", [d[0] for d in cur.description], rows))

    # restore scores for assignment 2
    cur.executescript(
        """
        UPDATE scores SET score = CASE student_id
            WHEN 1 THEN 96
            WHEN 2 THEN 85
            WHEN 3 THEN 77
            WHEN 4 THEN 90
        END
        WHERE assignment_id = 2;
        """
    )

    # Task 10
    cur.execute(
        """
        UPDATE scores
        SET score = MIN(score + 2, 100)
        WHERE assignment_id = 3
          AND student_id IN (SELECT student_id FROM students WHERE last_name LIKE '%Q%' OR last_name LIKE '%q%');
        """
    )
    rows = fetch_rows(cur, "SELECT student_id, score FROM scores WHERE assignment_id = 3 ORDER BY student_id;")
    outputs.append(format_rows("Task 10 - Homework 2 after +2 for last name containing Q", [d[0] for d in cur.description], rows))

    # restore assignment 3 scores
    cur.executescript(
        """
        UPDATE scores SET score = CASE student_id
            WHEN 1 THEN 92
            WHEN 2 THEN 88
            WHEN 3 THEN 80
            WHEN 4 THEN 93
        END
        WHERE assignment_id = 3;
        """
    )

    # Task 11
    rows = fetch_rows(
        cur,
        """
        WITH assignment_breakdown AS (
            SELECT a.assignment_id, a.course_id, cw.category_name, cw.percentage,
                   COUNT(*) OVER (PARTITION BY a.course_id, a.category_id) AS assignments_in_category,
                   sc.student_id, sc.score, a.perfect_score
            FROM assignments a
            JOIN category_weights cw ON a.category_id = cw.category_id
            JOIN scores sc ON sc.assignment_id = a.assignment_id
            WHERE a.course_id = 1 AND sc.student_id = 1
        )
        SELECT student_id,
               ROUND(SUM((score / perfect_score) * (percentage / assignments_in_category)), 2) AS final_grade
        FROM assignment_breakdown
        GROUP BY student_id;
        """,
    )
    outputs.append(format_rows("Task 11 - Final grade for student 1", [d[0] for d in cur.description], rows))

    # Task 12
    rows = fetch_rows(
        cur,
        """
        WITH ranked_scores AS (
            SELECT a.assignment_id, a.course_id, cw.category_name, cw.percentage,
                   sc.student_id, sc.score, a.perfect_score,
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
            SELECT student_id, category_name, percentage,
                   COUNT(*) AS kept_assignments,
                   SUM(score / perfect_score) AS sum_ratios
            FROM kept_scores
            GROUP BY student_id, category_name, percentage
        )
        SELECT student_id,
               ROUND(SUM((sum_ratios / kept_assignments) * percentage), 2) AS final_grade_drop_lowest
        FROM weighted
        GROUP BY student_id;
        """,
    )
    outputs.append(format_rows("Task 12 - Final grade for student 1 with lowest category score dropped", [d[0] for d in cur.description], rows))

    OUTPUT_PATH.write_text("\n".join(outputs), encoding="utf-8")
    conn.commit()
    conn.close()
    print(f"Created {DB_PATH.name} and {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
