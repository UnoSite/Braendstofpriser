import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers import device_registry as dr

from .const import *

# Opret logger til integrationen
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Opsætter integrationen 'Brændstofpriser' fra en config entry.

    Dette kaldes, når brugeren tilføjer integrationen via Home Assistant UI.
    - Lagrer config entry i `hass.data` under `DOMAIN`.
    - Sender opsætningen videre til 'sensor' platformen.

    Args:
        hass (HomeAssistant): Home Assistant instansen.
        entry (ConfigEntry): Den konfigurationsindgang, der er oprettet af brugeren.

    Returns:
        bool: True, hvis opsætningen lykkes.
    """
    _LOGGER.info("Opsætter Brændstofpriser integration for entry: %s", entry.entry_id)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry

    # Forward entry setup til sensor platform
    _LOGGER.debug("Sender opsætning videre til sensor platform")
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    _LOGGER.info("Brændstofpriser integration opsat for entry: %s", entry.entry_id)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Fjerner en konfigurationsindgang for integrationen.

    - Fjerner sensorer tilknyttet denne entry.
    - Fjerner data fra `hass.data` for at frigøre hukommelse.

    Args:
        hass (HomeAssistant): Home Assistant instansen.
        entry (ConfigEntry): Den konfigurationsindgang, der skal fjernes.

    Returns:
        bool: True, hvis afregistreringen lykkes.
    """
    _LOGGER.info("Afregistrerer Brændstofpriser integration for entry: %s", entry.entry_id)

    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    if unload_ok:
        _LOGGER.debug("Fjerner entry fra hass.data")
        hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.info("Brændstofpriser integration afregistreret for entry: %s", entry.entry_id)
    else:
        _LOGGER.warning("Kunne ikke afregistrere Brændstofpriser integration for entry: %s", entry.entry_id)

    return unload_ok
