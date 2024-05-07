import json

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'


usedMUX1Pins = []
usedMUX2Pins = []

def find_key_by_value(data, target_value, mode):
    # Search in the 'Inputs' dictionary for the target value
    if mode == 'Inputs':
        for key, value in data['Inputs'].items():
            if value == target_value:
                return key
    elif mode == 'Outputs':
        for key, value in data['Outputs'].items():
            if value == target_value:
                return key
    return None

def load_multiplexer_config(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

def export_connections(config, MCUpin, MAINpin, mode):

    mux1 = config['Multiplexers'][0]
    mux2 = config['Multiplexers'][1]

    currentMCUBreadboardPin = "MCUBreadboard" + str(MCUpin)
    currentMainBreadboardPin = "MainBreadboard" + str(MAINpin)
    
    YOfMCUBreadboard = find_key_by_value(mux1, currentMCUBreadboardPin, "Inputs")
    YOfMCUBreadboard = "MUX1_" + YOfMCUBreadboard

    XOfMainBreadboard = find_key_by_value(mux1, currentMainBreadboardPin, "Outputs")
    if XOfMainBreadboard is None:
        XOfMainBreadboard = find_key_by_value(mux2, currentMainBreadboardPin, "Outputs")
        XOfMainBreadboard = "MUX2_" + XOfMainBreadboard
    else:
        XOfMainBreadboard = "MUX1_" + XOfMainBreadboard

    # print(str(currentMCUBreadboardPin) + ": " + str(YOfMCUBreadboard) + " | " + str(currentMainBreadboardPin) + ": " + str(XOfMainBreadboard))

    splitYOfMCUBreadboard = YOfMCUBreadboard.split("_")
    splitXOfMainBreadboard = XOfMainBreadboard.split("_")

    if splitYOfMCUBreadboard[0] == splitXOfMainBreadboard[0]:
        print(f"SetConnection(1000, {splitYOfMCUBreadboard[1]}, {splitXOfMainBreadboard[1]}, {mode});")
    else:
        currentkey = None
        if mode == "false":
            usedMUX1Pins.pop()
            usedMUX2Pins.pop()

        for key, value in mux1['Outputs'].items():
            if key not in usedMUX1Pins:
                if key not in ["X8", "X9", "X10", "X11", "X12", "X13", "X14", "X15"]:
                    if mode == "true":
                        usedMUX1Pins.append(key)
                    currentkey = key
                    break
        else:
            print("No available pins in MUX1")
            return
        
        valueOfCurrentKey = mux1['Outputs'][currentkey]
        splitValueOfCurrentKey = valueOfCurrentKey.split("_")

        for key, value in mux2['Inputs'].items():
            if key not in usedMUX2Pins:
                if key == splitValueOfCurrentKey[1]:
                    if mode == "true":
                        usedMUX2Pins.append(key)
                    print(f"SetConnection(1000, {splitYOfMCUBreadboard[1]}, {currentkey}, {mode});")
                    print(f"SetConnection(1001, {key}, {splitXOfMainBreadboard[1]}, {mode});")
                    break
        else:
            print("No available pins in MUX2")    
                
            
if __name__ == "__main__":
    while True:
        export_connections(load_multiplexer_config('rules.json'), 1, 1)