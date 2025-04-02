import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from . import DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema({vol.Required("host"): str})

class WallPanelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configura l'integrazione WallPanel tramite UI."""

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Mostra il form per l'inserimento dei dati."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)

        return self.async_create_entry(title="WallPanel", data=user_input, options={"entities": ["light", "relay1", "relay2", "io1", "io2"]})
