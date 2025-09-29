import os
from fastmcp import FastMCP
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expense.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

# Create a FastMCP server instance
mcp = FastMCP(name="MCP Expense Tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
            """
        )
init_db()

@mcp.tool
def add_expense(date, amount, category, subcategory="", note=""):
    """Add a new expense entry to the database."""
    with sqlite3.connect(DB_PATH) as c:
        curr = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": curr.lastrowid}

@mcp.tool
def list_expense(start_date, end_date):
    """List all expense entries within an inclusive date range from the database."""
    with sqlite3.connect(DB_PATH) as c:
        curr = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, r)) for r in curr.fetchall()]

@mcp.tool
def summarize(start_date, end_date, category=None):
    """Summarize the expense by category within an inclusive date range from the database."""
    with sqlite3.connect(DB_PATH) as c:
        query = """
            SELECT category, SUM(amount) as total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """
        
        params = [start_date, end_date]
        if category:
            query += " AND LOWER(category) = LOWER(?)"
            params.append(category)
        
        query += " GROUP BY category ORDER BY category ASC"
        
        curr = c.execute(query, params)
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, r)) for r in curr.fetchall()]        

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the files without restarting the server
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()