import streamlit as st
from services.grocery_service import GroceryService

service = GroceryService()

# get grocery item from query params
item_id = st.session_state.get("selected_item_id")
item_name = st.session_state.get("selected_item_name")

if not item_id or not item_name:
    st.error("No grocery item selected.")
    st.stop()
    
if "search_results" not in st.session_state:
    st.session_state["search_results"] = []

if "last_query" not in st.session_state:
    st.session_state["last_query"] = None

if st.session_state["last_query"] is None:
    initial_query = item_name
    st.session_state["search_results"] = service.search_products(query=initial_query)
    st.session_state["last_query"] = initial_query


st.title(f"Search Products: {item_name.capitalize()}")

st.subheader("Tracked Products:")

tracked_products = service.get_tracked_products_for_item(int(item_id))

tracked_product_ids = {
    p["product_id"] for p in tracked_products
}

if not tracked_products:
    st.info("No products tracked yet.")
else:
    for product in tracked_products:
        col1, col2 = st.columns([5, 1])

        with col1:
            price = product["promo_price"] or product["regular_price"]
            price_text = f"${price:.2f}" if price is not None else "Price unavailable"

            st.write(
                f"**{product['name']}**  \n"
                f"{product['brand'] or 'No brand'} | "
                f"{product['size'] or 'No size'} | "
                f"{price_text}"
            )

        with col2:
            if st.button(
                "Remove",
                key=f"remove_{product['tracked_product_id']}",
                use_container_width=True,
            ):
                service.remove_tracked_product(product["tracked_product_id"])
                st.rerun()
        
        st.divider()



st.subheader(f'Search Results for "{st.session_state["last_query"].capitalize()}"')

more_query = st.text_input("Add more search terms", placeholder="optional")

search_query = f"{item_name} {more_query}".strip()

if st.button("Search"):
    st.session_state["search_results"] = service.search_products(query=search_query)
    st.session_state["last_query"] = search_query

products = st.session_state["search_results"]

if not products:
    st.info("Click Search to find Kroger products.")
else:
    for product in products:
        
        display_price = product.promo_price or product.regular_price

        if display_price is not None:
            price_text = f"${display_price:.2f}"
        else:
            price_text = "Price unavailable"
    
        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(
                f"**{product.name}**  \n"
                f"{product.brand or 'No brand'} | {product.size or 'No size'} | {price_text}"
            )

        with col2:
            if product.product_id in tracked_product_ids:
                st.button(
                    "Tracked",
                    key=f"tracked_{product.product_id}",
                    disabled=True,
                    use_container_width=True,
                )
            else:
                if st.button(
                    "Track",
                    key=f"track_{product.product_id}",
                    use_container_width=True,
                ):
                    service.track_product(
                        item_id=int(item_id),
                        product=product,
                    )
                    st.success(f"Now tracking {product.name}")
                    st.rerun()

        st.divider()

