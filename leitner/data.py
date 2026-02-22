# data.py — Database layer (SQLite)
#
# This file handles all database operations: creating the table,
# adding/reading/updating/deleting cards. The rest of the app
# calls these functions instead of writing SQL directly.

import sqlite3
from datetime import date
from pathlib import Path

# The database file lives next to this Python file (in the leitner/ folder)
DB_PATH = Path(__file__).parent / "cards.db"


def _connect() -> sqlite3.Connection:
    """Create and return a connection to the SQLite database.
    - detect_types: lets SQLite automatically convert DATE columns to Python date objects
    - row_factory: makes rows behave like dicts (access columns by name, not index)
    """
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the 'cards' table if it doesn't already exist.
    Called once when the app starts. Safe to call multiple times.
    Columns:
      - id: unique auto-incrementing identifier
      - front: the question/prompt side of the flashcard
      - back: the answer side of the flashcard
      - box: which Leitner box the card is in (1-5)
      - due_date: when this card should next be reviewed
    """
    conn = _connect()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            front TEXT NOT NULL,
            back TEXT NOT NULL,
            box INTEGER NOT NULL DEFAULT 1,
            due_date DATE NOT NULL
        )
    """)
    conn.commit()  # Save the change to disk
    conn.close()   # Always close the connection when done


def add_card(front: str, back: str, box: int, due_date: date) -> None:
    """Insert a single new flashcard into the database."""
    conn = _connect()
    # The '?' placeholders prevent SQL injection (never put values directly in the SQL string)
    conn.execute(
        "INSERT INTO cards (front, back, box, due_date) VALUES (?, ?, ?, ?)",
        (front, back, box, due_date),
    )
    conn.commit()
    conn.close()


def add_cards_bulk(cards: list[tuple[str, str]], box: int, due_date: date) -> int:
    """Insert many cards at once (more efficient than calling add_card in a loop).
    'cards' is a list of (front, back) tuples.
    Returns the number of cards inserted.
    """
    conn = _connect()
    # executemany runs the same INSERT for each item in the list
    conn.executemany(
        "INSERT INTO cards (front, back, box, due_date) VALUES (?, ?, ?, ?)",
        [(front, back, box, due_date) for front, back in cards],
    )
    conn.commit()
    conn.close()
    return len(cards)


def get_due_cards(today: date | None = None) -> list[dict]:
    """Get all cards that are due for review (due_date <= today).
    Returns them sorted by box (lowest first) then by id.
    This means you review the hardest cards (low box) first.
    """
    if today is None:
        today = date.today()
    conn = _connect()
    rows = conn.execute(
        "SELECT id, front, back, box, due_date FROM cards WHERE due_date <= ? ORDER BY box, id",
        (today,),
    ).fetchall()  # fetchall() loads all matching rows into memory
    conn.close()
    return [dict(r) for r in rows]  # Convert Row objects to plain dicts


def get_all_cards(box_filter: int | None = None) -> list[dict]:
    """Get all cards, optionally filtered to a specific box number.
    Used by the Browse page to display the full card collection.
    """
    conn = _connect()
    if box_filter is not None:
        # Only return cards in the specified box
        rows = conn.execute(
            "SELECT id, front, back, box, due_date FROM cards WHERE box = ? ORDER BY id",
            (box_filter,),
        ).fetchall()
    else:
        # Return all cards
        rows = conn.execute(
            "SELECT id, front, back, box, due_date FROM cards ORDER BY id"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_card(card_id: int, front: str, back: str, box: int, due_date: date) -> None:
    """Update all fields of an existing card (used when editing from the Browse page)."""
    conn = _connect()
    conn.execute(
        "UPDATE cards SET front = ?, back = ?, box = ?, due_date = ? WHERE id = ?",
        (front, back, box, due_date, card_id),
    )
    conn.commit()
    conn.close()


def update_card_review(card_id: int, box: int, due_date: date) -> None:
    """Update only the box and due_date after a review (used during study sessions).
    Unlike update_card(), this doesn't change the front/back text.
    """
    conn = _connect()
    conn.execute(
        "UPDATE cards SET box = ?, due_date = ? WHERE id = ?",
        (box, due_date, card_id),
    )
    conn.commit()
    conn.close()


def delete_card(card_id: int) -> None:
    """Permanently remove a card from the database."""
    conn = _connect()
    conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()