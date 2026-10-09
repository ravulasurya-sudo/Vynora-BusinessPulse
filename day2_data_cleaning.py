import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dataset" / "Sales-Data-Analysis.csv"

# Load original dataset
df = pd.read_csv(DATA_FILE)

print("=" * 50)
print("VYNORA BUSINESSPULSE - DAY 2")
print("=" * 50)

print("\nOriginal Dataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())



print("\n--- MISSING VALUE ANALYSIS ---")

missing_values = df.isnull().sum()

print(missing_values)

total_missing = df.isnull().sum().sum()

print("\nTotal Missing Values:", total_missing)

print("\n--- DUPLICATE ANALYSIS ---")

duplicate_count = df.duplicated().sum()

print("Duplicate Rows:", duplicate_count)

duplicates = df[df.duplicated(keep=False)]

print("\nDuplicate Records:")
print(duplicates.head(20))

print("\n--- DATA TYPES ---")

print(df.dtypes)

print("\n--- DATE VALIDATION ---")

df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

invalid_dates = df["Date"].isna().sum()

print("Invalid or Missing Dates:", invalid_dates)


df = pd.read_csv(DATA_FILE)

print("Column names in dataset:")
print(df.columns.tolist())


# Calculate revenue
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

df["Revenue"] = df["Price"] * df["Quantity"]

print("\nUpdated column names:")
print(df.columns.tolist())

print("\nRevenue preview:")
print(df[["Product", "Price", "Quantity", "Revenue"]].head())

print("\nTotal Revenue:", df["Revenue"].sum())

print("\n--- NUMERIC VALIDATION ---")

numeric_columns = ["Price", "Quantity", "Revenue"]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print(df[numeric_columns].dtypes)

print("\nMissing or Invalid Numeric Values:")
print(df[numeric_columns].isna().sum())

print("\n--- BUSINESS RULE VALIDATION ---")

print("Negative Prices:", (df["Price"] < 0).sum())

print("Negative Quantities:", (df["Quantity"] < 0).sum())

print("Negative Revenue:", (df["Revenue"] < 0).sum())

print("Zero Prices:", (df["Price"] == 0).sum())

print("Zero Quantities:", (df["Quantity"] == 0).sum())


print("\n--- BLANK TEXT VALUES ---")

text_columns = [
    "Product",
    "Purchase Type",
    "Payment Method",
    "Manager",
    "City"
]

for column in text_columns:
    blank_count = (
        df[column]
        .astype("string")
        .str.strip()
        .eq("")
        .sum()
    )

    print(f"{column}: {blank_count} blank values")



print("\n--- REVENUE VALIDATION ---")

df["Expected Revenue"] = df["Price"] * df["Quantity"]

df["Revenue Difference"] = (
    df["Revenue"] - df["Expected Revenue"]
)

df["Revenue Matches"] = (
    df["Revenue"].round(2)
    == df["Expected Revenue"].round(2)
)

print(
    "Rows with matching revenue:",
    df["Revenue Matches"].sum()
)

print(
    "Rows with different revenue:",
    (~df["Revenue Matches"]).sum()
)

print("\nSample Mismatched Records:")

print(
    df.loc[
        ~df["Revenue Matches"],
        [
            "Order ID",
            "Product",
            "Price",
            "Quantity",
            "Revenue",
            "Expected Revenue"
        ]
    ].head(10)
)





print("\n--- DATA CLEANING ---")

original_row_count = len(df)

# Remove exact duplicate rows.
# Ignore temporary analysis columns when identifying duplicates.
temporary_columns = [
    "Expected Revenue",
    "Revenue Difference",
    "Revenue Matches"
]

comparison_df = df.drop(
    columns=temporary_columns,
    errors="ignore"
)

duplicate_mask = comparison_df.duplicated()

df = df.loc[~duplicate_mask].copy()

removed_duplicates = original_row_count - len(df)

print("Exact duplicate rows removed:", removed_duplicates)

# Clean whitespace in text columns.
text_columns = [
    "Product",
    "Purchase Type",
    "Payment Method",
    "Manager",
    "City"
]

for column in text_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )

print("Text whitespace cleaned.")

print("Rows remaining:", len(df))





print("\n--- DATA QUALITY REPORT ---")

quality_report = pd.DataFrame({
    "Column": df.columns,
    "Data Type": [
        str(df[column].dtype)
        for column in df.columns
    ],
    "Missing Values": [
        df[column].isna().sum()
        for column in df.columns
    ],
    "Unique Values": [
        df[column].nunique(dropna=True)
        for column in df.columns
    ]
})

print(quality_report.to_string(index=False))




print("\n--- SAVING CLEANED DATA ---")

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

CLEANED_FILE = OUTPUT_DIR / "cleaned_sales_data.csv"

df.to_csv(CLEANED_FILE, index=False)

print("Cleaned dataset saved to:")
print(CLEANED_FILE)


REPORT_FILE = OUTPUT_DIR / "data_quality_report.csv"

quality_report.to_csv(REPORT_FILE, index=False)

print("\nData quality report saved to:")
print(REPORT_FILE)




print("\n--- CLEANED DATA BUSINESS KPIs ---")

total_revenue = df["Revenue"].sum()

total_orders = df["Order ID"].nunique()

total_quantity = df["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

print(f"Rows in Dataset:     {len(df):,}")
print(f"Unique Orders:       {total_orders:,}")
print(f"Total Revenue:       {total_revenue:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,.2f}")
print(f"Average Order Value: {average_order_value:,.2f}")


df["Order ID"].nunique()
len(df)