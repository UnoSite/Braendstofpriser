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
        companies = sorted(set(entry.get('selskab') for entry in data.get('priser', []) if entry.get('selskab')))
        return {company: company for company in companies} if companies else {}
    except (requests.Timeout, requests.RequestException, ValueError) as err:
        _LOGGER.error("Fejl ved hentning af selskaber: %s", err)
        return {}

class BraendstofpriserConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Håndterer opsætningen af Brændstofpriser integrationen."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Trin 1: Vælg selskaber."""
        if user_input is not None:
            self.context["selected_companies"] = user_input[CONF_COMPANIES]
            return await self.async_step_products()

        companies = await self.hass.async_add_executor_job(fetch_companies)
        if not companies:
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
        return BraendstofpriserOptionsFlowHandler()

class BraendstofpriserOptionsFlowHandler(config_entries.OptionsFlow):
    """Håndterer ændringer af indstillinger efter opsætning."""

    async def async_step_init(self, user_input=None):
        """Trin 1: Opdater selskaber."""
        return await self.async_step_select_companies()

    async def async_step_select_products(self, user_input=None):
        """Trin 2: Opdater brændstofprodukter."""
        return self.async_create_entry(title="", data={})
