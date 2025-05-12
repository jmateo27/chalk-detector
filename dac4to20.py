import machine
import time

# ADAPTED FROM https://github.com/DFRobot/DFRobot_GP8302/blob/master/python/raspberrypi/examples/

GP8302_DEF_I2C_ADDR       = 0x58
GP8302_CONFIG_CURRENT_REG = 0x02
GP8302_CURRENT_RESOLUTION = 0x0FFF
GP8302_MAX_CURRENT        = 25

GP8302_STORE_TIMING_HEAD  = 0x02
GP8302_STORE_TIMING_ADDR  = 0x10
GP8302_STORE_TIMING_CMD1  = 0x03
GP8302_STORE_TIMING_CMD2  = 0x00
GP8302_STORE_TIMING_DELAY = 0.01

I2C_CYCLE_TOTAL           = 0.000005
I2C_CYCLE_BEFORE          = 0.000002
I2C_CYCLE_AFTER           = 0.000003

class DAC_4to20:
    def __init__(self, scl_pin, sda_pin, freq, id):
        self.i2c = machine.I2C(id,
                  sda=machine.Pin(sda_pin),
                  scl=machine.Pin(scl_pin),
                  freq=freq)

        self._scl = machine.Pin(scl_pin, machine.Pin.OUT, value=1)
        self._sda = machine.Pin(sda_pin, machine.Pin.OUT, value=1)
        self._addr = GP8302_DEF_I2C_ADDR
        self._dac_4 = 655
        self._dac_20 = 3277
        self._calibration = False
        self._digital = 0

    def _i2c_delay(self):
        time.sleep(I2C_CYCLE_TOTAL)

    def _start_signal(self):
        self._sda.value(1)
        self._scl.value(1)
        time.sleep(I2C_CYCLE_BEFORE)
        self._sda.value(0)
        time.sleep(I2C_CYCLE_AFTER)
        self._scl.value(0)

    def _stop_signal(self):
        self._sda.value(0)
        self._scl.value(1)
        time.sleep(I2C_CYCLE_BEFORE)
        self._sda.value(1)
        time.sleep(I2C_CYCLE_AFTER)

    def _send_byte(self, data, delay=True):
        for i in range(8):
            self._sda.value((data >> (7 - i)) & 0x01)
            self._scl.value(1)
            if delay: time.sleep(I2C_CYCLE_TOTAL)
            self._scl.value(0)
        # ACK bit
        self._sda.init(machine.Pin.IN)
        self._scl.value(1)
        ack = self._sda.value()
        self._scl.value(0)
        self._sda.init(machine.Pin.OUT)
        return ack

    def begin(self):
        self._start_signal()
        if self._send_byte(self._addr << 1):
            self._stop_signal()
            return 2  # Device not found
        self._stop_signal()
        return 0

    def calibration4_20mA(self, dac_4, dac_20):
        if dac_4 >= dac_20 or dac_20 > GP8302_CURRENT_RESOLUTION:
            return
        self._dac_4 = dac_4
        self._dac_20 = dac_20
        self._calibration = True

    def output_mA(self, dac):
        self._digital = dac & GP8302_CURRENT_RESOLUTION
        self._start_signal()
        self._send_byte(self._addr << 1)
        self._send_byte(GP8302_CONFIG_CURRENT_REG)
        
        self._send_byte((self._digital << 4) & 0xF0)       
        self._send_byte((self._digital >> 4) & 0xFF)      

        self._stop_signal()
        return (self._digital / GP8302_CURRENT_RESOLUTION) * GP8302_MAX_CURRENT

    def output(self, current_mA):
        current_mA = min(max(current_mA, 0), GP8302_MAX_CURRENT)
        if self._calibration and 4 <= current_mA <= 20:
            self._digital = self._dac_4 + ((current_mA - 4) * (self._dac_20 - self._dac_4)) // 16
        else:
            self._digital = int((current_mA * GP8302_CURRENT_RESOLUTION) / GP8302_MAX_CURRENT)
        self.output_mA(self._digital)
        return self._digital

    def store(self):
        self._start_signal()
        self._send_byte(GP8302_STORE_TIMING_HEAD)
        self._stop_signal()

        self._start_signal()
        self._send_byte(GP8302_STORE_TIMING_ADDR)
        self._send_byte(GP8302_STORE_TIMING_CMD1)
        self._stop_signal()

        self._start_signal()
        self._send_byte(self._addr << 1)
        for _ in range(8):
            self._send_byte(GP8302_STORE_TIMING_CMD2)
        self._stop_signal()

        time.sleep(GP8302_STORE_TIMING_DELAY)