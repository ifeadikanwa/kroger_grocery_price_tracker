# ui
import streamlit as st
from services import grocery_service

service = grocery_service.GroceryService()

st.set_page_config(
    page_title="Grocery Price Tracker", page_icon="🛒", layout="centered"
)

st.title("Grocery Price Tracker")

st.subheader("Add Grocery Item")

item_name = st.text_input("Item name", placeholder="milk, eggs, bread")

if st.button("Add Item"):
    if item_name.strip():
        service.add_grocery_item(item_name.strip())
        st.success(f"Added {item_name.strip()}")
        item_name = None
        st.rerun()
    else:
        st.warning("Enter an item name first.")

st.divider()

st.subheader("Your Grocery Items")

items = service.get_grocery_items()

if not items:
    st.info("No grocery items added yet.")
else:
    for item in items:
        item_id = item.item_id
        name = item.name

        col1, col2, col3 = st.columns([5, 1.4, 1.4])

        with col1:
            st.write(name)

        with col2:
            if st.button("Search", key=f"search_{item_id}", use_container_width=True):
                st.session_state["selected_item_id"] = item_id
                st.session_state["selected_item_name"] = name
                st.switch_page("pages/search.py")

        with col3:
            if st.button("Delete", key=f"delete_{item_id}", use_container_width=True):
                service.delete_grocery_item(item_id)
                st.rerun()
