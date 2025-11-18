from fastapi import FastAPI
import sqlite3
from typing import List, Optional

app = FastAPI()

def get_db():
    conn = sqlite3.connect("kathanilayam.db")
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    return {"status": "API running locally on Mac!"}

@app.get("/story/{story_id}")
def get_story(story_id: int):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM stories WHERE story_id = ?", (story_id,)
    ).fetchone()
    return dict(row) if row else {"error": "not found"}

@app.get("/search")
def search(
    title: Optional[str] = None,
    writer: Optional[str] = None,
    magazine: Optional[str] = None
):
    conn = get_db()
    query = "SELECT * FROM stories WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")

    if writer:
        query += " AND writer LIKE ?"
        params.append(f"%{writer}%")

    if magazine:
        query += " AND magazine LIKE ?"
        params.append(f"%{magazine}%")

    rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]

