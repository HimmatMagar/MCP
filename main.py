import os
import sqlite3
from fastmcp import FastMCP

mcp = FastMCP(name="Expense Tracker")

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

def _init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                date        TEXT NOT NULL,
                amount      REAL NOT NULL,
                category    TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note        TEXT DEFAULT ''
            )  
        """)

_init_db()

@mcp.tool
def add_expenses(date, amount, category, subcategory="", note=""):
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note)
        )
        return {
            "status": 'Ok',
            "id": cur.lastrowid
        }

@mcp.tool
def list_expenses(start_date: str, end_date: str):
    """List expenses between start_date and end_date (inclusive).

    Dates must be in YYYY-MM-DD format, e.g. 2026-11-01.
    """
    with sqlite3.connect(DB_PATH) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            """
            SELECT * FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC, id DESC
            LIMIT ?
            """,
            (start_date, end_date),
        )
        return [dict(r) for r in rows]


@mcp.tool
def summarize_by_category(start_date: str, end_date: str):
    """Summarize total spending per category between start_date and end_date (inclusive).

    Dates must be in YYYY-MM-DD format, e.g. 2026-11-01.
    Returns each category with its total amount, number of expenses, and
    the grand total for the range.
    """
    with sqlite3.connect(DB_PATH) as c:
        c.row_factory = sqlite3.Row
        rows = c.execute(
            """
            SELECT category,
                   ROUND(SUM(amount), 2) AS total,
                   COUNT(*)              AS count
            FROM expenses
            WHERE date BETWEEN ? AND ?
            GROUP BY category
            ORDER BY total DESC
            """,
            (start_date, end_date),
        ).fetchall()

    categories = [dict(r) for r in rows]
    grand_total = round(sum(r["total"] for r in categories), 2)

    return {
        "start_date": start_date,
        "end_date": end_date,
        "grand_total": grand_total,
        "categories": categories,
    }


if __name__ == "__main__":
    mcp.run()