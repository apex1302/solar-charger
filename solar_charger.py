import json
import time
import csv
import os
import configparser
import paho.mqtt.client as mqtt

# Load config (allow inline comments with ; or #)
config = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
config.read("config.ini")

MQTT_HOST = config["settings"]["mqtt_host"]
MQTT_PORT = int(config["settings"]["mqtt_port"])
SOLAR_TOPIC = config["settings"]["solar_topic"]          # z.B. tele/SOLAR/SENSOR
CHARGER_TOPIC = config["settings"]["charger_topic"]      # z.B. cmnd/CHARGER/POWER
CSV_FILE = config["settings"]["csv_file"]

LIMIT = float(config["settings"]["limit"])
HYST = float(config["settings"]["hysteresis"])
CYCLE = int(config["settings"]["cycle"])

# State
last_action_time = 0
charger_state = None
solar_state = None

# CSV vorbereiten (Header nur wenn Datei neu)
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "power_w", "charger_state", "solar_state"])

def log_to_csv(power, charger_state, solar_state):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), power, charger_state, solar_state])

def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT broker")
    client.subscribe(SOLAR_TOPIC)
    client.subscribe("stat/CHARGER/POWER")
    client.subscribe("stat/SOLAR/POWER")

    # Initiale Abfragen (damit direkt Status + Messwerte reinkommen)
    client.publish("cmnd/SOLAR/STATUS", "10")     # Messwerte anfordern
    client.publish("cmnd/CHARGER/POWER", "")      # Charger-Status abfragen
    client.publish("cmnd/SOLAR/POWER", "")        # Solar-Status abfragen

def on_message(client, userdata, msg):
    global charger_state, solar_state, last_action_time

    topic = msg.topic
    now = time.time()

    try:
        # --- Solar Leistung (tele/.../SENSOR) ---
        if topic == SOLAR_TOPIC:
            payload = json.loads(msg.payload.decode())
            power = payload["ENERGY"]["Power"]
            print(f"⚡ Solar power: {power} W")

            if now - last_action_time >= CYCLE:
                # Charger steuern
                if power >= LIMIT:
                    client.publish(CHARGER_TOPIC, "ON")
                    charger_state = "ON"
                    print("➡️ Turning CHARGER ON")
                    last_action_time = now
                elif power <= (LIMIT - HYST):
                    client.publish(CHARGER_TOPIC, "OFF")
                    charger_state = "OFF"
                    print("➡️ Turning CHARGER OFF")
                    last_action_time = now

                # Solar wieder einschalten falls OFF
                if solar_state == "OFF":
                    client.publish("cmnd/SOLAR/POWER", "ON")
                    solar_state = "ON"
                    print("➡️ Forcing SOLAR back ON")
                    last_action_time = now

            # Log in CSV
            log_to_csv(power, charger_state, solar_state)

        # --- Charger Status ---
        elif topic == "stat/CHARGER/POWER":
            charger_state = msg.payload.decode()
            print(f"🔌 Charger state: {charger_state}")

        # --- Solar Status ---
        elif topic == "stat/SOLAR/POWER":
            solar_state = msg.payload.decode()
            print(f"☀️ Solar state: {solar_state}")

    except Exception as e:
        print("❌ Error processing message:", e)

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()

