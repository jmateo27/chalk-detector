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
        time.sleep(3)
        while True:
        # with open('data.txt', 'w') as file:
            time.sleep(0.1)
            v = self.adc.measure_voltage_drop()
            print("Voltage Reading = %f" % (v))
            # file.write("%d\t%d\t%d\t%d\n" % (x, r, g, b))
            time.sleep(5)
            
    def collectPaintSampleData(self):
        print("3 seconds to begin, get paint sample 01 ready...")
        time.sleep(3)
        with open('uphole_data_45m.txt', 'w') as file:
            for x in range(1, 23):
                v = self.adc.measure_voltage_drop()
                print("Paint sample %d:\nVoltage = %f\nCurrent = %fmA\n\n" % (x, v, v*1000.0/150.0))
                file.write("%d\t%f\t%f\t%d\n" % (x, v, v*1000.0/150.0, int(v*0xFFFF/3.3)))
                time.sleep(5)

if __name__ == "__main__":
    chokBaux = ChokBaux()
    chokBaux.collectPaintSampleData()