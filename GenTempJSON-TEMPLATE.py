import datetime
import board
import adafruit_dht
import socket
import gpiozero

# LIST OF SENSORS
#
# To add more sensors, copy the line that starts and ends with { and } respectively
# Example:
#  sensors = [
#       { "Name" : "Sensor One", "Description" : "Adafruit DHT22", "Sensor" : adafruit_dht.DHT22(board.D14) },
#       { "Name" : "Sensor Two", "Description" : "Adafruit DHT22", "Sensor" : adafruit_dht.DHT22(board.D15) },
#       { "Name" : "Sensor Three", "Description" : "Adafruit DHT11", "Sensor" : adafruit_dht.DHT11(board.D16) },
#    ]
#
# This script supports multiple sensors, that can each be either a DHT11 or a DHT22

sensors = [
        { "Name" : "S001", "Description" : "Adafruit DHT22", "Sensor" : adafruit_dht.DHT22(board.D14) },
]


# #################################################################
# You shouldn't need to customize anything below this line
# #################################################################

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial

def getModel():
  # Extract serial from cpuinfo file
  returnme = "Unknown"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:5]=='Model':
        returnme = line[8:999]
    f.close()
  except:
    returnme = "ERROR"

  return returnme.strip()

# Set default values for variables
# These are what are set if the rest of the script is unable to set them
hostname = "Unknown"
errmessage = ""
cputemp = -999
uptime = -999
lastscan = datetime.datetime.now(datetime.timezone.utc)
model = "Unknown"
serial = "Unknown"

# Gather data from everything except the temperature sensors (we'll do that next)
try:
  hostname = str(socket.gethostname())
  cputemp = gpiozero.CPUTemperature().temperature
  with open('/proc/uptime', 'r') as f:
    uptime = float(f.readline().split()[0])
  serial = getserial()
  model = getModel()
except Exception as e:
  errmessage = str(e)

# Gather data from all temperature sensors
for sensor in sensors:
  try :
    # These need initial default values or the script will crash later
    sensor["Temperature"] = -999
    sensor["Humidity"] = -999
    sensor["ErrorMessage"] = ""
    sensor["IsError"] = "false"

    # Now gather the actual values from the sensor
    sensor["Temperature"] = sensor["Sensor"].temperature
    sensor["Humidity"] = sensor["Sensor"].humidity
  except Exception as e:
    sensor["ErrorMessage"] = str(e)
    sensor["IsError"] = "true"

# Print JSON out to the screen. Piping the output of this script to a file will give you a JSON file.

print("{");
print(" \"System\": {")
print("  \"Name\": \"" + hostname + "\",")
print("  \"Description\": \"" + hostname + "\",")
print("  \"Model\": \"" + model + "\",")
print("  \"Serial\": \"" + serial + "\",")
print("  \"UptimeSeconds\": " + str(uptime) + "")
print(" },")

print(" \"CPUSensorReading\" : { ");
print("  \"SystemId\" : \"" + hostname + "\",");
print("  \"SensorId\" : \"" + hostname + "-cpu\",");
print("  \"TemperatureCelsius\" : " + str(cputemp) + ",");
print("  \"ReadingTimestamp\" : \"" + str(lastscan) + "\"");
print(" },");

print(" \"ExternalSensors\" : [");
for sensor in sensors:
  print("  {")
  print("   \"SystemId\" : \"" + hostname + "\",");
  print("   \"SensorId\" : \"" + hostname + "-" + str(sensor["Name"]) + "\",");
  print("   \"Description\" : \"" + str(sensor["Description"]) + "\"");
  print("  }")
print(" ],")

print(" \"TemperatureReadings\": [")
for sensor in sensors:
  if sensor["Temperature"] > -999:
    print("  {")
    print("   \"SystemId\" : \"" + hostname + "\",");
    print("   \"SensorId\" : \"" + hostname + "-" + str(sensor["Name"]) + "\",");
    print("   \"TemperatureCelsius\": {0:0.1f},".format(sensor["Temperature"]))
    print("   \"ReadingTimestamp\" : \"" + str(lastscan) + "\"");
    print("  }")

print(" ],")

print(" \"HumidityReadings\": [")
for sensor in sensors:
  if sensor["Humidity"] > -999:
    print("  {")
    print("   \"SystemId\" : \"" + hostname + "\",");
    print("   \"SensorId\" : \"" + hostname + "-" + str(sensor["Name"]) + "\",");
    print("   \"HumidityPercent\": {0:0.1f},".format(sensor["Humidity"]))
    print("   \"ReadingTimestamp\" : \"" + str(lastscan) + "\"");
    print("  }")

print(" ],")

print(" \"Troubleshooting\" : {")
print("  \"LastScan\": \"" + str(lastscan) + "\",")
print("  \"Errormessage\": \"" + str(errmessage) + "\"")
print(" }")

print ("}")
