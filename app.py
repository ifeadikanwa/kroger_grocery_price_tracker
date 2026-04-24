# ui
import streamlit as st
from services import grocery_service

service = grocery_service.GroceryService()

st.set_page_config(
    page_title="Grocery Price Tracker",
    page_icon="🛒",
    layout="centered"
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

        st.write(f"- {name}")