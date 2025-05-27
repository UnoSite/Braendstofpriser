import logging
import voluptuous as vol
import requests

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN, API_URL, CONF_PROVIDERS, CONF_PRICE_TYPES

_LOGGER = logging.getLogger(__name__)

def fetch_api_data():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        _LOGGER.error("Fejl ved API-kald: %s", err)
        return {}

class BraendstofpriserV3ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self.context["providers"] = user_input[CONF_PROVIDERS]
            return await self.async_step_price_types()

        data = await self.hass.async_add_executor_job(fetch_api_data)
        providers = sorted(set(entry["provider"] for entry in data.values()))

        schema = vol.Schema({
            vol.Required(CONF_PROVIDERS): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=providers,
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            )
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_price_types(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Brændstofpriser v3",
                data={
                    CONF_PROVIDERS: self.context["providers"],
                    CONF_PRICE_TYPES: user_input[CONF_PRICE_TYPES]
                }
            )

        data = await self.hass.async_add_executor_job(fetch_api_data)
        price_types = sorted(set(entry["price_type"] for entry in data.values()))

        schema = vol.Schema({
            vol.Required(CONF_PRICE_TYPES): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=price_types,
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            )
        })

        return self.async_show_form(step_id="price_types", data_schema=schema)
