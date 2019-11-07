import smbus
import time
import datetime

class LCD:
    def __init__(self, i2c_addr, sm_bus):
        self.i2c_addr = i2c_addr
        self.sm_bus = sm_bus

        self.lcd_width = 20     # Width (characters) display

        self.lcd_chr = 1        # Mode - Sending data
        self.lcd_cmd = 0        # Mode - Sending command

        self.e_pulse = 0.0005
        self.e_delay = 0.0005

        self.bus = smbus.SMBus(self.sm_bus)

        # Init display
        self.lcd_byte(0x33, self.lcd_cmd)  # 110011 Initialise
        self.lcd_byte(0x32, self.lcd_cmd)  # 110010 Initialise
        self.lcd_byte(0x06, self.lcd_cmd)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.lcd_cmd)  # 001100 Display On, Cursor Off, Blink Off
        self.lcd_byte(0x28, self.lcd_cmd)  # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.lcd_cmd)  # 000001 Clear display
        time.sleep(self.e_delay)


    def lcd_byte(self, bits, mode):
        lcd_backlight  = 0x08  # on 0x08 / off 0x00

        bits_high = mode | (bits & 0xF0)      | lcd_backlight
        bits_low  = mode | ((bits<<4) & 0xF0) | lcd_backlight

        self.bus.write_byte(self.i2c_addr, bits_high)
        self.toggle_enable(bits_high)

        self.bus.write_byte(self.i2c_addr, bits_low)
        self.toggle_enable(bits_low)


    def toggle_enable(self, bits):
        enable = 0b00000100

        time.sleep(self.e_delay)
        self.bus.write_byte(self.i2c_addr, (bits | enable))
        time.sleep(self.e_pulse)
        self.bus.write_byte(self.i2c_addr, (bits & ~enable))
        time.sleep(self.e_delay)


    def write(self, message, line):
        message = message.ljust(self.lcd_width, ' ')

        if line == 0:
            self.lcd_byte(0x80, self.lcd_cmd)
        elif line == 1:
            self.lcd_byte(0xC0, self.lcd_cmd)
        elif line == 2:
            self.lcd_byte(0x94, self.lcd_cmd)
        elif line == 3:
            self.lcd_byte(0xD4, self.lcd_cmd)

        for i in range(self.lcd_width):
            self.lcd_byte(ord(message[i]), self.lcd_chr)


if __name__ == '__main__':

    lcd = LCD(i2c_addr=0x27, sm_bus=1)
    lcd.write('hello world!', 0)
    lcd.write('hello world!', 1)
    lcd.write('hello world!', 2)
    lcd.write('hello world!', 3)
