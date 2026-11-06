import logging 

from extract import fetch_xml, parse_xml
from load import load_raw

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

def run(date_str):
    xml_text = fetch_xml(date_str)
    df = parse_xml(xml_text)
    load_raw(df)


if __name__ == "__main__":
    run("06.11.2026")
