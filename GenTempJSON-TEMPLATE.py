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
#       { "Name" : "Sensor One", "Sensor" : adafruit_dht.DHT22(board.D14) },
#       { "Name" : "Sensor Two", "Sensor" : adafruit_dht.DHT22(board.D15) },
#       { "Name" : "Sensor Three", "Sensor" : adafruit_dht.DHT11(board.D16) },
#    ]
#
# This script supports multiple sensors, that can each be either a DHT11 or a DHT22

sensors = [
        { "Name" : "Sensor-001", "Sensor" : adafruit_dht.DHT11(board.D14) },
  ]


# #################################################################
# You shouldn't need to customize anything below this line
# #################################################################

# Set default values for variables
# These are what are set if the rest of the script is unable to set them
hostname = "Unknown"
errmessage = ""
cputemp = -999
uptime = -999
lastscan = datetime.datetime.now(datetime.timezone.utc)

# Gather data from everything except the temperature sensors (we'll do that next)
try:
  hostname = str(socket.gethostname())
  cputemp = gpiozero.CPUTemperature().temperature
  with open('/proc/uptime', 'r') as f:
    uptime = float(f.readline().split()[0])
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
print(" \"Hostname\": \"" + hostname + "\",")
print(" \"CPUTempCelsius\": " + str(cputemp) + ",")
print(" \"UptimeSeconds\": " + str(uptime) + "")
print(" },")
print(" \"Sensors\": [")

for sensor in sensors:
  print(" {")
  print(" \"Name\": " + str(sensor["Name"]) + ",")
  print(" \"TemperatureCelsius\": {0:0.1f},".format(sensor["Temperature"]))
  print(" \"Humidity\": {0:0.1f}".format(sensor["Humidity"]))
  print(" \"ErrorMessage\": \"" + str(sensor["ErrorMessage"]) + "\"")
  print(" \"IsError\": " + str(sensor["IsError"]))
  print(" }")

print(" ],")
print(" \"Troubleshooting\" : {")
print("  \"LastScan\": \"" + str(lastscan) + "\",")
print("  \"Errormessage\": \"" + str(errmessage) + "\",")
print(" }")

print ("}")