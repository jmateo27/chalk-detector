import machine
import time

GP8302_DEF_I2C_ADDR       = 0x58

class GP8302:
    def __init__(self, scl_pin, sda_pin, freq, id):
        self.i2c = machine.I2C(id,
                               sda=machine.Pin(sda_pin),
                               scl=machine.Pin(scl_pin),
                               freq=freq)
        self.addr = GP8302_DEF_I2C_ADDR
        self._dac_4 = 655      # Calibrated value for 4 mA
        self._dac_20 = 3277    # Calibrated value for 20 mA
        self._calibration = False
        self._digital = 0

    def begin(self):
        try:
            self.i2c.writeto(self.addr, b'')  # Just ping the device
            return 0
        except OSError:
            return 2  # Device not found

    def calibration4_20mA(self, dac_4, dac_20):
        if dac_4 >= dac_20 or dac_20 > 0x0FFF:
            return
        self._dac_4 = dac_4
        self._dac_20 = dac_20
        self._calibration = True

    def output_mA(self, dac):
        self._digital = dac & 0x0FFF  # 12-bit value
        low_byte  = (self._digital & 0x0F) << 4
        high_byte = (self._digital >> 4) & 0xFF
        data = bytearray([0x02, low_byte, high_byte])  # 0x02 is the config register
        self.i2c.writeto(self.addr, data)

        return (self._digital / 0x0FFF) * 25  # Approximate current in mA

    def output(self, current_mA):
        current_mA = min(max(current_mA, 0), 25)
        if self._calibration and 4 <= current_mA <= 20:
            self._digital = self._dac_4 + ((current_mA - 4) * (self._dac_20 - self._dac_4)) // 16
        else:
            self._digital = int((current_mA * 0x0FFF) / 25)
        return self.output_mA(self._digital)

    def store(self):
        # Store sequence from datasheet
        try:
            self.i2c.writeto(self.addr, bytes([0x02]))  # Store timing head
            self.i2c.writeto(self.addr, bytes([0x10, 0x03]))
            self.i2c.writeto(self.addr, bytes([0x00] * 8))
            time.sleep(0.01)
        except OSError:
            print("Store failed – I2C error")
