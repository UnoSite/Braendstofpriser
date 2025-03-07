import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_COMPANIES, CONF_PRODUCTS, PRODUCTS
import requests

def fetch_companies():
    response = requests.get("https://raw.githubusercontent.com/UnoSite/Braendstofpriser/refs/heads/main/data/listprices.json")
    data = response.json()
    return sorted(set(entry['selskab'] for entry in data['priser']))

class BraendstofpriserConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self.companies = []

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self.companies = user_input[CONF_COMPANIES]
            return await self.async_step_products()

        companies = await self.hass.async_add_executor_job(fetch_companies)

        schema = vol.Schema({
            vol.Required(CONF_COMPANIES): vol.All(vol.Length(min=1), vol.In(companies))
        })

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={"text": "Her skal du vælge hvilke selskaber du vil have priser fra"}
        )

    async def async_step_products(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Brændstofpriser", data={
                CONF_COMPANIES: self.companies,
                CONF_PRODUCTS: user_input[CONF_PRODUCTS]
            })

        schema = vol.Schema({
            vol.Required(CONF_PRODUCTS): vol.All([vol.In(PRODUCTS.keys())])
        })

        return self.async_show_form(
            step_id="products",
            data_schema=schema,
            description_placeholders={"text": "Her skal du vælge hvilke produkter du vil have priser fra"}
        )
