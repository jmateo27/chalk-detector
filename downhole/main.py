from rgb import RGB_Sensor
from led import LED
# from adcReader import ADC_Reader
from dac4to20 import DAC_4to20

import time

# CONSTANTS
PERIPHERAL_FREQ             = 100000

RGB_SENSOR_SDA_PIN          = 16
RGB_SENSOR_SCL_PIN          = 17
LED_PWM_PIN                 = 21
# ADC1_PIN                    = 28
# ADC2_PIN                    = 27
DAC_SDA_PIN                 = 18
DAC_SCL_PIN                 = 19

INIT_WAIT_SECS              = 2
MEASUREMENT_LATENCY_MS      = 10

RED     = 1
GREEN   = 2
BLUE    = 3


class Chalk_Detector:
    def __init__(self):
        self.rgbSensor  = RGB_Sensor(RGB_SENSOR_SCL_PIN, RGB_SENSOR_SDA_PIN, PERIPHERAL_FREQ, 0)
        self.dac        = DAC_4to20(DAC_SCL_PIN, DAC_SDA_PIN, PERIPHERAL_FREQ, 1)
        self.led        = LED(LED_PWM_PIN)
        # self.adc        = ADC_Reader(ADC1_PIN, ADC2_PIN)
    
    def main(self):
        self.dac.begin()
        self.led.LED_on()
    
        while True:
            # print('Red:', self.rgbSensor.read_colour_raw(RED))
            # print('Green:', self.rgbSensor.read_colour_raw(GREEN))
            # print('Blue:', self.rgbSensor.read_colour_raw(BLUE))
            self.dac.output(self.rgbSensor.read_colour_mA(BLUE))
            # time.sleep(0.1)
            # self.adc.print_voltage_drop()
            # print('')
            time.sleep_ms(MEASUREMENT_LATENCY_MS)

if __name__ == "__main__":
    time.sleep(INIT_WAIT_SECS)
    chalkDetector = Chalk_Detector()
    chalkDetector.main()