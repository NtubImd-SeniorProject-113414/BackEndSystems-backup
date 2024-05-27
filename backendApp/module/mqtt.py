import paho.mqtt.client as mqtt

def send_mqtt_message(message, topic, qos=1):
    client = mqtt.Client()
    host = "140.131.115.152"
    port = 1883 
    username = "wow0422796353"
    password = "sunkaiwj00"
    if username and password:
        client.username_pw_set(username, password)
    client.connect(host, port)
    client.publish(topic, message, qos=qos)
    print('成功發送mqtt')
    client.disconnect()