import sys
import matplotlib.pyplot as plt
import numpy as np

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 {} <input> [<input2>]".format(sys.argv[1]))
        return 1
    
    # Get file name
    arch = sys.argv[1:]
    
    # Read tEvents and calculate the deltas
    tEvents = []
    for read in arch:
        with open(read, "r") as fread:
            ii = 1
            for line in fread:
                if len(tEvents) < ii:
                    tEvents.append([])
                
                tEvents[ii - 1] += [float(x) for x in line.split()]
                ii += 1
    
    for lst in tEvents:
        lst.sort()
    
    deltas = []
    for lst in tEvents:
        for ii in range(1, len(lst) - 1):
            deltas.append(lst[ii + 1] - lst[ii])
    
    # Get delta average
    meanDeltas = np.mean(deltas)
    
    # Get archName
    archName = arch[0]
    archName = archName.replace("tEvents", "deltas")
    isMixed = False
    if len(arch) > 1:
        if "pow" in arch[0] and "box" in arch[1]:
            archName = archName.replace("pow", "mixed")
            isMixed = True
        if "box" in arch[0] and "pow" in arch[1]:
            archName = archName.replace("box", "mixed")
            isMixed = True
        
        # Remove the distribution limits from the mixed name
        if isMixed:
            spltName = archName.split("_")
            archName = ""
            foundMixed = False
            for elem in spltName:
                if foundMixed:
                    if elem == "gamma":
                        foundMixed = False
                    else:
                        continue
                
                if elem == "mixed":
                    foundMixed = True
                
                # Be careful with last element
                if ".in" in elem:
                    archName += elem
                else:
                    archName += elem + "_"
    
    with open(archName, "w") as fwrite:
        s = ""
        for delta in deltas:
            s += "{:E} ".format(delta)
        fwrite.write(s)
    
    plt.hist(deltas, bins = int(1e3))
    plt.yscale("log")
    plt.xscale("log")
    plt.show()

if __name__ == "__main__":
    main()
