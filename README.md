**simple Solar Surplus EV Charger Controller**

This project allows surplus solar power from a small photovoltaic system (“Balkonkraftwerk”) to be used for charging an electric vehicle. It uses Tasmota NOUS A1T smart plugs controlled via MQTT (Mosquitto) running on a Raspberry Pi. The system switches the charger on when solar production exceeds a configurable threshold and turns it off when it drops below a defined hysteresis value, preventing rapid on/off cycling. The charger’s minimum current can be set (e.g., 6 A) to ensure most EVs will start charging. Currently, it only considers solar generation, not household consumption, but this could be added in the future.

Features:

Surplus-based EV charging

Configurable thresholds, hysteresis, and cycle time

Works with Tasmota smart plugs and MQTT

Minimal setup using a simple INI configuration please edit for your own needs


**einfaches Überschussladen für E-Autos mit Solarstrom**

Dieses Projekt ermöglicht es, überschüssigen Strom eines kleinen Balkonkraftwerks zum Laden eines Elektroautos zu nutzen. Es verwendet Tasmota NOUS A1T Steckdosen, gesteuert über MQTT (Mosquitto) auf einem Raspberry Pi. Der Ladeprozess wird aktiviert, wenn die Solarproduktion einen konfigurierbaren Schwellenwert überschreitet, und abgeschaltet, wenn die Leistung unter einen definierten Hysterese-Wert fällt, um häufiges Ein- und Ausschalten zu verhindern. Der minimale Ladestrom des Ladeziegels kann eingestellt werden (z. B. 6 A), damit die meisten E-Autos das Laden starten. Aktuell wird nur die Solarproduktion berücksichtigt; ein Abgleich mit dem tatsächlichen Hausverbrauch könnte in Zukunft ergänzt werden.

Funktionen:

Überschussbasiertes Laden von E-Autos

Konfigurierbare Schwellenwerte, Hysterese und Zykluszeit

Kompatibel mit Tasmota Steckdosen und MQTT

Einfache Einrichtung über eine INI-Datei, bitte für den eigenen Gebrauch anpassen


