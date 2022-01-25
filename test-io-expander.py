import time
import math
import plasma
from plasma import plasma2040
from pimoroni_i2c import PimoroniI2C
from pimoroni import RGBLED
from breakout_ioexpander import BreakoutIOExpander

# Set how many LEDs you have
NUM_LEDS = 144

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)
# Start updating the LED strip
led_strip.start()

led = RGBLED(plasma2040.LED_R, plasma2040.LED_G, plasma2040.LED_B)

# The speed that the LEDs will start cycling at
DEFAULT_SPEED = 50
HIGH_SPEED = 255

# How many times the LEDs will be updated per second
UPDATES = 60

# I2C config
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}
i2c = PimoroniI2C(**PINS_PICO_EXPLORER)
ioe = BreakoutIOExpander(i2c, address=0x18)

#Banks
banks = [
    {"id": 0,"name": "Bank A","pin": 1},
    {"id": 1,"name": "Bank B","pin": 2},
    {"id": 2,"name": "Bank C","pin": 3}
]

# The first bank is active by default
activeBank = 0
bankChanged = False

#Effects
effects = [
    {"id": 0,"name": "Effect 1","pin": 4},
    {"id": 1,"name": "Effect 2","pin": 5},
    {"id": 2,"name": "Effect 3","pin": 6},
    {"id": 3,"name": "Effect 4","pin": 7},
    {"id": 4,"name": "Effect 5","pin": 8},
    {"id": 5,"name": "Effect 6","pin": 9},
    {"id": 6,"name": "Effect 7","pin": 10}
]

# The first effect is active by default
activeEffect = 0
effectChanged = False

def initialiseBanks():
    for bank in banks:
        ioe.set_mode(bank["pin"], BreakoutIOExpander.PIN_IN_PU)
        
def initialiseEffects():
    for effect in effects:
        ioe.set_mode(effect["pin"], BreakoutIOExpander.PIN_IN_PU)

def updateActiveBank():
    global activeBank
    global bankChanged
    for bank in banks:
        if(isBankSelected(bank)):
            setActiveBank(bank);
            # When the active bank changes, we run the first effect of the bank
            activateFirsEffectOfBank()
            break
        
def isBankSelected(bank):
    global activeBank
    return switched(bank) and isNotAlreadyActive(activeBank, bank)

def setActiveBank(bank):
    global activeBank
    global bankChanged
    activeBank = bank["id"]
    bankChanged = True
    print(banks[activeBank]["name"] + " and " + effects[activeEffect]["name"] + " actives")
        
def activateFirsEffectOfBank():
    global activeEffect
    activeEffect = 0
        
def updateActiveEffect():
    global activeEffect
    global effectChanged
    for effect in effects:
        if(isEffectSelected(effect)):
            setActiveEffect(effect)
            break
        
def isEffectSelected(effect):
    global activeEffect
    return switched(effect) and isNotAlreadyActive(activeEffect, effect)

def setActiveEffect(effect):
    global activeEffect
    global effectChanged
    activeEffect = effect["id"]
    effectChanged = True
    print(banks[activeBank]["name"] + " and " + effects[activeEffect]["name"] + " actives")
    
# Switches are connected in pull-up mode so by default the state is 'high'. When a switch is pressed, the state changes to 'low'
def switched(switch):
    return not ioe.input(switch["pin"])

def isNotAlreadyActive(aciveSwitch, switch):
    return aciveSwitch is not switch["id"]
        
def effectOrBankChanged():
    global bankChanged
    global effectChanged
    updateActiveBank()
    updateActiveEffect()
    if (bankChanged or effectChanged):
        print("Bank or effect changed!")
        bankChanged = False
        effectChanged = False
        return True
    else:
        return False

def runActiveBankEffect():
    global activeEffect
    while(not effectOrBankChanged()):
        # print("Start effect (" + str(activeBank) + ":" + str(activeEffect) + ") [" + banks[activeBank]["name"] + " and " + effects[activeEffect]["name"] + "]")
        if (math.fmod(activeEffect, 2) == 0):
            rainbow(DEFAULT_SPEED)
        else:
            rainbow(HIGH_SPEED)
        # print("End effect [" + banks[activeBank]["name"] + " and " + effects[activeEffect]["name"] + "]")
        
offset = 0.0
count = 0

def resetEffect():
    global offset
    global count
    offset = 0.0
    count = 0

def rainbow(speed):
    global offset
    global count
    offset += float(speed) / 2000.0

    for i in range(NUM_LEDS):
        hue = float(i) / NUM_LEDS
        led_strip.set_hsv(i, hue + offset, 1.0, 1.0)

    led.set_rgb(speed, 0, 255 - speed)

    count += 1
    if count >= UPDATES:
        count = 0

    time.sleep(1.0 / UPDATES)
    
    
initialiseBanks()
initialiseEffects()

while True:
    resetEffect()
    runActiveBankEffect()