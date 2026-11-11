from pathlib import Path
import pandas as pd
import requests
#-----settings-------
URL = "https://api.github.com/orgs/python/repos"

PARAMS = {"per_page": 100}
RECORDS_KEY = None

RENAME = {"stargazers_count": "stars"}
KEEP=["name", "language", "stars", "forks", "open_issues", "size","created_at"]
MUST_HAVE=["language"]

RAW_FILE = Path(__file__).parent / "DATA" / "raw.csv"

#-----functions------

def get_data(url, params):
    """Ask the API for data. Returns the JSON reply, or None if something went wrong."""
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("Could not get the data: ", error)
        return None

def make_table(data, records_key):
    """Turn the JSON reply into a pandas table"""
    records = data[records_key] if records_key else data
    return pd.json_normalize(records, sep="_")

def tidy_data(df):
    """Rename, keep and clean the columns."""
    df = df.rename(columns=RENAME)
    df = df[KEEP]
    df = df.dropna(subset=MUST_HAVE)
    return df

def save_data(df, path):
    """Save the table as a csv file."""
    path.parent.mkdir(exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")

if __name__ =="__main__":
    data = get_data(URL, PARAMS)
    if data is not None:
        table = make_table(data, RECORDS_KEY)
        table = tidy_data(table)
        print(table.head())
        save_data(table, RAW_FILE)