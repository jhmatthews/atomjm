#! /Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
'''
		coll.py
		
Synopsis:
	This code uses q and A values to work out whether
	we expect jumping probabilities to dominate over emission probabilities in 
	collisionally dominated regimes, and vice versa when most transitions
	are radiative.
	
Usage:
	python coll.py
	
Comments:
	Related to bug report #54
History:
	131121	Coding began
'''

from line_routines import A21, q12, q21, read_line_info, read_level_info, read_chianti_data
import numpy as np
from recomb_const import *
from recomb_sub import *
import sys
import os



# first create ATOMJM environment 
ATOMJM = os.environ["ATOMJM"]

# atomic data filenames for 20 level H atom
line_filename = "%s/data/h20_lines.py" % (ATOMJM)	# atomic data file
level_filename = "%s/data/h20_levels.py" % (ATOMJM)

# read line and level info from the file and places in a class instance array
line = read_line_info (line_filename)
level = read_level_info (level_filename)

lev_range = np.arange (20)


eprbs_tot, jprbs_tot = np.zeros ( 20 ), np.zeros ( 20 )
eprbs_coll, jprbs_coll = np.zeros ( 20 ), np.zeros ( 20 )
eprbs_rad, jprbs_rad = np.zeros ( 20 ), np.zeros ( 20 )
eprbs_norm, jprbs_norm = np.zeros ( 20 ), np.zeros ( 20 )
eprbs_norm_coll, jprbs_norm_coll = np.zeros ( 20 ), np.zeros ( 20 )
eprbs_norm_rad, jprbs_norm_rad = np.zeros ( 20 ), np.zeros ( 20 )

qvals = np.zeros ( 20 )
Avals = np.zeros ( 20 )
Elowers, delta_Es = np.zeros ( 20 ), np.zeros ( 20 )

T = 10000.0
ne = 1.0e13

for i in range(len(line)):
	
	upper = line[i].lu
	lower = line[i].ll
	
	for j in range(len(level)):
		if level[j].lvl == upper: E_up = level[j].E
		
		if level[j].lvl == lower: E_low = level[j].E

	# calculate q values and store		
	q_up = q12 ( line[i], T )
	q_dn = q21 ( line[i], T )
	qvals[upper-1] += q_dn

	# calculate A values and store	
	Aval = A21 ( line[i] )
	Avals[upper-1] += Aval

	# calculate level energies and store	
	delta_E = E_up - E_low
	Elowers[upper-1] += E_low
	delta_Es[upper-1] += delta_E
	
	
	coll_rate = q_dn * ne 
	rad_rate = Aval
	
	rate_tot = coll_rate + rad_rate
	


import pylab	

pylab.subplot(311)
pylab.plot( lev_range, qvals)
pylab.ylabel("q21")

pylab.subplot(312)
pylab.plot( lev_range, Avals)
pylab.ylabel("A21")

pylab.subplot(313)
pylab.plot( lev_range, Elowers, label = "E_1")
pylab.plot( lev_range, delta_Es, label = "sum delta_E")
pylab.legend()
pylab.ylabel("E")
pylab.xlabel("n")
pylab.savefig("Figure1.png")
	
	
	
	
	
	
	
	
	
	
