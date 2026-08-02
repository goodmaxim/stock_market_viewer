import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime, timezone

RUN = True

if __name__ == "__main__":
    if not RUN:
        exit()
    load_dotenv()

    API_KEY = os.getenv("bit_api_key")
    print(API_KEY[:3], "...", API_KEY[-3:])
    CSV_FILE_PATH = "info.csv"

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    params = {
        "start": 1,
        "limit": 10,
        "convert": "USD",
        }

    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }

    current_time = datetime.now(timezone.utc).isoformat(timespec="minutes")

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed at {current_time} : {e}")
        exit()

    if (response.status_code//100) != 2:
        print(f"Error with code: {response.status_code} and text: {response.text}")
        exit()
        

    data = response.json()
    
    rows = []

    for coin in data["data"]:
        rows.append({
            "Time": current_time,
            "Name": coin["name"],
            "Symbol": coin["symbol"],
            "Price": coin["quote"]["USD"]["price"],
        })

    df = pd.DataFrame(rows)

    add_header = not os.path.exists(CSV_FILE_PATH) or os.path.getsize(CSV_FILE_PATH) == 0
    
    df.to_csv(
        CSV_FILE_PATH,
        mode="a",
        header=add_header,
        index=False
    )
    print(f"Sucessfully saved data for time {current_time}")


    

