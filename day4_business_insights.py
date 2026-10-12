import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dataset" / "Sales-Data-Analysis.csv"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Convert numeric columns
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

# Calculate revenue
df["Revenue"] = df["Price"] * df["Quantity"]

# Convert dates
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Remove records with invalid essential analysis values
df = df.dropna(
    subset=["Date", "Product", "Price", "Quantity", "Revenue"]
)

print("=" * 50)
print("VYNORA BUSINESSPULSE - DAY 4")
print("=" * 50)

print("Records analyzed:", len(df))



print("\n--- PRODUCT INSIGHTS ---")

product_revenue = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

top_product = product_revenue.idxmax()
top_product_revenue = product_revenue.max()

print("Top Product:", top_product)
print(f"Revenue: {top_product_revenue:,.2f}")

print("\nTop 5 Products:")
print(product_revenue.head(5))


print("\n--- LOWEST-REVENUE PRODUCTS ---")

bottom_products = product_revenue.sort_values().head(5)

print(bottom_products)



print("\n--- DAY-OF-WEEK ANALYSIS ---")

df["Day Name"] = df["Date"].dt.day_name()

weekday_revenue = (
    df.groupby("Day Name")["Revenue"]
    .sum()
)

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday_revenue = weekday_revenue.reindex(weekday_order)

print(weekday_revenue)

best_weekday = weekday_revenue.idxmax()

print("\nHighest-Revenue Weekday:", best_weekday)


print("\n--- PURCHASE TYPE INSIGHTS ---")

order_data = (
    df.groupby(["Purchase Type", "Order ID"], dropna=False)["Revenue"]
    .sum()
    .reset_index()
)

purchase_type_aov = (
    order_data.groupby("Purchase Type")["Revenue"]
    .mean()
    .sort_values(ascending=False)
)

print("Average Order Value by Purchase Type:")
print(purchase_type_aov)


print("\n--- PAYMENT METHOD INSIGHTS ---")

payment_revenue = (
    df.groupby("Payment Method")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

payment_share = (
    payment_revenue / payment_revenue.sum()
) * 100

print("Revenue by Payment Method:")
print(payment_revenue)

print("\nRevenue Share (%):")
print(payment_share.round(2))

print("\n--- AUTOMATED BUSINESS INSIGHTS ---")

insights = []

# Insight 1: Top product
insights.append(
    f"Product Insight: {top_product} generated the highest "
    f"recorded revenue ({top_product_revenue:,.2f})."
)

# Insight 2: Lowest-revenue product
lowest_product = product_revenue.idxmin()
lowest_product_revenue = product_revenue.min()

insights.append(
    f"Product Review: {lowest_product} had the lowest "
    f"recorded revenue ({lowest_product_revenue:,.2f}). "
    "Review its sales volume and costs before making decisions."
)

# Insight 3: Best weekday
if weekday_revenue.notna().any():
    best_weekday = weekday_revenue.idxmax()

    insights.append(
        f"Sales Timing: {best_weekday} had the highest "
        "total recorded revenue among weekdays."
    )

# Insight 4: Top payment method by revenue
if not payment_revenue.empty:
    best_payment = payment_revenue.idxmax()

    insights.append(
        f"Payment Insight: {best_payment} accounted for "
        "the highest recorded revenue among payment methods."
    )

for number, insight in enumerate(insights, start=1):
    print(f"{number}. {insight}")



INSIGHTS_FILE = OUTPUT_DIR / "day4_business_insights.txt"

with open(INSIGHTS_FILE, "w", encoding="utf-8") as file:
    file.write("VYNORA BUSINESSPULSE - DAY 4 INSIGHTS\n")
    file.write("=" * 45 + "\n\n")

    for number, insight in enumerate(insights, start=1):
        file.write(f"{number}. {insight}\n\n")

print("\nInsights saved to:")
print(INSIGHTS_FILE)

product_revenue.to_csv(
    OUTPUT_DIR / "day4_product_revenue.csv",
    header=["Revenue"]
)

weekday_revenue.to_csv(
    OUTPUT_DIR / "day4_weekday_revenue.csv",
    header=["Revenue"]
)

purchase_type_aov.to_csv(
    OUTPUT_DIR / "day4_purchase_type_aov.csv",
    header=["Average Order Value"]
)

payment_share.to_csv(
    OUTPUT_DIR / "day4_payment_revenue_share.csv",
    header=["Revenue Share Percentage"]
)

print("\nDay 4 analysis files saved successfully!")