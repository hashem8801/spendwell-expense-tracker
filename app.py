# =====================================================
# imports
# =====================================================

import streamlit as st
import matplotlib.pyplot as plt

from db import *
from utils import *


# =====================================================
# setup
# =====================================================

# Configure the Streamlit page title, icon, and layout
st.set_page_config(page_title="SpendWell", page_icon="💰", layout="wide")

# Create database tables if they do not already exist
create_table()


# =====================================================
# app title
# =====================================================

st.title("💰 SpendWell")
st.write("A simple finance tracker for managing expenses and improving spending habits.")


# =====================================================
# sidebar
# =====================================================

# Sidebar menu used to move between pages
page = st.sidebar.radio(
    "Select a page",
    ["📊 Overview", "➕ Add Transaction",
     "📋 History", "💡 Insights",
     "⚙️ Preferences"
     ],
)


# =====================================================
# load data
# =====================================================

# Get expenses from database
data = get_expenses()

# Convert expenses to pandas DataFrame
df = to_dataframe(data)

# Get selected currency from database
currency = get_currency()

# Get categories and colors from database
categories = get_categories()

# Store only category names for selectbox usage
category_names = [c[1] for c in categories]

# Store category names with their colors
category_colors = {c[1]: c[2] for c in categories}



# =================== Main Page =======================

if page == "📊 Overview":
    st.header("📊 Financial Overview")
    st.caption("Get a quick snapshot of your spending, key metrics, and trends over time.")
    st.divider()

    # If there are no transactions, show message
    if df.empty:
        st.info("No data until now.")

    else:
        # Create 3 columns for the main metrics
        col1, col2, col3 = st.columns(3)

        # Show spending metrics
        col1.metric("Total Spent", format_amount(total_spent(df), currency))
        col2.metric("Average", format_amount(avg_spent(df), currency))
        col3.metric("Top Category", top_category(df))

        # category chart
        st.subheader("Spending by Category")

        # Group spending by category
        cat_data = df.groupby("category")["amount"].sum()

        # Get color for each category
        colors = [category_colors.get(cat, "#999") for cat in cat_data.index]

        # Create bar chart
        fig, ax = plt.subplots()
        ax.bar(cat_data.index, cat_data.values, color=colors)

        # Rotate category names to make them easier to read
        plt.xticks(rotation=25)

        # Display chart in Streamlit
        st.pyplot(fig)


        # time chart
        st.subheader("Spending over Time")

        # Convert date column to date format
        df["date"] = pd.to_datetime(df["date"]).dt.date

        # Group spending by date
        time_data = df.groupby("date")["amount"].sum()

        # Format the date to look cleaner on the x-axis
        time_data.index = pd.to_datetime(time_data.index).strftime("%b %d, %Y")

        # Create line chart
        fig2, ax2 = plt.subplots()
        ax2.plot(time_data.index, time_data.values, marker="o")

        # Add chart labels and title
        ax2.set_xlabel("Date")
        ax2.set_ylabel(f"Amount in {currency}" )
        ax2.set_title("Spending over Time")

        # Rotate date labels and adjust chart layout
        plt.xticks(rotation=30)
        plt.tight_layout()

        # Display chart in Streamlit
        st.pyplot(fig2)



# =================== Add Expense =======================

elif page == "➕ Add Transaction":
    st.header("➕ Add New Transaction")
    st.caption("Record a new expense by entering the amount, category, and details.")
    st.divider()


    # Category dropdown
    category = st.selectbox(
            "Select a category", category_names, key="category_select")

    # Get selected category color
    selected_color = category_colors.get(category, "#999999")

    # Show selected category as a colored badge
    st.markdown(
            f"""
<div style="background-color:{selected_color}; color:white; padding:8px 18px; border-radius:14px; width:fit-content; font-weight:700; margin:10px 0 18px 0;">
{category}
</div>
            """,
            unsafe_allow_html=True
        )

    # Form for adding a transaction
    with st.form("form", clear_on_submit=True):

            # Expense amount input
            amount = st.number_input("Amount", min_value=0.0, value=0.0, step=0.250, format="%.3f")

            # Expense date input
            date = st.date_input("Date")

            # Optional notes input
            notes = st.text_input("Notes")

            # Submit button
            submit = st.form_submit_button("Save")

            # Show success message after rerun
            if "add_message" in st.session_state:
                st.success(st.session_state["add_message"])
                del st.session_state["add_message"]

            # When user clicks Save
            if submit:
                # Validate amount
                if amount <= 0:
                    st.error("Amount must be greater than 0.")

                else:
                    # Add expense to database
                    add_expense(amount, category, date, notes)

                    # Store message before rerun
                    st.session_state["add_message"] = "Transaction saved successfully."

                    # Refresh the app
                    st.rerun()



# =================== History =======================

elif page == "📋 History":
    st.header("📋 Transaction History")
    st.caption("Browse, search, and manage all your recorded transactions.")
    st.divider()

    # If there are no transactions, show message
    if df.empty:
        st.info("No data until now.")

    else:
        # Search box for notes or categories
        search = st.text_input("Search")

        # Filter transactions by category
        category_filter = st.selectbox("Filter", ["All"] + list(df["category"].unique()))

        # Sort transactions by date or amount
        sort = st.selectbox("Sort", ["Date", "Amount"])

        # Copy dataframe before filtering
        filtered = df.copy()

        # Search inside notes and category
        if search:
            filtered = filtered[
                filtered["notes"].str.contains(search, case=False, na=False) |
                filtered["category"].str.contains(search, case=False, na=False)
            ]

        # Apply category filter
        if category_filter != "All":
            filtered = filtered[filtered["category"] == category_filter]

        # Sort by newest date first
        if sort == "Date":
            filtered["date"] = pd.to_datetime(filtered["date"]).dt.date
            filtered = filtered.sort_values("date", ascending=False)

        # Sort by highest amount first
        else:
            filtered = filtered.sort_values("amount", ascending=False)

        # Format amount with 3 decimals and currency
        filtered["amount"] = filtered["amount"].map(lambda x: f"{x:.3f} {currency}")

        st.subheader("Transactions")

        # Display each transaction as a card
        for _, row in filtered.iterrows():
            # Get category color
            color = category_colors.get(row["category"], "#999999")

            # HTML card for one transaction
            html = f"""
        <div style="border:1px solid #ddd; border-radius:16px; padding:16px; margin-bottom:12px; background-color:#0f172a;">

        <span style="background-color:{color}; color:white; padding:6px 14px; border-radius:999px; font-weight:600; font-size:14px;">
        {row["category"]}
        </span>

        <h3 style="margin:8px 0 4px 0;">
        {row["amount"]}
        </h3>

        <p style="margin:0; opacity:0.8;">
        <b>Date:</b> {row["date"]}
        </p>

        <p style="margin:0; opacity:0.8;">
        <b>Notes:</b> {row["notes"] if row["notes"] else "—"}
        </p>

        <p style="margin:0; opacity:0.6;">
        ID: {row["id"]}
        </p>

        </div>
        """

            # Show transaction card
            st.markdown(html, unsafe_allow_html=True)

        st.subheader("Delete Transaction")



        # User enters the ID of the transaction to delete
        delete_id = st.number_input("Delete ID", min_value=1, step=1)


        # Delete button
        if st.button("Delete"):
            # Delete selected transaction from database
            delete_expense(delete_id)

            # Store message before rerun
            st.session_state["delete_message"] = "Transaction deleted successfully."

            # Refresh the app
            st.rerun()

    # Show delete message after rerun
    if "delete_message" in st.session_state:
            st.error(st.session_state["delete_message"])
            del st.session_state["delete_message"]



# =================== Insights =======================

elif page == "💡 Insights":
    st.header("💡 Spending Insights")

    # Show AI-style recommendation text from utils.py
    st.write(get_Insights(df, currency))



# =================== Settings =======================

elif page == "⚙️ Preferences":
    st.header("⚙️ Preferences")

    # -------------------------------
    # Currency Settings
    # -------------------------------

    st.subheader("Currency")

    # Available currency options
    currency_options = ["KD", "USD", "EUR", "GBP", "SAR", "AED"]

    # Currency dropdown
    new_currency = st.selectbox(
        "Select Currency",
        currency_options,
        index=currency_options.index(currency)
    )

    # Save selected currency
    if st.button("Save Currency"):
        update_currency(new_currency)
        st.session_state["currency_message"] = "Currency updated successfully."
        st.rerun()

    # Show currency update message after rerun
    if "currency_message" in st.session_state:
        st.success(st.session_state["currency_message"])
        del st.session_state["currency_message"]


    # -------------------------------
    # Add Category
    # -------------------------------

    st.subheader("Add Category")

    # New category name
    name = st.text_input("Category Name")

    # New category color
    color = st.color_picker("Color")

    # Add category button
    if st.button("Add Category"):
        # Validate category name
        if name == "":
            st.error("Category name cannot be empty.")

        else:
            # Add category to database
            add_category(name, color)

            # Store message before rerun
            st.session_state["add_cat_message"] = "Category added successfully."

            # Refresh app
            st.rerun()

    # Show add category message after rerun
    if "add_cat_message" in st.session_state:
        st.success(st.session_state["add_cat_message"])
        del st.session_state["add_cat_message"]


    # -------------------------------
    # Edit Categories
    # -------------------------------

    st.subheader("Edit Categories")

    # Loop through all categories
    for cid, name, color in categories:

        # Each category has its own expandable edit box
        with st.expander(name):

            # Input to edit category name
            new_name = st.text_input("Name", name, key=f"name{cid}")

            # Color picker to edit category color
            new_color = st.color_picker("Color", color, key=f"color{cid}")

            # Save edited category
            if st.button("Save", key=f"save{cid}"):
                update_category(cid, new_name, new_color)
                st.session_state["edit_cat_message"] = f"{new_name} updated successfully."
                st.rerun()


    # Show edit category message after rerun
    if "edit_cat_message" in st.session_state:
        st.success(st.session_state["edit_cat_message"])
        del st.session_state["edit_cat_message"]
