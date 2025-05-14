from adcReader import ADC_Reader
from pinInterface import Input_Pin_Interface
from inputPins import input_pins

import time
import machine
# CONSTANTS
ADC1_PIN                    = 28
ADC2_PIN                    = 27

MEASUREMENT_LATENCY_SECS    = 5.0

LOAD_RESISTOR_OHMS          = 150.0
A_to_mA                     = 1000.0

DEPTH_INCREMENT             = 0.25
CYCLE_LATENCY_MS            = 1
DEBOUNCE_MS                 = 50

class ChokBaux:
    def __init__(self):
        self.adc            = ADC_Reader(ADC1_PIN, ADC2_PIN)
#         Polling Version
#         self.dpt_rst_in     = Input_Pin_Interface(input_pins['DPT_RST'], 'REGULAR')
#         self.dpt_in         = Input_Pin_Interface(input_pins['DPT_IN'], 'REGULAR')
#         self.ena_in         = Input_Pin_Interface(input_pins['ENA_IN'], 'REGULAR')
        
#         Interrupt Version
        self.dpt_rst_in     = Input_Pin_Interface(input_pins['DPT_RST'], 'INTERRUPT')
        self.dpt_in         = Input_Pin_Interface(input_pins['DPT_IN'], 'INTERRUPT')
        self.ena_in         = Input_Pin_Interface(input_pins['ENA_IN'], 'REGULAR')
        self.timer1          = machine.Timer()
        self.timer2          = machine.Timer()
        self.last_trigger_time = 0
        
        self.depth_count    = 0
    
    def counts_to_voltage_drop_V(self, counts):
        return counts * self.adc.ADC_MAX_VOLTAGE / self.adc.ADC_MAX_READING
    
    def counts_to_current_consumption_mA(self, counts):
        return self.counts_to_voltage_drop_V(counts) * A_to_mA / LOAD_RESISTOR_OHMS

    def collectData(self):
        time.sleep(3)
        while True:
            with open('data.txt', 'w') as file:
                c = self.adc.measure_counts()
                v = self.counts_to_voltage_drop_V(c)
                i = self.counts_to_current_consumption_mA(c)
                print("Voltage = %f V\nCurrent = %f mA\n# Counts = %d\n\n" % (v, i, c))
                file.write("%f\t%f\t%d\n" % (v, i, c))
                time.sleep(MEASUREMENT_LATENCY_SECS)
            
    def collectPaintSampleData(self):
        print("3 seconds to begin, get paint sample 01 ready...")
        time.sleep(3)
        with open('uphole_data_45m.txt', 'w') as file:
            for x in range(1, 23):
                c = self.adc.measure_counts()
                v = self.counts_to_voltage_drop_V(c)
                i = self.counts_to_current_consumption_mA(c)
                print("Paint sample %d:\nVoltage = %f V\nCurrent = %f mA\n# Counts = %d\n\n" % (x, v, i, c))
                file.write("%d\t%f\t%f\t%d\n" % (x, v, i, c))
                time.sleep(MEASUREMENT_LATENCY_SECS)
                
    def test_inputs(self):
        time.sleep(3)
        while True:
            if self.dpt_in.isHigh():
                print('String pot is moving')
            if self.ena_in.isHigh():
                print('Enable switch is on')
            time.sleep_ms(CYCLE_LATENCY_MS)

    def main_polling(self):
        time.sleep(3)
        with open('data.txt', 'w') as file:
            file.write("Depth\tVoltage\tCurrent\t# Counts\n")
            file.flush()
            while True:
                time.sleep_ms(CYCLE_LATENCY_MS)
                if self.dpt_rst_in.isHigh():
                    self.depth_count = 0
                    continue

                if not self.ena_in.isHigh():
                    continue

                if self.dpt_in.isHigh():
                    self.depth_count += DEPTH_INCREMENT
                    c = self.adc.measure_counts()
                    v = self.counts_to_voltage_drop_V(c)
                    i = self.counts_to_current_consumption_mA(c)
                    print("Depth = %f\tVoltage = %f V\tCurrent = %f mA\t# Counts = %d\n\n" % (self.depth_count, v, i, c))
                    file.write("%f\t%f\t%f\t%d\n" % (self.depth_count, v, i, c))
                    file.flush()
                    while self.dpt_in.isHigh():
                        time.sleep_ms(CYCLE_LATENCY_MS)

    def depth_reset_timer_callback(self, t):
        self.depth_count = 0
        
    def depth_reset_handler(self, pin):
        print('Depth reset switch flipped. Setting depth back to 0 m')
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_trigger_time) > self.debounce_ms:
            self.last_trigger_time = current_time
            self.timer2.init(mode=machine.Timer.ONE_SHOT, period=10, callback=self.depth_reset_timer_callback)


    def depth_timer_callback(self, t):
        self.depth_count += DEPTH_INCREMENT
        c = self.adc.measure_counts()
        v = self.counts_to_voltage_drop_V(c)
        i = self.counts_to_current_consumption_mA(c)
        print("Depth = %f\tVoltage = %f V\tCurrent = %f mA\t# Counts = %d\n\n" % (self.depth_count, v, i, c))
        with open('data.txt', 'a') as file:
            file.write("%f\t%f\t%f\t%d\n" % (self.depth_count, v, i, c))
            file.flush()

    def depth_input_handler(self, pin):
        if self.ena_in.isHigh():
            self.timer1.init(mode=machine.Timer.ONE_SHOT, period=10, callback=self.depth_timer_callback)

    def main_interrupt(self):
        time.sleep(3)
        with open('data.txt', 'w') as file:
            file.write("Depth\tVoltage\tCurrent\t# Counts\n")
            file.flush()
        self.dpt_rst_in.setUpInterrupt(self.depth_reset_handler)
        self.dpt_in.setUpInterrupt(self.depth_input_handler)



if __name__ == "__main__":
    chokBaux = ChokBaux()
    chokBaux.main_interrupt()