import machine

LED_PWM_FREQ = 5000
PWM_MAX_DUTYCYCLE_VALUE = 65536
PWM_OFF = 0
PWM_ON = PWM_MAX_DUTYCYCLE_VALUE

class LED:
    def __init__(self, pwm_pin):
        self.led = machine.PWM(machine.Pin(pwm_pin))
        self.led.freq(LED_PWM_FREQ)
        self.led.duty_u16(PWM_OFF)
    
    def setDutyCycle_Pct(self, duty_cycle_pct):
        if duty_cycle_pct >= 0 and duty_cycle_pct <= 100:
            self.led.duty_u16(int(duty_cycle_pct / 100.0 * PWM_MAX_DUTYCYCLE_VALUE))
            return 0
        else:
            print('Incorrect duty cycle input')
            return -1
        
    def LED_on(self):
        self.setDutyCycle_Pct(100)

    def LED_off(self):
        self.setDutyCycle_Pct(0)
