import paho.mqtt.client as MyMqtt
import json, time, random

from Flowerpot_Engine import *
# Thingsboard connection 

# Initialize variables and MQTT details

iot_hub = "thingsboard.cloud"
port = 1883
cli_ID = f'clientID-{random.randint(0, 1000)}'
username = " "               # <==== Enter your device token from TB here
password = ""
TelemetryTopic = "v1/devices/me/telemetry"
RPCrequestTopic = 'v1/devices/me/rpc/request/+'
AttributesTopic = "v1/devices/me/attributes"

# Define dashboard state variables
pump = {"PumpRunning": False}


# MQTT on_connect callback function
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connection: {rc}")
    client.subscribe(RPCrequestTopic)
    # Send initial pump state to ThingsBoard
    client.publish(AttributesTopic, json.dumps(pump), 1)
    
# MQTT on_message callback function
def on_message(client, userdata, msg):
    if msg.topic.startswith('v1/devices/me/rpc/request/'):
        data = json.loads(msg.payload)

        if data['method'] == 'setValue':
            params = data['params']
            # Turn the pump on/off
            setValue(params)
            
            
# Function will set the Pump value
def setValue(params):
    if params == True:
        # Turn pump ON
        pump_ON()
        pump['PumpRunning'] = True
        # Update the ClientAttribute "PumpRunning" on the TB dashboard
        client.publish(AttributesTopic, json.dumps(pump), 1)

    elif params == False:
        # Turn pump OFF
        pump_OFF()
        pump['PumpRunning'] = False
        # Update the ClientAttribute "PumpRunning" on the TB dashboard
        client.publish(AttributesTopic, json.dumps(pump), 1)

# This function is used to send telemetry data to ThingsBoard
def send_data(data_out):
    JSON_data_out = json.dumps(data_out) # Convert to JSON format
    client.publish(TelemetryTopic, JSON_data_out, 0)

# This function is used to disconnect from ThingsBoard
def disconnect_tb():
    client.disconnect()
    client.loop_stop()
    
        
# Create MQTT client
client = MyMqtt.Client(client_id=cli_ID, callback_api_version=MyMqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)
client.connect(iot_hub, port) # Connect immediately, ( could make these into functions depending on what main.py will consist of )
client.loop_start()





    
