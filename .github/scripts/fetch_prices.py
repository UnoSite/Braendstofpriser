import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://www.fuelfinder.dk/listprices.php"
OUTPUT_FILE = "data/listprices.json"

def fetch_data():
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    table_section = soup.find(id="no-more-tables")
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
                "benzin": "N/A",  # Du kan tilføje logik her til at beregne ændringer
                "diesel": "N/A"
            }
        },
        "priser": prices
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    prices = fetch_data()
    update_json_file(prices)

if __name__ == "__main__":
    main()
