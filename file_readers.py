import pandas as pd
import json
from collections import defaultdict
import numpy as np
from typing import List, Dict, Any


def read_flight_invoice_report(file_path: str) -> pd.DataFrame:

    df = pd.read_excel(file_path, skiprows=12, header=None)

    df.columns = [
        "Number",
        "Date",
        "Date.1",
        "Number.1",
        "F",
        "J",
        "Y",
        "Goods Value",
        "Galley Serv",
        "Total",
        "Statement",
        "Period",
        "Cd",
    ]

    return df


def read_clean_invoice_report(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path, header=0)

    expected_columns = {"SUPPLIER", "FLIGHT DATE", "FLIGHT NO.", "DEP", "ARR"}
    if not expected_columns.issubset(df.columns):
        raise ValueError("Please share the correct file.")

    df.dropna(how="all", inplace=True)

    df.dropna(axis=1, how="all", inplace=True)

    df.reset_index(drop=True, inplace=True)

    return df


def format_date(date_value) -> str:
    """Formata datas no padrão YYYY-MM-DD"""
    if pd.isna(date_value):
        return None
    try:
        return pd.to_datetime(date_value).strftime('%Y-%m-%d')
    except Exception:
        return None


def read_pricing_inflair(file_path: str) -> List[Dict[str, Any]]:
    df = pd.read_excel(file_path, skiprows=7)

    df.columns = [
        'id', 'airline_code', 'item_code', 'start_date', 'end_date',
        'cost_center', 'unit', 'price', 'currency',
        'created_date', 'created_time', 'created_by',
        'type_of_change', 'statement_period'
    ]

    df = df[df['item_code'].notna()]

    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['start_date'] = df['start_date'].apply(format_date)
    df['created_date'] = df['created_date'].apply(format_date)
    df['price'] = df['price'].round(3)

    df = df.replace({np.nan: None})

    result = df.to_dict(orient='records')

    return result[3:5]


def read_pricing_promeus_with_flight_classes(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(
        file_path,
        sheet_name="Price History Report",
        engine="openpyxl",
        header=None
    )

    records = []
    current_class = None

    for index, row in df.iterrows():
        first_col = row[0]
        service_code = row[2]
        description = row[3]
        currency = row[4]
        price = row[5]

        if (
            pd.isna(service_code)
            and pd.isna(description)
            and pd.isna(currency)
            and pd.isna(price)
            and isinstance(first_col, str)
        ):
            current_class = first_col.strip()
            continue

        if (
            not pd.isna(service_code)
            and not pd.isna(description)
            and not pd.isna(price)
        ):
            records.append(
                {
                    "class": current_class,
                    "facility": first_col,
                    "service_code": service_code,
                    "description": description,
                    "currency": currency,
                    "price": price,
                }
            )
    return records


def group_data_by_class(data):
    grouped_data = defaultdict(list)

    for item in data:
        class_name = item.get("class")
        if (
            not class_name
            or "facility" not in item
            or item["facility"] == "Facility"
        ):
            continue

        item_copy = item.copy()
        item_copy.pop("class")
        grouped_data[class_name].append(item_copy)

    return dict(grouped_data)


def save_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)