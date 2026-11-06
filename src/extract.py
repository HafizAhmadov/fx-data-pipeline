import xml.etree.ElementTree as ET

import pandas as pd
import requests

BASE_URL = "https://cbar.az/currencies/{date}.xml"


def fetch_xml(date_str):
    url = BASE_URL.format(date=date_str)
    response = requests.get(url=url, timeout=30)
    response.raise_for_status()
    return response.text


def parse_xml(xml_text):
    root = ET.fromstring(xml_text)
    rate_date = root.get("Date")

    rows = []
    for val_type in root.findall("ValType"):
        type_name = val_type.get("Type")

        for valute in val_type.findall("Valute"):
            rows.append({
                "rate_date": rate_date,
                "currency_type": type_name,
                "currency_code": valute.get("Code"),
                "currency_name": valute.findtext("Name"),
                "nominal": valute.findtext("Nominal"),
                "rate": float(valute.findtext("Value")),
            })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    xml_text = fetch_xml("06.11.2026")
    df = parse_xml(xml_text)
    print(df.head(10))
    print(f"Total rows: {len(df)}")
