#!/usr/bin/python
import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
from RPLCD import CharLCD
GPIO.setwarnings(False)

## If using BOARD numbers such as PIN35, PIN31 etc, uncomment the line below
##lcd = CharLCD(numbering_mode=GPIO.BOARD,cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 23])

## If using BCM numbers such as GPIO13, GPIO11 etc), uncomment the line below
lcd = CharLCD(numbering_mode=GPIO.BCM,cols=16, rows=2, pin_rs=26, pin_e=19, pins_data=[13,6, 5, 11])

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 14)
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Temp: %d C" % temperature)
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Humidity: %d %%" % humidity)