"""Constants for blueprint."""
# Base component constants
DOMAIN = "qbo"
DOMAIN_DATA = "{}_data".format(DOMAIN)
VERSION = "0.0.1"
PLATFORMS = [ "sensor"]
REQUIRED_FILES = [
    "const.py",
    "manifest.json",
    "sensor.py",
]
ISSUE_URL = "https://github.com/custom-components/qbo/issues"
ATTRIBUTION = "Data from this is provided by qbo."
STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
"""

# Icons
ICON = "mdi:coffee"

# Configuration
CONF_SENSOR = "sensor"
CONF_ENABLED = "enabled"
CONF_NAME = "name"

# Defaults
DEFAULT_NAME = DOMAIN
