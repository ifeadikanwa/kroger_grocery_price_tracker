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

st.subheader("Your Grocery Items:")

st.divider()

items = service.get_grocery_items()

if not items:
    st.info("No grocery items added yet.")
else:
    for item in items:
        item_id = item.item_id
        name = item.name

        tracked_products = service.get_tracked_products_for_item(item_id)

        col1, col2, col3 = st.columns([5, 1.4, 1.4])

        with col1:
            if st.button(
                name.capitalize(),
                key=f"overview_{item_id}",
                type="tertiary",
            ):
                st.session_state["selected_item_id"] = item_id
                st.session_state["selected_item_name"] = name
                st.switch_page("pages/overview.py")

            if not tracked_products:
                st.caption("No tracked products yet.")
            else:
                for product in tracked_products:
                    price = product["promo_price"] or product["regular_price"]
                    price_text = f"${price:.2f}" if price is not None else "Price unavailable"

                    st.caption(
                        f"• {product['name']} — "
                        f"{product['brand'] or 'No brand'} | "
                        f"{product['size'] or 'No size'} | "
                        f"{price_text}"
                    )

        with col2:
            if st.button("Search", key=f"search_{item_id}", use_container_width=True):
                st.session_state["selected_item_id"] = item_id
                st.session_state["selected_item_name"] = name
                st.switch_page("pages/search.py")

        with col3:
            if st.button("Delete", key=f"delete_{item_id}", use_container_width=True):
                service.delete_grocery_item(item_id)
                st.rerun()

        st.divider()
