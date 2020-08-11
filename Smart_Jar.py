import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "d1w8bs"
deviceType = "Myjar"
deviceId = "123456"
authMethod = "token"
authToken = "DVQNoivCmGqgRX-SAV"
url = "https://www.fast2sms.com/dev/bulk"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        Pressure=random.randint(10, 40)
        Weight=random.randint(0, 100)
        #Send Pressure in container & weight to IBM Watson
        data = { 'Pressure' : Pressure, 'Weight': Weight }
        #print (data)
        def myOnPublishCallback():
            print ("Published Pressure = %sPa" % Pressure, "Weight = %sg" % Weight, "to IBM Watson")

        success = deviceCli.publishEvent("Sensordata", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback
       
        if Weight<5:
                payload = "sender_id=FSTSMS&message=The container is empty.&language=english&route=p&numbers=9491476109,9290736866"
                headers ={
                                  'authorization': "YXWCzbVEPgG0SnK4yJRLd3wB92qMma7iZTOfFUDthe8oupxAs6v8wXU075C2kETO9SDpPsoKAhHJuRGc",
                                  'Content-Type': "application/x-www-form-urlencoded",
                                  'Cache-Control': "no-cache",
                         }
                response = requests.request("POST", url, data=payload, headers=headers)
                print(response.text)
        if Pressure<15:
                payload = "sender_id=FSTSMS&message=There is a leakage in the container.&language=english&route=p&numbers=9491476109,9290736866"
                headers = {
                                  'authorization': "YXWCzbVEPgG0SnK4yJRLd3wB92qMma7iZTOfFUDthe8oupxAs6v8wXU075C2kETO9SDpPsoKAhHJuRGc",
                                  'Content-Type': "application/x-www-form-urlencoded",
                                  'Cache-Control': "no-cache",
                          }
                response = requests.request("POST", url, data=payload, headers=headers)
                print(response.text)
            
    
                
# Disconnect the device and application from the cloud
deviceCli.disconnect()
