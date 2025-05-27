import logging
import requests
from .const import API_URL

_LOGGER = logging.getLogger(__name__)

def fetch_data():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        _LOGGER.error("Fejl ved hentning af brændstofdata: %s", e)
        return {}
