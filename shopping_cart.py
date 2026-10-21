import streamlit as st

st.set_page_config(
    page_title="Shopping Cart",
    page_icon="🛒",
    layout="wide"
)

# Product dictionary: product name -> price
products = {
    "Laptop": 55000,
    "Mobile": 25000,
    "Headphones": 2000,
    "Keyboard": 1500,
    "Mouse": 800,
    "Smart Watch": 3500
}

# Create cart in session state
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "purchase_message" not in st.session_state:
    st.session_state.purchase_message = ""

st.title("🛒 Shopping Cart")
st.write("Choose products, add them to your cart, and purchase them.")

page = st.sidebar.radio(
    "Menu",
    ["🛍️ Products", "🛒 My Cart"]
)

# -------------------- PRODUCTS PAGE --------------------
if page == "🛍️ Products":
    st.header("🛍️ Available Products")
    st.session_state.purchase_message = ""

    for product_name, price in products.items():
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.subheader(product_name)

            with col2:
                st.write(f"**Price: ₹{price:,}**")

            with col3:
                if st.button(
                    "➕ Add to Cart",
                    key=f"add_{product_name}",
                    use_container_width=True
                ):
                    if product_name in st.session_state.cart:
                        st.session_state.cart[product_name]["quantity"] += 1
                    else:
                        st.session_state.cart[product_name] = {
                            "price": price,
                            "quantity": 1
                        }

                    st.success(f"{product_name} added to cart!")
                    st.rerun()

    item_count = sum(
        item["quantity"] for item in st.session_state.cart.values()
    )
    st.info(f"Items in cart: {item_count}")

# -------------------- CART PAGE --------------------
elif page == "🛒 My Cart":
    st.header("🛒 Your Cart")

    if st.session_state.purchase_message:
        st.success(st.session_state.purchase_message)

    if not st.session_state.cart:
        st.info("Your cart is empty. Please add some products first.")
    else:
        total = 0

        for product_name in list(st.session_state.cart.keys()):
            item = st.session_state.cart[product_name]
            price = item["price"]
            quantity = item["quantity"]
            subtotal = price * quantity
            total += subtotal

            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

                with col1:
                    st.subheader(product_name)
                    st.write(f"₹{price:,} each")

                with col2:
                    st.write(f"**Quantity: {quantity}**")

                with col3:
                    st.write(f"**Subtotal: ₹{subtotal:,}**")

                with col4:
                    if st.button(
                        "➖ Remove",
                        key=f"remove_{product_name}",
                        use_container_width=True
                    ):
                        del st.session_state.cart[product_name]
                        st.rerun()

        st.divider()
        st.subheader(f"💰 Total Amount: ₹{total:,}")

        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

        if st.button(
            "💳 Purchase Now",
            type="primary",
            use_container_width=True
        ):
            if st.session_state.cart:
                purchased_items = len(st.session_state.cart)
                st.session_state.cart = {}
                st.session_state.purchase_message = (
                    f"Purchase successful! You purchased {purchased_items} "
                    f"product type(s). Thank you for shopping!"
                )
                st.rerun()
