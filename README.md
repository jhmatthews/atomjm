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
	* std -- use Ferguson & Ferland 1996 fits to recombination coefficients, do not split by subshell
