
import streamlit as st
import pandas as pd
import plotly.express as px
from modules.order_operations import get_all_orders
from modules.feedback_operations import add_feedback, get_all_feedback
from services.customer_segmentation import get_customer_churn_risk
from modules.user_operations import authenticate_user
from services.dashboard_service import (
    get_dashboard_statistics,
    get_customers_by_city
)
from services.customer_segmentation import (
    get_rfm_customer_segments,
    get_customer_purchase_summary
)
from modules.feedback_operations import (
    add_feedback,
    get_all_feedback,
    bulk_import_feedback
)
from services.dashboard_service import (
    get_dashboard_statistics,
    get_customers_by_city,
    get_registration_trend
)
from modules.customer_operation import (
    get_all_customers,
    add_customer,
    bulk_import_customers,
    archive_customer,
    get_archived_customers,
    restore_customer
)
from modules.order_operations import (
    create_order,
    get_all_orders,
    update_order_status
)

from modules.customer_operation import get_all_customers
from modules.customer_operation import (
    get_all_customers,
    add_customer
)
from modules.order_operations import create_order
from modules.product_operations import get_all_products
# Page configuration
st.set_page_config(
    page_title="Customer360 CRM",
    page_icon="👥",
    layout="wide"
)
from modules.order_operations import (
    create_order,
    get_all_orders,
    update_order_status,
    get_order_details
)
from modules.order_operations import (
    create_order,
    get_all_orders,
    update_order_status,
    get_order_details,
    get_customer_orders
)

# Sidebar

# Initialize login session
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# Login Page
if not st.session_state.authenticated:

    st.title("Customer360 CRM")
    st.subheader("Login to Your Account")

    with st.form("login_form"):

        username = st.text_input(
            "Username or Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

        if login_button:

            if not username or not password:
                st.warning("Please enter username and password.")

            else:
                user = authenticate_user(username, password)

                if user:

                    st.session_state.authenticated = True
                    st.session_state.current_user = user

                    st.success("Login successful!")
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

    st.stop()
st.sidebar.write(
    f"Welcome, {st.session_state.current_user['username']}!"
)

if st.sidebar.button("Logout", use_container_width=True):

    st.session_state.authenticated = False
    st.session_state.current_user = None

    st.rerun()
st.sidebar.title("Customer360")
st.sidebar.caption("Customer Relationship Management")

menu = st.sidebar.selectbox(
    "Select a Module",
    [
        "Dashboard",
        "Customer Management",
        "Orders",
        "Feedback",
        "Analytics"
    ]
)

if menu == "Dashboard":

    st.title("CRM Dashboard")
    st.write("Overview of your customer database")

    stats = get_dashboard_statistics()

    if stats:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Customers", stats["total_customers"])

        with col2:
            st.metric("Active Customers", int(stats["active_customers"] or 0))

        with col3:
            st.metric("Inactive Customers", int(stats["inactive_customers"] or 0))

    else:
        st.error("Unable to load dashboard statistics.")

    # City distribution chart
    st.divider()

    st.subheader("Customer Distribution by City")

    city_data = get_customers_by_city()

    if city_data:

        df_city = pd.DataFrame(city_data)

        fig = px.bar(
            df_city,
            x="city",
            y="customer_count",
            title="Number of Customers by City",
            text="customer_count",
            color="city"
        )

        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Number of Customers",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No city data available.")
    
    # Customer registration trend
    st.divider()

    st.subheader("Customer Registration Trend")

    trend_data = get_registration_trend()

    if trend_data:

        df_trend = pd.DataFrame(trend_data)

        fig_trend = px.line(
            df_trend,
            x="registration_month",
            y="customer_count",
            title="Monthly Customer Registrations",
            markers=True,
            text="customer_count"
        )

        fig_trend.update_layout(
            xaxis_title="Registration Month",
            yaxis_title="Number of Customers"
        )

        st.plotly_chart(fig_trend, use_container_width=True)

    else:
        st.info("No registration trend data available.")
    

elif menu == "Customer Management":

    st.title("Customer Management")

    st.write("View and manage your customer records.")
    
    # Add New Customer
    with st.expander("➕ Add New Customer"):

        st.subheader("Customer Registration")

        with st.form("add_customer_form"):

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("Customer Name")
                email = st.text_input("Email Address")
                phone = st.text_input("Phone Number")

            with col2:
                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female", "Other"]
                )

                city = st.text_input("City")

                registration_date = st.date_input(
                    "Registration Date"
                )

            submitted = st.form_submit_button(
                "Register Customer"
            )

            if submitted:

                success = add_customer(
                    name,
                    email,
                    phone,
                    gender,
                    city,
                    registration_date
                )

                if success:
                    st.success("Customer registered successfully!")
                    st.rerun()

                else:
                    st.error(
                        "Customer registration failed. "
                        "Please check the input details."
                    )


    customers = get_all_customers()
    
    # Bulk Customer Import
    with st.expander("📁 Bulk Import Customers"):

        st.subheader("Upload Customer Records")

        uploaded_file = st.file_uploader(
            "Choose an Excel or CSV file",
            type=["xlsx", "csv"],
            key="customer_bulk_upload"
        )

        if uploaded_file is not None:

            try:
                if uploaded_file.name.endswith(".xlsx"):
                    df_import = pd.read_excel(uploaded_file)
                else:
                    df_import = pd.read_csv(uploaded_file)

                required_columns = [
                    "customer_name",
                    "email",
                    "phone",
                    "gender",
                    "city",
                    "registration_date"
                ]

                missing_columns = [
                    col for col in required_columns
                    if col not in df_import.columns
                ]

                if missing_columns:
                    st.error(
                        f"Missing columns: {', '.join(missing_columns)}"
                    )

                else:
                    df_import = df_import[required_columns]

                    # Remove completely empty rows
                    df_import = df_import.dropna(how="all")

                    # Convert blank cells to empty strings
                    df_import = df_import.astype(object).where(
                        pd.notna(df_import), ""
                    )

                    st.write("File Preview")
                    st.dataframe(
                        df_import,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.write("Total Records:", len(df_import))

                    if st.button(
                        "Import Customers",
                        key="bulk_import_button"
                    ):

                        records = df_import.to_dict(
                            orient="records"
                        )

                        report = bulk_import_customers(records)

                        st.success(
                            f"Successfully imported: {report['imported']}"
                        )

                        if report["failed"] > 0:
                            st.warning(
                                f"Failed records: {report['failed']}"
                            )

                            st.write("Import Errors:")

                            for error in report["errors"]:
                                st.error(error)

                        

            except Exception as e:
                st.error(f"Unable to read the uploaded file: {e}")


    if customers:

        df_customers = pd.DataFrame(customers)

        # Search
        st.subheader("Search Customers")

        search_value = st.text_input(
            "Search by Name, Email or City",
            placeholder="Enter customer name, email or city"
        )

        # Filters
        col1, col2 = st.columns(2)

        with col1:
            city_options = ["All"] + sorted(
                df_customers["city"].dropna().unique().tolist()
            )

            selected_city = st.selectbox(
                "Filter by City",
                city_options
            )

        with col2:
            status_options = ["All"] + sorted(
                df_customers["status"].dropna().unique().tolist()
            )

            selected_status = st.selectbox(
                "Filter by Status",
                status_options
            )

        # Apply search
        filtered_df = df_customers.copy()

        if search_value:
            mask = (
                filtered_df["customer_name"].str.contains(
                    search_value, case=False, na=False
                )
                | filtered_df["email"].str.contains(
                    search_value, case=False, na=False
                )
                | filtered_df["city"].str.contains(
                    search_value, case=False, na=False
                )
            )

            filtered_df = filtered_df[mask]

        # Apply city filter
        if selected_city != "All":
            filtered_df = filtered_df[
                filtered_df["city"] == selected_city
            ]

        # Apply status filter
        if selected_status != "All":
            filtered_df = filtered_df[
                filtered_df["status"] == selected_status
            ]

        st.divider()

        st.subheader("Customer Records")

        st.write("Matching Records:", len(filtered_df))

        display_columns = [
            "customer_id",
            "customer_name",
            "email",
            "phone",
            "gender",
            "city",
            "registration_date",
            "status"
        ]

        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True
        )
                # Delete Customer
        st.divider()

        st.subheader("Delete Customer")

        customer_options = {
            f"{customer['customer_id']} - {customer['customer_name']}":
            customer['customer_id']
            for customer in customers
        }

        selected_customer = st.selectbox(
            "Select Customer to Delete",
            options=list(customer_options.keys()),
            key="delete_customer_select"
        )

        customer_id = customer_options[selected_customer]

        confirm_delete = st.checkbox(
            "I confirm that I want to archive this customer.",
            key="confirm_customer_delete"
        )

        if st.button("Delete Customer", type="primary"):

            if confirm_delete:

                success = archive_customer(customer_id)

                if success:
                    st.success("Customer archived successfully!")
                    st.rerun()

                else:
                    st.error("Unable to archive customer.")

            else:
                st.warning("Please confirm before deleting.")
    else:
        st.info("No customers found.")
        # Archived Customers Management
    st.divider()

    with st.expander("Archived Customers"):

        st.subheader("Archived Customer Records")

        archived_customers = get_archived_customers()

        if archived_customers:

            df_archived = pd.DataFrame(archived_customers)

            st.write("Archived Records:", len(df_archived))

            st.dataframe(
                df_archived,
                use_container_width=True,
                hide_index=True
            )

            archived_options = {
                f"{customer['customer_id']} - {customer['customer_name']}":
                customer['customer_id']
                for customer in archived_customers
            }

            selected_archived = st.selectbox(
                "Select Customer to Restore",
                options=list(archived_options.keys()),
                key="restore_customer_select"
            )

            restore_id = archived_options[selected_archived]

            if st.button("Restore Customer", key="restore_customer_button"):

                success = restore_customer(restore_id)

                if success:
                    st.success("Customer restored successfully!")
                    st.rerun()

                else:
                    st.error("Unable to restore customer.")

        else:
            st.info("No archived customers available.")
    st.divider()

    st.subheader("Customer Purchase History")

    active_customers = get_all_customers()

    if active_customers:

        customer_options = {
            f"{customer['customer_name']} (ID: {customer['customer_id']})":
            customer['customer_id']
            for customer in active_customers
        }

        selected_customer = st.selectbox(
            "Select Customer",
            list(customer_options.keys()),
            key="purchase_history_customer"
        )

        selected_customer_id = customer_options[selected_customer]

        customer_orders = get_customer_orders(selected_customer_id)

        if customer_orders:

            total_orders = len(customer_orders)

            total_spent = sum(
                float(order["total_amount"])
                for order in customer_orders
            )

            last_order_date = customer_orders[0]["order_date"]

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Orders", total_orders)

            col2.metric(
                "Total Amount Spent",
                f"₹{total_spent:,.2f}"
            )

            col3.metric(
                "Last Order Date",
                str(last_order_date)
            )

            st.write("**Purchase History**")

            for order in customer_orders:

                with st.expander(
                    f"Order #{order['order_id']} | "
                    f"₹{float(order['total_amount']):,.2f} | "
                    f"{order['order_date']}"
                ):

                    st.write(
                        "Payment Status:",
                        order["payment_status"]
                    )

                    st.write(
                        "Order Status:",
                        order["order_status"]
                    )

                    order_details = get_order_details(
                        order["order_id"]
                    )

                    if order_details:

                        details_df = pd.DataFrame(order_details)

                        details_df["price"] = details_df["price"].apply(
                            lambda x: f"₹{float(x):,.2f}"
                        )

                        details_df["subtotal"] = details_df["subtotal"].apply(
                            lambda x: f"₹{float(x):,.2f}"
                        )

                        st.dataframe(
                            details_df[
                                ["product_name", "quantity", "price", "subtotal"]
                            ],
                            use_container_width=True,
                            hide_index=True
                        )

        else:
            st.info("This customer has not placed any orders yet.")

    else:
        st.info("No active customers available.")

elif menu == "Orders":
    

    st.title("Order Management")

    st.subheader("Create New Order")

    customers = get_all_customers()
    products = get_all_products()

    if not customers:
        st.warning("No active customers available.")

    elif not products:
        st.warning("No products available.")

    else:

        customer_options = {
            f"{customer['customer_name']} (ID: {customer['customer_id']})":
            customer['customer_id']
            for customer in customers
        }

        product_options = {
            f"{product['product_name']} (₹{product['price']})":
            product['product_id']
            for product in products
        }

        with st.form("create_order_form"):

            st.write("**Customer Details**")

            selected_customer = st.selectbox(
                "Select Customer",
                list(customer_options.keys())
            )

            order_date = st.date_input("Order Date")

            st.divider()

            st.write("**Select Products**")

            selected_products = st.multiselect(
                "Choose Products",
                list(product_options.keys())
            )

            quantities = {}

            for product in selected_products:

                quantities[product] = st.number_input(
                    f"Quantity - {product}",
                    min_value=1,
                    value=1,
                    step=1
                )

            st.divider()

            payment_status = st.selectbox(
                "Payment Status",
                ["Pending", "Paid", "Failed", "Refunded"]
            )

            order_status = st.selectbox(
                "Order Status",
                ["Processing", "Shipped", "Delivered", "Cancelled"]
            )

            submitted = st.form_submit_button(
                "Create Order",
                use_container_width=True
            )

            if submitted:

                if not selected_products:
                    st.error("Please select at least one product.")

                else:

                    order_items = []

                    for product in selected_products:

                        order_items.append({
                            "product_id": product_options[product],
                            "quantity": quantities[product]
                        })

                    result = create_order(
                        customer_id=customer_options[selected_customer],
                        order_date=order_date,
                        order_items=order_items,
                        payment_status=payment_status,
                        order_status=order_status
                    )

                    if result:
                        st.success(
                            f"Order created successfully! Order ID: {result}"
                        )
                    else:
                        st.error("Unable to create order.")
    st.divider()

    st.subheader("Order History")

    orders = get_all_orders()

    if orders:

        orders_df = pd.DataFrame(orders)

        # Format date and amount for display
        orders_df["order_date"] = orders_df["order_date"].astype(str)

        orders_df["total_amount"] = orders_df["total_amount"].apply(
            lambda amount: f"₹{float(amount):,.2f}"
        )

        st.dataframe(
            orders_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Total Orders: {len(orders_df)}")

    else:
        st.info("No orders have been created yet.")
    st.divider()

    st.subheader("Edit Order")

    orders = get_all_orders()

    if orders:

        order_options = {
            f"Order #{order['order_id']} - {order['customer_name']} - ₹{float(order['total_amount']):,.2f}":
            order
            for order in orders
        }

        selected_order_label = st.selectbox(
            "Select Order to Edit",
            list(order_options.keys())
        )

        selected_order = order_options[selected_order_label]

        st.write("**Current Order Details**")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Order ID:", selected_order["order_id"])
            st.write("Customer:", selected_order["customer_name"])

        with col2:
            st.write("Payment:", selected_order["payment_status"])
            st.write("Order Status:", selected_order["order_status"])

        payment_options = [
            "Pending", "Paid", "Failed", "Refunded"
        ]

        order_status_options = [
            "Processing", "Shipped", "Delivered", "Cancelled"
        ]

        with st.form("edit_order_form"):

            new_payment_status = st.selectbox(
                "Update Payment Status",
                payment_options,
                index=payment_options.index(
                    selected_order["payment_status"]
                )
            )

            new_order_status = st.selectbox(
                "Update Order Status",
                order_status_options,
                index=order_status_options.index(
                    selected_order["order_status"]
                )
            )

            update_button = st.form_submit_button(
                "Save Changes",
                use_container_width=True
            )

            if update_button:

                result = update_order_status(
                    order_id=selected_order["order_id"],
                    payment_status=new_payment_status,
                    order_status=new_order_status
                )

                if result:
                    st.success("Order updated successfully!")
                    st.rerun()

                else:
                    st.error("Unable to update order.")

    else:
        st.info("No orders available to edit.")
    st.divider()

    st.subheader("View Order Details")

    orders = get_all_orders()

    if orders:

        order_options = {
            f"Order #{order['order_id']} - {order['customer_name']}":
            order['order_id']
            for order in orders
        }

        selected_order = st.selectbox(
            "Select an Order",
            list(order_options.keys()),
            key="view_order_details"
        )

        selected_order_id = order_options[selected_order]

        details = get_order_details(selected_order_id)

        if details:

            details_df = pd.DataFrame(details)

            details_df["price"] = details_df["price"].apply(
                lambda x: f"₹{float(x):,.2f}"
            )

            details_df["subtotal"] = details_df["subtotal"].apply(
                lambda x: f"₹{float(x):,.2f}"
            )

            st.dataframe(
                details_df[
                    ["product_name", "quantity", "price", "subtotal"]
                ],
                use_container_width=True,
                hide_index=True
            )

            total_amount = sum(
                float(item["subtotal"]) for item in details
            )

            st.metric(
                "Order Total",
                f"₹{total_amount:,.2f}"
            )

        else:
            st.info("No products found for this order.")

    else:
        st.info("No orders available.")

elif menu == "Feedback":

    st.title("Customer Feedback Management")

    # ==========================================
    # 1. BULK IMPORT FEEDBACK
    # ==========================================

    st.divider()

    st.subheader("Bulk Import Feedback")

    st.write(
        "Upload customer feedback records using an Excel or CSV file."
    )

    uploaded_file = st.file_uploader(
        "Choose Excel or CSV file",
        type=["xlsx", "csv"],
        key="feedback_upload"
    )

    if uploaded_file is not None:

        try:

            if uploaded_file.name.lower().endswith(".csv"):

                feedback_df = pd.read_csv(uploaded_file)

            else:

                feedback_df = pd.read_excel(uploaded_file, header=1)

                # Remove completely empty rows
                feedback_df = feedback_df.dropna(how="all")

                # Clean column names
                feedback_df.columns = (
                    feedback_df.columns.astype(str).str.strip().str.lower()
                )

                # Remove unwanted unnamed columns
                feedback_df = feedback_df.loc[
                    :, ~feedback_df.columns.str.startswith("unnamed")
                ]
            

          

            # ==========================================
            # 2. CLEAN COLUMN NAMES
            # ==========================================

            feedback_df.columns = (
                feedback_df.columns
                .astype(str)
                .str.strip()
                .str.lower()
                .str.replace(r"[^a-z0-9]+", "_", regex=True)
                .str.strip("_")
            )

            # Remove completely empty rows
            feedback_df = feedback_df.dropna(how="all")

            # ==========================================
            # 3. CHECK REQUIRED COLUMNS
            # ==========================================

            required_columns = [
                "customer_email",
                "rating",
                "comments",
                "feedback_date"
            ]


           

            missing_columns = [
                col for col in required_columns
                if col not in feedback_df.columns
            ]

            if missing_columns:

                st.error(
                    f"Missing columns: {', '.join(missing_columns)}"
                )

                st.info(
                    "Please make sure your Excel file contains "
                    "customer_email, rating, comments and feedback_date."
                )

            elif feedback_df.empty:

                st.warning("The uploaded file contains no records.")

            else:

                # Keep only the required columns
                feedback_df = feedback_df[required_columns].copy()

                # ==========================================
                # 4. DATA PREVIEW
                # ==========================================

                st.success("File uploaded and columns validated!")

                st.subheader("Feedback Preview")

                st.dataframe(
                    feedback_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.write(
                    "Total Records:",
                    len(feedback_df)
                )

                # ==========================================
                # 5. IMPORT FEEDBACK
                # ==========================================

                if st.button(
                    "Import Feedback Records",
                    use_container_width=True,
                    key="import_feedback_button"
                ):

                    records = feedback_df.to_dict(
                        orient="records"
                    )

                    result = bulk_import_feedback(records)

                    st.divider()

                    st.subheader("Import Summary")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Successfully Imported",
                            result["imported"]
                        )

                    with col2:
                        st.metric(
                            "Failed Records",
                            result["failed"]
                        )

                    if result["imported"] > 0:

                        st.success(
                            "Feedback records imported successfully!"
                        )

                    if result["failed"] > 0:

                        st.warning("Some records could not be imported.")

                        st.write("Import Errors:")

                        for error in result["errors"]:
                            st.error(error)

        except Exception as e:

            st.error(
                f"Unable to process the uploaded file: {e}"
            )

    # ==========================================
    # 6. FEEDBACK HISTORY
    # ==========================================

    st.divider()

    st.subheader("Feedback History")

    feedback_records = get_all_feedback()

    if feedback_records:

        feedback_df = pd.DataFrame(feedback_records)

        feedback_df["feedback_date"] = (
            feedback_df["feedback_date"].astype(str)
        )

        # Feedback statistics
        total_feedback = len(feedback_df)

        average_rating = feedback_df["rating"].mean()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Feedback Records",
                total_feedback
            )

        with col2:
            st.metric(
                "Average Customer Rating",
                f"{average_rating:.2f} / 5"
            )

        # Feedback table
        st.write("**All Customer Feedback**")

        st.dataframe(
            feedback_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No feedback records available yet.")


elif menu == "Analytics":

    st.title("Customer Analytics Dashboard")

    st.divider()

    rfm_data = get_rfm_customer_segments()
    purchase_data = get_customer_purchase_summary()

    if not rfm_data.empty:

        # KPI calculations
        total_customers = len(purchase_data)
        purchasing_customers = len(rfm_data)
        total_revenue = rfm_data["total_spent"].sum()
        average_spending = (
            total_revenue / purchasing_customers
            if purchasing_customers > 0 else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Customers", total_customers)
        col2.metric("Purchasing Customers", purchasing_customers)
        col3.metric("Total Revenue", f"₹{total_revenue:,.2f}")
        col4.metric("Average Customer Spend", f"₹{average_spending:,.2f}")

        st.divider()

        # Customer Segmentation Chart
        st.subheader("Customer Segmentation")

        segment_counts = (
            rfm_data["customer_segment"]
            .value_counts()
            .reset_index()
        )

        segment_counts.columns = ["Customer Segment", "Customers"]

        fig = px.bar(
            segment_counts,
            x="Customer Segment",
            y="Customers",
            title="Customers by RFM Segment",
            text="Customers"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # RFM Customer Details
        st.subheader("RFM Customer Details")
        
        # Revenue by City
        st.subheader("Revenue by City")

        purchase_df = pd.DataFrame(purchase_data)

        # Convert spending values into numeric format
        purchase_df["total_spent"] = pd.to_numeric(
            purchase_df["total_spent"],
            errors="coerce"
        ).fillna(0)

        city_revenue = (
            purchase_df.groupby("city", as_index=False)["total_spent"]
            .sum()
            .sort_values("total_spent", ascending=False)
        )

        fig_city = px.bar(
            city_revenue,
            x="city",
            y="total_spent",
            title="Total Revenue by City",
            text_auto=".2s",
            labels={
                "city": "City",
                "total_spent": "Revenue (₹)"
            }
        )

        st.plotly_chart(fig_city, use_container_width=True)

        st.divider()

        # Top 5 Customers
        st.subheader("Top 5 Customers by Spending")

        top_customers = (
            purchase_df[purchase_df["total_spent"] > 0]
            .nlargest(5, "total_spent")
        )

        fig_top = px.bar(
            top_customers,
            x="customer_name",
            y="total_spent",
            title="Top 5 Highest-Spending Customers",
            text_auto=".2s",
            labels={
                "customer_name": "Customer",
                "total_spent": "Total Spending (₹)"
            }
        )

        st.plotly_chart(fig_top, use_container_width=True)


        display_columns = [
            "customer_name",
            "total_orders",
            "total_spent",
            "recency_days",
            "RFM_score",
            "customer_segment"
        ]

        st.dataframe(
            rfm_data[display_columns],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # Customers without purchases
        st.subheader("Customers Without Purchases")

        no_purchase = [
            customer for customer in purchase_data
            if customer["total_orders"] == 0
        ]

        if no_purchase:

            st.dataframe(
                pd.DataFrame(no_purchase)[
                    ["customer_name", "email", "city"]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("All customers have placed at least one order.")
        
        st.divider()

        # Customer Churn Risk Analysis
        st.subheader("Customer Churn Risk Analysis")

        churn_df = get_customer_churn_risk()

        if not churn_df.empty:

            churn_counts = (
                churn_df["churn_risk"]
                .value_counts()
                .reset_index()
            )

            churn_counts.columns = ["Risk Category", "Customers"]

            fig_churn = px.pie(
                churn_counts,
                names="Risk Category",
                values="Customers",
                title="Customer Churn Risk Distribution",
                hole=0.4
            )

            st.plotly_chart(
                fig_churn,
                use_container_width=True
            )

            st.subheader("Customer Risk Details")

            st.dataframe(
                churn_df[
                    [
                        "customer_name",
                        "city",
                        "total_orders",
                        "recency_days",
                        "churn_risk"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No churn-risk data available.")


    else:
        st.info("Not enough purchase data available for RFM analysis.")

