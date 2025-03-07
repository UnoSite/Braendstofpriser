"""
Konstantfil for Brændstofpriser integrationen.

Denne fil indeholder:
- Domænenavn for integrationen.
- Konfigurationsnøgler.
- API URL til brændstofpris-data.
- En liste over understøttede brændstofprodukter.
- En omvendt map for produktopslag (fra navn til nøgle).
"""

# Domænenavn for integrationen
DOMAIN = "braendstofpriser"

# Konfigurationsnøgler brugt i config_flow.py
CONF_COMPANIES = "companies"  # Valgte selskaber
CONF_PRODUCTS = "products"  # Valgte brændstofprodukter

# URL til API, der leverer brændstofpriser
API_URL = "https://raw.githubusercontent.com/UnoSite/Braendstofpriser/refs/heads/main/data/listprices.json"

# Dictionary over understøttede brændstofprodukter
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
    "el_lyn": "EL (Turbo)"
}

# Omvendt opslag for produktnavne → nøgler (bruges i config_flow og sensor)
PRODUCT_NAME_MAP = {v: k for k, v in PRODUCTS.items()}
