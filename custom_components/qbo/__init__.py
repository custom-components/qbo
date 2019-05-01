"""
Component to integrate with blueprint.

For more details about this component, please refer to
https://github.com/custom-components/blueprint
"""
import logging
import os
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_URL
from homeassistant.helpers import discovery
from homeassistant.util import Throttle

from .const import (CONF_ENABLED, CONF_NAME, CONF_SENSOR, DEFAULT_NAME, DOMAIN,
                    DOMAIN_DATA, ISSUE_URL, PLATFORMS, REQUIRED_FILES, STARTUP,
                    VERSION)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)

SENSOR_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_ENABLED, default=True): cv.boolean,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_URL): cv.string,
                vol.Optional(CONF_SENSOR): vol.All(cv.ensure_list, [SENSOR_SCHEMA]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up this component."""
    # Import client from a external python package hosted on PyPi
    from qbo import Qbo

    # Print startup message
    startup = STARTUP.format(name=DOMAIN, version=VERSION, issueurl=ISSUE_URL)
    _LOGGER.info(startup)

    # Check that all required files are present
    file_check = await check_files(hass)
    if not file_check:
        return False

    # Create DATA dict
    hass.data[DOMAIN_DATA] = {}

    # Get "global" configuration.
    url = config[DOMAIN].get(CONF_URL)

    # Configure the client.
    client = Qbo(url)
    hass.data[DOMAIN_DATA]["client"] = QboData(hass, client)

    # Load platforms
    for platform in PLATFORMS:
        # Get platform specific configuration
        platform_config = config[DOMAIN].get(platform, {})

        # If platform is not enabled, skip.
        if not platform_config:
            continue

        for entry in platform_config:
            entry_config = entry
            _LOGGER.critical(entry_config)

            # If entry is not enabled, skip.
            if not entry_config[CONF_ENABLED]:
                continue

            hass.async_create_task(
                discovery.async_load_platform(
                    hass, platform, DOMAIN, entry_config, config
                )
            )
    return True


class QboData:
    """This class handle communication and stores the data."""

    def __init__(self, hass, client):
        """Initialize the class."""
        self.hass = hass
        self.client = client

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update_data(self):
        import requests.exceptions
        """Update data."""
        # This is where the main logic to update platform data goes.
        try:
            name = self.client.name()
            maintenance_status = self.client.maintenance_status()
            machine_info = self.client.machine_info()

            self.hass.data[DOMAIN_DATA]["name"] = name
            self.hass.data[DOMAIN_DATA]["maintenance_status"] = maintenance_status
            self.hass.data[DOMAIN_DATA]["machine_info"] = machine_info

            self.hass.data[DOMAIN_DATA]["available"] = True
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
            _LOGGER.error("Could not reach host - %s", error)
            self.hass.data[DOMAIN_DATA]["available"] = False
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error("Could not update data - %s", error)


async def check_files(hass):
    """Return bool that indicates if all files are present."""
    # Verify that the user downloaded all files.
    base = "{}/custom_components/{}/".format(hass.config.path(), DOMAIN)
    missing = []
    for file in REQUIRED_FILES:
        fullpath = "{}{}".format(base, file)
        if not os.path.exists(fullpath):
            missing.append(file)

    if missing:
        _LOGGER.critical("The following files are missing: %s", str(missing))
        returnvalue = False
    else:
        returnvalue = True

    return returnvalue
