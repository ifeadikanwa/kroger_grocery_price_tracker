import streamlit as st

item_id = st.session_state.get("selected_item_id")
item_name = st.session_state.get("selected_item_name")

if not item_id or not item_name:
    st.error("No grocery item selected.")
    st.stop()

st.title(f"{item_name.capitalize()} Overview")

st.info("Overview page coming soon.")