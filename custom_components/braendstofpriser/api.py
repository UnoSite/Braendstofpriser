import requests
from .const import API_URL

def fetch_fuel_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    return data['priser']
