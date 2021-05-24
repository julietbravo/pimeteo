#import board
#from adafruit_onewire.bus import OneWireBus
#from adafruit_ds18x20 import DS18X20
#
#ow_bus = OneWireBus(board.D4)
#ds18 = DS18X20(ow_bus, ow_bus.scan()[0])
#ds18.temperature

#import board
#import busio
#onewire = busio.OneWire(board.D4)

import board
from adafruit_onewire.bus import OneWireBus
ow_bus = OneWireBus(board.D2)
devices = ow_bus.scan()
for d in devices:
    print("ROM={}\tFamily=0x{:02x}".format(d.rom, d.family_code))
