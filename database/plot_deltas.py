import sys
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) > 1:
        filName = sys.argv[1]
    else:
        print("Give me a file name!")
        return 1
    
    with open(filName, "r") as fread:
        lnlst = [float(x)*1e-6 for x in fread.readline().split()]
    
    plt.hist(lnlst, bins = 1000, density = True)
    plt.xlabel("Time (Myr)")
    plt.title(filName)
    plt.xscale("log")
    plt.show()

main()
