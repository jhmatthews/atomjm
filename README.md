atomjm
======

Atomic Routines written by James

To run, simply 

* clone the repository
* python setup.py will create environment variables in .bash_profile if you are on OSX
* python recomb.py [mode] [temp] [nlevels]
* modes:
	* oster -- do non-subshell calculations for Osterbrock recombination coefficients
	* suboster -- do subshell calculations and normal n calculations, using recomb from Osterbrock
	* probs -- read in a file transitions which contains transition probabilities, check expected probabilities against A values
	* cloudy -- use cloudy recombination coefficients from h_iso_recomb_mod.dat
	* py -- use recombination coefficients direct from Python printout
