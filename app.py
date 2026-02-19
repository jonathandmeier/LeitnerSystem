import streamlit as st
import data
import leitner

data.init_db()

st.set_page_config(page_title="Leitner System", page_icon="🧠", layout="centered")
st.title("🧠 Leitner Flashcards")

# --- Session state init ---
if "due_cards" not in st.session_state:
    st.session_state.due_cards = data.get_due_cards()
    st.session_state.current_index = 0
    st.session_state.revealed = False


def load_session():
    st.session_state.due_cards = data.get_due_cards()
    st.session_state.current_index = 0
    st.session_state.revealed = False


def next_card():
    st.session_state.current_index += 1
    st.session_state.revealed = False


# --- Sidebar stats ---
with st.sidebar:
    st.header("📊 Session")
    total = len(st.session_state.due_cards)
    remaining = max(0, total - st.session_state.current_index)
    done = total - remaining
    st.metric("Due today", total)
    st.metric("Remaining", remaining)
    st.metric("Done this session", done)
    if st.button("🔄 Refresh cards"):
        load_session()
        st.rerun()

# --- Main study area ---
cards = st.session_state.due_cards
idx = st.session_state.current_index

if idx >= len(cards):
    st.success("🎉 No more cards due! Come back tomorrow.")
    st.balloons()
    if st.button("Reload session"):
        load_session()
        st.rerun()
else:
    card = cards[idx]
    progress = idx / len(cards) if len(cards) > 0 else 1.0
    st.progress(progress, text=f"Card {idx + 1} of {len(cards)}")

    st.markdown(f"**Box {card['box']}** · Due: {card['due_date']}")
    st.divider()

    # Front
    st.markdown("### ❓ Front")
    st.markdown(f"> {card['front']}")

    if not st.session_state.revealed:
        if st.button("👁️ Reveal answer", use_container_width=True):
            st.session_state.revealed = True
            st.rerun()
    else:
        st.markdown("### 💡 Back")
        st.markdown(f"> {card['back']}")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Correct", use_container_width=True, type="primary"):
                new_box, new_due = leitner.answer_correct(card["box"])
                data.update_card_progress(card["id"], new_box, new_due)
                next_card()
                st.rerun()
        with col2:
            if st.button("❌ Wrong", use_container_width=True):
                new_box, new_due = leitner.answer_wrong(card["box"])
                data.update_card_progress(card["id"], new_box, new_due)
                next_card()
                st.rerun()
