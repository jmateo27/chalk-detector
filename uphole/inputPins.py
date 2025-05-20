input_pins = {
    'DPT_RST': 9,
    'DPT_IN':  10,
    'ENA_IN':  11
}

input_types = [
    'REGULAR',
    'INTERRUPT'
]

interrupt_types = [
     'RISING',
     'FALLING'
]

def get_label_from_pin(pin_number):
    for label, number in input_pins.items():
        if number == pin_number:
            return label
    return None  # Not found