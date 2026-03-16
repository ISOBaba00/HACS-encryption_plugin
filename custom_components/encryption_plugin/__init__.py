import logging
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Şifreyi şimdilik kodun içine sabitliyoruz, ileride ayarlardan çekebiliriz.
DOGRU_SIFRE = "1234" 

async def async_setup(hass: HomeAssistant, config: dict):
    """Eklentiyi başlatır ve servisi kaydeder."""

    async def verify_code_service(call: ServiceCall):
        """Şifreyi kontrol eden servis fonksiyonu."""
        girilen = call.data.get("entered_code")

        if girilen == DOGRU_SIFRE:
            _LOGGER.info("Şifre Doğru! Eylem tetikleniyor...")
            # Burada şifre doğruysa ne olacağını belirleyeceğiz.
            # Örn: Bir ışığı aç veya bir event fırlat.
            hass.bus.async_fire("encryption_plugin_success")
        else:
            _LOGGER.warning("Hatalı şifre denemesi: %s", girilen)

    # Servisi Home Assistant'a kaydet
    hass.services.async_register(DOMAIN, "verify_code", verify_code_service)

    return True