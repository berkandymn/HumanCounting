
import paho.mqtt.publish as publish

# MQTT broker bilgileri
broker_address = "192.168.0.11"
port = 1883

# Publish edilecek topic ve mesaj
topic = "test"
message = 1

# MQTT broker'a bağlanma ve mesajı publish etme

def mqttPublish(value):
    publish.single(topic, value, hostname=broker_address, port=port)