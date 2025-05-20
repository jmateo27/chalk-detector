import machine
from inputPins import get_label_from_pin
from inputPins import input_types
from inputPins import interrupt_types

class Input_Pin_Interface:
    def __init__(self, GPIO_num, input_type):  
        self.label = get_label_from_pin(GPIO_num)
        self.gpio_num = GPIO_num
        if self.label == None:
            print('Wrong pin number inputted %d' % (GPIO_num))
            return
        if input_type in input_types:
            if input_type == 'REGULAR':
                self.pin = machine.Pin(GPIO_num, machine.Pin.IN)
            else:
                print('This pin must be an interrupt. Set properly')
                
        else:
            print('Wrong input type inputted %s' % (input_type))
            return
        
    def setUpInterrupt(self, handler, interrupt_type):
        if interrupt_type in interrupt_types:
            if interrupt_type == 'FALLING':
                self.pin = machine.Pin(self.gpio_num, machine.Pin.IN, machine.Pin.PULL_UP)
                self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=handler)
            else:
                self.pin = machine.Pin(self.gpio_num, machine.Pin.IN, machine.Pin.PULL_DOWN)
                self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=handler)
        else:
            print('Wrong interrupt type inputted %s' % (interrupt_type))
        

    def isHigh(self):
        return self.pin.value() == 1
    
    def isLow(self):
        return self.pin.value() == 0