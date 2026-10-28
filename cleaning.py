import pandas as pd
import numpy as np

df = pd.read_csv("dirty_cafe_sales.csv")

# Step 1: Replace ERROR and UNKNOWN with NaN in all columns
df = df.replace(["ERROR", "UNKNOWN"], np.nan)

# Step 2: Check how many missing values now
print(df.shape)
print(df.isnull().sum())

# Step 3: Convert numeric columns to proper types
df["Quantity"] = pd.to_numeric(df["Quantity"])
df["Price Per Unit"] = pd.to_numeric(df["Price Per Unit"])
df["Total Spent"] = pd.to_numeric(df["Total Spent"])

print(df.dtypes)

# Step 4: Fill Total Spent where possible (Quantity × Price Per Unit)
mask = df["Total Spent"].isnull() & df["Quantity"].notnull(
) & df["Price Per Unit"].notnull()
df.loc[mask, "Total Spent"] = df.loc[mask, "Quantity"] * \
    df.loc[mask, "Price Per Unit"]

print(df["Total Spent"].isnull().sum())

# Step 5:
mask = df["Quantity"].isnull() & df["Total Spent"].notnull(
) & df["Price Per Unit"].notnull()
df.loc[mask, "Quantity"] = df.loc[mask, "Total Spent"] / \
    df.loc[mask, "Price Per Unit"]

print(df["Quantity"].isnull().sum())


# Step 6:
mask = df["Price Per Unit"].isnull(
) & df["Total Spent"].notnull() & df["Quantity"].notnull()
df.loc[mask, "Price Per Unit"] = df.loc[mask,
                                        "Total Spent"] / df.loc[mask, "Quantity"]

print(df["Price Per Unit"].isnull().sum())

# Step 7: Convert Transaction Date to datetime
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
print(df["Transaction Date"].dtype)


# Step 8: Fill Item based on Price Per Unit
price_to_item = {1.0: "Cookie", 1.5: "Tea", 2: "Coffee", 5: "Salad"}
mask = df["Item"].isnull() & df["Price Per Unit"].isin(price_to_item.keys())
df.loc[mask, "Item"] = df.loc[mask, "Price Per Unit"].map(price_to_item)

print(df["Item"].isnull().sum())

df = df.dropna(subset=["Item", "Quantity",
               "Price Per Unit", "Total Spent", "Transaction Date"])
print(df.shape)
print(df.isnull().sum())

df["Payment Method"] = df["Payment Method"].fillna("Unknown")
df["Location"] = df["Location"].fillna("Unknown")
print(df.isnull().sum())

df.to_csv("cleaned_cafe_sales.csv", index=False)
