import requests
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Registra le entità switch."""
    host = entry.data["host"]
    entities = [
        WallPanelRelay(host, 1),
        WallPanelRelay(host, 2),
        WallPanelIO(host, 1),
        WallPanelIO(host, 2),
    ]
    async_add_entities(entities)

class WallPanelRelay(SwitchEntity):
    def __init__(self, host, relay):
        self._host = host
        self._relay = relay
        self._state = False

    @property
    def unique_id(self):
        return f"wallpanel_relay_{self._host}_{self._relay}"

    @property
    def name(self):
        return f"WallPanel Relay {self._relay}"

    @property
    def is_on(self):
        return self._state

    @property
    def device_info(self):
        """Restituisce le informazioni del dispositivo a cui appartiene l'entità."""
        return {
            "identifiers": {(DOMAIN, self._host)},
            "name": "WallPanel",
            "manufacturer": "WallPanel Manufacturer",
            "model": "WallPanel Model",
            "sw_version": "1.0.0",
        }

    def turn_on(self, **kwargs):
        url = f"http://{self._host}:8080/setRelay?relay={self._relay}&state=true"
        requests.get(url)
        self._state = True

    def turn_off(self, **kwargs):
        url = f"http://{self._host}:8080/setRelay?relay={self._relay}&state=false"
        requests.get(url)
        self._state = False

    def update(self):
        url = f"http://{self._host}:8080/getRelay?relay={self._relay}"
        try:
            response = requests.get(url, timeout=5).text.strip().lower()
            self._state = response == "true"
        except Exception as e:
            _LOGGER.error(f"Errore aggiornamento stato Relay {self._relay}: {e}")

class WallPanelIO(SwitchEntity):
    def __init__(self, host, io):
        self._host = host
        self._io = io
        self._state = False

    @property
    def unique_id(self):
        return f"wallpanel_io_{self._host}_{self._io}"

    @property
    def name(self):
        return f"WallPanel IO {self._io}"

    @property
    def is_on(self):
        return self._state

    @property
    def device_info(self):
        """Restituisce le informazioni del dispositivo a cui appartiene l'entità."""
        return {
            "identifiers": {(DOMAIN, self._host)},
            "name": "WallPanel",
            "manufacturer": "WallPanel Manufacturer",
            "model": "WallPanel Model",
            "sw_version": "1.0.0",
        }

    def turn_on(self, **kwargs):
        url = f"http://{self._host}:8080/setIO?IO={self._io}&state=true"
        response = requests.get(url).text.strip().lower()
        self._state = response == "true"

    def turn_off(self, **kwargs):
        url = f"http://{self._host}:8080/setIO?IO={self._io}&state=false"
        response = requests.get(url).text.strip().lower()
        self._state = response == "false"

    def update(self):
        url = f"http://{self._host}:8080/getIO?IO={self._io}"
        try:
            response = requests.get(url, timeout=5).text.strip().lower()
            self._state = response == "true"
        except Exception as e:
            _LOGGER.error(f"Errore aggiornamento stato IO {self._io}: {e}")
