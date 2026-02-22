# pages/add_cards.py — Page for adding new flashcards
#
# Streamlit automatically creates sidebar navigation for files in a "pages/" folder.
# This page provides three ways to add cards:
#   1. One at a time (single card form)
#   2. Upload a CSV file with many cards
#   3. Paste multiple cards as text (front | back format)

import csv
import io
import streamlit as st
from data import add_card, add_cards_bulk
from leitner import new_card_defaults, parse_bulk_text
import style

# Apply the dark theme
style.inject()

st.title("Add Cards")

# Get default values for new cards (Box 1, due today)
box, due = new_card_defaults()

# --- Method 1: Add a single card ---
st.header("Single Card")
# st.form groups inputs together so the page only re-runs when you click "Add Card"
# (without a form, every keystroke would trigger a re-run)
with st.form("single_card", clear_on_submit=True):
    front = st.text_input("Front")   # The question side
    back = st.text_input("Back")     # The answer side
    submitted = st.form_submit_button("Add Card")
    if submitted:
        if front.strip() and back.strip():
            add_card(front.strip(), back.strip(), box, due)  # Save to database
            st.success("Card added.")
        else:
            st.warning("Both front and back are required.")

# --- Method 2: Import from a CSV file ---
st.header("Import from CSV")
st.caption("Upload a CSV with columns `front` and `back`.")
# File upload widget (only accepts .csv files)
uploaded = st.file_uploader("Choose CSV file", type=["csv"])
if uploaded is not None:
    # Read the uploaded file and decode it from bytes to a string
    text = uploaded.read().decode("utf-8")
    # csv.DictReader parses each row into a dictionary using the header row as keys
    reader = csv.DictReader(io.StringIO(text))
    cards = []
    for row in reader:
        f = row.get("front", "").strip()  # Get the 'front' column value
        b = row.get("back", "").strip()   # Get the 'back' column value
        if f and b:                        # Skip rows with missing data
            cards.append((f, b))
    if cards:
        count = add_cards_bulk(cards, box, due)  # Insert all cards at once
        st.success(f"Imported {count} cards.")
    else:
        st.warning("No valid cards found. Make sure headers are `front` and `back`.")

# --- Method 3: Paste cards as text ---
st.header("Bulk Paste")
st.caption("One card per line: `front | back`")
# Large text area for pasting multiple lines
bulk_text = st.text_area("Paste cards here", height=200, key="bulk_paste")
if st.button("Import Pasted Cards"):
    cards = parse_bulk_text(bulk_text)  # Parse the "front | back" format
    if cards:
        count = add_cards_bulk(cards, box, due)
        st.success(f"Imported {count} cards.")
    else:
        st.warning("No valid cards found. Use the format: front | back")