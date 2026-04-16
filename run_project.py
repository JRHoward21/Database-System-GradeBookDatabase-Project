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

    if rows:
        body = "\n".join(
            " | ".join(str(v).ljust(widths[i]) for i, v in enumerate(row))
            for row in rows
        )
    else:
        body = "(no rows)"

    return f"{title}\n{line}\n{sep}\n{body}\n"


def show_section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def run_and_display(
    cur: sqlite3.Cursor,
    outputs: list[str],
    title: str,
    query: str,
) -> None:
    rows = fetch_rows(cur, query)
    headers = [desc[0] for desc in cur.description]
    formatted = format_rows(title, headers, rows)
    print(formatted)
    outputs.append(formatted)


def pause() -> None:
    input("Press Enter to continue to the next task...")


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Building database...")
    execute_script(cur, SCHEMA_PATH)
    execute_script(cur, DATA_PATH)

    outputs: list[str] = []

    # Show inserted table contents first
    show_section("INSERTED TABLE CONTENTS")
    for table in ["students", "courses", "enrollments", "category_weights", "assignments", "scores"]:
        run_and_display(
            cur,
            outputs,
            f"Contents of {table}",
            f"SELECT * FROM {table};"
        )
        pause()

    # Task 4
    show_section("TASK 4: Compute average / highest / lowest score of an assignment")
    run_and_display(
        cur,
        outputs,
        "Task 4 - Avg/Highest/Lowest for Homework 1",
        """
        SELECT a.assignment_name,
               ROUND(AVG(s.score), 2) AS average_score,
               MAX(s.score) AS highest_score,
               MIN(s.score) AS lowest_score
        FROM assignments a
        JOIN scores s ON a.assignment_id = s.assignment_id
        WHERE a.assignment_name = 'Homework 1'
          AND a.course_id = 1;
        """
    )
    pause()

    # Task 5
    show_section("TASK 5: List all students in a given course")
    run_and_display(
        cur,
        outputs,
        "Task 5 - Students in CSCI 340",
        """
        SELECT st.student_id, st.first_name, st.last_name, st.email
        FROM students st
        JOIN enrollments e ON st.student_id = e.student_id
        WHERE e.course_id = 1
        ORDER BY st.last_name, st.first_name;
        """
    )
    pause()

    # Task 6
    show_section("TASK 6: List all students in a course and all of their scores on every assignment")
    run_and_display(
        cur,
        outputs,
        "Task 6 - Every student and every assignment score",
        """
        SELECT st.student_id,
               st.first_name,
               st.last_name,
               a.assignment_name,
               COALESCE(s.score, 'NULL') AS score
        FROM students st
        JOIN enrollments e ON st.student_id = e.student_id
        JOIN assignments a ON a.course_id = e.course_id
        LEFT JOIN scores s
          ON s.assignment_id = a.assignment_id
         AND s.student_id = st.student_id
        WHERE e.course_id = 1
        ORDER BY st.last_name, st.first_name, a.assignment_id;
        """
    )
    pause()

    # Task 7
    show_section("TASK 7: Add an assignment to a course")
    cur.execute("""
        INSERT INTO assignments
        (assignment_id, course_id, category_id, assignment_name, perfect_score, due_date)
        VALUES (13, 1, 4, 'Project 2', 100, '2026-05-05');
    """)
    run_and_display(
        cur,
        outputs,
        "Task 7 - Added assignment",
        """
        SELECT assignment_id, assignment_name, category_id, due_date
        FROM assignments
        WHERE assignment_id = 13;
        """
    )
    pause()

    # Task 8
    show_section("TASK 8: Change the percentages of the categories for a course")
    cur.executescript("""
        UPDATE category_weights
        SET percentage = 5
        WHERE course_id = 1 AND category_name = 'Participation';

        UPDATE category_weights
        SET percentage = 45
        WHERE course_id = 1 AND category_name = 'Tests';

        UPDATE category_weights
        SET percentage = 25
        WHERE course_id = 1 AND category_name = 'Homework';

        UPDATE category_weights
        SET percentage = 25
        WHERE course_id = 1 AND category_name = 'Projects';
    """)
    run_and_display(
        cur,
        outputs,
        "Task 8 - Updated category percentages",
        """
        SELECT category_name, percentage
        FROM category_weights
        WHERE course_id = 1
        ORDER BY category_id;
        """
    )
    pause()

    # Restore original values safely
    cur.executescript("""
        UPDATE category_weights
        SET percentage = 15
        WHERE course_id = 1 AND category_name = 'Homework';

        UPDATE category_weights
        SET percentage = 20
        WHERE course_id = 1 AND category_name = 'Tests';

        UPDATE category_weights
        SET percentage = 10
        WHERE course_id = 1 AND category_name = 'Participation';

        UPDATE category_weights
        SET percentage = 20
        WHERE course_id = 1 AND category_name = 'Homework';

        UPDATE category_weights
        SET percentage = 20
        WHERE course_id = 1 AND category_name = 'Projects';

        UPDATE category_weights
        SET percentage = 50
        WHERE course_id = 1 AND category_name = 'Tests';
    """)

    # Task 9
    show_section("TASK 9: Add 2 points to the score of each student on an assignment")
    cur.execute("""
        UPDATE scores
        SET score = MIN(score + 2, 100)
        WHERE assignment_id = 2;
    """)
    run_and_display(
        cur,
        outputs,
        "Task 9 - Homework 1 after +2 points",
        """
        SELECT student_id, score
        FROM scores
        WHERE assignment_id = 2
        ORDER BY student_id;
        """
    )
    pause()

    # Restore original Task 9 values
    cur.executescript("""
        UPDATE scores
        SET score = CASE student_id
            WHEN 1 THEN 96
            WHEN 2 THEN 85
            WHEN 3 THEN 77
            WHEN 4 THEN 90
        END
        WHERE assignment_id = 2;
    """)

    # Task 10
    show_section("TASK 10: Add 2 points just to those students whose last name contains a 'Q'")
    cur.execute("""
        UPDATE scores
        SET score = MIN(score + 2, 100)
        WHERE assignment_id = 3
          AND student_id IN (
              SELECT student_id
              FROM students
              WHERE last_name LIKE '%Q%' OR last_name LIKE '%q%'
          );
    """)
    run_and_display(
        cur,
        outputs,
        "Task 10 - Homework 2 after +2 for last name containing Q",
        """
        SELECT student_id, score
        FROM scores
        WHERE assignment_id = 3
        ORDER BY student_id;
        """
    )
    pause()

    # Restore original Task 10 values
    cur.executescript("""
        UPDATE scores
        SET score = CASE student_id
            WHEN 1 THEN 92
            WHEN 2 THEN 88
            WHEN 3 THEN 80
            WHEN 4 THEN 93
        END
        WHERE assignment_id = 3;
    """)

    # Task 11
    show_section("TASK 11: Compute the grade for a student")
    run_and_display(
        cur,
        outputs,
        "Task 11 - Final grade for student 1",
        """
        WITH assignment_breakdown AS (
            SELECT a.assignment_id,
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
        SELECT student_id,
               ROUND(SUM((score * 1.0 / perfect_score) * (percentage * 1.0 / assignments_in_category)), 2) AS final_grade
        FROM assignment_breakdown
        GROUP BY student_id;
        """
    )
    pause()

    # Task 12
    show_section("TASK 12: Compute the grade for a student, where the lowest score for a given category is dropped")
    run_and_display(
        cur,
        outputs,
        "Task 12 - Final grade for student 1 with lowest category score dropped",
        """
        WITH ranked_scores AS (
            SELECT a.assignment_id,
                   cw.category_name,
                   cw.percentage,
                   sc.student_id,
                   sc.score,
                   a.perfect_score,
                   ROW_NUMBER() OVER (
                       PARTITION BY cw.category_name, sc.student_id
                       ORDER BY (sc.score * 1.0 / a.perfect_score) ASC
                   ) AS rn,
                   COUNT(*) OVER (
                       PARTITION BY cw.category_name, sc.student_id
                   ) AS category_count
            FROM assignments a
            JOIN category_weights cw ON a.category_id = cw.category_id
            JOIN scores sc ON sc.assignment_id = a.assignment_id
            WHERE a.course_id = 1
              AND sc.student_id = 1
        ),
        kept_scores AS (
            SELECT *
            FROM ranked_scores
            WHERE category_count = 1 OR rn > 1
        ),
        category_totals AS (
            SELECT student_id,
                   category_name,
                   percentage,
                   COUNT(*) AS kept_assignments,
                   SUM(score * 1.0 / perfect_score) AS sum_ratios
            FROM kept_scores
            GROUP BY student_id, category_name, percentage
        )
        SELECT student_id,
               ROUND(SUM((sum_ratios / kept_assignments) * percentage), 2) AS final_grade_drop_lowest
        FROM category_totals
        GROUP BY student_id;
        """
    )
    pause()

    OUTPUT_PATH.write_text("\n".join(outputs), encoding="utf-8")
    conn.commit()
    conn.close()

    print(f"\nCreated {DB_PATH.name} and {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
    