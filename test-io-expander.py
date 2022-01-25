import time
from pimoroni_i2c import PimoroniI2C
from breakout_ioexpander import BreakoutIOExpander

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
    {"id": 2,"name": "Effect 3","pin": 6}
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
        if(not ioe.input(bank["pin"])):
            if (activeBank is not bank["id"]):
                bankChanged = True
                activeBank = bank["id"]
                activateFirsEffectOfBank()
                print(banks[activeBank]["name"] + " and " + effects[activeEffect]["name"] + " actives")
            break
        
def activateFirsEffectOfBank():
    global activeEffect
    activeEffect = 0
        
def updateActiveEffect():
    global activeEffect
    global effectChanged
    for effect in effects:
        if(not ioe.input(effect["pin"])):
            if (activeEffect is not effect["id"]):
                effectChanged = True
                activeEffect = effect["id"]
                print(banks[activeBank]["name"] + " and " + effects[activeEffect]["name"] + " actives")
            break
        
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
    while(not effectOrBankChanged()):
        print("Start effect (" + str(activeBank) + ":" + str(activeEffect) + ") [" + banks[activeBank]["name"] + " and " + effects[activeEffect]["name"] + "]")
        time.sleep(1)
        if (effectOrBankChanged()):
            break
        time.sleep(1)
        if (effectOrBankChanged()):
            break
        print("End effect [" + banks[activeBank]["name"] + " and " + effects[activeEffect]["name"] + "]")
    
initialiseBanks()
initialiseEffects()

while True:
    updateActiveBank()
    updateActiveEffect()
    runActiveBankEffect()
    # time.sleep(0.25)