# Generated from: ETL_pipeline.ipynb
# Converted at: 2026-09-28T23:40:21.147Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

import pandas as pd
from pathlib import Path

import re

import pandas as pd
import numpy as np
from pathlib import Path
import zipfile
import re

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)


INPUT_FILE = Path(r"C:\Users\user\Downloads\Data Samples\Data Samples\latest_monthly_orders_combined2.csv")
OUTPUT_DIR = Path(r"C:\Users\user\Downloads\Data Samples\Data Samples")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MART_DIR = OUTPUT_DIR / "Data_Marts"
MART_DIR.mkdir(parents=True, exist_ok=True)

print("Input:", INPUT_FILE)
print("Output:", OUTPUT_DIR)


df = pd.read_csv(INPUT_FILE)

print("Raw shape:", df.shape)
print("Columns:")
print(df.columns.tolist())
df.head()

# Duplicate Row ID check
print("Duplicate Row IDs:", df["Row ID"].duplicated().sum())

# Null counts
null_report = (
    df.isna()
      .sum()
      .reset_index()
      .rename(columns={"index": "Column", 0: "Null Count"})
)

null_report["Null %"] = (null_report["Null Count"] / len(df) * 100).round(2)
print(null_report[null_report["Null Count"] > 0])


# Blank-string check
blank_counts = {}

for col in df.columns:
    blank_counts[col] = (df[col].astype("string").str.strip() == "").sum()

blank_report = pd.Series(blank_counts, name="Blank Count")
print(blank_report[blank_report > 0])


# A. Missing Profit
missing_profit_mask = df["Profit"].isna()
print("Missing Profit rows:", int(missing_profit_mask.sum()))

# B. Negative Quantity
negative_quantity_mask = df["Quantity"] < 0
print("Negative Quantity rows:", int(negative_quantity_mask.sum()))

# C. Customer IDs associated with multiple states
state_check = df.groupby("Customer ID")["State"].nunique(dropna=True)
multi_state_customer_ids = state_check[state_check > 1].index

customer_multiple_state_mask = df["Customer ID"].isin(multi_state_customer_ids)

print("Affected Customer IDs:", len(multi_state_customer_ids))
print("Affected Row IDs:", df.loc[customer_multiple_state_mask, "Row ID"].nunique())


df.head()

df.shape

df = df.drop_duplicates()

df.info()

#1 data incosistency


df.isna().sum()

#there are 234 nul values in profit


columns = ['Order ID', 'Customer ID', 'Product ID', 
           'Order Date', 'Ship Date', 'Sales']

print(df[columns].isna().sum())

for col in df.columns:
    count = (df[col].astype(str).str.strip() == '').sum()
    print(col, count)


#to make sure no column have an empty string

print("\n Duplicate Row IDs")
print(df['Row ID'].duplicated().sum())


# D. Product IDs associated with multiple Product Names
product_name_check = (
    df.groupby("Product ID")["Product Name"]
      .nunique(dropna=True)
)

conflicting_product_ids = product_name_check[product_name_check > 1].index
product_conflict_mask = df["Product ID"].isin(conflicting_product_ids)

print("Affected Product IDs:", len(conflicting_product_ids))
print("Affected rows:", int(product_conflict_mask.sum()))
print("Conflicting Product IDs:")
print(list(conflicting_product_ids))

#2 data incosistency

print("\n--- Negative/Invalid Values ---")
print("Quantity <= 0:", (df['Quantity'] <= 0).sum())
print("Sales < 0:", (df['Sales'] < 0).sum())
print("Discount < 0:", (df['Discount'] < 0).sum())
print("Discount > 1:", (df['Discount'] > 1).sum())

#there are 4 negative values in quantity


print("\n Ship Mode Values")
print(df['Ship Mode'].value_counts(dropna=False))

#no diference in capatilization between unique values

print("\n Segment Values")
print(df['Segment'].value_counts(dropna=False))

postal_conflicts = postal_conflicts[
    postal_conflicts > 1
]
print(postal_conflicts)


#3 data incosistency



postal_conflicts = (
    df.groupby('Postal Code')['City']
      .nunique()
)

conflict_codes = postal_conflicts[postal_conflicts > 1].index

problematic_rows = df[
    df['Postal Code'].isin(conflict_codes)
].sort_values('Postal Code')

print(problematic_rows[['Row ID', 'Postal Code', 'City']])


# the post cose associated twice with 2 cities, equires validation/SME clarification

#4 data incosistency

# to check if one customer can be associated with more than one state

state_check = df.groupby('Customer ID')['State'].nunique()
print((state_check > 1).sum())

#the location of a customer can change over time , so we may have one order ID 
#of a customer who used to live in dfferent state, to solve it we may spot the order
#id with different state rows, and adopt the state from most updated recods, but
#we need SME validation for this due to the large number of rows and to
#determine whether it's a real business inconsistency

#unresolvable inconsistency

##5 data incosistency
#check if the order date is before dilevery date

print("Order Date after Ship Date:",
      (df['Order Date'] > df['Ship Date']).sum())

#the outcome is unrelaistic, may indicate unified standardization of date format 

print(df['Order Date'].dropna().unique()[:100])


#'08-01-2019' this date formate is different than all other values using DD-MM-YYYY format

print(df['Ship Date'].dropna().unique()[:100])


print(df['Ship Date'].astype(str).str.contains('/').sum())


print(df[df['Order Date'].astype(str).str.contains('/')][
    ['Row ID', 'Order Date', 'Ship Date']
])

#to fix the date error, firt thing is to standardize the 27 in 
# order date column,

df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    format='mixed',
    dayfirst=True
)

df['Ship Date'] = pd.to_datetime(
    df['Ship Date'],
    dayfirst=True
)

print("Order Date after Ship Date:",
      (df['Order Date'] > df['Ship Date']).sum())

#problem solved

#check If each Order ID always have only one unique Customer Name

df.groupby("Order ID")["Customer Name"].nunique().loc[lambda x: x > 1]

# A. Missing Profit
missing_profit_mask = df["Profit"].isna()
print("Missing Profit rows:", int(missing_profit_mask.sum()))

# B. Negative Quantity
negative_quantity_mask = df["Quantity"] < 0
print("Negative Quantity rows:", int(negative_quantity_mask.sum()))

# C. Customer IDs associated with multiple states
state_check = df.groupby("Customer ID")["State"].nunique(dropna=True)
multi_state_customer_ids = state_check[state_check > 1].index

customer_multiple_state_mask = df["Customer ID"].isin(multi_state_customer_ids)

print("Affected Customer IDs:", len(multi_state_customer_ids))
print("Affected Row IDs:", df.loc[customer_multiple_state_mask, "Row ID"].nunique())


# D. Product IDs associated with multiple Product Names
product_name_check = (
    df.groupby("Product ID")["Product Name"]
      .nunique(dropna=True)
)

conflicting_product_ids = product_name_check[product_name_check > 1].index
product_conflict_mask = df["Product ID"].isin(conflicting_product_ids)

print("Affected Product IDs:", len(conflicting_product_ids))
print("Affected rows:", int(product_conflict_mask.sum()))
print("Conflicting Product IDs:")
print(list(conflicting_product_ids))


# E. Inconsistent Order Date formatting
# The dominant source format is DD-MM-YYYY.
# The known non-dominant formats are slash-formatted dates and ISO dates.

order_date_raw = df["Order Date"].astype("string").str.strip()

slash_date_mask = order_date_raw.str.contains(r"/", regex=True, na=False)
iso_date_mask = order_date_raw.str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)

date_format_mask = slash_date_mask | iso_date_mask

print("Slash-formatted Order Date rows:", int(slash_date_mask.sum()))
print("ISO-formatted Order Date rows:", int(iso_date_mask.sum()))
print("Inconsistent Order Date Format rows:", int(date_format_mask.sum()))


# F. Check for invalid business ordering of dates.
# Dates are parsed only for validation here; the actual cleaning happens below.

order_dates_check = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

ship_dates_check = pd.to_datetime(
    df["Ship Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

print(
    "Order Date after Ship Date:",
    int((order_dates_check > ship_dates_check).sum())
)


# Two examples for each issue

examples = {}

examples["Missing Profit"] = (
    df.loc[missing_profit_mask, ["Row ID", "Profit"]]
      .head(2)
)

examples["Negative Quantity"] = (
    df.loc[negative_quantity_mask, ["Row ID", "Quantity"]]
      .head(2)
)

examples["Inconsistent Order Date Format"] = (
    df.loc[date_format_mask, ["Row ID", "Order Date", "Ship Date"]]
      .head(2)
)

examples["Product ID with Multiple Product Names"] = (
    df.loc[product_conflict_mask, ["Row ID", "Product ID", "Product Name"]]
      .drop_duplicates()
      .sort_values(["Product ID", "Row ID"])
      .head(2)
)

examples["Customer ID with Multiple States"] = (
    df.loc[customer_multiple_state_mask, ["Row ID", "Customer ID", "Customer Name", "State"]]
      .drop_duplicates()
      .sort_values(["Customer ID", "Row ID"])
      .head(2)
)

for issue, example_df in examples.items():
    print("\n---", issue, "---")
    display(example_df)


clean_df = df.copy()

# Standardize text
text_columns = [
    "Order ID", "Customer ID", "Customer Name", "Segment",
    "Country", "City", "State", "Region",
    "Product ID", "Product Name", "Category", "Sub-Category",
    "Ship Mode"
]

for col in text_columns:
    clean_df[col] = clean_df[col].astype("string").str.strip()

# Standardize dates
clean_df["Order Date"] = pd.to_datetime(
    clean_df["Order Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

clean_df["Ship Date"] = pd.to_datetime(
    clean_df["Ship Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

# Standardize numeric fields
numeric_columns = [
    "Row ID", "Postal Code", "Sales", "Quantity", "Discount", "Profit"
]

for col in numeric_columns:
    clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce")

print("Rows after technical standardization:", len(clean_df))


# Recalculate masks from the standardized dataframe
missing_profit_mask = clean_df["Profit"].isna()
negative_quantity_mask = clean_df["Quantity"] < 0

product_name_check = (
    clean_df.groupby("Product ID")["Product Name"]
            .nunique(dropna=True)
)
conflicting_product_ids = product_name_check[product_name_check > 1].index
product_conflict_mask = clean_df["Product ID"].isin(conflicting_product_ids)

# Customer multiple-state records are deliberately NOT quarantined.
state_check = clean_df.groupby("Customer ID")["State"].nunique(dropna=True)
multi_state_customer_ids = state_check[state_check > 1].index
customer_multiple_state_mask = clean_df["Customer ID"].isin(multi_state_customer_ids)

quarantine_mask = (
    missing_profit_mask
    | negative_quantity_mask
    | product_conflict_mask
)

quarantine_df = clean_df.loc[quarantine_mask].copy()
warehouse_df = clean_df.loc[~quarantine_mask].copy()

print("Missing Profit:", int(missing_profit_mask.sum()))
print("Negative Quantity:", int(negative_quantity_mask.sum()))
print("Product conflict:", int(product_conflict_mask.sum()))
print("Customer multiple states:", int(customer_multiple_state_mask.sum()))
print("Quarantined rows:", len(quarantine_df))
print("Final warehouse rows:", len(warehouse_df))



# Confirm the expected overlap and final count.
overlap_missing_product = int((missing_profit_mask & product_conflict_mask).sum())

print("Missing Profit ∩ Product Conflict:", overlap_missing_product)
print("Expected quarantine calculation: 234 + 4 + 54 - 1 =", 234 + 4 + 54 - 1)
print("Actual quarantined rows:", len(quarantine_df))

assert overlap_missing_product == 1, "Expected one overlap between Missing Profit and Product conflict."
assert len(quarantine_df) == 291, "Expected 291 quarantined rows."
assert len(warehouse_df) == 9703, "Expected 9,703 final warehouse rows."


warehouse_df = warehouse_df.rename(columns={
    "Product ID": "Product_ID",
    "Product Name": "Product_Name",
    "Customer ID": "Customer_ID",
    "Customer Name": "Customer_Name",
    "Sub-Category": "Sub_Category",
    "Postal Code": "Postal_Code",
    "Order Date": "Order_Date",
    "Ship Date": "Ship_Date",
    "Ship Mode": "Ship_Mode",
    "Row ID": "Row_ID"
})

print("Warehouse source rows:", len(warehouse_df))


# DIM_CATEGORY
dim_category = (
    warehouse_df[["Category", "Sub_Category"]]
    .drop_duplicates()
    .sort_values(["Category", "Sub_Category"])
    .reset_index(drop=True)
)

dim_category.insert(0, "Category_Key", range(1, len(dim_category) + 1))


# DIM_PRODUCT
# Built from the cleaned data so ambiguous product IDs do not violate Product_ID uniqueness.

dim_product = (
    warehouse_df[["Product_ID", "Product_Name", "Category", "Sub_Category"]]
    .drop_duplicates()
    .merge(
        dim_category,
        on=["Category", "Sub_Category"],
        how="left"
    )
    [["Product_ID", "Product_Name", "Category_Key"]]
    .sort_values(["Product_ID", "Product_Name"])
    .reset_index(drop=True)
)

# A product ID must map to exactly one master record.
product_id_counts = dim_product.groupby("Product_ID").size()
assert (product_id_counts > 1).sum() == 0, "DIM_PRODUCT contains duplicate Product_ID values."

dim_product.insert(0, "Product_Key", range(1, len(dim_product) + 1))

print("DIM_PRODUCT rows:", len(dim_product))


# DIM_LOCATION
# Location remains transaction-level so historical delivery geography is preserved.

dim_location = (
    warehouse_df[
        ["Country", "City", "State", "Postal_Code", "Region"]
    ]
    .drop_duplicates()
    .sort_values(["Country", "State", "City", "Postal_Code"])
    .reset_index(drop=True)
)

dim_location.insert(0, "Location_Key", range(1, len(dim_location) + 1))

print("DIM_LOCATION rows:", len(dim_location))


# DIM_DATE
all_dates = pd.concat([
    warehouse_df["Order_Date"],
    warehouse_df["Ship_Date"]
]).dropna().drop_duplicates()

dim_date = pd.DataFrame({
    "Full_Date": pd.to_datetime(all_dates).dt.normalize()
})

dim_date = dim_date.sort_values("Full_Date").drop_duplicates().reset_index(drop=True)

dim_date.insert(
    0,
    "Date_Key",
    dim_date["Full_Date"].dt.strftime("%Y%m%d").astype(int)
)

dim_date["Year"] = dim_date["Full_Date"].dt.year
dim_date["Quarter"] = dim_date["Full_Date"].dt.quarter
dim_date["Month"] = dim_date["Full_Date"].dt.month
dim_date["Month_Name"] = dim_date["Full_Date"].dt.month_name()

dim_date = dim_date[
    ["Date_Key", "Full_Date", "Year", "Quarter", "Month", "Month_Name"]
]

print("DIM_DATE rows:", len(dim_date))


# DIM_SEGMENT
dim_segment = (
    warehouse_df[["Segment"]]
    .drop_duplicates()
    .sort_values("Segment")
    .reset_index(drop=True)
)

dim_segment.insert(0, "Segment_Key", range(1, len(dim_segment) + 1))

print("DIM_SEGMENT rows:", len(dim_segment))


# DIM_CUSTOMER
# Use Segment_Key instead of repeating Segment text, matching the normalized model.

customer_base = (
    warehouse_df[["Customer_ID", "Customer_Name", "Segment"]]
    .drop_duplicates()
)

customer_segment_counts = customer_base.groupby("Customer_ID")["Segment"].nunique()
assert (customer_segment_counts > 1).sum() == 0, (
    "A Customer_ID maps to multiple segments in the cleaned source; SME review is required before "
    "creating a single customer master record."
)

dim_customer = (
    customer_base
    .merge(dim_segment, on="Segment", how="left")
    [["Customer_ID", "Customer_Name", "Segment_Key"]]
    .sort_values("Customer_ID")
    .reset_index(drop=True)
)

dim_customer.insert(0, "Customer_Key", range(1, len(dim_customer) + 1))

print("DIM_CUSTOMER rows:", len(dim_customer))


fact = warehouse_df.copy()

# Connect Product
fact = fact.merge(
    dim_product[["Product_Key", "Product_ID"]],
    on="Product_ID",
    how="left",
    validate="many_to_one"
)

# Connect Customer
fact = fact.merge(
    dim_customer[["Customer_Key", "Customer_ID"]],
    on="Customer_ID",
    how="left",
    validate="many_to_one"
)

# Connect Location
fact = fact.merge(
    dim_location[
        ["Location_Key", "Country", "City", "State", "Postal_Code", "Region"]
    ],
    on=["Country", "City", "State", "Postal_Code", "Region"],
    how="left",
    validate="many_to_one"
)

# Connect Order Date
fact["Order_Date"] = pd.to_datetime(fact["Order_Date"]).dt.normalize()

fact = fact.merge(
    dim_date[["Date_Key", "Full_Date"]],
    left_on="Order_Date",
    right_on="Full_Date",
    how="left",
    validate="many_to_one"
)

fact = fact.rename(columns={"Date_Key": "Order_Date_Key"})
fact = fact.drop(columns=["Full_Date"], errors="ignore")

# Connect Ship Date
fact["Ship_Date"] = pd.to_datetime(fact["Ship_Date"]).dt.normalize()

fact = fact.merge(
    dim_date[["Date_Key", "Full_Date"]],
    left_on="Ship_Date",
    right_on="Full_Date",
    how="left",
    validate="many_to_one"
)

fact = fact.rename(columns={"Date_Key": "Ship_Date_Key"})
fact = fact.drop(columns=["Full_Date"], errors="ignore")

# Connect Segment
fact = fact.merge(
    dim_segment,
    on="Segment",
    how="left",
    validate="many_to_one"
)

# Create Sales_Key
fact.insert(0, "Sales_Key", range(1, len(fact) + 1))

# Final FACT_SALES structure
fact = fact[
    [
        "Sales_Key",
        "Row_ID",
        "Order ID",
        "Product_Key",
        "Customer_Key",
        "Location_Key",
        "Order_Date_Key",
        "Ship_Date_Key",
        "Segment_Key",
        "Ship_Mode",
        "Sales",
        "Quantity",
        "Discount",
        "Profit"
    ]
]

print("FACT_SALES rows:", len(fact))
print("FACT_SALES columns:", fact.columns.tolist())


# Primary-key uniqueness
assert dim_category["Category_Key"].is_unique
assert dim_product["Product_Key"].is_unique
assert dim_product["Product_ID"].is_unique
assert dim_location["Location_Key"].is_unique
assert dim_date["Date_Key"].is_unique
assert dim_segment["Segment_Key"].is_unique
assert dim_customer["Customer_Key"].is_unique
assert dim_customer["Customer_ID"].is_unique
assert fact["Sales_Key"].is_unique
assert fact["Row_ID"].is_unique

# Foreign-key completeness
assert fact["Product_Key"].notna().all()
assert fact["Customer_Key"].notna().all()
assert fact["Location_Key"].notna().all()
assert fact["Order_Date_Key"].notna().all()
assert fact["Ship_Date_Key"].notna().all()
assert fact["Segment_Key"].notna().all()

# Required business-quality checks
assert len(fact) == 9703
assert fact["Profit"].notna().all()
assert (fact["Quantity"] >= 0).all()

print("All key and referential-integrity checks passed.")


marts = {
    "DIM_CATEGORY": dim_category,
    "DIM_PRODUCT": dim_product,
    "DIM_LOCATION": dim_location,
    "DIM_DATE": dim_date,
    "DIM_SEGMENT": dim_segment,
    "DIM_CUSTOMER": dim_customer,
    "FACT_SALES": fact
}

primary_keys = {
    "DIM_CATEGORY": "Category_Key",
    "DIM_PRODUCT": "Product_Key",
    "DIM_LOCATION": "Location_Key",
    "DIM_DATE": "Date_Key",
    "DIM_SEGMENT": "Segment_Key",
    "DIM_CUSTOMER": "Customer_Key",
    "FACT_SALES": "Sales_Key"
}

task6_rows = []

for name, mart in marts.items():
    pk = primary_keys[name]
    distinct_row_id = mart["Row_ID"].nunique() if "Row_ID" in mart.columns else ""

    task6_rows.append({
        "Data Mart System Name": name,
        "Count Rows": len(mart),
        "Count Distinct Primary Key": mart[pk].nunique(),
        "Count Distinct Row ID": distinct_row_id
    })

task6_rows = pd.DataFrame(task6_rows)

display(task6_rows)


INPUT_FILE = Path(r"C:\Users\user\Downloads\Data Samples\Data Samples\latest_monthly_orders_combined2.csv")
OUTPUT_DIR = Path(r"C:\Users\user\Downloads\Data Samples\Data Samples")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MART_DIR = OUTPUT_DIR / "Data_Marts"
MART_DIR.mkdir(parents=True, exist_ok=True)

print("Input:", INPUT_FILE)
print("Output:", OUTPUT_DIR)

print("DIM_DATE actual rows:", len(dim_date))
print("DIM_DATE distinct dates:", dim_date["Full_Date"].nunique())

print(warehouse_df.columns.tolist())

# ============================================================
# CREATE CLEANED WAREHOUSE DATA
# ============================================================

# 1. Find Product IDs that have multiple Product Names
product_check = (
    warehouse_df
    .groupby("Product_ID")["Product_Name"]
    .nunique()
)

conflicting_product_ids = product_check[
    product_check > 1
].index

print("Conflicting Product IDs:", len(conflicting_product_ids))
print("Product IDs:", conflicting_product_ids.tolist())


# 2. Create quarantine mask
#
# Quarantine:
# - Missing Profit
# - Negative Quantity
# - Product ID with multiple Product Names
#
# Do NOT quarantine date-format inconsistencies because
# valid dates will be standardized separately.
quarantine = (
    warehouse_df["Profit"].isna()
    | (warehouse_df["Quantity"] < 0)
    | warehouse_df["Product_ID"].isin(conflicting_product_ids)
)


# 3. Create cleaned warehouse dataset
warehouse_clean = warehouse_df[~quarantine].copy()


# 4. Validation
print("Original rows:", len(warehouse_df))
print("Quarantined rows:", quarantine.sum())
print("Clean rows:", len(warehouse_clean))

# ============================================================
# DIM_CATEGORY
# ============================================================

dim_category = (
    warehouse_clean[["Category", "Sub_Category"]]
    .drop_duplicates()
    .sort_values(["Category", "Sub_Category"])
    .reset_index(drop=True)
)

dim_category.insert(
    0,
    "Category_Key",
    range(1, len(dim_category) + 1)
)

print("DIM_CATEGORY rows:", len(dim_category))

# DIM_PRODUCT
# ============================================================

dim_product = (
    warehouse_clean[
        ["Product_ID", "Product_Name", "Category", "Sub_Category"]
    ]
    .drop_duplicates()
    .merge(
        dim_category,
        on=["Category", "Sub_Category"],
        how="left"
    )
    [
        ["Product_ID", "Product_Name", "Category_Key"]
    ]
    .sort_values(["Product_ID", "Product_Name"])
    .reset_index(drop=True)
)

# Verify Product_ID uniqueness
product_id_counts = dim_product.groupby("Product_ID").size()

assert (product_id_counts > 1).sum() == 0, (
    "DIM_PRODUCT contains duplicate Product_ID values."
)

dim_product.insert(
    0,
    "Product_Key",
    range(1, len(dim_product) + 1)
)

print("DIM_PRODUCT rows:", len(dim_product))
print("Distinct Product_ID:", dim_product["Product_ID"].nunique())

# DIM_LOCATION
# ============================================================

dim_location = (
    warehouse_clean[
        ["Country", "City", "State", "Postal_Code", "Region"]
    ]
    .drop_duplicates()
    .sort_values(
        ["Country", "State", "City", "Postal_Code"]
    )
    .reset_index(drop=True)
)

dim_location.insert(
    0,
    "Location_Key",
    range(1, len(dim_location) + 1)
)

print("DIM_LOCATION rows:", len(dim_location))

# DIM_DATE
# ============================================================

# Standardize Order_Date and Ship_Date
warehouse_clean["Order_Date"] = pd.to_datetime(
    warehouse_clean["Order_Date"],
    errors="coerce"
)

warehouse_clean["Ship_Date"] = pd.to_datetime(
    warehouse_clean["Ship_Date"],
    errors="coerce"
)

all_dates = pd.concat([
    warehouse_clean["Order_Date"],
    warehouse_clean["Ship_Date"]
]).dropna()

dim_date = pd.DataFrame({
    "Full_Date": all_dates.dt.normalize().drop_duplicates()
})

dim_date = (
    dim_date
    .sort_values("Full_Date")
    .reset_index(drop=True)
)

dim_date.insert(
    0,
    "Date_Key",
    dim_date["Full_Date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

dim_date["Year"] = dim_date["Full_Date"].dt.year
dim_date["Quarter"] = dim_date["Full_Date"].dt.quarter
dim_date["Month"] = dim_date["Full_Date"].dt.month
dim_date["Month_Name"] = dim_date["Full_Date"].dt.month_name()

dim_date = dim_date[
    [
        "Date_Key",
        "Full_Date",
        "Year",
        "Quarter",
        "Month",
        "Month_Name"
    ]
]

print("DIM_DATE rows:", len(dim_date))

# ============================================================
# DIM_SEGMENT
# ============================================================

dim_segment = (
    warehouse_clean[["Segment"]]
    .drop_duplicates()
    .sort_values("Segment")
    .reset_index(drop=True)
)

dim_segment.insert(
    0,
    "Segment_Key",
    range(1, len(dim_segment) + 1)
)

print("DIM_SEGMENT rows:", len(dim_segment))

# ============================================================
# DIM_CUSTOMER
# ============================================================

customer_base = (
    warehouse_clean[
        ["Customer_ID", "Customer_Name", "Segment"]
    ]
    .drop_duplicates()
)

customer_segment_counts = (
    customer_base
    .groupby("Customer_ID")["Segment"]
    .nunique()
)

assert (customer_segment_counts > 1).sum() == 0, (
    "A Customer_ID maps to multiple segments in the cleaned "
    "source; SME review is required."
)

dim_customer = (
    customer_base
    .merge(
        dim_segment,
        on="Segment",
        how="left"
    )
    [
        ["Customer_ID", "Customer_Name", "Segment_Key"]
    ]
    .sort_values("Customer_ID")
    .reset_index(drop=True)
)

dim_customer.insert(
    0,
    "Customer_Key",
    range(1, len(dim_customer) + 1)
)

print("DIM_CUSTOMER rows:", len(dim_customer))



all_dates = pd.concat([
    warehouse_clean["Order_Date"],
    warehouse_clean["Ship_Date"]
]).dropna().drop_duplicates()

dim_date = pd.DataFrame({
    "Full_Date": pd.to_datetime(all_dates).dt.normalize()
})

print("DIM_DATE actual rows:", len(dim_date))

print("Distinct Order Dates:",
      warehouse_clean["Order_Date"].dropna().dt.normalize().nunique())

print("Distinct Ship Dates:",
      warehouse_clean["Ship_Date"].dropna().dt.normalize().nunique())

print("Combined distinct dates:",
      pd.concat([
          warehouse_clean["Order_Date"],
          warehouse_clean["Ship_Date"]
      ]).dropna().dt.normalize().nunique())

expected_counts = {
    "DIM_CATEGORY": 17,
    "DIM_PRODUCT": 1880,
    "DIM_LOCATION": 627,
    "DIM_DATE": 1411,
    "DIM_SEGMENT": 3,
    "DIM_CUSTOMER": 793,
    "FACT_SALES": 9703
}

actual_counts = dict(zip(
    task6_rows["Data Mart System Name"],
    task6_rows["Count Rows"]
))

for name, expected in expected_counts.items():
    print(f"{name}: expected={expected}, actual={actual_counts[name]}")
    assert actual_counts[name] == expected, (
        f"{name} count differs from the expected corrected target."
    )

assert fact["Sales_Key"].nunique() == 9703
assert fact["Row_ID"].nunique() == 9703

print("\nAll expected Task 6 counts passed.")

for name, mart in marts.items():
    file_path = MART_DIR / f"{name}.csv"
    mart.to_csv(
        file_path,
        index=False,
        encoding="utf-8-sig"
    )
    print(f"Exported: {file_path}")


# Package all data-mart CSVs
task6_zip = OUTPUT_DIR / "Task_6_1_Data_Marts.zip"

with zipfile.ZipFile(task6_zip, "w", zipfile.ZIP_DEFLATED) as archive:
    for csv_file in sorted(MART_DIR.glob("*.csv")):
        archive.write(csv_file, arcname=csv_file.name)

print("Created:", task6_zip)


task6_rows_file = OUTPUT_DIR / "Task_6_2_Data_Marts_Rows.csv"

task6_rows.to_csv(
    task6_rows_file,
    index=False,
    encoding="utf-8-sig"
)

print("File created:", task6_rows_file)