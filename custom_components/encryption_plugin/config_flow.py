import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_CODE, CONF_LOCK_TIME, CONF_BRUTE_FORCE

class EncryptionPluginConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Kasa Sistemi", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_CODE, default="1234"): str,
                vol.Required(CONF_LOCK_TIME, default=30): int,
                vol.Required(CONF_BRUTE_FORCE, default=True): bool,
            })
        )