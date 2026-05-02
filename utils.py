import pandas as pd


def to_dataframe(data):
    return pd.DataFrame(
        data,
        columns=['id', 'amount', 'category', 'date', 'notes']
    )

def total_spent(df):
    if df.empty:
        return 0
    return df['amount'].sum()


def avg_spent(df):
    if df.empty:
        return 0
    return df['amount'].mean()

def top_category(df):
    if df.empty:
        return None

    grouped = df.groupby('category')['amount'].sum()
    return grouped.idxmax()


def top_category_total(df):
    if df.empty:
        return 0
    top = top_category(df)
    return df[df["category"] == top]["amount"].sum()


def get_Insights(df, currency):
    if df.empty:
        return "No data yet. Add some transactions first."

    top = top_category(df)
    top_total = top_category_total(df)
    total = total_spent(df)
    average = avg_spent(df)

    return f"""
You are spending the most on **{top}**

Total spent on **{top}**: **{top_total:.3f} {currency}**

Overall spending: **{total:.3f} {currency}**

Average transaction: **{average:.3f} {currency}**

Try to reduce your spending on **{top}** this month.
"""


def format_amount(value, currency):
    return f"{value:.3f} {currency}"
