"""Sensor platform for blueprint."""
from homeassistant.helpers.entity import Entity

from .const import ATTRIBUTION, DEFAULT_NAME, DOMAIN_DATA, ICON, VERSION

__version__ = VERSION

async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Setup sensor platform."""
    async_add_entities([QboSensor(hass, discovery_info)], True)


class QboSensor(Entity):
    """qbo Sensor class."""

    def __init__(self, hass, config):
        self.hass = hass
        self.attr = {}
        self._state = None
        self._name = config.get("name", DEFAULT_NAME)

    async def async_update(self):
        """Update the sensor."""
        # Send update "signal" to the component
        await self.hass.data[DOMAIN_DATA]["client"].update_data()


        # Get new data (if any)
        name = self.hass.data[DOMAIN_DATA].get("name", self.name)
        maintenance_status = self.hass.data[DOMAIN_DATA]["maintenance_status"]
        available = self.hass.data[DOMAIN_DATA].get("available", False)
        machine_info = self.hass.data[DOMAIN_DATA].get("machine_info", None)

        if machine_info is not None:
            self._unique_id = machine_info.mac_address.replace(":","_")

        self._name = name
        self._available = available

        # Set/update attributes
        self.attr["attribution"] = ATTRIBUTION
        self.attr["name"] = name

        for key,value in vars(maintenance_status).items():
            self.attr[key[1:]] = value

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def available(self):
        return self._available

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.attr
