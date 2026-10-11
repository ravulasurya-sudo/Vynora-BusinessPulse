import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dataset" / "Sales-Data-Analysis.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)

# Convert columns to numeric
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

# Remove rows missing essential analysis values
df = df.dropna(
    subset=["Date", "Product", "Price", "Quantity", "Revenue"]
)

# Create output folder
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 50)
print("VYNORA BUSINESSPULSE - DAY 3 EDA")
print("=" * 50)

print("\nDataset Shape:", df.shape)
print("\nFirst Five Records:")
print(df.head())



print("\n--- BUSINESS KPIs ---")

total_revenue = df["Revenue"].sum()

total_orders = df["Order ID"].nunique()

total_quantity = df["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

unique_products = df["Product"].nunique()

print(f"Total Revenue:       {total_revenue:,.2f}")
print(f"Total Orders:        {total_orders:,}")
print(f"Average Order Value: {average_order_value:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,.0f}")
print(f"Unique Products:     {unique_products:,}")

print("\n--- PRODUCT ANALYSIS ---")

product_quantity = (
    df.groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

product_revenue = (
    df.groupby("Product")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Products by Quantity Sold:")
print(product_quantity.head(10))

print("\nTop 10 Products by Revenue:")
print(product_revenue.head(10))


top_products = product_revenue.head(10).sort_values()

plt.figure(figsize=(10, 6))

top_products.plot(kind="barh")

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_products_by_revenue.png",
    dpi=150
)

plt.show()


print("\n--- DAILY SALES ANALYSIS ---")

daily_revenue = (
    df.groupby("Date")["Revenue"]
    .sum()
    .sort_index()
)

best_day = daily_revenue.idxmax()
worst_day = daily_revenue.idxmin()

print("Best Sales Day:", best_day.date())
print(f"Best Day Revenue: {daily_revenue.max():,.2f}")

print("Lowest Sales Day:", worst_day.date())
print(f"Lowest Day Revenue: {daily_revenue.min():,.2f}")


plt.figure(figsize=(12, 6))

daily_revenue.plot()

plt.title("Daily Revenue Trend")
plt.xlabel("Date")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "daily_revenue_trend.png",
    dpi=150
)

plt.show()



print("\n--- MONTHLY SALES ANALYSIS ---")

df["Month"] = df["Date"].dt.to_period("M")

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
    .sort_index()
)

print("\nMonthly Revenue:")
print(monthly_revenue)

plt.figure(figsize=(12, 6))

monthly_revenue.plot(kind="bar")

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "monthly_revenue.png",
    dpi=150
)

plt.show()



print("\n--- CITY PERFORMANCE ---")

city_revenue = (
    df.groupby("City")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by City:")
print(city_revenue)

city_revenue.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "revenue_by_city.png",
    dpi=150
)

plt.show()


print("\n--- PAYMENT METHOD ANALYSIS ---")

payment_counts = df["Payment Method"].value_counts()

payment_revenue = (
    df.groupby("Payment Method")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTransactions by Payment Method:")
print(payment_counts)

print("\nRevenue by Payment Method:")
print(payment_revenue)

payment_counts.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Transactions by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Records")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "payment_method_analysis.png",
    dpi=150
)

plt.show()

print("\n--- PURCHASE TYPE ANALYSIS ---")

purchase_counts = df["Purchase Type"].value_counts()

purchase_revenue = (
    df.groupby("Purchase Type")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRecords by Purchase Type:")
print(purchase_counts)

print("\nRevenue by Purchase Type:")
print(purchase_revenue)


purchase_revenue.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Revenue by Purchase Type")
plt.xlabel("Purchase Type")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "purchase_type_revenue.png",
    dpi=150
)

plt.show()

print("\n--- MANAGER ANALYSIS ---")

manager_revenue = (
    df.groupby("Manager")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Manager:")
print(manager_revenue)

print("\n--- BUSINESS INSIGHTS ---")

# Highest-revenue product
best_product = product_revenue.idxmax()
best_product_revenue = product_revenue.max()

print(
    f"1. Highest-revenue product: {best_product}, "
    f"generating {best_product_revenue:,.2f} in calculated revenue."
)

# Highest-revenue city
if not city_revenue.empty:
    best_city = city_revenue.idxmax()

    print(
        f"2. Highest-revenue city: {best_city}, "
        f"with {city_revenue.max():,.2f} in calculated revenue."
    )

# Most popular payment method
if not payment_counts.empty:
    popular_payment = payment_counts.idxmax()

    print(
        f"3. Most common payment method by record count: "
        f"{popular_payment}."
    )

# Highest-revenue month
if not monthly_revenue.empty:
    best_month = monthly_revenue.idxmax()

    print(
        f"4. Highest-revenue month: {best_month}, "
        f"with {monthly_revenue.max():,.2f} in calculated revenue."
    )


summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Total Orders",
        "Average Order Value",
        "Total Quantity Sold",
        "Unique Products"
    ],
    "Value": [
        total_revenue,
        total_orders,
        average_order_value,
        total_quantity,
        unique_products
    ]
})

summary_file = OUTPUT_DIR / "day3_kpi_summary.csv"

summary.to_csv(summary_file, index=False)

print("\nKPI summary saved to:")
print(summary_file)    


product_revenue.to_csv(
    OUTPUT_DIR / "product_revenue.csv"
)

daily_revenue.to_csv(
    OUTPUT_DIR / "daily_revenue.csv"
)

monthly_revenue.to_csv(
    OUTPUT_DIR / "monthly_revenue.csv"
)

city_revenue.to_csv(
    OUTPUT_DIR / "city_revenue.csv"
)