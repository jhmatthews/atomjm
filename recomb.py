#! /Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
'''
		recomb.py
		
Synopsis:
	An attempt to calculate level populations in an n level
	H atom, based only on recombination coefficients and 
	A values (Einstein A coefficient).

Usage:
	python recomb.py [mode] [temp] [nlevels]
	
Comments:
	This code uses
History:
	131023		Coding began (matom effort)
'''

from line_routines import A21, q12, q21, read_line_info, read_level_info, read_chianti_data
import numpy as np
from recomb_const import *
from recomb_sub import *
import sys
import os

	
ATOMJM = os.environ["ATOMJM"]

# physical characteristics of medium
ne = 1.4e6			# electron density
nprots = 1.4e6		# H+ density
V = 1.3e23			# volume of cell


print "\nCalculating strength of recombination lines for Case A.\n\n"

mode = sys.argv[1]	
T = float(sys.argv[2])
nlevels = int(sys.argv[3])			# n level macro atom




#Let's work with an n level Hydrogen atom, up to 20.
line_filename = "%s/data/h20_lines.py" % (ATOMJM)	# atomic data file
level_filename = "%s/data/h20_levels.py" % (ATOMJM)


# this next line simply reads line info from the file and places in a line class instance
line_info = read_line_info (line_filename)

# obtain recombination coefficients
if mode == "cloudy":
	data_use = get_cloudy_recombs()
	alphas = [ get_cloudy_alpha (  n, T,  alpha_data = data_use) for n in range(1,nlevels+1) ]
	print alphas
	
if mode == "py":
	data_use = get_cloudy_recombs()
	alphas = [ get_cloudy_alpha (  n, T,  alpha_data = data_use) for n in range(1,nlevels+1) ]
	print alphas

# recombination coefficients from Osterbrock. 
# the subscript gives the name of the subshell
# note that entry 0 is level 1

if mode == "oster" or mode == "suboster":

	if T == 10000.0:
		alpha_S = np.array([ 1.58e-13, 2.34e-14, 7.81e-15, 3.59e-15 ])
		alpha_P = np.array([0.0, 5.35e-14, 2.04e-14, 9.66e-15])
		alpha_D = np.array([0.0, 0.0, 1.73e-14, 1.08e-14])
		alpha_F = np.array([0.0, 0.0, 0.0, 5.54e-15])
	
	elif T == 20000.0:
		alpha_S = np.array([ 1.08e-13, 1.60e-14, 5.29e-15, 2.40e-15 ])
		alpha_P = np.array([0.0, 3.24e-14, 1.23e-14, 5.81e-15])
		alpha_D = np.array([0.0, 0.0, 9.49e-15, 5.68e-15])
		alpha_F = np.array([0.0, 0.0, 0.0, 2.56e-15])
		
	else:
	
		print "Error, T must be 10000 or 20000 in oster mode"
		
	alpha_sum = alpha_S + alpha_P + alpha_D + alpha_F
	
	if mode == "suboster": 
		alphas = [alpha_S, alpha_P, alpha_D, alpha_F]

	print alpha_sum


if mode =="oster" or mode == "suboster":
	level_pops, emiss = level_populations ( nlevels, alpha_sum, ne, line_info)
	
else:
	level_pops, emiss = level_populations ( nlevels, alphas, ne, line_info)



if mode != "probs":

	print "A VALUES"
	line_max = 0 
	lines_to_do=[]
	for i_line in range(len(line_info)):
		if line_info[i_line].lu <= nlevels:
			print "A%i%i %8.4e" % (line_info[i_line].lu,  line_info[i_line].ll, A21 ( line_info[i_line] ))
			line_max += 1
			lines_to_do.append(i_line)


	print "\n  Level\t|\t  Pops     \t|  Emissivity rel to level 4"
	print "------------------------------------------------------"
	for i in range(1,len(level_pops)):
		print "  %i   \t|\t %8.2e \t|\t%.2f" % (i+1, level_pops[i], emiss[i]/emiss[3])


	# find where Halpha and Hbeta are in the line list
	for i_line in range(len(line_info)):

		if line_info[i_line].lu == 3 and line_info[i_line].ll == 2: 	# then it is H alpha
			where_H_alpha = i_line
			nu_H_alpha = line_info[i_line].freq
		
		if line_info[i_line].lu == 4 and  line_info[i_line].ll == 2: 	# then it is H beta
			nu_H_beta = line_info[i_line].freq
			where_H_beta = i_line


	# calculate line strengths for Halpha and Hbeta
	H_alpha = H * nu_H_alpha * A21(line_info[where_H_alpha]) * level_pops[2]
	H_beta = H * nu_H_beta * A21(line_info[where_H_beta]) * level_pops[3]



	# print out the relative emissivity of Halpha to Hbeta
	print "\nH_alpha / H_beta  %f\n" % (H_alpha / H_beta)



	# print out all other line strengths
	for i_line in lines_to_do:
		I = H *  A21(line_info[i_line]) * level_pops[line_info[i_line].lu - 1] *line_info[i_line].freq / H_beta
		print "Line strength %i => %i:  %.2f" % (line_info[i_line].lu, line_info[i_line].ll, I)
		
	print "\n"


#######################################################################################
#
#CHIANTI WORK
#
#######################################################################################


# read in chianti data
if mode == 'suboster' or mode == 'sub':
	print "\n\n"
	chianti_levels, chianti_wgfa = read_chianti_data ( level_filename = ATOMJM + "/data/h_1.clvlc", 
		                                               radiative_filename = ATOMJM + "/data/h_1.wgfa")

	print 'Read Chianti data.'

	npops, emiss_sub, emiss_principle, Halpha_ratio, lyman_ratio = subshell_pops ( 4, alphas, ne, chianti_levels, chianti_wgfa )


	for i_em in range(len(emiss)):
		print "Level %i, pops_nonsub %f pops_sub %f" % (i_em+1, 
			                                            emiss[i_em]/emiss[3], 
			                                            emiss_principle[i_em]/ emiss_principle[3])


	print "Halpha_ratio",  Halpha_ratio                              
	print "Lyman ratio", lyman_ratio








#####################################
#procedures for working out level information base on transition probabilities
#####################################

elif mode == "probs":


	transition_probs = np.loadtxt("transitions", dtype = "float", comments = "#", unpack=True)

	eprbs_norm = np.zeros(5)
	jprbs_norm = np.zeros(5)
	Anorm = np.zeros(5)
	Ajnorm = np.zeros(5)

	for i in range(len(transition_probs[0])):

		n_old = transition_probs[0][i]
		n_new = transition_probs[1][i]
		eprbs = transition_probs[2][i]
		jprbs = transition_probs[3][i]
	
		eprbs_norm[n_old-1] += eprbs
		jprbs_norm[n_old-1] += jprbs
		#print "jprbs %8.4e eprbs %8.4e" %( jprbs, eprbs)
		if n_old < 5 and n_new <5 and n_old >1 and n_new < n_old:
			E_old = level[n_old-1].E
			E_new = level[n_new-1].E
		
			if jprbs>0:
				ratio = jprbs/eprbs
			else:
				ratio = 0.0
			if E_new != 0:
				print "%i => %i   jprbs/eprbs   %8.4e   predicted   %8.4e" % ( n_old, n_new, eprbs/jprbs, (E_old - E_new) / E_new )
			
		for i_line in range(len(line_info)):
			if line_info[i_line].lu == n_old and line_info[i_line].ll == n_new:
				Anorm[n_old-1] += A21(line_info[i_line]) * line_info[i_line].freq
				if jprbs>0:
					Ajnorm[n_old-1] += A21(line_info[i_line]) 






	for i in range(len(transition_probs[0])):

		# level in transition probability matrix
		n_old = transition_probs[0][i]
		n_new = transition_probs[1][i]
	
		# normalise transition probability
		eprbs = transition_probs[2][i] / eprbs_norm[n_old-1] 
		jprbs = transition_probs[3][i] / jprbs_norm[n_old-1]
	
	
		for i_line in range(len(line_info)):
			if line_info[i_line].lu == n_old and line_info[i_line].ll == n_new:
				Aval =  (A21(line_info[i_line])* line_info[i_line].freq) / Anorm[n_old-1]
				if jprbs>0:
					Ajval = (A21(line_info[i_line])) / Ajnorm[n_old-1]
					print "%i => %i eprbs %f jprbs %f Ae value %f Aj value %f" % ( n_old, n_new, eprbs, jprbs, Aval, Ajval)
				else:
					print "%i => %i eprbs %f jprbs %f Ae value %f" % ( n_old, n_new, eprbs, jprbs, Aval)
				
		if n_old == 5 and n_new < 5:	# then we have a recombination process

			alpha_val = alpha_sum[n_new-1] / np.sum(alpha_sum)
			if n_new!=1:
				alpha_jval = alpha_sum[n_new-1] / np.sum(alpha_sum[1:])
				print "%i => %i eprbs %f jprbs %f alphae %f alphaj %f" % ( n_old, n_new, eprbs, jprbs, alpha_val, alpha_jval)
			else:
				print "%i => %i eprbs %f jprbs %f alphae %f" % ( n_old, n_new, eprbs, jprbs, alpha_val)
			
			









