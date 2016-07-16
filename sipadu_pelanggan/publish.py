import paho.mqtt.publish as publish

publish.single("USERS/SIPADU_PELANGGAN/get_notif", "payload", hostname="localhost")