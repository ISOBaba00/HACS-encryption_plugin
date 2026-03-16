import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_CODE

class EncryptionPluginConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Şifreleme eklentisi için kurulum akışı."""

    async def async_step_user(self, user_input=None):
        """Kullanıcı arayüzünden ilk kurulum adımı."""
        errors = {}
        if user_input is not None:
            # Kurulum tamamlandığında bu bilgileri kaydet
            return self.async_create_entry(title="Kasa Şifre Sistemi", data=user_input)

        # Kurulum ekranında görünecek form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_CODE): str, # Şifreyi burada soruyoruz
            }),
            errors=errors,
        )