from dac4to20 import DAC_4to20
from rgb import RGB_Sensor

import time

# === CONSTANTS ===

PERIPHERAL_FREQ = 100000              # I2C frequency for peripherals (in Hz)

# GPIO pin assignments
RGB_SDA_PIN		   = 16
RGB_SCL_PIN		   = 17
DAC_SDA_PIN		   = 18
DAC_SCL_PIN		   = 19

# Timing constants
INIT_WAIT_SECS         = 2           # Delay before main logic starts (to allow peripherals to power up)
MEASUREMENT_LATENCY_MS = 10          # Delay between measurements (in milliseconds)

# Color channel identifiers
RED   = 1
GREEN = 2
BLUE  = 3


class Chalk_Detector:
    def __init__(self):
        """
        Initialize the Chalk Detector system, setting up:
        - LED for illumination or indication via PWM
        """
        self.rgb	   = RGB_Sensor(RGB_SCL_PIN, RGB_SDA_PIN, PERIPHERAL_FREQ, 0)
        self.dac	   = DAC_4to20(DAC_SCL_PIN, DAC_SDA_PIN, PERIPHERAL_FREQ, 1)

    def main(self):
        while True:
            self.dac.output(self.rgb.read_colour_mA(BLUE))
            time.sleep_ms(MEASUREMENT_LATENCY_MS)
        

if __name__ == "__main__":
    # Wait for devices to settle before starting main logic
    time.sleep(INIT_WAIT_SECS)
    chalkDetector = Chalk_Detector()
    chalkDetector.main()
