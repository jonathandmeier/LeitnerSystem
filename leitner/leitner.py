# leitner.py — Core Leitner system logic (no UI, no database)
#
# The Leitner system is a flashcard method using numbered "boxes".
# New cards start in Box 1. Get it right → move to the next box.
# Get it wrong → move back one box. Higher boxes are reviewed less often.

from datetime import date, timedelta

# How many days to wait before reviewing a card in each box.
# Box 1 = every day, Box 2 = every 3 days, ..., Box 5 = every 30 days.
BOX_INTERVALS = {
    1: 1,
    2: 3,
    3: 7,
    4: 14,
    5: 30,
}

MAX_BOX = 5  # Highest box a card can reach (well-known cards)
MIN_BOX = 1  # Lowest box (cards you're still learning)


def next_due_date(box: int, from_date: date | None = None) -> date:
    """Calculate when a card in the given box should next be reviewed."""
    if from_date is None:
        from_date = date.today()
    # Look up how many days to wait for this box (default 1 if unknown)
    days = BOX_INTERVALS.get(box, 1)
    # Return today's date + that many days
    return from_date + timedelta(days=days)


def answer_correct(box: int) -> tuple[int, date]:
    """Called when the user gets a card right.
    Promotes the card to the next box (max 5), and sets its next due date."""
    new_box = min(box + 1, MAX_BOX)  # Move up one box, but don't exceed 5
    due = next_due_date(new_box)      # Schedule review based on new box
    return new_box, due


def answer_wrong(box: int) -> tuple[int, date]:
    """Called when the user gets a card wrong.
    Demotes the card one box (min 1), and schedules it for tomorrow."""
    new_box = max(box - 1, MIN_BOX)       # Move down one box, but don't go below 1
    due = date.today() + timedelta(days=1) # Always review wrong cards tomorrow
    return new_box, due


def new_card_defaults() -> tuple[int, date]:
    """Returns the default box and due date for a brand-new card.
    New cards go to Box 1 and are due immediately (today)."""
    return MIN_BOX, date.today()


def parse_bulk_text(text: str) -> list[tuple[str, str]]:
    """Parse multi-line text into flashcard pairs.
    Expected format: one card per line, front and back separated by '|'.
    Example:
        hello | hej
        goodbye | farvel
    Returns a list of (front, back) tuples.
    """
    cards = []
    for line in text.strip().splitlines():
        if "|" not in line:       # Skip lines without a separator
            continue
        parts = line.split("|", 1) # Split on the first '|' only
        front = parts[0].strip()   # Text before '|' = front of card
        back = parts[1].strip()    # Text after '|' = back of card
        if front and back:         # Only add if both sides have text
            cards.append((front, back))
    return cards