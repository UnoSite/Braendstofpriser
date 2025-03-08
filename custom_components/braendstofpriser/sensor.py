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
    """
    Opsætter sensorer baseret på brugerens valg i config flow.

    - Henter valgte selskaber og produkter fra entry.
    - Opretter en DataUpdateCoordinator til håndtering af API-kald.
    - Tilføjer sensorer til Home Assistant.

    Args:
        hass (HomeAssistant): Home Assistant instansen.
        entry (ConfigEntry): Den konfigurationsindgang, der blev oprettet af brugeren.
        async_add_entities (Callable): Funktion til at tilføje entiteter.

    Returns:
        None
    """
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
        """
        Initialiserer DataUpdateCoordinator.

        - Angiver update-interval til 1 time.
        - Logger opdateringer for at spore API-forbindelse.

        Args:
            hass (HomeAssistant): Home Assistant instansen.
        """
        super().__init__(
            hass,
            logger=_LOGGER,
            name="Brændstofpriser",
            update_interval=timedelta(hours=1)
        )

    async def _async_update_data(self):
        """
        Henter data fra API og håndterer fejl.

        - Logger forsøg på at hente data.
        - Markerer sensorer som "unavailable", hvis data ikke kan hentes.

        Returns:
            list: Brændstofprisdata fra API.

        Raises:
            UpdateFailed: Hvis API-fejl opstår.
        """
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
        """
        Initialiserer en sensor for et specifikt produkt og selskab.

        - Opretter unik ID for enheden.
        - Knytter sensoren til den tilhørende device (selskab).
        - Definerer navn og metadata.

        Args:
            coordinator (FuelPriceCoordinator): Data koordinatoren.
            entry_id (str): ID for config entry.
            company (str): Navnet på selskabet.
            product (str): Koden for produktet.
        """
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
        """
        Returnerer den aktuelle pris.

        - Søger i de hentede API-data efter matchende selskab og produkt.
        - Konverterer værdien til float for bedre statistik-håndtering.

        Returns:
            float | None: Den aktuelle pris, eller None hvis ingen data findes.
        """
        for entry in self.coordinator.data:
            selskab = entry.get("selskab")
            produkt = entry.get("produkt")
            pris = entry.get("pris")

            # Tjek om de nødvendige nøgler findes
            if selskab is None or produkt is None or pris is None:
                _LOGGER.warning("Ugyldig API-data modtaget: %s", entry)
                continue  # Spring dette entry over

            if selskab == self._company and produkt == self._product:
                try:
                    return float(pris)  # Konverter til float
                except (TypeError, ValueError):
                    _LOGGER.error("Ugyldig pris-data modtaget: %s", pris)
                    return None  # Returner None ved fejl

        _LOGGER.warning("Ingen pris fundet for %s", self._attr_name)
        return None

    @property
    def native_unit_of_measurement(self):
        """
        Returnerer enheden for målingen.

        Returns:
            str: "kr."
        """
        return "kr."

    @property
    def extra_state_attributes(self):
        """
        Returnerer ekstra attributter til sensoren.

        Returns:
            dict: Yderligere information om selskab og produkt.
        """
        return {
            "selskab": self._company,
            "produkt": PRODUCTS.get(self._product, self._product)  # Brug læseligt navn
        }
