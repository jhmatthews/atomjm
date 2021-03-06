#! /Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
'''
		recomb_sub.py
		
Synopsis:
	Subroutines for an attempt to calculate level populations in an n level
	H atom, based only on recombination coefficients and 
	A values (Einstein A coefficient).
	
	

Usage:
	
Comments:

History:
	131023		Coding began (matom effort)
'''

from line_routines import A21, q12, q21, read_line_info, read_level_info, read_chianti_data
import numpy as np
from recomb_const import *
import os, sys
import matplotlib.pyplot as plt

# set ATOMJM os environment
ATOMJM = os.environ ['ATOMJM']



def levels_from_probs( n, eprbs, jprbs, eprbsnorm, jprbsnorm):
	'''
	Calculates level populations for an n level atom by considering the jumping
	probabilties '''
	return 0
	


def subshell_pops ( n, alphas, ne, level, rad_info ):

	'''
	Calculates level populations for an n level atom populated only by recombination
	and cascades from upper levels.
    
    :INPUT:  
            n:  			int      
                			number of levels in atom
            alphas:		float array
            				recombination coefficients for levels, split by subshell.
            				in form [alpha_s, alpha_p, etc...]
            ne:			float
            				electron density
            level		object array
						array of chianti_level class instances
			rad_info		object array
						array of chianti_rad class instances
						contains radiative information
	:OUTPUT:
            npops:				array
            						level populations in number / cm**3
            	emiss:				array
            						level emissivities in ergs
            	emiss_principal:		array
            						level emissivities in ergs summed over subshells
            						for each n
            		
     
     '''
	print 'SUBSHELL POPS:\n'
	print "----------------------------------------"
	print 'Calculating for %i level atom' % n
	
	
	# first check you have recombination coefficients for levels in question
	if len(alphas[0]) < n:
		print "Error: level_populations: Only %i alphas and a %i level atom" % (len(alphas),  n)
		return (-1)
	
	# work out which levels we are using. n here is the maximum principal quantum number we are using
	levels_used=[]
	for i in range ( len (level)):
		if level[i].n <= n : 
			levels_used.append ( level[i])
	
	
	# total levels is the sum of all subshells used and so is the length of the levels_used array
	total_levels = len(levels_used)
	
	
	emiss_principal = np.zeros(n)		# arrays of emissivity by principal quantum number
	npops = np.zeros(total_levels)		# level population by sub state
	emiss = np.zeros(total_levels)		# emissivity by sub state
	
	halpha = 0.0
	hbeta = 0.0
	lyman = 0.0
	
	# now cycle over levels, with the highest first	
	# for level 1s the i index is 0
	# for the highest level e.g. 4f the i index is total_levels - 1.
	for i in range ( total_levels - 1, -1, -1):
	
		subshell = levels_used[i].notation[1]			# subshell string, e.g. s, p
		n_level = levels_used[i].n						# principal quantum number of level
		
		
		
		# alpha_index helps us choose the recombination coefficient
		# according to the subshell we are working with
		# alphas are ordered by level and angular momentum
		alpha_index = levels_used[i].l		
		
		
		# get the relative weight of this specific state
		# relative to the sub orbital as a whole
		relative_weight = get_weight ( level, i)
		
		
		# initially set n_i to be the number of recombinations direct to this sub state
		# equal to recombinations to subshell times relative weight of state
		n_i = (ne * ne * alphas [alpha_index][n_level-1] * relative_weight)
		
		
		
		
		# now we need to loop over all higher levels and work out their contribution to the 
		# level population, given by A12 * n2
		for j in range (i + 1, total_levels):
		
			upper = levels_used[j].notation		# LS coupling notation for upper subshell
			lower = levels_used[i].notation		# LS coupling notation for lower subshell
		
			J_upper = levels_used[j].j
			J_lower = levels_used[i].j
			
			# loop over all lines in the wgfa file
			for i_line in range(len(rad_info)):
				
				if rad_info[i_line].note_up == upper and \
				   rad_info[i_line].note_low == lower and \
				   rad_info[i_line].J_up == J_upper and \
				   rad_info[i_line].J_low == J_lower:

					#add the cascades from upper into i
					n_i += rad_info[i_line].A * npops[j]		# add the contribution
						
						
		
		Asum = 0
	
		#now sum up the A coefficients for all downward transitions from level i
		for j in range( i-1, -1, -1):
		
			upper = levels_used[i].notation		# LS coupling notation for upper subshell
			lower = levels_used[j].notation		# LS coupling notation for lower subshell
			
			J_upper = levels_used[i].j
			J_lower = levels_used[j].j
			#print upper, lower
			
			# loop over all lines in the wgfa file
			for i_line in range(len(rad_info)):

				if rad_info[i_line].note_up == upper and \
				   rad_info[i_line].note_low == lower and \
				   rad_info[i_line].J_up == J_upper and \
				   rad_info[i_line].J_low == J_lower:
					Asum += rad_info[i_line].A



		# dividing by the sum of A coefficients out of level i gives level populations
		
		n_i = n_i / Asum
		
		npops[i] = n_i
		
	
	
		
		# we know have level populations, can work out level emissivities = A_ij n_i h nu_ij
		for j in range(i, -1, -1):
		
			upper = levels_used[i].notation		# LS coupling notation for upper subshell
			lower = levels_used[j].notation		# LS coupling notation for lower subshell
			J_upper = levels_used[i].j
			J_lower = levels_used[j].j
		
			emiss_sum = 0.
			for i_line in range(len(rad_info)):

				if rad_info[i_line].note_up == upper and \
				   rad_info[i_line].note_low == lower and \
				   rad_info[i_line].J_up == J_upper and \
				   rad_info[i_line].J_low == J_lower:
				   
					emiss_sum += rad_info[i_line].A * n_i * H * rad_info[i_line].freq
					
					if upper[0] == '4' and lower[0] == '2':
						hbeta += rad_info[i_line].A * n_i * H * rad_info[i_line].freq
					if upper[0] == '3' and lower[0] == '2':
						halpha += rad_info[i_line].A * n_i * H * rad_info[i_line].freq
					if upper[0] == '2' and lower[0] == '1':
						lyman += rad_info[i_line].A * n_i * H * rad_info[i_line].freq
			
			emiss[i] = emiss_sum
			emiss_principal[ n_level - 1] += emiss_sum
		
		print "Level %i, %s: n_i %8.4e weighted %8.4e " %( i, levels_used[i].notation, n_i, n_i/relative_weight)
	
	
	h_alpha_ratio = halpha / hbeta
	lyman_ratio = lyman / hbeta
	print emiss_principal
	print npops
	return npops, emiss, emiss_principal, h_alpha_ratio, lyman_ratio
	
	
	





def level_populations ( n, alphas, ne, line ):

	'''
	Calculates level populations for an n level atom populated only by recombination
	and cascades from upper levels.
    
    :INPUT:  
            n:  			int      
                			number of levels in atom
            alphas:		float array
            				recombination coefficients for levels.
            ne:			float
            				electron density

    :OUTPUT:
            npops:		array
            				level populations in number / cm**3
            	emiss:		array
            				level emissivities in ergs
            				
    :EXAMPLE:
            levels = level_populations ( n, alphas, ne )
            
    :COMMENTS:
    		careful with indices here. 0 in the alphas array is 1 in other arrays. 
    		
    		This is works out level populations by doing:
    			nrecombs direct to this level + number of transitions from upper levels to this level,
    			divided by the sum of the A coefficients for downwards transitions 
	'''
	
	npops = np.zeros(n)
	emiss = np.zeros(n)
	
	# first check you have recombination coefficients for levels in question
	if len(alphas) < n:
		print "Error: level_populations: Only %i alphas and a %i level atom" % (len(alphas),  n)
		return (-1)

	print "\n\t%s\t|\t%s\t|\t%s\t\t|\t%s\t" % ("Level", "Asum*n_i", "Asum", "nrecombs")
	print "------------------------------------------------------------------------------"
	
	# now cycle over levels, with the highest first	
	for i in range(n, 1, -1):
		
		# initially set n_i to be the number of recombinations direct to level i
		n_i = (ne * ne * alphas[i-1])

		# Calculating cascades into level- do all levels above i up to n
		# we start with the higher levels so as to get the correct populations
		# for lower levels populated from above
		for upper in range(i+1, n+1):
		
			for i_line in range(len(line)):
				
				if line[i_line].lu == upper and line[i_line].ll == i:

						#add the cascades from upper into i
						n_i += A21 ( line[i_line] ) * npops[upper-1]		# add the contribution
		
		Asum = 0
		



		#now sum up the A coefficients for all downward transitions from level i
		for lower in range(i-1, 0, -1):
		
			for i_line in range(len(line)):

				if line[i_line].lu == i and line[i_line].ll == lower:
				
					Asum += A21 ( line[i_line] )

		# dividing by the sum of A coefficients out of level i gives level populations
		n_i = n_i / Asum
		
		npops[i-1] = n_i
		
		
		# we know have level populations, can work out level emissivities = A_ij n_i h nu_ij
		for lower in range(i-1, 0, -1):
		
			emiss_sum = 0.
			for i_line in range(len(line)):

				if line[i_line].lu == i and line[i_line].ll == lower:
					emiss_sum += A21 ( line[i_line] ) * n_i * H * line[i_line].freq
			
			emiss[i-1] = emiss_sum
		
		print "\t%i\t|\t%.4f  \t|\t%8.2e\t|\t%.4f\t" %(i, n_i*Asum, Asum,  (ne * ne*alphas[i-1]) )
	
	return npops, emiss
	




	
	
def get_weight (level_class, index):
		
	'''
	Using a chianti_level class, the class that stores level information from a clvlc file,
	get the relative statistical weight of a sub quantum state of a given subshell relative 
	to the subshell as a whole. 
    
    :INPUT:  
            level_class:  		object
            						chianti level class instance
            	index:				int
            						location of state in level class instance

    :OUTPUT:
            relative_weight:		float
            						relative statistical weight of quantum state
            						
    :EXAMPLE:
            weight = get_weight (rad_class, i)
            
    :COMMENTS:
    			due to some levels having multiple states we sometimes need to split up the 4f level, for example
    			by statistical weight. 
	'''
	
	# subshell string e.g. 2s
	subshell = level_class[index].notation
	
	weight_sum = 0.0
	
	# loop over all substates
	for i in range(len(level_class)):
		
		if level_class[i].notation == subshell:
			weight_sum += 1.0 * level_class[i].multiplicity
			
	
	# relative weight needs to be divided by weight for all these substates
	weight = ( 1.0 * level_class[index].multiplicity ) / weight_sum	
	
	return weight
		

def get_py_recombs():

	'''
	gets Python recombination data from file data/python_recombs.dat
	
	:INPUT: 
		none
		requires python_recombs.dat file in $ATOMJM/data/
	
	:OUTPUT:
		alphas:		float array
					array of python recomb data, indexed by level. 
				
				
	:COMMENTS:
		make sure you have the $ATOMJM environment variables
		set up.
	'''

	data = "%s/data/python_recombs.dat" % ATOMJM
	
	array = np.loadtxt(data, comments ="#", dtype = "float")
	
	array = np.transpose(array)
	
	alphas = array[0:2]
	
	return alphas



	
def get_py_alpha ( n, T, alpha_data = get_py_recombs() ):
	
	'''
	gets the python recombination coefficient at 10000K or 20000K
	'''
	
	if T==10000.0:
		alpha = alpha_data[1][n-1]
		
	elif T==20000.0:
		alpha = alpha_data[0][n-1]
		
	else:
		print 'Sorry, can only do recombination coefficients at 10000 or 2000K! Exiting.'
		sys.exit()
	
	return alpha
	
	











	
def get_cloudy_recombs():

	'''
	gets Cloudy recombination data from file data/h_iso_recomb.dat
	
	:INPUT: 
		none
		requires h_iso_recomb.dat file in $ATOMJM/data/
	
	:OUTPUT:
		array:	float array
				array of cloudy recomb data, indexed by level. 
				
				
	:COMMENTS:
		make sure you have the $ATOMJM environment variables
		set up.
	'''
	
	data = "%s/data/h_iso_recomb_mod.dat" % ATOMJM
	
	array = np.loadtxt(data, comments ="#", dtype = "float")
	
	array = np.transpose(array)
	
	array = array[2:]
	
	array = np.transpose(array)
	
	array = 10.0**array
	
	# can now index with [level][temperature_index]
	
	return array
	
	
	
	






	
	
def get_cloudy_alpha ( n, T, alpha_data = get_cloudy_recombs()):

	'''
	works out recombination coefficient for element nelem
	level n, by using cloudy data from h_iso_recomb.dat
	
	:INPUT:
		nelem:			int
						atomic number
		n:				int
						principal quantum number of level
		T:				float
						electron temperature, K
		data:			optional
						data array
						
	:OUTPUT:
		alpha:			float
						recombination coefficient in cm**-3 s**-1
						for principal quantum number n

	'''
	
	i_temp = int ( (np.log10(T) - 3.0) / 0.1)
	alpha = alpha_data [n-1][i_temp]
	
	return alpha	



	
'''
the routines below all deal with calculating recombination coefficients 
using the fitting formula presented by Ferguson & Ferland 1996

http://cdsads.u-strasbg.fr/abs/1997ApJ...479..363F

As yet I can't get these fits to spit out reasonable numbers. 
I get erroneously large recombination coefficients for n=3, for example.
'''	
	
	
def alpha_ferguson( n , T):

	'''
	get recombination coefficient for level n, electron temperature T
	
	:INPUT:
		n:			int
					principal quantum number of level
		T:			float
					Electron temperature, K
	
	:OUTPUT:
		alpha:		float
					recombination coefficient in cm**-3 s**-1
					for principal quantum number n
	'''
	
	x = np.log10 (T)
	
	if n <= 15:
	
		# if n is less than 15 we use the fitting formula from Ferguson and Ferland 1996
		alpha = ( 10.0 ** ( ferguson_F (x, n) ) ) / T

	
	elif n ==16:
		print "CASE B"
		alpha = ( 10.0 ** ( ferguson_F (x, n) ) ) / T
	else:
	
		print "Don't have enough Ferguson data to deal with n>15 yet- \
			   need to implement asymptotic formula, sorry! Exiting."
		sys.exit()

	
	return alpha
	





def ferguson_F (x, n):
	
	'''
	Equation (1) from Ferguson and Ferland 1996.
	Uses coefficients as input which should be taken from get_ferguson_data()
	
	:INPUT:
		x:			float
					log(T_e)
		n:			int
					principal quantum number of level
					
	:OUTPUT:
		F:			float
					F value for input to alpha calculation
					
	:COMMENTS:
		make sure you have the $ATOMJM environment variables
		set up.
		
	'''
	
	data = get_ferguson_data()
	
	coeffs = data[n-1] 
	
	#print coeffs
	
	numerator = coeffs[0] +  x*coeffs[2]  +   (x**2)*coeffs[4]  + \
	             (x**3)*coeffs[6]  +  (x**4)*coeffs[8] 
	
	denominator = 1.0 + x*coeffs[1] +  (x**2)*coeffs[3]  + \
	               (x**3)*coeffs[5] +  (x**4)*coeffs[7] 
	               
	F = 	numerator / denominator  
	                      
	
	print n, F, x, numerator, coeffs[0],  coeffs[2], coeffs[4],coeffs[6], coeffs[8]
	
	return F



	
	
def get_ferguson_data():
	
	'''
	gets Ferguson & Ferland 1996 data from file data/ferguson.dat
	
	:INPUT: 
		none
		requires ferguson.dat file in $ATOMJM/data/
	
	:OUTPUT:
		array:	float array
				array of fergusion data, indexed by level. 
				9 coefficients for each level
				
	:COMMENTS:
		make sure you have the $ATOMJM environment variables
		set up.
	'''
	
	
	data = ATOMJM + "/data/ferguson.dat"
	
	# import data into array, then transpose so array[n-1] is coefficients for level n
	array = np.loadtxt ( data, comments ="#", dtype = "float")	
	array = np.transpose ( array )
	
	return array
	
	
# set some standard parameters
def setpars():
    
	print 'Setting plot parameters for matplotlib.'
	plt.rcParams['lines.linewidth'] = 1.0
	plt.rcParams['axes.linewidth'] = 1.3
	plt.rcParams['font.family'] = 'serif'
	plt.rcParams['font.serif'] = 'Times New Roman'
	plt.rcParams['text.usetex']='True'
    
	return 0	
	

