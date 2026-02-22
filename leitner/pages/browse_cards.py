# pages/browse_cards.py — Page for viewing, editing, and deleting cards
#
# Shows all cards in the database. You can filter by box number,
# edit any card's front/back/box, or delete cards you no longer want.

import streamlit as st
from data import get_all_cards, update_card, delete_card
from leitner import next_due_date
import style

# Apply the dark theme
style.inject()

st.title("Browse Cards")

# --- Filter dropdown ---
# Let the user choose "All" or a specific box number (1-5)
box_options = ["All", 1, 2, 3, 4, 5]
box_filter = st.selectbox("Filter by box", box_options)

# Fetch cards from the database based on the filter
if box_filter == "All":
    cards = get_all_cards()               # Get every card
else:
    cards = get_all_cards(box_filter=int(box_filter))  # Get cards in that box only

# If no cards match, show a message and stop
if not cards:
    st.info("No cards found.")
    st.stop()

# Show how many cards were found
st.caption(f"{len(cards)} card(s)")

# Display each card in an expandable section
for card in cards:
    # The expander header shows a summary: front / back — Box N — Due: date
    with st.expander(f"{card['front']}  /  {card['back']}  —  Box {card['box']}  —  Due: {card['due_date']}"):
        # Each card gets its own form (unique key prevents conflicts between cards)
        with st.form(key=f"edit_{card['id']}"):
            # Editable fields, pre-filled with the card's current values
            new_front = st.text_input("Front", value=card["front"], key=f"front_{card['id']}")
            new_back = st.text_input("Back", value=card["back"], key=f"back_{card['id']}")
            # Dropdown for box number, pre-selected to the card's current box
            new_box = st.selectbox("Box", [1, 2, 3, 4, 5], index=card["box"] - 1, key=f"box_{card['id']}")

            # Two buttons side by side: Save and Delete
            col1, col2 = st.columns(2)
            with col1:
                save = st.form_submit_button("Save")
            with col2:
                remove = st.form_submit_button("Delete")

            if save:
                # Recalculate due date based on the (possibly new) box number
                due = next_due_date(new_box)
                update_card(card["id"], new_front.strip(), new_back.strip(), new_box, due)
                st.success("Card updated.")
                st.rerun()  # Refresh the page to show updated data
            if remove:
                delete_card(card["id"])
                st.success("Card deleted.")
                st.rerun()  # Refresh the page to remove the deleted card