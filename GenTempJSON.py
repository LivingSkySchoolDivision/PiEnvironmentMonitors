import Adafruit_DHT
import datetime

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 14

humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
print("{");
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