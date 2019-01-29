import paho.mqtt.client as mqtt
from subprocess import call
from influxdb import InfluxDBClient
import datetime
import time
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import os



# Create and influxDB client
dbclient = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

# Create a database with the client
dbclient.create_database('test')
msg_number = 0




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("data1", 0), ("data2", 0), ("data3", 0), ("data4", 0)])



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic)
    # Use utc as timestamp
    receiveTime=datetime.datetime.today()
    epoch_time = time.time()

    global msg_number

    message=msg.payload.decode("utf-8")


    print(str(receiveTime) + ": " + msg.topic + " " + message)

    try:
        # Convert the string to a float so that it is stored as a number and not a string in the database
        val = float(message)
        isfloatValue=True
    except:
        isfloatValue=False

    if isfloatValue:
            print(str(receiveTime) + ": " + msg.topic + " " + str(val))

	    # Catch a json body from the received message.
	    json_body = [
	    {
		"measurement": msg.topic,
		"tags": {
	    		"host": "serverA"
		},
		"time": receiveTime,
		"fields": {
		    "value": val
		}
	    }
	    # Write the json to the influxDB data base.
	    dbclient.write_points(json_body)

    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to an MQTT broker on the localhost
client.connect("127.0.0.1", 1883, 60)



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
