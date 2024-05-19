import paho.mqtt.client as mqtt

def send_mqtt_message(message, topic, qos=1):
    client = mqtt.Client()
    host = "127.0.0.1"
    port = 1883 
    username = "abce"
    password = "1234"
    if username and password:
        client.username_pw_set(username, password)
    client.connect(host, port)
    client.publish(topic, message, qos=qos)
    client.disconnect()