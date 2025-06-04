"""
Konstantfil for Braendstofpriser integrationen.

Denne fil indeholder:
- Domaenenavn for integrationen.
- Konfigurationsnoegler.
- API URL til braendstofpris-data.
- En liste over understoettede braendstofprodukter.
- En omvendt map for produktopslag (fra navn til noegle).
- En liste af understoettede platforme.
"""

# 🔹 Domaenenavn for integrationen
DOMAIN = "braendstofpriser"
CONF_MANUFACTURER = "UnoSite"
CONF_MODEL = "Brændstofpriser"

# 🔹 Konfigurationsnoegler brugt i config_flow.py
CONF_COMPANIES = "companies"  # Valgte selskaber
CONF_PRODUCTS = "products"  # Valgte braendstofprodukter

# 🔹 URL til API, der leverer braendstofpriser
API_URL = "https://raw.githubusercontent.com/UnoSite/Braendstofpriser/refs/heads/main/data/listprices.json"

# 🔹 Dictionary over understoettede braendstofprodukter
PRODUCTS = {
    "blyfri_92": "Benzin 92 (E5)",
    "blyfri_95_e10": "Benzin 95 (E10)",
    "blyfri_95_plus_e10": "Benzin 95 + (E10)",
    "blyfri_plus_e5": "Benzin 100 (E5)",
    "diesel_b7": "Diesel (B7)",
    "diesel_plus": "Diesel +",
    "hvo_xtl": "HVO (XTL)",
    "el_normal": "EL (Normal)",
    "el_hurtig": "EL (Hurtig)",
    "el_lyn": "EL (Turbo)",
}

# 🔹 Omvendt opslag for produktnavne → noegler (bruges i config_flow og sensor)
#   - Goer det muligt at slaa op fra laeseligt navn til API-noegle
PRODUCT_NAME_MAP = {v: k for k, v in PRODUCTS.items()}

# 🔹 Understoettede platforme (bruges i __init__.py ved async_forward_entry_setups)
SUPPORTED_PLATFORMS = ["sensor"]
