from machine import Pin, I2C, ADC
from pico_i2c_lcd import I2cLcd
import utime

i2c = I2C(0, sda=Pin(0), scl=Pin(1))
lcd = I2cLcd(i2c, 0x27, 2, 16)

sensor = ADC(Pin(26))

led = Pin(15, Pin.OUT)


#class is defined here 
class VitalDisplaySystem:

    def __init__(self, lcd, sensor, led):

        self.lcd = lcd
        self.sensor = sensor
        self.led = led
        self.readings = []

    def read_sensor(self):

        raw = self.sensor.read_u16()
        value = int(40 + (raw / 65535) * 140)
        return value

    def store_data(self, value):

        if len(self.readings) == 0 or value != self.readings[-1]:

            self.readings.append(value)
            print("Stored:", value)

    def analyze(self, value):

        if value < 60:
            return "LOW"

        elif value > 100:
            return "HIGH"

        else:
            return "NORMAL"

    def control_led(self, status):

        if status == "HIGH":
            self.led.on()

        else:
            self.led.off()

    def display_current(self, value, status):

        self.lcd.clear()

        self.lcd.move_to(0, 0)
        self.lcd.putstr("HR:" + str(value))

        self.lcd.move_to(0, 1)
        self.lcd.putstr(status)

    def display_average(self):

        average = sum(self.readings) / len(self.readings)

        self.lcd.clear()

        self.lcd.move_to(0, 0)
        self.lcd.putstr("Average HR")

        self.lcd.move_to(0, 1)
        self.lcd.putstr(str(round(average, 1)))

        print("Final Readings:", self.readings)
        print("Average:", average)
        if average  < 60:
            print("LOW")

        elif average> 100:
            print("HIGH")

        else:
            print("NORMAL")

    # Main program
    def run(self):

        while len(self.readings) < 10:

            value = self.read_sensor()

            self.store_data(value)

            status = self.analyze(value)

            self.control_led(status)

            self.display_current(value, status)

            utime.sleep(1)

        self.display_average()

#object creation 
system = VitalDisplaySystem(lcd, sensor, led)

# running the program 
system.run()