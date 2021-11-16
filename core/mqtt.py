import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
broker_address="localhost"
#broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client(__name__) #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address, port=18883) #connect to broker
# client.loop_start() #start the loop
print("Subscribing to topic","foo/baz")
client.subscribe("foo/baz")

while True:
    client.loop()