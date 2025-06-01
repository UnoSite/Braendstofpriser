# Brændstofpriser v3 - Home Assistant integration

[![Version](https://img.shields.io/github/v/release/UnoSite/Braendstofpriser?display_name=tag&style=for-the-badge&color=a4d57c)](https://github.com/UnoSite/Braendstofpriser/releases/latest)
[![Last Commit](https://img.shields.io/github/last-commit/UnoSite/Braendstofpriser?style=for-the-badge&color=a4d57c)](https://github.com/UnoSite/Braendstofpriser/commits/main/)
[![License](https://img.shields.io/github/license/UnoSite/Braendstofpriser?style=for-the-badge&color=a4d57c)](https://github.com/UnoSite/Braendstofpriser/blob/main/LICENSE.md)
[![Code Size](https://img.shields.io/github/languages/code-size/UnoSite/Braendstofpriser?style=for-the-badge&color=a4d57c)](#)
[![Stars](https://img.shields.io/github/stars/UnoSite/Braendstofpriser?style=for-the-badge&color=a4d57c)](#)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/UnoSite/Braendstofpriser/total?style=for-the-badge&color=a4d57c)](#)

![Logo](https://github.com/UnoSite/Braendstofpriser/blob/main/logo.png)

[![Sponsor Github](https://img.shields.io/badge/Sponsor-Github-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=EA4AAA)](https://github.com/sponsors/UnoSite)\
[![Sponsor Buy Me a Coffee](https://img.shields.io/badge/Sponsor-Buy_Me_a_Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=FFDD00)](https://buymeacoffee.com/UnoSite)\
[![Sponsor PayPal.Me](https://img.shields.io/badge/Sponsor-PayPal.ME-003087?style=for-the-badge&logo=paypal&logoColor=003087)](https://paypal.me/UnoSite)

---

## 📃 **Beskrivelse**

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

### 🔹 **HACS Installation (Anbefales)** 
1. Tilføj dette repository som et *brugerdefineret repository* i [HACS](https://hacs.xyz/).
2. Søg efter **Brændstofpriser** i HACS og installer integrationen.
3. Genstart Home Assistant.

[![Installer via hacs.](https://img.shields.io/badge/Install_integration_via-HACS-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore
)](https://my.home-assistant.io/redirect/hacs_repository/?owner=UnoSite&repository=Braendstofpriser&category=Integration)

### 🔹 **Manuel Installation**
1. Download den seneste udgivelse fra [GitHub releases](https://github.com/UnoSite/Braendstofpriser/releases).
2. Kopiér mappen `braendstofpriser` til din Home Assistant `custom_components`-mappe.
3. Genstart Home Assistant.
4. Tilføj integrationen:
   - Gå til *Indstillinger* > *Enheder og Tjenester* > *Integrationer*.
   - Klik på Tilføj Integration og søg efter Brændstofpriser.

---

## ⚙️ **Konfigurering**

Når integrationen er installeret, kan du konfigurere den direkte fra Home Assistant-brugerfladen.

### **Første opsætning**
1. Vælg forhandlere – Vælg hvilke forhandlere du vil overvåge.
2. Vælg type-lister – Vælg hvilke lister du vil overvåge.

### **Genkonfiguration**
- Hvis du vil tilføje eller fjerne forhandlere/lister, skal du blot bruge Genkonfigurer-funktionen i Home Assistant.
- Ubrugte enheder fjernes automatisk, når du opdaterer dine valg.

---

## ⛽ **Tilgængelige forhandlere**

| Forhandlere | Pumpepriser | Listepriser | Ladepriser |
|:------------|:-----------:|:-----------:|:----------:|
| Circle K    | ✅          | ✅          | ✅         |
| Clever      | ⛔          | ⛔          | ✅         |
| E.ON        | ⛔          | ⛔          | ✅         |
| F24         | ✅          | ⛔          | ✅         |
| Go'on       | ✅          | ✅          | ⛔         |
| Ingo        | ✅          | ⛔          | ⛔         |
| Oil!        | ✅          | ✅          | ⛔         |
| OK          | ✅          | ✅          | ✅         |
| Q8          | ✅          | ✅          | ✅         |
| Shell       | ⛔          | ✅          | ✅         |
| UnoX        | ✅          | ✅          | ⛔         |

---

## 🔧 **Opdater integrationen**

Når en ny version er tilgængelig:
1. **HACS-brugere** – Opdater direkte fra HACS.
2. **Manuelle brugere** – Erstat mappen `braendstofpriser` med den nyeste udgivelse og genstart Home Assistant.

---

## ❓ **Anmeld fejl eller få hjælp**

Hvis du støder på problemer eller har forslag til nye funktioner, så opret venligst en issue på GitHub:

[![Static Badge](https://img.shields.io/badge/Report-issues-E00000?style=for-the-badge)](https://github.com/UnoSite/Braendstofpriser/issues)

---

## 📜 **License**

Denne integration er licenseret under [MIT-licensen](https://github.com/UnoSite/Braendstofpriser/blob/main/LICENSE.md).
