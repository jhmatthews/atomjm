#! /Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
'''
	levden.py

Compares Python level populations to LTE
'''


# import modules
import sys
from line_routines import *
import recomb_sub as sub
import matplotlib.pyplot as plt

# set aTOMJM environment
ATOMJM = os.environ["ATOMJM"]

# set plotting parameters
sub.setpars()



# filename containing level populations in format 
# Level 20 Levden 1.0000e+00
filename = sys.argv[1]


# open file
f = open( filename, "r" )


# read level and populations from file, place in two arrays
n, levden = [], []

for line in f:
	data = line.split()

	n.append (int(data[1]))	
	levden.append (float(data[3]))



# now get relative populations relative to previous level
levden_rel = []

for i in range(1,len(levden)):
	levden_rel.append(levden[i]/levden[i-1])


# total of level pops, should sum to 1
nr = np.sum ( levden[0:20] )
print nr


# temperature
T = 2.5e+04 


# atomic data
#Let's work with an n level Hydrogen atom, up to 20.
line_filename = "%s/data/h20_lines.py" % (ATOMJM)	# atomic data file
level_filename = "%s/data/h20_levels.py" % (ATOMJM)

# read level information and get boltzmann factors
level = read_level_info (level_filename)
bolt = boltzmann (level, T, nr)

bolt_rel= boltzmann_rel (level, T)

fig = plt.figure()

# create subplot and plot N_i / Ntot
ax = fig.add_subplot(211)

ax.plot( n[0:20], np.array(levden[0:20]), label = "Python")
ax.plot( n[0:20], bolt[0:20], "r--", label = "LTE")

ax.set_ylabel("$N_i / N$")
ax.set_xlabel("n")
#ax.set_yscale("log")


# create subplot and plot N_{i+1} / N_i
ax = fig.add_subplot(212)

ax.plot(n[0:19], np.array(levden_rel[0:19]), label = "Python")
ax.plot(n[0:19], bolt_rel[0:19], "r--", label = "LTE")

ax.set_ylabel("$N_{i+1} / N_i$")
ax.set_xlabel("i (level)")
#ax.set_yscale("log")
plt.legend(loc=4)



# show plot
plt.show()



