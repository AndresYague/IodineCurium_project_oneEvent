IodineCurium_project_oneEvent

Public version of the MonteCarlo code for the one event probability calculation for the Iodine and Curium project

==========How to use=========

Once the database directory (see README.txt file in there) contains the
appropriate deltas*.in files for the experiment, and the chosen ratios are
stored in the isoratios_sites.dat file (see example file
isoratios_sites.dat.example), then the input for the experiment can be selected in
oneEventMC.in. (see oneEventMC.in.example for an example file).

=========Published experiments=========

The experiments published from this code can be reproduced with the following
input files for the DZ10 mass models and ABLA07 fission fragments:

# Input file # 1, maximum pollution case

# Program options
nRuns = 1e6         # Number of runs for the MC experiment
gamma = 1.00e8      # Choosen gamma (in years) for non-mixed deltas
gammaMix = 2.00e8   # Choosen gamma (in years) for mixed deltas. Should always be double of gamma
writeEnd = False    # Wether to write to a file (True) or print to terminal (False)
diskIs = long       # can be long, short or mix, delta distribution for the disk
myrsBack = 100      # can be 0 (ESS values), 100 or 200 Myr back-decay from ESS values

# Input file # 2, minimum pollution case

# Program options
nRuns = 1e6         # Number of runs for the MC experiment
gamma = 5.00e8      # Choosen gamma (in years) for non-mixed deltas
gammaMix = 1.00e9   # Choosen gamma (in years) for mixed deltas. Should always be double of gamma
writeEnd = False    # Wether to write to a file (True) or print to terminal (False)
diskIs = short      # can be long, short or mix, delta distribution for the disk
myrsBack = 100      # can be 0 (ESS values), 100 or 200 Myr back-decay from ESS values
