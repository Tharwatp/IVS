import time
import board
import busio as io
import Adafruit_DHT
import pyrebase
import sys
import adafruit_mlx90614
import serial
import string
import os

os.system("sudo service motion start")
TempString = 16.6
HumidityString = 48.4
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
EMULATE_HX711=False
referenceUnit = 1
mlx = adafruit_mlx90614.MLX90614(i2c)
ser = serial.Serial('/dev/ttyACM0' , 9600)

config = {
  "apiKey": "8XbGQpi2pvbyjCewerJw4HPHT3kN0aLZkqJyA1zk",
  "authDomain": "proj-2-78771.firebaseapp.com",
  "databaseURL": "https://proj-2-78771-default-rtdb.firebaseio.com",
  "storageBucket": "proj-2-78771.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

print("Send Data to Firebase Using Raspberry Pi")
print("—————————————-")
print()


if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(-300)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")


while True:
        line = ser.readline()
        Cry = float(line)
        print(Cry)
        ambientString = "{:.2f}".format(mlx.ambient_temperature)
        objectString = "{:.2f}".format(mlx.object_temperature)
        ambientCelsius = float(ambientString)
        objectCelsius = float(objectString)
        print("Ambient Temp: {} °C".format(ambientString))
        print("Object Temp: {} °C".format(objectString))
        print()
        val = hx.get_weight(5)
        HX = float(val)
        print(val)
        print()

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
        
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)  
        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
            TempString = "{:.2f}".format(temperature)
            HumidityString = "{:.2f}".format(humidity)

        TempCelsius = float(TempString)
        HPercentage = float(HumidityString)

        print("Temp: {} °C".format(TempString))
        print("Humidity: {} %".format(HumidityString))
        print()

        data = {
          "Temp": TempCelsius,
          "Humidity": HPercentage,
          "Weight":HX,
          "ambient": ambientCelsius,
          "object": objectCelsius,
          "Cry":Cry,
          
        }
        db.child("DHT22").child("1-set").set(data)
        
        if Cry > 75 :
          os.system("mpg321 /home/pi/Final/abcd.mp3")

        time.sleep(2)
