#! /Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python

import numpy as np
import matplotlib.pyplot as plt
import sys
import os



plt.rcParams['lines.linewidth'] = 1.0
plt.rcParams['axes.linewidth'] = 1.3
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'
plt.rcParams['text.usetex']='True'


NPLASMA = 1000
NLEVELS = 21


class jump:
	'''Stores information from a Python levels file'''
	def __init__(self, _pjnorm, _penorm, _coll_tot, _rad_tot, _jprbs, _eprbs):
		self.pjnorm = _pjnorm
		self.penorm = _penorm
		self.coll_tot = _coll_tot
		self.rad_tot = _rad_tot
		self.jprbs = _jprbs
		self.eprbs = _eprbs


def get_data ( normfile = "norms.out", probsfile = "probs.out", nplasma = NPLASMA, nlevels = NLEVELS):

	# load data
	data_norm = np.loadtxt ( normfile, usecols = ( 1, 3,5, 7, 9, 11), dtype = 'float' )

	data_probs = np.loadtxt ( probsfile, usecols = ( 1, 3, 5, 7, 9), dtype = 'float' )


	# first make plots of pjnorm and penorm

	data_norm = np.transpose(data_norm)
	data_probs = np.transpose (data_probs)

	nplasma_want = np.arange (0, NPLASMA)
	uplvls_want = np.arange (0, NLEVELS)


	jump_array = np.ndarray ( (NPLASMA, NLEVELS), dtype = np.object )



	nplasma = data_norm[0]
	uplvls = data_norm[1]
	pjnorm = data_norm[2]
	penorm = data_norm[3]
	coll_tot = data_norm[4]
	rad_tot= data_norm[5]

	nplasma2 = data_probs[0]
	uplvls2 = data_probs[1]
	levels = data_probs[2]
	jprbs = data_probs[3]
	eprbs = data_probs[4]
	print jprbs

	




	for i in range(len(nplasma)):

		n = int(nplasma[i])
		uplvl = int(uplvls[i])


		jump_array[n][uplvl] = jump (pjnorm[i], penorm[i], coll_tot[i], rad_tot[i], np.zeros(nlevels), np.zeros(nlevels))



	for i in range(len(nplasma2)):

		n = int(nplasma2[i])
		uplvl = uplvls2[i]
		level = levels[i]

		if uplvl > 6 and uplvl < 17:

			print jprbs[i]
			jump_array[n][uplvl].jprbs[level] = jprbs[i]
			jump_array[n][uplvl].eprbs[level] = eprbs[i]


	print jump_array[48][7].pjnorm, jump_array[48][16].penorm 
	return jump_array


def plot_norms(pltdata, savename, nplasma = 48, x1 = 7, x2 = 17):

	fig = plt.figure()
	ax = fig.add_subplot(211)


	jnorm = np.array ( [ pltdata[nplasma][x].pjnorm for x in range(x1, x2) ] )
	enorm = np.array ( [ pltdata[nplasma][x].penorm for x in range(x1, x2) ] )
	coll = np.array ( [ pltdata[nplasma][x].coll_tot for x in range(x1, x2) ] )
	rad = np.array ( [ pltdata[nplasma][x].rad_tot for x in range(x1, x2) ] )
	x = np.arange(x1, x2)

	ax.plot( x, enorm, label="Emission")
	ax.plot( x, jnorm, label="Jumping")

	ax.set_ylabel("$P_{norm}$")

	ax.set_xlabel("level")
	ax.set_yscale("log")
	plt.legend()

	ax = fig.add_subplot(212)

	ax.plot(x, rad, label="Rad")
		
	ax.plot(x, coll, label="Coll")

	ax.set_ylabel("bb rate")

	#pylab.ylabel("Penorm")
	ax.set_xlabel("level")
	ax.set_yscale("log")

	plt.legend()

	plt.savefig(savename)

	os.system("open -a preview " + savename)


def plot_probs(pltdata, savename, nplasma = 48, x1 = 7, x2 = 17):
	fig = plt.figure()
	ax = fig.add_subplot(111)

	jp = np.array ( [ pltdata[nplasma][x].jprbs for x in range(x1, x2) ] )
	ep = np.array ( [ pltdata[nplasma][x].eprbs for x in range(x1, x2) ] )
	#lev = np.array ( [ pltdata[nplasma][x].level for x in range(x1, x2) ] )

	up = np.arange(x1, x2)


	for i in range(x1, x2):
		x = np.arange( len(pltdata[nplasma][i].jprbs) )
		ax.plot(x, pltdata[nplasma][i].jprbs, label = str(i))

	plt.legend()

	plt.savefig(savename)

	os.system("open -a preview " + savename)



data = get_data()

print data[48][7].jprbs

ncell = int(sys.argv[1])
#savename = "JvE_" + str(ncell) + ".png"
savename = "probs" + str(ncell) + ".png"


plot_probs( data, savename, nplasma = ncell)










