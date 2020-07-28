import matplotlib.pyplot as plt
import numpy as np
import random

class Distribution(object):
    '''Class for creating a distribution and
    retreiving the values'''
    
    def __init__(self, array, binSize = None):
        '''Initialize distribution'''
        
        # Get the binsize
        self.minDist = min(array)
        self.maxDist = max(array)
        if binSize is None:
            self.binSize = 1e-2*(maxDist - minDist)
        else:
            self.binSize = binSize
        
        # Number of bins
        nZeros = (self.maxDist - self.minDist)/self.binSize
        if nZeros > int(nZeros):
            nZeros += 1
        nZeros = int(nZeros)
        
        # Get the distribution
        self.distribution = np.zeros(nZeros)
        
        # Count the occurences
        for val in array:
            ii = int((val - self.minDist)/self.binSize)
            self.distribution[ii] += 1
        
        self.lenDist = len(self.distribution)
        self.distribution /= max(self.distribution)
    
    def getProb(self, val):
        '''Return probability for value val'''
        
        ii = int((val - self.minDist)/self.binSize)
        if ii < 0 or ii > self.lenDist - 1:
            return 0
        else:
            return self.distribution[ii]
    
def muinitcalc(tauCm, tauI, muess, tlaste):
    # the variables are randomly generated (Cm, I mean lives; muess; time from last event)
    taueq = (tauCm * tauI) / (tauCm - tauI)
    muinit = muess * np.exp(tlaste / taueq)
    return muinit

def generateDistribution(nRuns, myrsBack, binSize = None):
    Cm_T       = 15.6 # Myr, halflife
    Cm_err     = 0.5  # Myr, 1 sigma of halflife error
    II_T       = 15.7 # Myr
    II_err     = 0.4  # Myr
    muess      = 438  # Cm/I
    muess_err  = 92 # 1 sigma of Cm/I at ESS
    
    
    muinits = []
    for cyc in range(nRuns):
        tauCm_rand = np.random.normal(Cm_T, Cm_err)/np.log(2)
        tauI_rand  = np.random.normal(II_T, II_err)/np.log(2)
        muess_rand = np.random.normal(muess, muess_err)
        muinit_rand = muinitcalc(tauCm_rand, tauI_rand, muess_rand, myrsBack)
        if muinit_rand > 0:
            muinits.append(muinit_rand)
    
    muinit_mid = np.median(muinits)
    muinit_min_1sig = np.percentile(muinits, 15.865)
    muinit_max_1sig = np.percentile(muinits, 84.135)
    muinit_min_2sig = np.percentile(muinits, 2.275)
    muinit_max_2sig = np.percentile(muinits, 97.725)
    
    
    #muinit_minus = muinit_mid - muinit_min_2sig
    #muinit_plus = muinit_max_2sig - muinit_mid
    
    print("Initial ratio median: {:.2f}".format(muinit_mid))
    print("Median + 48%: {:.2f}".format(muinit_max_2sig))
    print("Median - 48%: {:.2f}".format(muinit_min_2sig))
    
    # Create the distribution
    distribution = Distribution(muinits, binSize)
    
    return distribution

def evolve(i1, cm1, i2, cm2, delta):
    # Mean lives in years
    tau1 = np.random.normal(15.7, 0.4)/np.log(2)*1e6
    tau2 = np.random.normal(15.6, 0.5)/np.log(2)*1e6
    
    #Evolve p1 from 0 to delta
    iodine = i1*np.exp(-delta/tau1)
    curium = cm1*np.exp(-delta/tau2)
    
    # Calculate percentage
    percent = 0.5*(iodine/(i2 + iodine) + curium/(cm2 + curium))
    
    # Now add the new ones and return
    iodine += i2
    curium += cm2
    
    return iodine/curium, percent, tau1/1e6, tau2/1e6

def main():
    random.seed()
    
    # Get the options from "oneEventMC.in"
    optDict = {}
    with open("oneEventMC.in") as fread:
        for line in fread:
            if line[0] == "#":
                continue
            
            lnlst = line.split()
            optDict[lnlst[0]] = lnlst[2]
    
    # Parse the options
    nRuns = int(float(optDict["nRuns"]))
    gamma = optDict["gamma"]
    gammaMix = optDict["gammaMix"]
    writeEnd = True if optDict["writeEnd"] is "True" else False
    diskIs = optDict["diskIs"]
    myrsBack = int(float(optDict["myrsBack"]))
    
    # Get distribution
    print("Calculating distribution of ESS values")
    
    ratioDistribution = generateDistribution(nRuns*10, myrsBack, binSize = 1)
    
    print("Doing two-events calculation")
    
    # Define box, power and mix
    box = "box_3e6_5e7_gamma_"
    power = "pow_5e7_1e10_gamma_"
    mixed = "mixed_gamma_"
    
    # Read deltas
    deltBoxFile = "database/deltas_" + box + gamma + "_tend_1e11_1e3runs.in"
    deltPowFile = "database/deltas_" + power + gamma + "_tend_1e11_1e3runs.in"
    deltMixedFile = "database/deltas_" + mixed + gammaMix + "_tend_1e11_1e3runs.in"
    with open(deltBoxFile, "r") as fread:
        allBoxDeltas = [float(x) for x in fread.readline().split()]
    with open(deltPowFile, "r") as fread:
        allPowDeltas = [float(x) for x in fread.readline().split()]
    with open(deltMixedFile, "r") as fread:
        allMixedDeltas = [float(x) for x in fread.readline().split()]
    
    # Read ratios
    allRatios = []
    with open("isoratios_sites.dat", "r") as fread:
        for line in fread:
            lnlst = line.split()
            if len(lnlst) == 0 or "#" in line:
                continue
            
            iodVal = float(lnlst[-2])
            cmVal = float(lnlst[-1])
            tag = " ".join(lnlst[:-5])
            allRatios.append((tag, iodVal, cmVal))
    
    finalRatios = []
    while len(finalRatios) < nRuns:
        # Here we get the values corresponding to each event
        tag1, i1, cm1 = random.choice(allRatios)
        tag2, i2, cm2 = random.choice(allRatios)
        
        caseNum = 0
        if "dyn" in tag1 and "dyn" in tag2:
            caseNum = 1
        elif "MHD" in tag1 and "MHD" in tag2:
            caseNum = 2
        elif "dyn" in tag1 + tag2 and "MHD" in tag1 + tag2:
            caseNum = 3
        elif "Disk" in tag1 and "Disk" in tag2:
            if diskIs == "long":
                caseNum = 1
            elif diskIs == "short":
                caseNum = 2
            elif diskIs == "mix":
                caseNum = 3
        elif "Disk" in tag1 + tag2 and "dyn" in tag1 + tag2:
            if diskIs == "long":
                caseNum = 1
            else:
                caseNum = 3
        elif "Disk" in tag1 + tag2 and "MHD" in tag1 + tag2:
            if diskIs == "short":
                caseNum = 2
            else:
                caseNum = 3
        
        if caseNum == 0:
            raise Exception("Check case number!")
        
        # Get the delta
        if caseNum == 1:
            delta = random.choice(allPowDeltas)
        if caseNum == 2:
            delta = random.choice(allBoxDeltas)
        if caseNum == 3:
            delta = random.choice(allMixedDeltas)
        
        ratio, percent, tau1, tau2 = evolve(i1, cm1, i2, cm2, delta)
        
        # Filter the ratios and store:
        if random.random() < ratioDistribution.getProb(ratio):
            finalRatios.append((ratio, percent, tag1, tag2))
    
    # Now count how many are 1 event
    nn25 = 0; nn10 = 0; nn1 = 0
    nnDisk = 0; nnNoDisk = 0; nnFirstDisk = 0; nnSecondDisk = 0
    nnDisk25 = 0; nnSecondDisk25 = 0
    nnDisk10 = 0; nnSecondDisk10 = 0; nnDisk1 = 0; nnSecondDisk1 = 0
    for info in finalRatios:
        ratio, percent, tag1, tag2 = info
        
        # Both disks
        if "Disk" in tag1 and "Disk" in tag2:
            nnDisk += 1
            if percent < 0.25 or percent > 4:
                nnDisk25 += 1
            if percent < 0.1 or percent > 10:
                nnDisk10 += 1
            if percent < 0.01 or percent > 100:
                nnDisk1 += 1
        
        # One disk
        if "Disk" in tag1 and "Disk" not in tag2:
            nnFirstDisk += 1
        if "Disk" in tag2 and "Disk" not in tag1:
            nnSecondDisk += 1
            if percent < 0.25 or percent > 4:
                nnSecondDisk25 += 1
            if percent < 0.1 or percent > 10:
                nnSecondDisk10 += 1
            if percent < 0.01 or percent > 100:
                nnSecondDisk1 += 1
        
        # No disks
        if "Disk" not in tag1 and "Disk" not in tag2:
            nnNoDisk += 1
        
        # Less than 25%
        if percent < 0.25 or percent > 4:
            nn25 += 1
        
        # Less than 10%
        if percent < 0.1 or percent > 10:
            nn10 += 1
        
        # Less than 1%
        if percent < 0.01 or percent > 100:
            nn1 += 1
    
    # Chose file to write or stdout
    if writeEnd:
        fun = lambda x: fwrite.write(x + '\n')
    else:
        fun = lambda x: print(x)
    writeName = "diskDTD_" + diskIs + "_" + gamma
    writeName += "_backTime_{:.2E}_DC3".format(myrsBack)
    
    totNN = float(len(finalRatios))
    if writeEnd:
        fwrite = open(writeName, "w")
    
    fun("{:.2f}% of events < 25%".format(nn25/totNN*100))
    fun("{:.2f}% of events < 10%".format(nn10/totNN*100))
    fun("{:.2f}% of events < 1%".format(nn1/totNN*100))
    fun("{:.2f}% of events are two disks".format(nnDisk/totNN*100))
    #fun("-> of which {:.2f}% < 25%".format(nnDisk25/float(nnDisk)*100))
    #fun("-> of which {:.2f}% < 10%".format(nnDisk10/float(nnDisk)*100))
    #fun("-> of which {:.2f}% < 1%".format(nnDisk1/float(nnDisk)*100))
    fun("{:.2f}% of events are no disks".format(nnNoDisk/totNN*100))
    fun("{:.2f}% of events is first disk".format(nnFirstDisk/totNN*100))
    fun("{:.2f}% of events is second disk".format(nnSecondDisk/totNN*100))
    fun("-> of which {:.2f}% < 25%".format(nnSecondDisk25/float(nnSecondDisk)*100))
    fun("-> of which {:.2f}% < 10%".format(nnSecondDisk10/float(nnSecondDisk)*100))
    fun("-> of which {:.2f}% < 1%".format(nnSecondDisk1/float(nnSecondDisk)*100))
    
    if writeEnd:
        fwrite.close()
    

if __name__ == "__main__":
    main()
