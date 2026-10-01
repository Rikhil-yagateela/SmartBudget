import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SmartBudget", layout="wide")

CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Shopping", "Health", "Savings"]


def default_budget():
    return pd.DataFrame({
        "Category": CATEGORIES,
        "Planned": [180, 80, 500, 120, 90, 70, 60, 100]
    })


def default_expenses():
    return pd.DataFrame({
        "Category": CATEGORIES,
        "Actual": [150, 65, 500, 110, 100, 90, 45, 80]
    })


def monthly_data():
    return pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Total": [1200, 1350, 1500, 1600, 1700, 1825]
    })


def get_difference(budget_df, actual_df):
    merged = budget_df.merge(actual_df, on="Category", how="outer")
    merged["Difference"] = merged["Actual"] - merged["Planned"]
    return merged


def forecast(month_df):
    x = np.arange(1, len(month_df) + 1)
    y = month_df["Total"].values.astype(float)
    slope, intercept = np.polyfit(x, y, 1)
    next_value = slope * (len(x) + 1) + intercept
    return slope, next_value


st.title("SmartBudget")
st.caption("Simple budget tracker")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Planned Budget")
        budget_df = st.data_editor(default_budget(), hide_index=True, use_container_width=True, key="budget")

    with col2:
        st.subheader("Actual Expenses")
        actual_df = st.data_editor(default_expenses(), hide_index=True, use_container_width=True, key="actual")

planned_total = float(budget_df["Planned"].sum())
actual_total = float(actual_df["Actual"].sum())
remaining = planned_total - actual_total
difference = actual_total - planned_total

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Planned", f"₹{planned_total:,.2f}")
col2.metric("Actual", f"₹{actual_total:,.2f}")
col3.metric("Remaining", f"₹{remaining:,.2f}")
col4.metric("Difference", f"₹{difference:,.2f}")

st.subheader("Category Breakdown")
comparison = get_difference(budget_df, actual_df)
st.dataframe(comparison, hide_index=True, use_container_width=True)

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(comparison["Category"], comparison["Difference"], color=["green" if x >= 0 else "red" for x in comparison["Difference"]])
ax.axhline(0, color="black", linewidth=1)
ax.set_title("Actual - Planned")
ax.set_ylabel("Amount")
plt.xticks(rotation=30)
st.pyplot(fig)

st.markdown("---")
st.subheader("Monthly Trend")
month_df = monthly_data()
st.line_chart(month_df.set_index("Month")["Total"])

slope, next_value = forecast(month_df)
st.write(f"Trend: ₹{slope:,.2f} per month")
st.metric("Next Month Estimate", f"₹{next_value:,.2f}")

st.caption("Simple app for daily and monthly budget planning.")
