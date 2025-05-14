import machine
from inputPins import get_label_from_pin
from inputPins import input_types

class Input_Pin_Interface:
    def __init__(self, GPIO_num, input_type):  
        self.label = get_label_from_pin(GPIO_num)
        if self.label == None:
            print('Wrong pin number inputted %d' % (GPIO_num))
            return
        if input_type in input_types:
            if input_type == 'REGULAR':
                self.pin = machine.Pin(GPIO_num, machine.Pin.IN)
            else:
                self.pin = machine.Pin(GPIO_num, machine.Pin.IN, machine.Pin.PULL_DOWN)
        else:
            print('Wrong input type inputted %s' % (input_type))
            return
        
    def setUpInterrupt(self, handler):
        self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=handler)

    def isHigh(self):
        return self.pin.value() == 1
    
    def isLow(self):
        return self.pin.value() == 0