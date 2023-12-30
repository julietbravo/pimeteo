# pimeteo
Simple meteo station/logger based on a Raspberry Pi

# Installed packages Pi
`sudo apt-get install vim git i2c-tools gpiod`
`pip3 install matplotlib numpy ipython smbus adafruit-circuitpython-dht adafruit-circuitpython-bme281 adafruit-circuitpython-ds19x20 adafruit-circuitpython-onewire paho-mqtt`

# Installing MQTT et al.
sudo apt-get install mosquitto -y
sudo apt-get install mosquitto-clients -y

Edit `/etc/mosquitto/mosquitto.conf`:
remove: `include_dir /etc/mosquitto/conf.d`
add: `listener 1883`



# Setup fixed IP Raspberry Pi:
Check if DHCPCD is active:

