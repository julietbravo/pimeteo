import numpy as np
import datetime
import time
import board
import sys
from w1thermsensor import W1ThermSensor

# custom pimeteo modules
from timer import Timer
from display import LCD
from sensors import DHT, BME280, DS1820, MHZ14A

def fix_none(value):
    if value is None:
        return -1
    else:
        return value

# Global settings:
# Display
i2c_addr_display=0x27
i2c_addr_baro=0x76
sm_bus_display=1
serial_port = '/dev/serial0'

# DHT11 sensor:
dht11_pin   = board.D17
dht22_1_pin = board.D27
dht22_2_pin = board.D22
dht22_3_pin = board.D23

# DS18b20 sensors:
ds18_ids = {
    1:  '00000caa3da0',
    2:  '00000caaea05',
    3:  '00000caa36e3',
    4:  '00000ca91025',
    5:  '00000caa70f8',
    6:  '00000ca95be8',
    7:  '00000ca918d3',
    8:  '00000caa2f16',
    9:  '00000ca9a207',
    10: '00000ca98d16'}

dt_update = 5   # Update frequency display (s)
dt_log = 30     # Logging frequency (s)

# Setup modules:
lcd = LCD(i2c_addr_display, sm_bus_display)
timer = Timer(dt_log, dt_update)
bme280 = BME280(i2c_addr_baro)
mhz14 = MHZ14A(serial_port)
#mhz14.reset()

dht11   = DHT(dht11_pin,   'DHT11')
dht22_1 = DHT(dht22_1_pin, 'DHT22')
dht22_2 = DHT(dht22_2_pin, 'DHT22')
dht22_3 = DHT(dht22_3_pin, 'DHT22')

ds18 = {}
for i,sid in ds18_ids.items():
    sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, sid)
    ds18[i] = sensor

# TMP log file
now = datetime.datetime.now()
#log_file = '/home/pi/meteo/pimeteo/logs/{0:04d}{1:02d}{2:02d}_{3:02d}{4:02d}.csv'.format(
#        now.year, now.month, now.day, now.hour, now.minute)
log_file = '/home/pi/meteo/pimeteo/logs/log2.csv'

# Execute timeloop:
while True:

    do_update = timer.do_update()
    do_log = timer.do_log()

    if do_update or do_log:

        success = False

        try:
            now = datetime.datetime.utcnow()
            P1  = fix_none(bme280.get_pressure())
            T1  = fix_none(bme280.get_temperature())
            RH1 = fix_none(bme280.get_humidity())

            CO2 = fix_none(mhz14.get_co2())

            T2  = fix_none(dht11  .get_temperature())
            T3  = fix_none(dht22_1.get_temperature())
            T4  = fix_none(dht22_2.get_temperature())
            T5  = fix_none(dht22_3.get_temperature())

            RH2  = fix_none(dht11  .get_humidity())
            RH3  = fix_none(dht22_1.get_humidity())
            RH4  = fix_none(dht22_2.get_humidity())
            RH5  = fix_none(dht22_3.get_humidity())

            ds18_vals = []
            for ds in ds18.values():
                ds18_vals.append(ds.get_temperature())

            success = True

        except:
            print("Error: ", sys.exc_info()[0])


    if do_update and success:
        lcd.set_values(now, T1, T2, ds18_vals[0], RH1, P1, CO2)

    if do_log and success:
        variables = [T1, T2, T3, T4, T5, RH1, RH2, RH3, RH4, RH5, P1, CO2]
        for v in ds18_vals:
            variables.append(v)

        with open(log_file, 'a') as f:
            f.write('{0:}'.format(timer.log_time))
            for v in variables:
                f.write(', {0:6.2f}'.format(v))
            f.write('\n')
