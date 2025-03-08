import logging
import voluptuous as vol
import requests
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from .const import *

_LOGGER = logging.getLogger(__name__)

def fetch_companies():
    """Henter listen af selskaber fra brændstofpris-API'et."""
    _LOGGER.info("Henter liste over selskaber fra API: %s", API_URL)
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Filtrer selskaber fra API-data
        companies = sorted(set(entry.get('selskab') for entry in data.get('priser', []) if entry.get('selskab')))

        if not companies:
            _LOGGER.warning("API returnerede ingen selskaber.")
        else:
            _LOGGER.debug("Modtaget %d selskaber fra API.", len(companies))

        return {company: company for company in companies}

    except (requests.Timeout, requests.RequestException, ValueError) as err:
        _LOGGER.error("Fejl ved hentning af selskaber: %s", err)
        return {}

class BraendstofpriserConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Håndterer opsætningen af Brændstofpriser integrationen."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Trin 1: Vælg selskaber."""
        if user_input is not None:
            _LOGGER.debug("Brugeren har valgt selskaber: %s", user_input[CONF_COMPANIES])
            self.context["selected_companies"] = user_input[CONF_COMPANIES]
            return await self.async_step_products()

        companies = await self.hass.async_add_executor_job(fetch_companies)
        if not companies:
            _LOGGER.error("Kunne ikke hente selskaber fra API. Afbryder opsætning.")
            return self.async_abort(reason="cannot_connect")

        schema = vol.Schema({
            vol.Required(CONF_COMPANIES, default=[]): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list(companies.keys()),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_products(self, user_input=None):
        """Trin 2: Vælg brændstofprodukter."""
        if user_input is not None:
            _LOGGER.debug("Brugeren har valgt produkter: %s", user_input[CONF_PRODUCTS])
            return self.async_create_entry(title="Brændstofpriser", data={
                CONF_COMPANIES: self.context["selected_companies"],
                CONF_PRODUCTS: [PRODUCT_NAME_MAP[name] for name in user_input[CONF_PRODUCTS]]
            })

        schema = vol.Schema({
            vol.Required(CONF_PRODUCTS, default=[]): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list(PRODUCT_NAME_MAP.keys()),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
        })

        return self.async_show_form(step_id="products", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Returnerer options flow handleren."""
        return BraendstofpriserOptionsFlowHandler(config_entry)

class BraendstofpriserOptionsFlowHandler(config_entries.OptionsFlow):
    """Håndterer ændringer af indstillinger efter opsætning."""

    def __init__(self, config_entry):
        """Gemmer en reference til den aktuelle konfigurationsindgang."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Trin 1: Opdater selskaber."""
        return await self.async_step_select_companies()

    async def async_step_select_companies(self, user_input=None):
        """Trin 1: Opdater valgte selskaber."""
        _LOGGER.info("Reconfiguration: Trin 1 - Vælg selskaber")

        if user_input is not None:
            _LOGGER.debug("Opdaterede selskaber: %s", user_input[CONF_COMPANIES])
            self.hass.config_entries.async_update_entry(self.config_entry, data={
                CONF_COMPANIES: user_input[CONF_COMPANIES],
                CONF_PRODUCTS: self.config_entry.data.get(CONF_PRODUCTS, [])
            })
            return await self.async_step_select_products()

        companies = await self.hass.async_add_executor_job(fetch_companies)

        schema = vol.Schema({
            vol.Required(CONF_COMPANIES, default=self.config_entry.data.get(CONF_COMPANIES, [])): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list(companies.keys()) if companies else [],
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
        })

        return self.async_show_form(step_id="select_companies", data_schema=schema)

    async def async_step_select_products(self, user_input=None):
        """Trin 2: Opdater valgte brændstofprodukter."""
        _LOGGER.info("Reconfiguration: Trin 2 - Vælg brændstofprodukter")

        if user_input is not None:
            _LOGGER.debug("Opdaterede produkter: %s", user_input[CONF_PRODUCTS])
            self.hass.config_entries.async_update_entry(self.config_entry, data={
                CONF_COMPANIES: self.config_entry.data[CONF_COMPANIES],
                CONF_PRODUCTS: [PRODUCT_NAME_MAP[name] for name in user_input[CONF_PRODUCTS]]
            })

            # Genindlæs integrationen for at anvende ændringer
            await self.hass.config_entries.async_reload(self.config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        schema = vol.Schema({
            vol.Required(CONF_PRODUCTS, default=[PRODUCTS[p] for p in self.config_entry.data.get(CONF_PRODUCTS, [])]): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=list(PRODUCT_NAME_MAP.keys()),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
        })

        return self.async_show_form(step_id="select_products", data_schema=schema)
