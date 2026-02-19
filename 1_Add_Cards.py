import streamlit as st
import pandas as pd
import data
import leitner

st.set_page_config(page_title="Add Cards", page_icon="➕", layout="centered")
st.title("➕ Add Cards")

tab1, tab2, tab3 = st.tabs(["Single Card", "CSV Upload", "Bulk Paste"])

# --- Single card ---
with tab1:
    with st.form("single_card_form"):
        front = st.text_area("Front", placeholder="Question or word...")
        back = st.text_area("Back", placeholder="Answer or translation...")
        submitted = st.form_submit_button("Add Card", type="primary")
        if submitted:
            if front.strip() and back.strip():
                data.add_card(front, back, leitner.initial_due_date())
                st.success("Card added!")
            else:
                st.error("Both front and back are required.")

# --- CSV upload ---
with tab2:
    st.markdown("Upload a CSV with two columns: `front` and `back`. All cards start in Box 1, due today.")
    uploaded = st.file_uploader("Choose CSV file", type="csv")
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            if "front" not in df.columns or "back" not in df.columns:
                st.error("CSV must have columns named `front` and `back`.")
            else:
                df = df.dropna(subset=["front", "back"])
                st.dataframe(df[["front", "back"]], use_container_width=True)
                if st.button(f"Import {len(df)} cards", type="primary"):
                    cards = list(zip(df["front"].astype(str), df["back"].astype(str)))
                    data.add_cards_bulk(cards, leitner.initial_due_date())
                    st.success(f"✅ Imported {len(df)} cards!")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

# --- Bulk paste ---
with tab3:
    st.markdown("One card per line in `front | back` format.")
    st.code("What is the capital of France? | Paris\nHello in Spanish | Hola")
    pasted = st.text_area("Paste cards here", height=200)
    if st.button("Import pasted cards", type="primary"):
        lines = [l.strip() for l in pasted.strip().splitlines() if l.strip()]
        cards = []
        errors = []
        for i, line in enumerate(lines, 1):
            parts = line.split("|", 1)
            if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
                errors.append(f"Line {i}: `{line}`")
            else:
                cards.append((parts[0].strip(), parts[1].strip()))

        if errors:
            st.warning(f"Skipped {len(errors)} invalid lines:")
            for e in errors:
                st.text(e)

        if cards:
            data.add_cards_bulk(cards, leitner.initial_due_date())
            st.success(f"✅ Imported {len(cards)} cards!")
        elif not errors:
            st.error("Nothing to import.")
