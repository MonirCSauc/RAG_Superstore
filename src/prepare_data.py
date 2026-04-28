import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/Sample_Superstore.csv")
OUTPUT_PATH = Path("data/sales_documents.csv")


def load_data():
    df = pd.read_csv(DATA_PATH, encoding="latin1")

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

    return df


def create_transaction_documents(df):
    documents = []

    for _, row in df.iterrows():
        text = (
            f"Transaction record: On {row['Order Date'].date()}, customer "
            f"{row['Customer Name']} from the {row['Segment']} segment bought "
            f"{row['Product Name']} in the {row['Category']} category and "
            f"{row['Sub-Category']} sub-category. The order was shipped using "
            f"{row['Ship Mode']} to {row['City']}, {row['State']} in the "
            f"{row['Region']} region. Sales were {row['Sales']:.2f}, quantity "
            f"was {row['Quantity']}, discount was {row['Discount']:.2f}, and "
            f"profit was {row['Profit']:.2f}."
        )

        documents.append({
            "text": text,
            "doc_type": "transaction",
            "date": str(row["Order Date"].date()),
            "year": int(row["Year"]),
            "month": int(row["Month"]),
            "category": row["Category"],
            "sub_category": row["Sub-Category"],
            "region": row["Region"],
            "state": row["State"],
            "city": row["City"]
        })

    return documents


def create_monthly_summary_documents(df):
    documents = []

    monthly = df.groupby("YearMonth").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean"
    }).reset_index()

    for _, row in monthly.iterrows():
        text = (
            f"Monthly sales summary for {row['YearMonth']}: total sales were "
            f"{row['Sales']:.2f}, total profit was {row['Profit']:.2f}, "
            f"total quantity sold was {int(row['Quantity'])}, and average "
            f"discount was {row['Discount']:.2f}."
        )

        documents.append({
            "text": text,
            "doc_type": "monthly_summary",
            "date": row["YearMonth"],
            "year": int(row["YearMonth"][:4]),
            "month": int(row["YearMonth"][5:7]),
            "category": "all",
            "sub_category": "all",
            "region": "all",
            "state": "all",
            "city": "all"
        })

    return documents


def create_category_summary_documents(df):
    documents = []

    category_summary = df.groupby(["Category", "Sub-Category"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean"
    }).reset_index()

    for _, row in category_summary.iterrows():
        profit_margin = row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0

        text = (
            f"Category performance summary: The {row['Sub-Category']} "
            f"sub-category under {row['Category']} generated total sales of "
            f"{row['Sales']:.2f}, total profit of {row['Profit']:.2f}, "
            f"total quantity sold of {int(row['Quantity'])}, average discount "
            f"of {row['Discount']:.2f}, and profit margin of "
            f"{profit_margin:.4f}."
        )

        documents.append({
            "text": text,
            "doc_type": "category_summary",
            "date": "all",
            "year": 0,
            "month": 0,
            "category": row["Category"],
            "sub_category": row["Sub-Category"],
            "region": "all",
            "state": "all",
            "city": "all"
        })

    return documents


def create_region_summary_documents(df):
    documents = []

    region_summary = df.groupby(["Region", "State"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean"
    }).reset_index()

    for _, row in region_summary.iterrows():
        text = (
            f"Regional performance summary: In the {row['Region']} region, "
            f"the state of {row['State']} achieved total sales of "
            f"{row['Sales']:.2f}, total profit of {row['Profit']:.2f}, "
            f"total quantity sold of {int(row['Quantity'])}, and average "
            f"discount of {row['Discount']:.2f}."
        )

        documents.append({
            "text": text,
            "doc_type": "regional_summary",
            "date": "all",
            "year": 0,
            "month": 0,
            "category": "all",
            "sub_category": "all",
            "region": row["Region"],
            "state": row["State"],
            "city": "all"
        })

    return documents

def create_category_total_documents(df):
    documents = []

    category_total = df.groupby("Category").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean"
    }).reset_index()

    for _, row in category_total.iterrows():
        profit_margin = row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0

        text = (
            f"Overall category summary: The {row['Category']} category generated "
            f"total sales of {row['Sales']:.2f}, total profit of {row['Profit']:.2f}, "
            f"total quantity sold of {int(row['Quantity'])}, average discount of "
            f"{row['Discount']:.2f}, and profit margin of {profit_margin:.4f}."
        )

        documents.append({
            "text": text,
            "doc_type": "category_total_summary",
            "date": "all",
            "year": 0,
            "month": 0,
            "category": row["Category"],
            "sub_category": "all",
            "region": "all",
            "state": "all",
            "city": "all"
        })

    return documents

def create_region_total_documents(df):
    documents = []

    region_total = df.groupby("Region").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean"
    }).reset_index()

    for _, row in region_total.iterrows():
        profit_margin = row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0

        text = (
            f"Overall regional summary: The {row['Region']} region generated "
            f"total sales of {row['Sales']:.2f}, total profit of {row['Profit']:.2f}, "
            f"total quantity sold of {int(row['Quantity'])}, average discount of "
            f"{row['Discount']:.2f}, and profit margin of {profit_margin:.4f}."
        )

        documents.append({
            "text": text,
            "doc_type": "region_total_summary",
            "date": "all",
            "year": 0,
            "month": 0,
            "category": "all",
            "sub_category": "all",
            "region": row["Region"],
            "state": "all",
            "city": "all"
        })

    return documents

def create_yearly_summary_documents(df):
    documents = []

    yearly = df.groupby("Year").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean"
    }).reset_index()

    for _, row in yearly.iterrows():
        profit_margin = row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0

        text = (
            f"Yearly sales trend summary: In {int(row['Year'])}, total sales were "
            f"{row['Sales']:.2f}, total profit was {row['Profit']:.2f}, total quantity "
            f"sold was {int(row['Quantity'])}, average discount was {row['Discount']:.2f}, "
            f"and profit margin was {profit_margin:.4f}."
        )

        documents.append({
            "text": text,
            "doc_type": "yearly_summary",
            "date": str(int(row["Year"])),
            "year": int(row["Year"]),
            "month": 0,
            "category": "all",
            "sub_category": "all",
            "region": "all",
            "state": "all",
            "city": "all"
        })

    return documents


def create_month_name_summary_documents(df):
    documents = []

    month_summary = df.groupby("Month").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean"
    }).reset_index()

    for _, row in month_summary.iterrows():
        text = (
            f"Seasonality summary: Across all years, month {int(row['Month'])} generated "
            f"total sales of {row['Sales']:.2f}, total profit of {row['Profit']:.2f}, "
            f"total quantity sold of {int(row['Quantity'])}, and average discount of "
            f"{row['Discount']:.2f}."
        )

        documents.append({
            "text": text,
            "doc_type": "seasonality_summary",
            "date": "all",
            "year": 0,
            "month": int(row["Month"]),
            "category": "all",
            "sub_category": "all",
            "region": "all",
            "state": "all",
            "city": "all"
        })

    return documents


def create_product_discount_documents(df):
    documents = []

    discounted = df[df["Discount"] > 0]

    product_discount = discounted.groupby("Product Name").agg({
        "Discount": ["count", "mean"],
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()

    product_discount.columns = [
        "Product Name", "Discounted Orders", "Average Discount", "Sales", "Profit"
    ]

    product_discount = product_discount.sort_values(
        by="Discounted Orders", ascending=False
    ).head(20)

    for _, row in product_discount.iterrows():
        text = (
            f"Product discount summary: The product '{row['Product Name']}' was sold "
            f"with a discount in {int(row['Discounted Orders'])} orders. Its average "
            f"discount was {row['Average Discount']:.2f}, total discounted sales were "
            f"{row['Sales']:.2f}, and total profit was {row['Profit']:.2f}."
        )

        documents.append({
            "text": text,
            "doc_type": "product_discount_summary",
            "date": "all",
            "year": 0,
            "month": 0,
            "category": "all",
            "sub_category": "all",
            "region": "all",
            "state": "all",
            "city": "all"
        })

    return documents


def create_state_total_documents(df):
    documents = []

    state_total = df.groupby("State").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum",
        "Discount": "mean"
    }).reset_index()

    for _, row in state_total.iterrows():
        text = (
            f"State performance summary: The state of {row['State']} generated total "
            f"sales of {row['Sales']:.2f}, total profit of {row['Profit']:.2f}, "
            f"total quantity sold of {int(row['Quantity'])}, and average discount of "
            f"{row['Discount']:.2f}."
        )

        documents.append({
            "text": text,
            "doc_type": "state_total_summary",
            "date": "all",
            "year": 0,
            "month": 0,
            "category": "all",
            "sub_category": "all",
            "region": "all",
            "state": row["State"],
            "city": "all"
        })

    return documents


def create_city_total_documents(df):
    documents = []

    city_total = df.groupby(["City", "State"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum"
    }).reset_index()

    city_total = city_total.sort_values(by="Sales", ascending=False).head(20)

    for _, row in city_total.iterrows():
        text = (
            f"City performance summary: The city of {row['City']} in {row['State']} "
            f"generated total sales of {row['Sales']:.2f}, total profit of "
            f"{row['Profit']:.2f}, and total quantity sold of {int(row['Quantity'])}."
        )

        documents.append({
            "text": text,
            "doc_type": "city_total_summary",
            "date": "all",
            "year": 0,
            "month": 0,
            "category": "all",
            "sub_category": "all",
            "region": "all",
            "state": row["State"],
            "city": row["City"]
        })

    return documents


def create_category_yearly_trend_documents(df):
    documents = []

    cat_year = df.groupby(["Year", "Category"]).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Quantity": "sum"
    }).reset_index()

    for _, row in cat_year.iterrows():
        text = (
            f"Category yearly trend summary: In {int(row['Year'])}, the "
            f"{row['Category']} category generated total sales of {row['Sales']:.2f}, "
            f"total profit of {row['Profit']:.2f}, and total quantity sold of "
            f"{int(row['Quantity'])}."
        )

        documents.append({
            "text": text,
            "doc_type": "category_yearly_trend",
            "date": str(int(row["Year"])),
            "year": int(row["Year"]),
            "month": 0,
            "category": row["Category"],
            "sub_category": "all",
            "region": "all",
            "state": "all",
            "city": "all"
        })

    return documents

def main():
    df = load_data()

    documents = []
    documents.extend(create_transaction_documents(df))
    documents.extend(create_monthly_summary_documents(df))
    documents.extend(create_category_summary_documents(df))
    documents.extend(create_category_total_documents(df))
    documents.extend(create_region_summary_documents(df))
    documents.extend(create_region_total_documents(df))
    documents.extend(create_yearly_summary_documents(df))
    documents.extend(create_month_name_summary_documents(df))
    documents.extend(create_product_discount_documents(df))
    documents.extend(create_state_total_documents(df))
    documents.extend(create_city_total_documents(df))
    documents.extend(create_category_yearly_trend_documents(df))

    out_df = pd.DataFrame(documents)
    out_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Created {len(out_df)} text documents.")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()