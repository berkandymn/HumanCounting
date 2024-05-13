import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from influxdb import InfluxDBClient

# MQTT broker bilgileri
broker_address = "192.168.0.11"
port = 1883

# Publish edilecek topic ve mesaj
topic = "test"
message = 1

# MQTT broker'a bağlanma ve mesajı publish etme
def on_connect(client, userdata, flags, rc):
    print("Broker'a bağlanıldı. Bağlantı durumu: " + mqtt.connack_string(rc))

def on_message(client, userdata, msg):
    ppldeger= str(msg.payload)

def mqttPublish(value):
    publish.single(topic, value, hostname=broker_address, port=port)

def ilkDeger():
    # InfluxDB'ye bağlanma
    client = InfluxDBClient(host='192.168.0.11', port=8086, username='', password='', database='insidePeople')

    # Son veriyi sorgulama
    result = client.query('SELECT last(value)  FROM people')

    points = result.get_points()

    # İlk satırı al ve 'last' değerini al
    for point in points:
        last_value = point['last']
    return int(last_value)


