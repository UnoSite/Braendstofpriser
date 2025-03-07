from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN, CONF_COMPANIES, CONF_PRODUCTS, PRODUCTS
from .api import fetch_fuel_data

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    companies = data[CONF_COMPANIES]
    products = data[CONF_PRODUCTS]

    coordinator = FuelPriceCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for company in companies:
        for product in products:
            entities.append(FuelPriceSensor(coordinator, company, product))

    async_add_entities(entities)

class FuelPriceCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant):
        super().__init__(
            hass,
            logger=hass.logger,
            name="Brændstofpriser",
            update_interval=timedelta(hours=1)
        )

    async def _async_update_data(self):
        return await self.hass.async_add_executor_job(fetch_fuel_data)

class FuelPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, company, product):
        super().__init__(coordinator)
        self._company = company
        self._product = product

    @property
    def name(self):
        return f"{self._company} {PRODUCTS[self._product]}"

    @property
    def unique_id(self):
        return f"braendstofpriser_{self._company}_{self._product}"

    @property
    def state(self):
        for entry in self.coordinator.data:
            if entry['selskab'] == self._company and entry['produkt'] == self._product:
                return f"{entry['pris']} kr."
        return "N/A"
