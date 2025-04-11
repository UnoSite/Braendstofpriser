# Brændstofpriser v3 - Home Assistant integration

> [!Warning]
> This integration is for the Danish market.

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

## 📌 **Overview**

**Brændstofpriser** is a custom integration for Home Assistant that fetches live fuel prices from various providers in Denmark. This integration allows you to monitor up-to-date fuel prices directly in your Home Assistant dashboard.

- Automatically updates fuel prices every hour.
- Supports multiple fuel providers and fuel types.
- Easy setup via the Home Assistant UI.

---

## 🚀 **Features**

✅ Fetches real-time fuel prices from an online API.  
✅ Supports **gasoline, diesel, and electric charging prices**.  
✅ Automatically removes unused entities after reconfiguration.  
✅ Integration updates prices **hourly** via a Home Assistant DataUpdateCoordinator.  
✅ **Fully configurable via Home Assistant UI** – no YAML required!  

---

## 📥 **Installation**

### **🔹 Manual Installation**
1. **Download the latest release** from the [GitHub releases](https://github.com/UnoSite/Braendstofpriser/releases).
2. **Copy the `braendstofpriser` folder** into your Home Assistant `custom_components` directory.
3. **Restart Home Assistant.**
4. **Add the integration:**
   - Navigate to **Settings > Devices & Services > Integrations**.
   - Click **Add Integration** and search for **Brændstofpriser**.

### **🔹 HACS Installation (Recommended)**
1. Add this repository as a **custom repository** in [HACS](https://hacs.xyz/).
2. Search for **Brændstofpriser** in HACS and install the integration.
3. Restart Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=UnoSite&repository=Braendstofpriser&category=Integration)

---

## ⚙️ **Configuration**

Once installed, you can configure the integration directly from the Home Assistant UI.

### **Initial Setup**
1. **Select fuel providers** – Choose which companies' fuel prices you want to track.
2. **Select fuel types** – Choose which fuel products you want to monitor.

### **Reconfiguration**
- If you want to **add or remove providers/products**, simply use the **Reconfigure** option in Home Assistant.
- **Unused entities will be automatically removed** when updating your selections.

---

## 📊 **Supported Fuel Types**
| Fuel Type |
|-------------|
| Benzin 92 (E5) |
| Benzin 95 (E10) |
| Benzin 95+ (E10) |
| Benzin 100 (E5) |
| Diesel (B7) |
| Diesel+ |
| HVO (XTL) |
| EL (Normal) |
| EL (Hurtig) |
| EL (Turbo) |

---

## 🔧 **Updating the Integration**
When a new version is available:
1. **HACS Users** – Update directly from HACS.
2. **Manual Users** – Replace the `braendstofpriser` folder with the latest release and restart Home Assistant.

---

## ❓ **Issues & Support**
If you encounter any issues or have feature requests, please open an issue on GitHub:

[![Static Badge](https://img.shields.io/badge/Report-issues-E00000?style=for-the-badge)](https://github.com/UnoSite/Braendstofpriser/issues)

---

## 📜 **License**
This integration is licensed under the [MIT License](https://github.com/UnoSite/Braendstofpriser/blob/main/LICENSE.md).
