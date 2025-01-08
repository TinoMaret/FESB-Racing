import can
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from datetime import datetime

# InfluxDB konfiguracija
INFLUXDB_URL = "http://localhost:8086"  # URL vaše InfluxDB instance
INFLUXDB_TOKEN = "hjyutJ-cdWK1rfo7PUNQrJNJ4EyygydPiJakaI40zRblPsN8f2gFOxFLBrP9amL-Y7uDHWVw22hZ9WfsCjH6uA=="  # vaš InfluxDB token
INFLUXDB_ORG = "Racing"  # vaša organizacija u InfluxDB
INFLUXDB_BUCKET = "racing"  # naziv vašeg bucket-a

# Postavljanje InfluxDB klijenta
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Funkcija za spremanje podataka u InfluxDB
def save_to_influxdb(timestamp, can_id, data):
    point = Point("can_data") \
        .tag("can_id", str(can_id)) \
        .field("data", data) \
        .time(timestamp, WritePrecision.NS)
    write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)

# Postavljanje CAN sučelja
def receive_can_messages():
    # Kreiramo bus za virtualni CAN port (vcan0)
    bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

    try:
        while True:
            message = bus.recv()  # Čekaj i primi poruku
            if message is not None:
                timestamp = datetime.utcfromtimestamp(message.timestamp).isoformat()
                can_id = message.arbitration_id
                data = message.data.hex()  # Pretvaramo podatke u heksadecimalni format
                print(f"Received message: Timestamp={timestamp}, CAN ID={can_id}, Data={data}")
                save_to_influxdb(timestamp, can_id, data)
    except KeyboardInterrupt:
        print("Prekid rada.")
    finally:
        bus.shutdown()

if __name__ == "__main__":
    print("Pokrećem primanje CAN poruka...")
    receive_can_messages()
