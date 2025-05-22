from led import LED                 # Import LED control class

import time

# === CONSTANTS ===

PERIPHERAL_FREQ = 100000              # I2C frequency for peripherals (in Hz)

# GPIO pin assignments
LED_PWM_PIN        = 21              # PWM pin connected to LED

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
        self.led       = LED(LED_PWM_PIN)

    def main(self):
        """
        Main loop of the Chalk Detector:
        - Turns on the LED
        """
        self.led.LED_on()      # Turn on LED for lighting

if __name__ == "__main__":
    # Wait for devices to settle before starting main logic
    time.sleep(INIT_WAIT_SECS)
    chalkDetector = Chalk_Detector()
    chalkDetector.main()
