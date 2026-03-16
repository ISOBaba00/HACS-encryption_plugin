import logging
from homeassistant.core import HomeAssistant, ServiceCall
from .const import DOMAIN, CONF_CODE

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    """Kurulum arayüzünden gelen verilerle eklentiyi başlatır."""
    
    # Kurulumda girilen şifreyi alıyoruz
    sifre = entry.data.get(CONF_CODE)

    async def verify_code_service(call: ServiceCall):
        girilen = call.data.get("entered_code")
        if girilen == sifre:
            _LOGGER.info("Şifre Doğru! Varlık tetikleniyor...")
            hass.bus.async_fire("encryption_plugin_success")
        else:
            _LOGGER.warning("Hatalı şifre!")

    hass.services.async_register(DOMAIN, "verify_code", verify_code_service)
    return True