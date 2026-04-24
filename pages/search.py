import streamlit as st
from services.grocery_service import GroceryService

service = GroceryService()

# get grocery item from query params
item_id = st.session_state.get("selected_item_id")
item_name = st.session_state.get("selected_item_name")

if not item_id or not item_name:
    st.error("No grocery item selected.")
    st.stop()

st.title(f"Search Products: {item_name.capitalize()}")

st.subheader("Tracking:")
st.info("Tracked products will show here later.")

st.divider()


more_query = st.text_input("Add more search terms", value="", placeholder="optional")


search_clicked = st.button(label="Search")

search_query = f"{item_name} {more_query}".strip()

st.subheader(f"Search Results for: {search_query.capitalize()}")

if search_clicked:
    products = service.search_products(query=search_query)

    if not products:
        st.warning("No products found.")
    else:
        for product in products:
            st.write(
                f"**{product.name}** | "
                f"{product.brand or 'No brand'} | "
                f"{product.size or 'No size'}"
            )
else:
    st.info("Click Search to find Kroger products.")
