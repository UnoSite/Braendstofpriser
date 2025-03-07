import voluptuous as vol
import requests
from homeassistant import config_entries
from homeassistant.core import callback
from .const import *

async def fetch_companies():
    """Fetch the list of companies from the fuel price API."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return sorted(set(entry['selskab'] for entry in data.get('priser', [])))
    except (requests.RequestException, ValueError) as err:
        return []

class BraendstofpriserConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Brændstofpriser integration."""
    
    VERSION = 1

    def __init__(self):
        self.companies = []

    async def async_step_user(self, user_input=None):
        """Step 1: Select companies."""
        if user_input is not None:
            self.companies = user_input[CONF_COMPANIES]
            return await self.async_step_products()

        companies = await self.hass.async_add_executor_job(fetch_companies)

        if not companies:
            return self.async_abort(reason="cannot_connect")

        schema = vol.Schema({
            vol.Required(CONF_COMPANIES): vol.All(vol.Length(min=1), vol.In(companies))
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={"text": "Her skal du vælge hvilke selskaber du vil have priser fra"}
        )

    async def async_step_products(self, user_input=None):
        """Step 2: Select products."""
        if user_input is not None:
            return self.async_create_entry(title="Brændstofpriser", data={
                CONF_COMPANIES: self.companies,
                CONF_PRODUCTS: user_input[CONF_PRODUCTS]
            })

        schema = vol.Schema({
            vol.Required(CONF_PRODUCTS): vol.All(vol.Length(min=1), [vol.In(PRODUCTS.keys())])
        })

        return self.async_show_form(
            step_id="products",
            data_schema=schema,
            description_placeholders={"text": "Her skal du vælge hvilke produkter du vil have priser fra"}
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return BraendstofpriserOptionsFlowHandler(config_entry)

class BraendstofpriserOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow."""
    
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Optional(CONF_COMPANIES, default=self.config_entry.data.get(CONF_COMPANIES, [])): vol.All(vol.Length(min=1), [str]),
            vol.Optional(CONF_PRODUCTS, default=self.config_entry.data.get(CONF_PRODUCTS, [])): vol.All(vol.Length(min=1), [vol.In(PRODUCTS.keys())])
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders={"text": "Opdater dine valgte selskaber og produkter"}
        )
