import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("EIA_API_KEY")

url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"

SERIES = {
    "wti": "RWTC",
    "gasoline": "EER_EPMRU_PF4_RGC_DPG",
    "diesel": "EER_EPD2DXL0_PF4_RGC_DPG",
}



def fetch_series(series_id, length=60):
    
#Pulls the most recent `length` daily records for a given EIA series ID. (similar to crude_balance.py)
#Returns a pandas DataFrame with columns: period, value

    params = [
        ("api_key", API_KEY),
        ("frequency", "daily"),
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

#  pulling all three series
prices = {}

for name, series_id in SERIES.items():
    print(f"Fetching {name} ({series_id})...")
    prices[name] = fetch_series(series_id)

# --- Merge into one table, aligned by date ---
crack = prices["wti"][["period", "value"]].rename(columns={"value": "wti"})

for name in ["gasoline", "diesel"]:
    temp = prices[name][["period", "value"]].rename(columns={"value": name})
    crack = crack.merge(temp, on="period", how="inner")

print(crack.tail(10))