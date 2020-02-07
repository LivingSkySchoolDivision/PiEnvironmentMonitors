import datetime
import board
import adafruit_dht
import socket

dhtDevice = adafruit_dht.DHT11(board.D14)

humidity = dhtDevice.humidity
temperature = dhtDevice.temperature

print("{");
print("\"Hostname\": \"" + str(socket.gethostname()) + "\",")

if temperature is not None:
 print(" \"TemperatureCelsius\": {0:0.1f},".format(temperature));
else:
 print(" \"TemperatureCelsius\": -999.0,");

if humidity is not None:
 print(" \"Humidity\": {0:0.1f},".format(humidity));
else:
 print(" \"Humidity\": -1,");

print(" \"ScanTimeUTC\": \"" + str(datetime.datetime.utcnow()) + "\"");
print ("}");