import sqlite3
from datetime import date
from pathlib import Path
from typing import Optional
import pandas as pd

DB_PATH = Path(__file__).parent / "cards.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                front    TEXT NOT NULL,
                back     TEXT NOT NULL,
                box      INTEGER NOT NULL DEFAULT 1,
                due_date TEXT NOT NULL
            )
        """)


def get_due_cards() -> list[dict]:
    today = date.today().isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM cards WHERE due_date <= ? ORDER BY due_date ASC",
            (today,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_all_cards() -> pd.DataFrame:
    with get_connection() as conn:
        df = pd.read_sql("SELECT * FROM cards ORDER BY box, due_date", conn)
    return df


def add_card(front: str, back: str, due_date: date) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO cards (front, back, box, due_date) VALUES (?, ?, 1, ?)",
            (front.strip(), back.strip(), due_date.isoformat())
        )
        return cursor.lastrowid


def add_cards_bulk(cards: list[tuple[str, str]], due_date: date):
    due_str = due_date.isoformat()
    with get_connection() as conn:
        conn.executemany(
            "INSERT INTO cards (front, back, box, due_date) VALUES (?, ?, 1, ?)",
            [(f.strip(), b.strip(), due_str) for f, b in cards]
        )


def update_card_progress(card_id: int, box: int, due_date: date):
    with get_connection() as conn:
        conn.execute(
            "UPDATE cards SET box = ?, due_date = ? WHERE id = ?",
            (box, due_date.isoformat(), card_id)
        )


def update_card(card_id: int, front: str, back: str, box: int, due_date: date):
    with get_connection() as conn:
        conn.execute(
            "UPDATE cards SET front = ?, back = ?, box = ?, due_date = ? WHERE id = ?",
            (front.strip(), back.strip(), box, due_date.isoformat(), card_id)
        )


def delete_card(card_id: int):
    with get_connection() as conn:
        conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))


def get_card(card_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
    return dict(row) if row else None
