import paho.mqtt.client as mqtt

def send_mqtt_message(message, topic, qos=1):
    client = mqtt.Client()
    host = "140.131.115.42"
    port = 1883 
    username = "medimate"
    password = "t;65l4u xul6vu4wj/3"
    if username and password:
        client.username_pw_set(username, password)
    client.connect(host, port)
    client.publish(topic, message, qos=qos)
    print('成功發送mqtt')
    client.disconnect()