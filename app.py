import streamlit as st
import matplotlib.pyplot as plt

from db import *
from utils import *


# setup
st.set_page_config(page_title="SpendWell", page_icon="💰", layout="wide")
create_table()


st.title("💰 SpendWell")
st.write("A simple finance tracker for managing expenses and improving spending habits.")


# sidebar
page = st.sidebar.radio(
    "Select a page",
    ["📊 Overview", "➕ Add Transaction",
     "📋 History", "💡 Insights",
     "⚙️ Preferences"
     ],
)

# load data
data = get_expenses()
df = to_dataframe(data)

currency = get_currency()
categories = get_categories()
category_names = [c[1] for c in categories]
category_colors = {c[1]: c[2] for c in categories}



# =================== Main Page =======================
if page == "📊 Overview":
    st.header("📊 Financial Overview")
    st.caption("Get a quick snapshot of your spending, key metrics, and trends over time.")
    st.divider()

    if df.empty:
        st.info("No data until now.")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Spent", format_amount(total_spent(df), currency))
        col2.metric("Average", format_amount(avg_spent(df), currency))
        col3.metric("Top Category", top_category(df))

        # category chart
        st.subheader("Spending by Category")
        cat_data = df.groupby("category")["amount"].sum()
        colors = [category_colors.get(cat, "#999") for cat in cat_data.index]


        fig, ax = plt.subplots()
        ax.bar(cat_data.index, cat_data.values, color=colors)
        plt.xticks(rotation=25)
        st.pyplot(fig)


        # time chart
        st.subheader("Spending over Time")

        df["date"] = pd.to_datetime(df["date"]).dt.date
        time_data = df.groupby("date")["amount"].sum()
        time_data.index = pd.to_datetime(time_data.index).strftime("%b %d, %Y")

        fig2, ax2 = plt.subplots()
        ax2.plot(time_data.index, time_data.values, marker="o")
        ax2.set_xlabel("Date")
        ax2.set_ylabel(f"Amount in {currency}" )
        ax2.set_title("Spending over Time")

        plt.xticks(rotation=30)
        plt.tight_layout()

        st.pyplot(fig2)



# =================== Add Expense =======================
elif page == "➕ Add Transaction":
    st.header("➕ Add New Transaction")
    st.caption("Record a new expense by entering the amount, category, and details.")
    st.divider()


    category = st.selectbox(
            "Select a category", category_names, key="category_select")

    selected_color = category_colors.get(category, "#999999")

    st.markdown(
            f"""
<div style="background-color:{selected_color}; color:white; padding:8px 18px; border-radius:14px; width:fit-content; font-weight:700; margin:10px 0 18px 0;">
{category}
</div>
            """,
            unsafe_allow_html=True
        )

    with st.form("form", clear_on_submit=True):
            amount = st.number_input("Amount", min_value=0.0, value=0.0, step=0.250, format="%.3f")

            date = st.date_input("Date")
            notes = st.text_input("Notes")

            submit = st.form_submit_button("Save")

            if submit:
                if amount <= 0:
                    st.error("Amount must be greater than 0.")
                else:
                    add_expense(amount, category, date, notes)
                    st.success("Successfully Saved")
                    st.rerun()



# =================== History =======================
elif page == "📋 History":
    st.header("📋 Transaction History")
    st.caption("Browse, search, and manage all your recorded transactions.")
    st.divider()

    if df.empty:
        st.info("No data until now.")

    else:
        search = st.text_input("Search")
        category_filter = st.selectbox("Filter", ["All"] + list(df["category"].unique()))
        sort = st.selectbox("Sort", ["Date", "Amount"])

        filtered = df.copy()

        if search:
            filtered = filtered[
                filtered["notes"].str.contains(search, case=False, na=False) |
                filtered["category"].str.contains(search, case=False, na=False)
            ]

        if category_filter != "All":
            filtered = filtered[filtered["category"] == category_filter]

        if sort == "Date":
            filtered["date"] = pd.to_datetime(filtered["date"]).dt.date
            filtered = filtered.sort_values("date", ascending=False)
        else:
            filtered = filtered.sort_values("amount", ascending=False)

        filtered["amount"] = filtered["amount"].map(lambda x: f"{x:.3f} {currency}")

        st.subheader("Transactions")

        for _, row in filtered.iterrows():
            color = category_colors.get(row["category"], "#999999")

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

            st.markdown(html, unsafe_allow_html=True)

        st.subheader("Delete Transaction")

        delete_id = st.number_input("Delete ID", min_value=1, step=1)

        if st.button("Delete"):
            delete_expense(delete_id)
            st.error("Deleted successfully. Refresh the page.")
            st.rerun()



# =================== Insights =======================
elif page == "💡 Insights":
    st.header("💡 Spending Insights")

    st.write(get_Insights(df, currency))



# =================== Settings =======================
elif page == "⚙️ Preferences":
    st.header("⚙️ Preferences")

    st.subheader("Currency")
    currency_options = ["KD", "USD", "EUR", "GBP", "SAR", "AED"]

    new_currency = st.selectbox(
        "Select Currency",
        currency_options,
        index=currency_options.index(currency)
    )

    if st.button("Save Currency"):
        update_currency(new_currency)
        st.success("Currency updated")
        st.rerun()

    st.subheader("Add Category")
    name = st.text_input("Category Name")
    color = st.color_picker("Color")

    if st.button("Add Category"):
        if name == "":
            st.error("Category name cannot be empty.")
        else:
            add_category(name, color)
            st.success("Added")
            st.rerun()

    st.subheader("Edit Categories")
    for cid, name, color in categories:
        with st.expander(name):
            new_name = st.text_input("Name", name, key=f"name{cid}")
            new_color = st.color_picker("Color", color, key=f"color{cid}")

            if st.button("Save", key=f"save{cid}"):
                update_category(cid, new_name, new_color)
                st.success("Updated")
                st.rerun()
