import pandas as pd

df = pd.read_csv("dataset/Sales-Data-Analysis.csv")

print("FIRST 5 ROWS")
print(df.head())

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns)

print("\nDATA TYPES")
print(df.dtypes)

print("\nDATASET INFO")
print(df.info())

print("\nSTATISTICS")
print(df.describe())
print(df.columns.tolist())


print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE ROWS")
print(df.duplicated().sum())

print("\nDATA TYPES")
print(df.dtypes)

df["Revenue"] = df["Price"] * df["Quantity"]

print(df[["Price", "Quantity", "Revenue"]].head())


total_revenue = df["Revenue"].sum()

print("Total Revenue:", total_revenue)

total_quantity = df["Quantity"].sum()

print("Total Quantity Sold:", total_quantity)

total_orders = len(df)

print("Total Orders:", total_orders)

total_orders = df["Order ID"].nunique()

print("Total Orders:", total_orders)

average_order_value = total_revenue / total_orders

print("Average Order Value:", average_order_value)

product_sales = df.groupby("Product")["Quantity"].sum()

print(product_sales.sort_values(ascending=False).head(10))



product_revenue = df.groupby("Product")["Revenue"].sum()

print(product_revenue.sort_values(ascending=False).head(10))


print(df["Purchase Type"].value_counts())


print("\nEXACT COLUMN NAMES:")
print(df.columns.tolist())


df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)


df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

print("\nDATE DATA TYPE:")
print(df["Date"].dtype)

# Step 18 - Daily revenue

daily_revenue = df.groupby("Date")["Revenue"].sum()

print("\nDAILY REVENUE:")
print(daily_revenue.sort_values(ascending=False).head(10))


# Step 19 - Best sales day

best_day = daily_revenue.idxmax()
best_day_revenue = daily_revenue.max()

print("\nBEST SALES DAY:")
print("Date:", best_day)
print("Revenue:", best_day_revenue)


print("\n" + "=" * 40)
print("BUSINESSPULSE DAY 1 SUMMARY")
print("=" * 40)

print(f"Total Revenue: {total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: {average_order_value:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Best Sales Day: {best_day}")
print(f"Best Day Revenue: {best_day_revenue:,.2f}")