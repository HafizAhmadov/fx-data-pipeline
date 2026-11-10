import logging
import time
import xml.etree.ElementTree as ET

import pandas as pd
import requests

logger = logging.getLogger(__name__)

BASE_URL = "https://cbar.az/currencies/{date}.xml"

TIMEOUT = (10, 30)
MAX_ATTEMPTS = 3
BACKOFF_SECONDS = 2
RETRYABLE_STATUS_CODES = [408, 500, 502, 503, 504]

def fetch_xml(date_str):
    url = BASE_URL.format(date=date_str)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(url=url, timeout=TIMEOUT)
        except (requests.exceptions.timeout, requests.exceptions.ConnectionError) as e:
            error = f"Attempt {attempt} failed: {e}"
        else:
            if response.ok:
                return response.text
            if response.status_code not in RETRYABLE_STATUS_CODES:
                response.raise_for_status()
            error = f"HTTP {response.status_code}"
        
        if attempt == MAX_ATTEMPTS:
            raise RuntimeError(f"{date_str}: giving up after {MAX_ATTEMPTS} attempts ({error})")
        
        wait = BACKOFF_SECONDS * 2 ** (attempt - 1)
        logger.warning("%s: attempt %d/%d failed (%s), retrying in %ds",
            date_str, attempt, MAX_ATTEMPTS, error, wait)

        time.sleep(wait)


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
