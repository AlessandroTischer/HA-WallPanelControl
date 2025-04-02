import requests
import logging
from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Registra l'entità Light in Home Assistant."""
    host = entry.data["host"]
    async_add_entities([WallPanelLight(host)])

class WallPanelLight(LightEntity):
    def __init__(self, host):
        self._host = host
        self._state = False
        self._color = "FFFFFF"

    @property
    def unique_id(self):
        return f"wallpanel_light_{self._host}"

    @property
    def name(self):
        return "WallPanel LED"

    @property
    def is_on(self):
        return self._state

    @property
    def supported_color_modes(self):
        return {"rgb"}

    @property
    def rgb_color(self):
        return tuple(int(self._color[i:i+2], 16) for i in (0, 2, 4))

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
        if "rgb_color" in kwargs:
            r, g, b = kwargs["rgb_color"]
            self._color = f"{r:02X}{g:02X}{b:02X}"
        url = f"http://{self._host}:8080/setLED?color={self._color}"
        requests.get(url)
        self._state = True

    def turn_off(self, **kwargs):
        url = f"http://{self._host}:8080/setLED?color=000000"
        requests.get(url)
        self._state = False
