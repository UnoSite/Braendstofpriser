import logging
import voluptuous as vol
import requests
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector  # Rettet import her
from .const import *

# Opret logger til integrationen
_LOGGER = logging.getLogger(__name__)

def fetch_companies():
    """
    Henter listen af selskaber fra brændstofpris-API'et.

    - Forsøger at hente data fra `API_URL`.
    - Returnerer en **alfabetisk sorteret** liste af selskaber.
    - Hvis der opstår fejl, returneres en tom liste.

    Returns:
        dict: Dictionary med selskaber til multi-select UI.
    """
    _LOGGER.info("Henter liste over selskaber fra API: %s", API_URL)

    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()

        data = response.json()
        companies = sorted(set(entry['selskab'] for entry in data.get('priser', [])))

        if not companies:
            _LOGGER.warning("API returnerede ingen selskaber.")
        else:
            _LOGGER.debug("Modtaget %d selskaber fra API.", len(companies))

        # Returnér dictionary for UI (Home Assistant multi-select kræver en dict)
        return {company: company for company in companies}

    except requests.Timeout:
        _LOGGER.error("Timeout ved forsøg på at hente selskaber fra API.")
        return {}

    except requests.RequestException as err:
        _LOGGER.error("Netværksfejl ved hentning af selskaber: %s", err)
        return {}

    except ValueError as err:
        _LOGGER.error("Fejl ved parsing af JSON fra API: %s", err)
        return {}

class BraendstofpriserConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Håndterer opsætningen af Brændstofpriser integrationen."""

    VERSION = 1

    def __init__(self):
        self.companies = {}

    async def async_step_user(self, user_input=None):
        """
        Første trin i opsætningen: Vælg selskaber.

        - Henter listen af selskaber fra API'et.
        - Viser en **scrollbar multi-select** UI til valg af selskaber.
        - Hvis ingen selskaber kan hentes, stopper opsætningen.

        Args:
            user_input (dict, optional): Brugerens valg fra UI.

        Returns:
            FlowResult: Næste trin eller fejlmeddelelse.
        """
        _LOGGER.info("Starter opsætning af Brændstofpriser: Trin 1 - Vælg selskaber")

        if user_input is not None:
            _LOGGER.debug("Brugeren har valgt selskaber: %s", user_input[CONF_COMPANIES])
            self.companies = user_input[CONF_COMPANIES]
            return await self.async_step_products()

        # Hent selskaber i en synkron helper
        companies = await self.hass.async_add_executor_job(fetch_companies)

        if not companies:
            _LOGGER.error("Kunne ikke hente selskaber fra API. Afbryder opsætning.")
            return self.async_abort(reason="cannot_connect")

        schema = vol.Schema({
            vol.Required(CONF_COMPANIES): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list(companies.keys()),  # Multi-select med alfabetisk sorteret liste
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,  # Giver en liste med scrollbar
                )
            ),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={"text": "Her skal du vælge hvilke selskaber du vil have priser fra"}
        )

    async def async_step_products(self, user_input=None):
        """
        Andet trin i opsætningen: Vælg brændstofprodukter.

        - Bruger kan vælge hvilke produkter der skal overvåges.
        - Hvis brugeren trykker 'OK', oprettes integrationen.

        Args:
            user_input (dict, optional): Brugerens valg fra UI.

        Returns:
            FlowResult: Gemmer konfiguration eller viser valgmuligheder.
        """
        _LOGGER.info("Opsætning af Brændstofpriser: Trin 2 - Vælg produkter")

        if user_input is not None:
            _LOGGER.debug("Brugeren har valgt produkter: %s", user_input[CONF_PRODUCTS])
            return self.async_create_entry(title="Brændstofpriser", data={
                CONF_COMPANIES: self.companies,
                CONF_PRODUCTS: user_input[CONF_PRODUCTS]
            })

        schema = vol.Schema({
            vol.Required(CONF_PRODUCTS): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list(PRODUCTS.keys()),  # Multi-select med korrekt produktnavne
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
        })

        return self.async_show_form(
            step_id="products",
            data_schema=schema,
            description_placeholders={"text": "Her skal du vælge hvilke produkter du vil have priser fra"}
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Returnerer options flow handleren, så brugeren kan ændre indstillinger senere."""
        return BraendstofpriserOptionsFlowHandler(config_entry)

class BraendstofpriserOptionsFlowHandler(config_entries.OptionsFlow):
    """Håndterer ændringer af indstillinger efter opsætning."""
    
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """
        Viser en menu til at ændre valgte selskaber og produkter.

        - Bruger kan ændre selskaber og produkter uden at slette integrationen.
        - Hvis brugeren trykker 'OK', gemmes de nye indstillinger.

        Args:
            user_input (dict, optional): Brugerens valg fra UI.

        Returns:
            FlowResult: Gemmer ændringerne eller viser valgmuligheder.
        """
        _LOGGER.info("Bruger åbner options flow for Brændstofpriser.")

        if user_input is not None:
            _LOGGER.debug("Brugeren har opdateret indstillinger: %s", user_input)
            return self.async_create_entry(title="", data=user_input)

        companies = await self.hass.async_add_executor_job(fetch_companies)

        schema = vol.Schema({
            vol.Required(CONF_COMPANIES, default=self.config_entry.data.get(CONF_COMPANIES, [])): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list(companies.keys()),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
            vol.Required(CONF_PRODUCTS, default=self.config_entry.data.get(CONF_PRODUCTS, [])): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list(PRODUCTS.keys()),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={"text": "Opdater dine valgte selskaber og produkter"}
    )
