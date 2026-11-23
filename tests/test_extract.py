from pathlib import Path
 
from src.extract import parse_xml

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixtures(name):
    return (FIXTURES / name).read_text(encoding="utf-8")


def test_parse_real_file_returns_expected_shape():
    df = parse_xml(load_fixtures("cbar_2026-11-06.xml"))

    assert len(df) > 30
    assert list(df.columns) == [
        "rate_date", "currency_type", "currency_code",
        "currency_name", "nominal", "rate",
    ]
    assert df["rate_date"].nunique() == 1
    assert "USD" in set(df["currency_code"])

def test_parse_real_file_values():
    df = parse_xml(load_fixtures("cbar_2026-11-06.xml"))

    for rate in list(df["rate"]):
        assert rate > 0
        
    assert df.loc[df["currency_code"] == "USD", "currency_type"].iloc[0] == "Xarici valyutalar"
    assert df.loc[df["currency_code"] == "XAU", "nominal"].iloc[0] == "1 t.u."

