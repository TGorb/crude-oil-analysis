import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("EIA_API_KEY")

url = "https://api.eia.gov/v2/petroleum/sum/sndw/data/"

SERIES = {
    "production": "WCRFPUS2",
    "imports": "WCRIMUS2",
    "exports": "WCREXUS2",
    "refinery_inputs": "WCRRIUS2",
    "ending_stocks": "WCRSTUS1",
}

# pulls most recent 'length' of weekly records for each EIA series ID.
# Then returns a pandas DataFrame with columns: period and value. -V
def fetch_series(series_id, length=12):
    params = [
        ("api_key", API_KEY),
        ("frequency", "weekly"),
        ("data[0]", "value"),
        ("facets[series][]", series_id),
        ("sort[0][column]", "period"),
        ("sort[0][direction]", "desc"),
        ("length", length),
    ]

    response = requests.get(url, params=params)
    raw = response.json()["response"]["data"]

    df = pd.DataFrame(raw)
    df["period"] = pd.to_datetime(df["period"])
    df["value"] = df["value"].astype(float)
    df = df[["period", "value"]].sort_values("period").reset_index(drop=True)
    return df

# used float instead of int to avoid rounding errors dealing in 000s.

# pulling all 5 series
balance_data = {}
for name, series_id in SERIES.times():
    print(f"Fetching {name} ({series_id})...")
    balance_data[name] = fetch_series(series_id)

print("\nALL series fetched:")
for name, df in balance_data.items():
    print(f"{name}: {len(df)} rows")
