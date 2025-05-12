from adcReader import ADC_Reader

import time

# CONSTANTS
ADC1_PIN                    = 28
ADC2_PIN                    = 27

MEASUREMENT_LATENCY_SECS    = 2.0

class ChokBaux:
    def __init__(self):
        self.adc        = ADC_Reader(ADC1_PIN, ADC2_PIN)

    def collectData(self):
        self.dac.begin()
        self.led.LED_on()
        time.sleep(3)
    # with open('data.txt', 'w') as file:
        time.sleep(0.1)
        v = self.adc.measure_voltage_drop()
        print("Voltage Reading = %f" % (v))
        # file.write("%d\t%d\t%d\t%d\n" % (x, r, g, b))
        time.sleep(2)

if __name__ == "__main__":
    chokBaux = ChokBaux()
    chokBaux.collectData()