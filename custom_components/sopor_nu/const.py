"""Constants for the Sopor.nu integration."""

from typing import Final

DOMAIN: Final = "sopor_nu"

API_BASE_URL: Final = (
    "https://avfallshubben.avfallsverige.se/umbraco/Api/SoporApi/"
)

CONF_STATION_ID: Final = "station_id"
CONF_MUNICIPALITY_CODE: Final = "municipality_code"
CONF_STATION_NAME: Final = "station_name"

DEFAULT_SCAN_INTERVAL: Final = 21600  # 6 hours in seconds

# serviceType values from the API
SERVICE_TYPE_PAPER_PACKAGING: Final = 1
SERVICE_TYPE_PLASTIC_PACKAGING: Final = 2
SERVICE_TYPE_METAL_PACKAGING: Final = 3
SERVICE_TYPE_GLASS_CLEAR: Final = 4
SERVICE_TYPE_GLASS_COLORED: Final = 5
SERVICE_TYPE_NEWSPAPERS: Final = 6
SERVICE_TYPE_BATTERIES: Final = 7
SERVICE_TYPE_TEXTILES: Final = 8
SERVICE_TYPE_CLEANING: Final = 9
SERVICE_TYPE_SNOW_REMOVAL: Final = 10

SERVICE_TYPE_NAMES: Final = {
    SERVICE_TYPE_PAPER_PACKAGING: "Paper packaging",
    SERVICE_TYPE_PLASTIC_PACKAGING: "Plastic packaging",
    SERVICE_TYPE_METAL_PACKAGING: "Metal packaging",
    SERVICE_TYPE_GLASS_CLEAR: "Clear glass packaging",
    SERVICE_TYPE_GLASS_COLORED: "Colored glass packaging",
    SERVICE_TYPE_NEWSPAPERS: "Newspapers",
    SERVICE_TYPE_BATTERIES: "Batteries",
    SERVICE_TYPE_TEXTILES: "Textiles",
    SERVICE_TYPE_CLEANING: "Cleaning",
    SERVICE_TYPE_SNOW_REMOVAL: "Snow removal",
}

SERVICE_TYPE_NAMES_SV: Final = {
    SERVICE_TYPE_PAPER_PACKAGING: "Pappersförpackningar",
    SERVICE_TYPE_PLASTIC_PACKAGING: "Plastförpackningar",
    SERVICE_TYPE_METAL_PACKAGING: "Metallförpackningar",
    SERVICE_TYPE_GLASS_CLEAR: "Ofärgade glasförpackningar",
    SERVICE_TYPE_GLASS_COLORED: "Färgade glasförpackningar",
    SERVICE_TYPE_NEWSPAPERS: "Tidningar",
    SERVICE_TYPE_BATTERIES: "Batterier",
    SERVICE_TYPE_TEXTILES: "Textilier",
    SERVICE_TYPE_CLEANING: "Städning",
    SERVICE_TYPE_SNOW_REMOVAL: "Snöröjning",
}

SERVICE_TYPE_ICONS: Final = {
    SERVICE_TYPE_PAPER_PACKAGING: "mdi:package-variant",
    SERVICE_TYPE_PLASTIC_PACKAGING: "mdi:bottle-soda-outline",
    SERVICE_TYPE_METAL_PACKAGING: "mdi:food-fork-drink",
    SERVICE_TYPE_GLASS_CLEAR: "mdi:bottle-wine-outline",
    SERVICE_TYPE_GLASS_COLORED: "mdi:bottle-wine",
    SERVICE_TYPE_NEWSPAPERS: "mdi:newspaper",
    SERVICE_TYPE_BATTERIES: "mdi:battery",
    SERVICE_TYPE_TEXTILES: "mdi:tshirt-crew",
    SERVICE_TYPE_CLEANING: "mdi:broom",
    SERVICE_TYPE_SNOW_REMOVAL: "mdi:snowflake",
}
