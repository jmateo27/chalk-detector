from rgb import RGB_Sensor
from led import LED
from adcReader import ADC_Reader
from dac4to20 import DAC_4to20

import time

# CONSTANTS
PERIPHERAL_FREQ             = 100000

RGB_SENSOR_SDA_PIN          = 16
RGB_SENSOR_SCL_PIN          = 17
LED_PWM_PIN                 = 21
ADC1_PIN                    = 28
ADC2_PIN                    = 27
DAC_SDA_PIN                 = 18
DAC_SCL_PIN                 = 19

MEASUREMENT_LATENCY_SECS    = 2.0

RED     = 1
GREEN   = 2
BLUE    = 3


class Paint_Sample_DAQ:
    def __init__(self):
        self.rgbSensor  = RGB_Sensor(RGB_SENSOR_SCL_PIN, RGB_SENSOR_SDA_PIN, PERIPHERAL_FREQ, 0)
        self.dac        = DAC_4to20(DAC_SCL_PIN, DAC_SDA_PIN, PERIPHERAL_FREQ, 1)
        self.led        = LED(LED_PWM_PIN)
        self.adc        = ADC_Reader(ADC1_PIN, ADC2_PIN)

    def collectPaintSampleData(self):
        self.dac.begin()
        self.led.LED_on()
        print("3 seconds to begin, get paint sample 01 ready...")
        time.sleep(3)
        with open('data.txt', 'w') as file:
            for x in range(1, 23):
                r = self.rgbSensor.read_colour_raw(RED)
                g = self.rgbSensor.read_colour_raw(GREEN)
                b = self.rgbSensor.read_colour_raw(BLUE)
                self.dac.output(self.rgbSensor.read_colour_mA(BLUE))
                time.sleep(0.1)
                v = self.adc.measure_voltage_drop()
                print("Paint sample %d:\nR:%d\nG:%d\nB:%d\nVoltage = %f\nCurrent = %fmA\n\n" % (x, r, g, b, v, v*1000/150.0))
                file.write("%d\t%d\t%d\t%d\n" % (x, r, g, b))
                time.sleep(5)

if __name__ == "__main__":
    paintSampleDAQ = Paint_Sample_DAQ()
    paintSampleDAQ.collectPaintSampleData()