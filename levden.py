


import sys
from line_routines import *
import recomb_sub as sub
import matplotlib.pyplot as plt


sub.setpars()

filename = sys.argv[1]


f = open( filename, "r" )


n, levden = [], []
for line in f:
	data = line.split()
	n.append (int(data[1]))
	
	levden.append (float(data[3]))


fig = plt.figure()
ax = fig.add_subplot(211)
ax.plot(n[0:20], np.array(levden[0:20]), label = "Python")


nr = np.sum ( levden[0:20] )
print nr

T = 2.5e+04 
ATOMJM = os.environ["ATOMJM"]


#Let's work with an n level Hydrogen atom, up to 20.
line_filename = "%s/data/h20_lines.py" % (ATOMJM)	# atomic data file
level_filename = "%s/data/h20_levels.py" % (ATOMJM)


level = read_level_info (level_filename)

bolt = boltzmann (level, T, nr)
ax.plot(n[0:20], bolt[0:20],"r--", label = "LTE")
ax.set_ylabel("$N_i / N$")
ax.set_xlabel("n")
ax.set_yscale("log")

ax = fig.add_subplot(212)


levden_rel = []

for i in range(1,len(levden)):
	levden_rel.append(levden[i]/levden[i-1])

ax.plot(n[0:19], np.array(levden_rel[0:19]), label = "Python")

bolt = boltzmann_rel (level, T, levden[0], level[0].g)
ax.plot(n[0:19], bolt[0:19], "r--", label = "LTE")
ax.set_ylabel("$N_{i+1} / N_i$")
ax.set_xlabel("i (level)")
#ax.set_yscale("log")
plt.legend(loc=4)

plt.show()

x = np.zeros(20)
n = np.arange(1,21)
for i in range(20):

	x[i] = level[i].E

y = np.exp ( ( - x  * 1.6e-19) / ( 1.38e-23 * T) ) 	

yy = 2.0 * ( n**2 ) / 2.0	

print y, yy
	
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(y*yy)
#ax.plot(yy)
plt.show()



