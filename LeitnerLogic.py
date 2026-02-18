import pandas as pd
from datetime import datetime, timedelta
import random

sheet = "250_most_frequent_german_words_danish.xlsx"

def reset_cards(df):
    now = datetime.today().replace(microsecond=0)
    df["Box"] = 1
    df["Last Review"] = now
    df["Next Review"] = now
    return df

def move_card_right(df, card_id):
    if df.at[card_id, "Box"] < 5:
        df.at[card_id, "Box"] += 1
    update_review_dates(df, card_id)
    return df

def move_card_left(df, card_id):
    if df.at[card_id, "Box"] > 1:
        df.at[card_id, "Box"] -= 1
    update_review_dates(df, card_id)
    return df

def calculate_next_review(box, now=None):
    if now is None:
        now = datetime.today().replace(microsecond=0)
    if box == 1:
        return now + timedelta(days=1)
    elif box == 2:
        return now + timedelta(days=2)
    elif box == 3:
        return now + timedelta(weeks=1)
    elif box == 4:
        return now + timedelta(weeks=2)
    elif box == 5:
        return now + timedelta(weeks=4)
    else:
        return now

def update_review_dates(df, card_id, now=None):
    if now is None:
        now = datetime.today().replace(microsecond=0)
    df.at[card_id, "Last Review"] = now
    current_box = df.at[card_id, "Box"]
    df.at[card_id, "Next Review"] = calculate_next_review(current_box, now)
    return df

def get_due_cards(df, now=None):
    if now is None:
        now = datetime.today().replace(microsecond=0)
    due_cards = df[
        (df["Next Review"].isna()) |
        (df["Next Review"] <= now)
    ]
    return due_cards

def pick_random_due_card(df, now=None):
    due_cards = get_due_cards(df, now)
    if due_cards.empty:
        return None, None
    idx = random.choice(due_cards.index.tolist())
    card = df.loc[idx]
    return idx, card

def load_data(sheet=sheet):
    df = pd.read_excel(sheet)
    df["Last Review"] = pd.to_datetime(df["Last Review"], errors="coerce")
    df["Next Review"] = pd.to_datetime(df["Next Review"], errors="coerce")
    return df

def save_data(df, sheet=sheet):
    df.to_excel(sheet, index=False)

