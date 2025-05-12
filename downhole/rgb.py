import machine
import time

#---------------------------------------------------
# CONSTANTS
CURRENT_MIN_mA      = 4.0
CURRENT_MAX_mA      = 20.0
CURRENT_RANGE_mA    = CURRENT_MAX_mA - CURRENT_MIN_mA

VEML3328_ADDR = 0x10
VEML3328_DEV_ID = 0x28
VEML3328_R_ADDR = 0x05
VEML3328_G_ADDR = 0X06
VEML3328_B_ADDR = 0X07
REG_CONTROL = 0x00
CONFIG_VALUE = b'\x00\x00'
VEML3328_MAX_READING = 65536

RED     = 1
GREEN   = 2
BLUE    = 3

class RGB_Sensor:
    def __init__(self, scl_pin, sda_pin, freq, id):
        self.i2c = machine.I2C(id,
                               sda = machine.Pin(sda_pin),
                               scl = machine.Pin(scl_pin),
                               freq = freq)
        
        self.i2c.writeto_mem(VEML3328_ADDR, REG_CONTROL, CONFIG_VALUE)
        time.sleep(0.1)

    def reg_readword_from(self, colour_reg):
        data = self.i2c.readfrom_mem(VEML3328_ADDR, colour_reg, 2)
    
        value = data[0] | (data[1] << 8)
        return value
    
    def read_colour_raw(self, colour):
        colour_addr = VEML3328_R_ADDR
        if colour == RED:
            colour_addr = VEML3328_R_ADDR
        elif colour == GREEN:
            colour_addr = VEML3328_G_ADDR
        elif colour == BLUE:
            colour_addr = VEML3328_B_ADDR
        else:
            print('Cannot read this colour with code ', colour)
        
        return self.reg_readword_from(colour_addr)
    
    def read_colour_mA(self, colour):
        raw_reading = self.read_colour_raw(colour)
        
        return raw_reading / VEML3328_MAX_READING * CURRENT_RANGE_mA + CURRENT_MIN_mA
            
    