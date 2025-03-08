import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity, UpdateFailed
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import *
from .api import *

# Opret logger til integrationen
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Opsætter sensorer baseret på brugerens valg i config flow."""
    _LOGGER.info("Opsætter brændstofpriser sensorer for entry: %s", entry.entry_id)

    data = hass.data[DOMAIN][entry.entry_id].data
    companies = data[CONF_COMPANIES]
    products = data[CONF_PRODUCTS]

    coordinator = FuelPriceCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for company in companies:
        for product in products:
            _LOGGER.debug("Opretter sensor for %s - %s", company, PRODUCTS.get(product, product))
            entities.append(FuelPriceSensor(coordinator, entry.entry_id, company, product))

    async_add_entities(entities)
    _LOGGER.info("Brændstofpriser sensorer oprettet for entry: %s", entry.entry_id)

class FuelPriceCoordinator(DataUpdateCoordinator):
    """Håndterer API-kald og opdatering af sensorer."""
    def __init__(self, hass: HomeAssistant):
        """Initialiserer DataUpdateCoordinator."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name="Brændstofpriser",
            update_interval=timedelta(hours=1)
        )

    async def _async_update_data(self):
        """Henter data fra API og håndterer fejl."""
        _LOGGER.info("Henter nye brændstofpriser fra API...")
        try:
            data = await self.hass.async_add_executor_job(fetch_fuel_data)
            if not data:
                _LOGGER.warning("Ingen data modtaget fra API!")
                raise UpdateFailed("No data received from fuel price API")
            _LOGGER.debug("Modtaget %d priser fra API.", len(data))
            return data
        except Exception as err:
            _LOGGER.error("Fejl ved hentning af brændstofpriser: %s", err)
            raise UpdateFailed(f"Error fetching data: {err}") from err

class FuelPriceSensor(CoordinatorEntity, SensorEntity):
    """Sensor, der repræsenterer prisen på et produkt fra et selskab."""
    def __init__(self, coordinator, entry_id, company, product):
        """Initialiserer en sensor for et specifikt produkt og selskab."""
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._company = company
        self._product = product
        self._attr_unique_id = f"{entry_id}_{company}_{product}"
        self._attr_name = f"{company} {PRODUCTS.get(product, product)}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{entry_id}_{company}")},
            name=f"{company} Brændstofpriser",
            manufacturer="Brændstofpriser API",
            model="Brændstofpriser Sensor",
            configuration_url="https://github.com/UnoSite/Braendstofpriser"
        )
        _LOGGER.debug("Oprettet sensor: %s", self._attr_name)

    @property
    def native_value(self):
        """Returnerer den aktuelle pris."""
        for entry in self.coordinator.data:
            selskab = entry.get("selskab")
            pris = entry.get(self._product)

            if selskab == self._company and pris and pris != "\u200b":
                try:
                    return float(pris)
                except (TypeError, ValueError):
                    _LOGGER.error("Ugyldig pris-data modtaget: %s", pris)
                    return None
        
        _LOGGER.warning("Ingen pris fundet for %s", self._attr_name)
        return None

    @property
    def native_unit_of_measurement(self):
        """Returnerer enheden for målingen."""
        return "kr."

    @property
    def extra_state_attributes(self):
        """Returnerer ekstra attributter til sensoren."""
        return {
            "selskab": self._company,
            "produkt": PRODUCTS.get(self._product, self._product)
        }
