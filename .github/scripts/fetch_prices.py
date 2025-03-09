import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

URL = ${{ env.FUELPRICES }}
OUTPUT_FILE = "data/listprices.json"

def fetch_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    # Retry logic in case of temporary issues
    for attempt in range(5):
        try:
            response = requests.get(URL, headers=headers, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            print(f"Forsøg {attempt+1} fejlede: {e}")
            if attempt < 4:
                time.sleep(5)  # Vent 5 sekunder og prøv igen
            else:
                raise Exception(f"Kunne ikke hente data efter 5 forsøg: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')
    table_section = soup.find(id="no-more-tables")
    if not table_section:
        raise Exception("Kunne ikke finde sektionen 'no-more-tables' på siden")

    rows = table_section.find_all("tr")[1:]  # Skip header row

    prices = []

    for row in rows:
        cells = row.find_all("td")
        prices.append({
            "selskab": cells[0].text.strip(),
            "blyfri_92": cells[1].text.strip() or None,
            "blyfri_95_e10": cells[2].text.strip() or None,
            "blyfri_95_plus_e10": cells[3].text.strip() or None,
            "blyfri_plus_e5": cells[4].text.strip() or None,
            "diesel_b7": cells[5].text.strip() or None,
            "diesel_plus": cells[6].text.strip() or None,
            "hvo_xtl": cells[7].text.strip() or None,
            "el_normal": cells[8].text.strip() or None,
            "el_hurtig": cells[9].text.strip() or None,
            "el_lyn": cells[10].text.strip() or None,
            "sidst_opdateret": cells[11].text.strip() or None,
        })

    return prices

def update_json_file(prices):
    now = datetime.now().strftime("%Y-%m-%d")
    data = {
        "seneste_ændring": {
            "dato": now,
            "ændring": {
                "benzin": "N/A",  # Kan udvides med mere logik hvis ønsket
                "diesel": "N/A"
            }
        },
        "priser": prices
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    try:
        prices = fetch_data()
        update_json_file(prices)
        print("Brændstofpriser opdateret og gemt.")
    except Exception as e:
        print(f"Fejl under kørsel: {e}")

if __name__ == "__main__":
    main()
