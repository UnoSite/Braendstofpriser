import logging
import requests
from .const import *

# Opret logger til integrationen
_LOGGER = logging.getLogger(__name__)

def fetch_fuel_data():
    """
    Henter brændstofpriser fra det eksterne GitHub JSON API.

    - Forsøger at hente data fra `API_URL`.
    - Timeout på 10 sekunder for at forhindre lange svartider.
    - Returnerer en tom liste hvis 'priser' ikke findes i svaret.

    Returns:
        list: Liste af brændstofpriser eller en tom liste ved fejl.
    
    Raises:
        RuntimeError: Hvis der opstår en netværksfejl, JSON-fejl eller ugyldigt svar.
    """
    _LOGGER.info("Henter brændstofpriser fra API: %s", API_URL)

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict):  # Sikrer at svaret er et dictionary
            _LOGGER.error("API returnerede et ugyldigt JSON-format: %s", data)
            raise RuntimeError("API returnerede et ugyldigt JSON-format")

        fuel_prices = data.get('priser', [])
        if not isinstance(fuel_prices, list):  # Sikrer at 'priser' er en liste
            _LOGGER.error("API returnerede en ugyldig 'priser'-struktur: %s", fuel_prices)
            raise RuntimeError("API returnerede en ugyldig 'priser'-struktur")

        if not fuel_prices:
            _LOGGER.warning("API returnerede ingen priser.")
        else:
            _LOGGER.debug("Modtaget %d brændstofpriser fra API.", len(fuel_prices))

        return fuel_prices

    except requests.Timeout:
        _LOGGER.error("Timeout ved forsøg på at hente brændstofpriser fra API.")
        raise RuntimeError("Timeout ved hentning af brændstofpriser fra API.")

    except requests.RequestException as err:
        _LOGGER.error("Netværksfejl ved hentning af brændstofpriser: %s", err)
        raise RuntimeError(f"Netværksfejl ved hentning af brændstofpriser: {err}")

    except ValueError as err:
        _LOGGER.error("Fejl ved parsing af JSON fra API: %s", err)
        raise RuntimeError(f"Fejl ved parsing af JSON fra API: {err}")
