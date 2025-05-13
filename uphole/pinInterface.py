import machine
from inputPins import get_label_from_pin

class Input_Pin_Interface:
    def __init__(self, GPIO_num):  
        self.label = get_label_from_pin(GPIO_num)
        if self.label == None:
            print('Wrong pin number inputted %d' % (GPIO_num))
            return
        
        self.pin = machine.Pin(GPIO_num, machine.Pin.IN)

    def isHigh(self):
        return self.pin.value() == 1
    
    def isLow(self):
        return self.pin.value() == 0