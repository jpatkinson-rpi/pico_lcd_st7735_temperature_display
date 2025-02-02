#-------------------------------------------------------------------
# RPi PICO temperature display
# - ST7735 TFT display
# - DS18x20 onewire temperature sensor on GPIO 22
#-------------------------------------------------------------------
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import time
import math
import machine, onewire, ds18x20

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,8,12,9)
tft.initr()
tft.rgb(True)
tft.rotation(0)
tft.fill(TFT.BLACK)
tft.fillrect( (1, 1),(tft.size()[0], tft.size()[1]), TFT.BLACK)

tft.rotation(1)
tft.fillrect( (0, 0),(tft.size()[0], tft.size()[1]), TFT.BLACK)

print('size0', tft.size()[0])
print('size1', tft.size()[1])

ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)

def temperature_display():
    while True:
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        value = ds_sensor.read_temp(roms[0])
        valuestr = '{:.1f}°C'.format(value)
        valuestr = '{:>4}'.format(valuestr)
        tft.fill(TFT.BLACK)
        tft.text((0, 40), str(valuestr), TFT.GREEN, sysfont, 5, nowrap=True)
        value = value + 0.1
        if value > 99.9 :
           value = 0
        time.sleep(5)
        
temperature_display()
