import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, SUPPORTED_PLATFORMS

# Opret logger til integrationen
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Opsaetter integrationen 'Braendstofpriser' fra en config entry.

    Dette kaldes, naar brugeren tilfoejer integrationen via Home Assistant UI.
    - Lagrer config entry i `hass.data` under `DOMAIN`.
    - Forwarder opsaetningen til de understoettede platforme.

    Args:
        hass (HomeAssistant): Home Assistant instansen.
        entry (ConfigEntry): Den konfigurationsindgang, der er oprettet af brugeren.

    Returns:
        bool: True, hvis opsaetningen lykkes.
    """
    _LOGGER.info("Opsaetter Braendstofpriser integration for entry: %s", entry.entry_id)

    # Opret domaenedata hvis det ikke findes
    hass.data.setdefault(DOMAIN, {})

    # Gem konfigurationsindgangen
    hass.data[DOMAIN][entry.entry_id] = entry

    # Forward opsaetning til platforme
    try:
        await hass.config_entries.async_forward_entry_setups(entry, SUPPORTED_PLATFORMS)
        _LOGGER.info("Braendstofpriser integration opsat for entry: %s", entry.entry_id)
        return True
    except Exception as err:
        _LOGGER.error("Fejl under opsaetning af Braendstofpriser: %s", err)
        return False

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """
    Fjerner en konfigurationsindgang for integrationen.

    - Fjerner alle platforme tilknyttet denne entry.
    - Rydder `hass.data` for at frigoere hukommelse.

    Args:
        hass (HomeAssistant): Home Assistant instansen.
        entry (ConfigEntry): Den konfigurationsindgang, der skal fjernes.

    Returns:
        bool: True, hvis afregistreringen lykkes.
    """
    _LOGGER.info("Afregistrerer Braendstofpriser integration for entry: %s", entry.entry_id)

    try:
        unload_ok = await hass.config_entries.async_unload_platforms(entry, SUPPORTED_PLATFORMS)
        if unload_ok:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            _LOGGER.info("Braendstofpriser integration afregistreret for entry: %s", entry.entry_id)
        else:
            _LOGGER.warning("Kunne ikke afregistrere Braendstofpriser integration for entry: %s", entry.entry_id)
        return unload_ok
    except Exception as err:
        _LOGGER.error("Fejl under afregistrering af Braendstofpriser: %s", err)
        return False
