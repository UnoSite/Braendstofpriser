import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity, UpdateFailed
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, CONF_PROVIDERS, CONF_PRICE_TYPES
from .api import fetch_data

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    config = entry.data
    providers = config.get(CONF_PROVIDERS, [])
    price_types = config.get(CONF_PRICE_TYPES, [])

    coordinator = FuelPriceCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    entities = []

    for item in coordinator.data.values():
        provider = item["provider"]
        price_type = item["price_type"]
        if provider not in providers or price_type not in price_types:
            continue

        device_id = f"{provider}_{price_type}".lower().replace(" ", "_")
        device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=f"{provider} - {price_type}",
            manufacturer=provider,
            model=price_type,
        )

        for product, price in item["prices"].items():
            sensor = FuelPriceSensor(
                coordinator=coordinator,
                unique_id=f"{device_id}_{product}".lower().replace(" ", "_"),
                name=f"{provider} {price_type} {product}",
                device_info=device_info,
                product=product,
                provider=provider,
                price_type=price_type,
                last_updated=item.get("timestamp"),
            )
            entities.append(sensor)

    async_add_entities(entities)

class FuelPriceCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="Brændstofpriser v3",
            update_interval=timedelta(hours=1),
        )

    async def _async_update_data(self):
        data = await self.hass.async_add_executor_job(fetch_data)
        if not data:
            raise UpdateFailed("Ingen data modtaget fra API")
        return data

class FuelPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, unique_id, name, device_info, product, provider, price_type, last_updated):
        super().__init__(coordinator)
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._attr_device_info = device_info
        self._product = product
        self._provider = provider
        self._price_type = price_type
        self._last_updated = last_updated
        self._attr_icon = "mdi:ev-station" if "el" in product.lower() else "mdi:gas-station"
        self._attr_native_unit_of_measurement = "kr."

    @property
    def native_value(self):
        for item in self.coordinator.data.values():
            if item["provider"] == self._provider and item["price_type"] == self._price_type:
                return item["prices"].get(self._product)
        return None

    @property
    def extra_state_attributes(self):
        return {
            "forhandler": self._provider,
            "pristype": self._price_type,
            "produkt": self._product,
            "sidst_opdateret": self._last_updated,
        }
