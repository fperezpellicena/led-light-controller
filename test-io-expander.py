import time
from pimoroni_i2c import PimoroniI2C
from breakout_ioexpander import BreakoutIOExpander

PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

ioe_button_pins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
last_states = [True, True, True, True, True, True, True, True, True, True]
current_states = [True, True, True, True, True, True, True, True, True, True]

i2c = PimoroniI2C(**PINS_PICO_EXPLORER)
ioe = BreakoutIOExpander(i2c, address=0x18)

def initialiseInputPins():
    for ioe_button_pin in ioe_button_pins:
        ioe.set_mode(ioe_button_pin, BreakoutIOExpander.PIN_IN_PU)
        
def readInputPins():
    for ioe_button_pin in ioe_button_pins:
        if ioe.input(ioe_button_pin) == 1:
            current_states[ioe_button_pin - 1] = True
        else:
            current_states[ioe_button_pin - 1] = False
        
def checkInputPins():
    for ioe_button_pin in ioe_button_pins:
        current_state = current_states[ioe_button_pin - 1]
        last_state = last_states[ioe_button_pin - 1]
        if current_state is not last_state:
            print("Button " + str(ioe_button_pin) + " has been switched from " + str(last_state) + " to " + str(current_state))
        
        last_states[ioe_button_pin - 1] = current_state
    
initialiseInputPins()

while True:
    readInputPins();
    checkInputPins();
    time.sleep(0.25)