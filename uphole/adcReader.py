import machine

class ADC_Reader:
    ADC_MAX_VOLTAGE     = 3.3
    ADC_MAX_READING     = 0xFFFF

    def __init__(self, adc1_pin, adc2_pin):
        self.adc1 = machine.ADC(adc1_pin)
        self.adc2 = machine.ADC(adc2_pin)
    
    def measure_counts(self):
        self.counts = self.adc1.read_u16() - self.adc2.read_u16()
        return self.counts

    def print_voltage_drop(self):
        print('Current voltage drop is ', self.measure_voltage_drop())