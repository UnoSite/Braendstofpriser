import requests
from .const import API_URL

def fetch_fuel_data():
    """Fetches the fuel prices data from the external GitHub JSON file."""
    try:
        response = requests.get(API_URL, timeout=10)  # Sæt en timeout for bedre stabilitet
        response.raise_for_status()
        data = response.json()
        return data.get('priser', [])  # Returnér en tom liste hvis 'priser' mangler
    except (requests.RequestException, ValueError) as err:
        raise RuntimeError(f"Failed to fetch fuel data: {err}") from err
