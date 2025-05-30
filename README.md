# Brændstofpriser v3 - Home Assistant integration


[![Version](https://img.shields.io/github/v/release/UnoSite/Braendstofpriser?label=version&style=for-the-badge)](https://github.com/UnoSite/Braendstofpriser/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/UnoSite/Braendstofpriser?style=for-the-badge)](https://github.com/UnoSite/Braendstofpriser/commits/main/)
[![License](https://img.shields.io/github/license/UnoSite/Braendstofpriser?style=for-the-badge)](https://github.com/UnoSite/Braendstofpriser/blob/main/LICENSE.md)
[![Code Size](https://img.shields.io/github/languages/code-size/UnoSite/Braendstofpriser?style=for-the-badge)](#)
[![Stars](https://img.shields.io/github/stars/UnoSite/Braendstofpriser?style=for-the-badge)](#)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/UnoSite/Braendstofpriser/total?style=for-the-badge)](#)

![Logo](https://github.com/UnoSite/Braendstofpriser/blob/main/logo.png)

[![Sponsor Github](https://img.shields.io/badge/Sponsor-Github-EA4AAA?style=for-the-badge&logo=githubsponsors)](https://github.com/sponsors/UnoSite)\
[![Sponsor Buy Me a Coffee](https://img.shields.io/badge/Sponsor-By%20me%20a%20coffee-FFDD00?style=for-the-badge&logo=buymeacoffee)](https://buymeacoffee.com/UnoSite)\
[![Sponsor PayPal.Me](https://img.shields.io/badge/Sponsor-paypal.me-003087?style=for-the-badge&logo=paypal)](https://paypal.me/UnoSite)

---

## 📌 **Beskrivelse**

**Brændstofpriser** er en custom integration til Home Assistant, der henter live brændstofpriser fra forskellige udbydere i Danmark. Denne integration gør det muligt at overvåge opdaterede brændstofpriser direkte i dit Home Assistant-dashboard.

- Opdaterer brændstofpriser automatisk hver time.
- Understøtter flere brændstofudbydere og brændstoftyper.
- Nem opsætning via Home Assistant-brugerfladen.

---

## 🚀 **Funktioner**

- Henter brændstofpriser i realtid fra et online API.
- Understøtter benzin-, diesel- og el-ladepriser.
- Fjerner automatisk ubrugte enheder efter en ny konfiguration.
- Integration opdaterer priser hver time via en Home Assistant DataUpdateCoordinator.
- Fuldt konfigurerbar via Home Assistant-brugerfladen – ingen YAML nødvendig!

---

## 📥 **Installation**

### **🔹 Manuel Installation**
1. **Download the latest release** from the [GitHub releases](https://github.com/UnoSite/Braendstofpriser/releases).
2. **Copy the `braendstofpriser` folder** into your Home Assistant `custom_components` directory.
3. **Restart Home Assistant.**
4. **Add the integration:**
   - Navigate to **Settings > Devices & Services > Integrations**.
   - Click **Add Integration** and search for **Brændstofpriser**.

### **🔹 HACS Installation (Anbefales)**
1. Add this repository as a **custom repository** in [HACS](https://hacs.xyz/).
2. Search for **Brændstofpriser** in HACS and install the integration.
3. Restart Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=UnoSite&repository=Braendstofpriser&category=Integration)

---

## ⚙️ **Konfigurering**

Once installed, you can configure the integration directly from the Home Assistant UI.

### **Initial Setup**
1. **Select fuel providers** – Choose which companies' fuel prices you want to track.
2. **Select fuel types** – Choose which fuel products you want to monitor.

### **Reconfiguration**
- If you want to **add or remove providers/products**, simply use the **Reconfigure** option in Home Assistant.
- **Unused entities will be automatically removed** when updating your selections.

---

## ⛽ **Tilgængelige brændstof typer**
| Brændstof typer |
|-------------|
| Benzin 92 (E5) |
| Benzin 95 (E10) |
| Benzin 95+ (E10) |
| Benzin 100 (E5) |
| Diesel (B7) |
| Diesel+ (B7) |
| HVO (XTL) |
| EL (Normal) |
| EL (Hurtig) |
| EL (Lyn) |

---

## 🔧 **Opdater integrationen**
When a new version is available:
1. **HACS Users** – Update directly from HACS.
2. **Manual Users** – Replace the `braendstofpriser` folder with the latest release and restart Home Assistant.

---

## ❓ **Anmeld fejl eller få hjælp**
If you encounter any issues or have feature requests, please open an issue on GitHub:

[![Static Badge](https://img.shields.io/badge/Report-issues-E00000?style=for-the-badge)](https://github.com/UnoSite/Braendstofpriser/issues)

---

## 📜 **License**
This integration is licensed under the [MIT License](https://github.com/UnoSite/Braendstofpriser/blob/main/LICENSE.md).
