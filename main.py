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
def list_expenses(limit=50):
    with sqlite3.connect(DB_PATH) as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM expenses ORDER BY date DESC, id DESC LIMIT ?", (limit,)
        )]



if __name__ == "__main__":
    mcp.run()