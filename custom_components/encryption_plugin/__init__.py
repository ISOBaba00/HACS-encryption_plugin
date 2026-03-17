import logging
import asyncio
from homeassistant.core import HomeAssistant, ServiceCall
from .const import DOMAIN, CONF_CODE, CONF_LOCK_TIME, CONF_BRUTE_FORCE

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry):
    conf_sifre = str(entry.data.get(CONF_CODE))
    lock_time = entry.data.get(CONF_LOCK_TIME)
    brute_force = entry.data.get(CONF_BRUTE_FORCE)

    # Durum takibi için değişkenler
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"wrong_attempts": 0, "is_blocked": False}

    # Başlangıç durumu: Kilitli
    hass.states.async_set(f"lock.{DOMAIN}_kasa", "locked", {"friendly_name": "Kasa Kilidi", "icon": "mdi:lock"})

    async def verify_code_service(call: ServiceCall):
        data = hass.data[DOMAIN][entry.entry_id]
        
        if data["is_blocked"]:
            _LOGGER.warning("Sistem blokeli! Deneme reddedildi.")
            return

        girilen = str(call.data.get("entered_code", ""))

        if girilen == conf_sifre:
            _LOGGER.info("Şifre Doğru!")
            data["wrong_attempts"] = 0
            hass.states.async_set(f"lock.{DOMAIN}_kasa", "unlocked", {"icon": "mdi:lock-open"})
            hass.bus.async_fire("encryption_plugin_success")

            # Otomatik Geri Kilitleme
            if lock_time > 0:
                await asyncio.sleep(lock_time)
                hass.states.async_set(f"lock.{DOMAIN}_kasa", "locked", {"icon": "mdi:lock"})
        else:
            data["wrong_attempts"] += 1
            _LOGGER.warning(f"Hatalı Giriş! Deneme: {data['wrong_attempts']}")
            
            if brute_force and data["wrong_attempts"] >= 3:
                data["is_blocked"] = True
                _LOGGER.error("3 Hatalı giriş! 60 saniye bloke edildi.")
                await asyncio.sleep(60)
                data["is_blocked"] = False
                data["wrong_attempts"] = 0

    hass.services.async_register(DOMAIN, "verify_code", verify_code_service)
    return True