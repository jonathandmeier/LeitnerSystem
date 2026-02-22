# app.py — Main study page (the flashcard review session)
#
# This is the entry point of the app. Run it with:
#   streamlit run leitner/app.py
#
# How Streamlit works:
#   - Every time you click a button, Streamlit re-runs this ENTIRE script from top to bottom.
#   - To keep data between re-runs, we use st.session_state (a persistent dictionary).
#   - st.rerun() forces an immediate re-run (used after updating state).

import streamlit as st
from data import init_db, get_due_cards, update_card_review
from leitner import answer_correct, answer_wrong
import style

# Configure the browser tab title and page layout (must be the first st.* call)
st.set_page_config(page_title="Leitner Flashcards", layout="centered")

# Create the database table if it doesn't exist yet
init_db()

# Apply the custom dark theme CSS
style.inject()

# Page heading
st.title("Study")


def load_session():
    """Load all due cards into session_state and reset the review position.
    Called once at the start, or when the user clicks 'Refresh'.
    """
    st.session_state.cards = get_due_cards()  # Fetch cards due today from the DB
    st.session_state.index = 0                # Start at the first card
    st.session_state.reveal = False           # Don't show the answer yet


# Only load cards on the very first run (not on every re-run)
if "cards" not in st.session_state:
    load_session()

# Grab the current cards list and position from session state
cards = st.session_state.cards
idx = st.session_state.index

# If we've gone through all cards (or there are none), show a "done" message
if idx >= len(cards):
    st.info("No cards due today.")
    if st.button("Refresh"):
        load_session()
        st.rerun()
    st.stop()  # Stop executing the rest of the script

# Get the current card and show a progress bar
card = cards[idx]
total = len(cards)
st.progress(idx / total, text=f"Card {idx + 1} of {total}")

# Convert **bold** markdown to HTML <b> tags for the front text
front_html = card["front"].replace("**", "<b>", 1).replace("**", "</b>", 1)

# --- State: answer is HIDDEN ---
if not st.session_state.reveal:
    # Show only the front of the card
    st.markdown(
        f'<div class="card-panel"><p class="card-front">{front_html}</p></div>',
        unsafe_allow_html=True,
    )
    # "Show Answer" button — when clicked, reveal the back
    if st.button("Show Answer", use_container_width=True):
        st.session_state.reveal = True
        st.rerun()

# --- State: answer is REVEALED ---
else:
    # Show both front and back of the card, plus which box it's in
    st.markdown(
        f'<div class="card-panel">'
        f'<p class="card-front">{front_html}</p>'
        f'<p class="card-back">{card["back"]}</p>'
        f'<p class="card-meta">Box {card["box"]}</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Two buttons side by side: Correct and Wrong
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Correct", use_container_width=True):
            # User got it right → promote to next box, schedule later review
            new_box, due = answer_correct(card["box"])
            update_card_review(card["id"], new_box, due)
            st.session_state.index += 1    # Move to the next card
            st.session_state.reveal = False # Hide answer for the next card
            st.rerun()
    with col2:
        if st.button("Wrong", use_container_width=True):
            # User got it wrong → demote one box, review again tomorrow
            new_box, due = answer_wrong(card["box"])
            update_card_review(card["id"], new_box, due)
            st.session_state.index += 1
            st.session_state.reveal = False
            st.rerun()

# Small hint at the bottom showing keyboard shortcuts
st.markdown(
    '<p class="shortcut-hint">Space — show answer &nbsp;&nbsp; '
    'Left arrow — wrong &nbsp;&nbsp; Right arrow — correct</p>',
    unsafe_allow_html=True,
)

# JavaScript that listens for keyboard presses and clicks the matching button.
# This lets you use the keyboard instead of clicking buttons with the mouse.
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    // Don't intercept keys if the user is typing in an input field
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    // Find all buttons on the page and map them by their text
    const buttons = document.querySelectorAll('button[kind="secondary"], .stButton button');
    const buttonTexts = Array.from(buttons).map(b => ({el: b, text: b.textContent.trim()}));

    if (e.code === 'Space') {
        e.preventDefault();  // Prevent page from scrolling
        const show = buttonTexts.find(b => b.text === 'Show Answer');
        if (show) show.el.click();  // Simulate clicking "Show Answer"
    } else if (e.code === 'ArrowRight') {
        e.preventDefault();
        const correct = buttonTexts.find(b => b.text === 'Correct');
        if (correct) correct.el.click();  // Simulate clicking "Correct"
    } else if (e.code === 'ArrowLeft') {
        e.preventDefault();
        const wrong = buttonTexts.find(b => b.text === 'Wrong');
        if (wrong) wrong.el.click();  // Simulate clicking "Wrong"
    }
});
</script>
""", unsafe_allow_html=True)