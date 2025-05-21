import machine

# Constants for PWM control
LED_PWM_FREQ = 5000                    # Frequency of the PWM signal in Hz
PWM_MAX_DUTYCYCLE_VALUE = 65536        # Maximum duty cycle value for 16-bit PWM
PWM_OFF = 0                            # Duty cycle value for LED OFF
PWM_ON = PWM_MAX_DUTYCYCLE_VALUE       # Duty cycle value for LED fully ON

class LED:
    def __init__(self, pwm_pin):
        """
        Initialize the LED object on the specified PWM-capable pin.
        Sets the PWM frequency and ensures the LED starts in the OFF state.
        
        :param pwm_pin: The GPIO pin number used for PWM output to the LED.
        """
        self.led = machine.PWM(machine.Pin(pwm_pin))  # Create PWM object on the given pin
        self.led.freq(LED_PWM_FREQ)                   # Set PWM frequency
        self.led.duty_u16(PWM_OFF)                    # Start with LED turned off

    def setDutyCycle_Pct(self, duty_cycle_pct):
        """
        Set the LED brightness using a percentage-based duty cycle.

        :param duty_cycle_pct: A value from 0 to 100 representing duty cycle percentage.
        :return: 0 on success, -1 on invalid input.
        """
        if duty_cycle_pct >= 0 and duty_cycle_pct <= 100:
            # Convert percentage to 16-bit duty cycle value and apply it
            self.led.duty_u16(int(duty_cycle_pct / 100.0 * PWM_MAX_DUTYCYCLE_VALUE))
            return 0
        else:
            print('Incorrect duty cycle input')
            return -1

    def LED_on(self):
        self.setDutyCycle_Pct(100)

    def LED_off(self):
        self.setDutyCycle_Pct(0)
