from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity, UpdateFailed
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN, CONF_COMPANIES, CONF_PRODUCTS, PRODUCTS
from .api import fetch_fuel_data

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id].data
    companies = data[CONF_COMPANIES]
    products = data[CONF_PRODUCTS]

    coordinator = FuelPriceCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for company in companies:
        for product in products:
            entities.append(FuelPriceSensor(coordinator, entry.entry_id, company, product))

    async_add_entities(entities)

class FuelPriceCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data."""

    def __init__(self, hass: HomeAssistant):
        """Initialize coordinator."""
        super().__init__(
            hass,
            logger=hass.logger,
            name="Brændstofpriser",
            update_interval=timedelta(hours=1)
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            data = await self.hass.async_add_executor_job(fetch_fuel_data)
            if not data:
                raise UpdateFailed("No data received from fuel price API")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

class FuelPriceSensor(CoordinatorEntity, SensorEntity):
    """Sensor representing a single product price for a company."""

    def __init__(self, coordinator, entry_id, company, product):
        """Initialize sensor."""
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._company = company
        self._product = product
        self._attr_unique_id = f"{entry_id}_{company}_{product}"
        self._attr_name = f"{company} {PRODUCTS[product]}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry_id}_{company}")},
            name=f"{company} Brændstofpriser",
            manufacturer="Brændstofpriser API",
            model="Brændstofpriser Sensor",
            configuration_url="https://github.com/UnoSite/Braendstofpriser"
        )

    @property
    def native_value(self):
        """Return the current price."""
        for entry in self.coordinator.data:
            if entry['selskab'] == self._company and entry['produkt'] == self._product:
                return float(entry['pris'])  # Returnér som float hvis muligt
        return None  # Ingen pris fundet

    @property
    def native_unit_of_measurement(self):
        """Return unit of measurement."""
        return "kr."

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {
            "selskab": self._company,
            "produkt": PRODUCTS[self._product]
        }
