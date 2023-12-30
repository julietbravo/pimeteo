import serial
import board
#from adafruit_onewire.bus import OneWireBus
#import adafruit_ds18x20
import adafruit_dht
import adafruit_bme280
import busio
import sys
from w1thermsensor import W1ThermSensor


class DHT:
    def __init__(self, board_pin, sensor_type):
        if sensor_type == 'DHT11':
            self.dht = adafruit_dht.DHT11(board_pin)
        elif sensor_type == 'DHT22':
            self.dht = adafruit_dht.DHT22(board_pin)
        else:
            sys.exit('Invalid DHT sensor code: {}'.format(sensor_type))

        self.last_T  = 0
        self.last_RH = 0

    def get_temperature(self):
        try:
            tmp = self.dht.temperature
            self.last_T = tmp
            return tmp
        except:
            return self.last_T

    def get_humidity(self):
        try:
            tmp = self.dht.humidity
            self.last_RH = tmp
            return tmp
        except:
            return self.last_RH


class BME280:
    def __init__(self, i2c_addr):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=i2c_addr)

    def get_temperature(self):
        return self.bme280.temperature

    def get_humidity(self):
        return self.bme280.humidity

    def get_pressure(self):
        return self.bme280.pressure


class DS1820:
    def __init__(self, device_path):
        self.device_path = device_path

    def get_temperature(self):
        with open('{}/w1_slave'.format(self.device_path), 'r') as f:
            return float(f.read().strip('\n').split('t=')[-1])/1000.


class MHZ14A:
    #def __init__(self, port='/dev/ttyAMA0'):
    def __init__(self, port='/dev/serial0'):
        self.request_bytes = [0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79]

        self.serial = serial.Serial(
            port = port,
            baudrate = 9600,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 1)

    def reset(self):
        reset_bytes = [0xff, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78]
        self.serial.write(bytearray(reset_bytes))

    def get_co2(self):
        self.serial.write(bytearray(self.request_bytes))
        response = self.serial.read(9)
        if len(response) == 9:
            return (response[2] << 8) | response[3]
        else:
            return -1


if __name__ == '__main__':
    import time

    if True:

        sensor_ids = {
                1: '00000caa3da0',
                2: '00000caaea05',
                3: '00000caa36e3',
                4: '00000ca91025',
                5: '00000caa70f8',
                6: '00000ca95be8',
                7: '00000ca918d3',
                8: '00000caa2f16',
                9: '00000ca9a207',
                10: '00000ca98d16'}
                11: '67a055096461',
                12: '202b56096461',
                13: None,
                14: 'bbdb57096461',
                15: 'f52e83096461',
                16: '327b56096461',
                17: 'ca7a54096461',
                18: 'f6b055096461',
                19: '9c8f83096461',
                20: '2f8f55096461'}

        sensor_obj = {}

        for i,sid in sensor_ids.items():
            if sid is not None:
                sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, sid)
            else:
                sensor = None
            sensor_obj[i] = sensor

        for i,sensor in sensor_obj.items():
            if sensor is not None:
                print(i, sensor.get_temperature())

        #for sensor in W1ThermSensor.get_available_sensors():
        #    #print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
        #    print("Sensor %s" % (sensor.id))


    if False:
        dht11_1 = DHT(board.D17, 'DHT11')
        dht22_1 = DHT(board.D27, 'DHT22')
        dht22_2 = DHT(board.D22, 'DHT22')
        dht22_3 = DHT(board.D23, 'DHT22')

        while True:
            print('-----')
            print(dht11_1.get_temperature(), dht11_1.get_humidity())
            print(dht22_1.get_temperature(), dht22_1.get_humidity())
            print(dht22_2.get_temperature(), dht22_2.get_humidity())
            print(dht22_3.get_temperature(), dht22_3.get_humidity())
            time.sleep(1)

    if False:
        bme280 = BME280(0x76)

    if False:
        ds18 = DS1820('/sys/bus/w1/devices/10-000802791b65')
        while True:
            print(ds18.get_temperature())

    if False:
        co2 = MHZ14A()
        while True:
            print(co2.get_co2())
            time.sleep(1)



