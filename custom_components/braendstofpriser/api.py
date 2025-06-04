import logging

import requests

from .const import API_URL

# Opret logger til integrationen
_LOGGER = logging.getLogger(__name__)


def fetch_fuel_data():
    """
    Henter braendstofpriser fra det eksterne GitHub JSON API.

    - Forsoeger at hente data fra `API_URL` med en timeout paa 10 sekunder.
    - Validerer API-svaret for at sikre, at det indeholder gyldige data.
    - Returnerer en tom liste, hvis ingen brugbare priser findes.

    Returns:
        list: Liste af braendstofpriser eller en tom liste ved fejl.

    Raises:
        RuntimeError: Hvis der opstaar en netvaerksfejl, JSON-fejl eller ugyldigt svar.
    """
    _LOGGER.info("Henter braendstofpriser fra API: %s", API_URL)

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        # Proev at parse JSON-data
        try:
            data = response.json()
        except ValueError as err:
            _LOGGER.error("Fejl ved parsing af JSON fra API: %s", err)
            raise RuntimeError(f"Fejl ved parsing af JSON fra API: {err}")

        # Tjek om data er en dictionary
        if not isinstance(data, dict):
            _LOGGER.error("API returnerede et ugyldigt JSON-format: %s", data)
            raise RuntimeError("API returnerede et ugyldigt JSON-format")

        # Hent 'priser' fra data
        fuel_prices = data.get("priser", [])
        if not isinstance(fuel_prices, list):
            _LOGGER.error(
                "API returnerede en ugyldig 'priser'-struktur: %s", fuel_prices
            )
            raise RuntimeError("API returnerede en ugyldig 'priser'-struktur")

        # Log hvis ingen priser findes
        if not fuel_prices:
            _LOGGER.warning("API returnerede ingen priser.")
        else:
            _LOGGER.debug("Modtaget %d braendstofpriser fra API.", len(fuel_prices))

        return fuel_prices

    except requests.Timeout:
        _LOGGER.error("Timeout ved forsoeg paa at hente braendstofpriser fra API.")
        raise RuntimeError("Timeout ved hentning af braendstofpriser fra API.")

    except requests.RequestException as err:
        _LOGGER.error("Netvaerksfejl ved hentning af braendstofpriser: %s", err)
        raise RuntimeError(f"Netvaerksfejl ved hentning af braendstofpriser: {err}")
