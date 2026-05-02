# =====================================================
# imports
# =====================================================

import pandas as pd


# =====================================================
# convert database data to dataframe
# =====================================================

def to_dataframe(data):
    # Converts the list of database rows into a pandas DataFrame
    return pd.DataFrame(
        data,
        columns=['id', 'amount', 'category', 'date', 'notes']
    )


# =====================================================
# calculate total spending
# =====================================================

def total_spent(df):
    # If there is no data, return 0 instead of causing an error
    if df.empty:
        return 0

    # Add all values in the amount column
    return df['amount'].sum()


# =====================================================
# calculate average spending
# =====================================================

def avg_spent(df):
    # If there is no data, return 0 instead of causing an error
    if df.empty:
        return 0

    # Calculate the average transaction amount
    return df['amount'].mean()


# =====================================================
# find top spending category
# =====================================================

def top_category(df):
    # If there is no data, return None
    if df.empty:
        return None

    # Group spending by category, then add the total amount for each category
    grouped = df.groupby('category')['amount'].sum()

    # Return the category with the highest total spending
    return grouped.idxmax()


# =====================================================
# calculate total spent on top category
# =====================================================

def top_category_total(df):
    # If there is no data, return 0
    if df.empty:
        return 0

    # Get the category where the user spent the most
    top = top_category(df)

    # Return the total spending for only that top category
    return df[df["category"] == top]["amount"].sum()


# =====================================================
# spending insights
# =====================================================

def get_Insights(df, currency):
    # If there is no data, show a helpful message
    if df.empty:
        return "No data yet. Add some transactions first."

    # Calculate values needed for the insight message
    top = top_category(df)
    top_total = top_category_total(df)
    total = total_spent(df)
    average = avg_spent(df)

    # Return a formatted spending recommendation
    return f"""
You are spending the most on **{top}**

Total spent on **{top}**: **{top_total:.3f} {currency}**

Overall spending: **{total:.3f} {currency}**

Average transaction: **{average:.3f} {currency}**

Try to reduce your spending on **{top}** this month.
"""


# =====================================================
# format amount with currency
# =====================================================

def format_amount(value, currency):
    # Formats numbers to 3 decimal places with the selected currency
    return f"{value:.3f} {currency}"
