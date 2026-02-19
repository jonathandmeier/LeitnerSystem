import streamlit as st
from datetime import date
import data

st.set_page_config(page_title="Browse Cards", page_icon="📚", layout="wide")
st.title("📚 Browse Cards")

df = data.get_all_cards()

if df.empty:
    st.info("No cards yet. Go to **Add Cards** to get started.")
    st.stop()

# --- Filters ---
col1, col2 = st.columns([1, 3])
with col1:
    box_filter = st.selectbox("Filter by box", ["All"] + [1, 2, 3, 4, 5])

filtered = df if box_filter == "All" else df[df["box"] == box_filter]
st.caption(f"Showing {len(filtered)} of {len(df)} cards")

# --- Card table with edit/delete ---
for _, row in filtered.iterrows():
    card_id = int(row["id"])
    with st.expander(f"**{row['front']}** · Box {row['box']} · Due {row['due_date']}"):
        with st.form(f"edit_{card_id}"):
            new_front = st.text_area("Front", value=row["front"], key=f"front_{card_id}")
            new_back = st.text_area("Back", value=row["back"], key=f"back_{card_id}")
            col_box, col_due = st.columns(2)
            with col_box:
                new_box = st.selectbox("Box", [1, 2, 3, 4, 5],
                                       index=int(row["box"]) - 1,
                                       key=f"box_{card_id}")
            with col_due:
                new_due = st.date_input("Due date",
                                        value=date.fromisoformat(row["due_date"]),
                                        key=f"due_{card_id}")

            col_save, col_delete = st.columns([3, 1])
            with col_save:
                if st.form_submit_button("💾 Save changes", type="primary", use_container_width=True):
                    data.update_card(card_id, new_front, new_back, new_box, new_due)
                    st.success("Saved!")
                    st.rerun()
            with col_delete:
                if st.form_submit_button("🗑️ Delete", use_container_width=True):
                    data.delete_card(card_id)
                    st.rerun()
