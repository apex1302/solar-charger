import json
import time
import configparser
import paho.mqtt.client as mqtt

# Load config (allow inline comments with ; or #)
config = configparser.ConfigParser(inline_comment_prefixes=(";", "#"))
config.read("config.ini")

MQTT_HOST = config["settings"]["mqtt_host"]
MQTT_PORT = int(config["settings"]["mqtt_port"])
SOLAR_TOPIC = config["settings"]["solar_topic"]
CHARGER_TOPIC = config["settings"]["charger_topic"]

LIMIT = float(config["settings"]["limit"])
HYST = float(config["settings"]["hysteresis"])
CYCLE = int(config["settings"]["cycle"])

# State
last_action_time = 0
charger_state = None  # "ON" or "OFF"

def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT broker")
    client.subscribe(SOLAR_TOPIC)

    # Ask SOLAR for immediate sensor data so we don't wait for TelePeriod
    client.publish("cmnd/SOLAR/STATUS", "10")

def on_message(client, userdata, msg):
    global charger_state, last_action_time

    try:
        payload = json.loads(msg.payload.decode())
        power = payload["ENERGY"]["Power"]
        print(f"⚡ Solar power: {power} W")

        now = time.time()
        if now - last_action_time < CYCLE:
            return  # skip, still in cooldown

        if charger_state != "ON" and power >= LIMIT:
            client.publish(CHARGER_TOPIC, "ON")
            charger_state = "ON"
            last_action_time = now
            print("➡️  Turning CHARGER ON")

        elif charger_state != "OFF" and power <= (LIMIT - HYST):
            client.publish(CHARGER_TOPIC, "OFF")
            charger_state = "OFF"
            last_action_time = now
            print("➡️  Turning CHARGER OFF")

    except Exception as e:
        print("❌ Error processing message:", e)

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()

