'''
	University of Southampton -- JM -- 30 September 2013

				classes.py

Synopsis:
	classes
    
    This is a set of classes for use with the radiative transfer code python

Usage:
	

Arguments:
'''




class spectotclass:
    '''This is a class for storing any values read from a Python spec_tot file'''	
    def __init__(self, fre, wave, emi, cen, dis, win, sca, hit):
        self.freq = fre
        self.wavelength = wave
        self.emitted = emi
        self.censrc = cen
        self.disk = dis
        self.wind = win
        self.scattered = sca
        self.hitSurf = hit



class specclass:
    '''This is a class for storing any values read from a Python spec file'''	
    def __init__(self, fre, wave, emi, cen, dis, win, sca, hit, spe):
        self.freq = fre
        self.wavelength = wave
        self.emitted = emi
        self.censrc = cen
        self.disk = dis
        self.wind = win
        self.scattered = sca
        self.hitSurf = hit
        self.spec = spe


class topbase_class:
	'''This is a class for topbase photoionization data'''	
	def __init__(self, nz, ne, islp_init, E0_init, linit, np_init, energies, cross_sections):
		self.Z = nz
		self.ion = ne
		self.islp = islp_init
		self.l = linit
		self.E0 = E0_init 
		self.np = np_init
		self.energy = energies
		self.XS = cross_sections
		




'''
Verner, D. A., & Yakovlev, D. G. 1995, A&AS, 109, 125. 
Analytic fits for partial photoionization cross sections.
Table 1 `Fit parameters for partial photoionization cross sections'
Byte-per-byte description of file: table1.dat
-------------------------------------------------------------------------------
   Bytes Format  Units   Label        Explanations
-------------------------------------------------------------------------------
   1-  2  I2     ---     Z            Atomic number
   4-  5  I2     ---     N            Number of electrons
   7-  7  I1     ---     n            Principal quantum number of the shell 
   9-  9  I1     ---     l            Orbital quantum number of the subshell 
  11- 20  E10.4  eV      E_th         Subshell ionization threshold energy
  22- 31  E10.4  eV      E_0          Fit parameter
  33- 42  E10.4  Mb      \sigma_0     Fit parameter
  44- 53  E10.4  ---     y_a          Fit parameter
  55- 64  E10.4  ---     P            Fit parameter
  66- 75  E10.4  ---     y_w          Fit parameter
-------------------------------------------------------------------------------
-------------------------------------------------------------------------------
'''
class verner_class:
	'''verner photoionization data from Verner & Yakovlev 1995'''
	def __init__(self, _Z, _N, _n, _l, _E_th, _E_0, _sigma_0, _y_a, _P, _y_w):
		self.Z = _Z
		self.N = _N
		self.n = _n
		self.l = _l
		self.E_th = _E_th
		self.E_0 = _E_0
		self.sigma_0 = _sigma_0
		self.y_a = _y_a
		self.P = _P
		self.y_w = _y_w
        


   
#mode class: sets mode from command line
class modeclass:
	'''The mode class: for reading arguments from command line'''
	def __init__(self, smmode, normmode, compmode, sourcesmode, mxmode, logmode, residmode, relative_resmode, helpmode, vlinesmode, rangemode):
		self.sm=smmode
		self.norm=normmode
		self.comp=compmode
		self.sources=sourcesmode
		self.mx=mxmode
		self.log=logmode
		self.resid=residmode
		self.relative_res=relative_resmode
		self.help=helpmode
		self.vlines=vlinesmode
		self.range=rangemode
		#self.name=instancename

#store class: sets stored valuesfrom command line
class stored_args:
	'''This is a class for storing any values read from the command line'''	
	def __init__(self, lminptr, lmaxptr, fnamecmdptr, maxy, ibinptr, filestore, titlestore):
		self.lmin=lminptr
		self.lmax=lmaxptr
		self.ibin=ibinptr
		self.fnamecmd=fnamecmdptr
		self.maximum_y=maxy
		self.filename=filestore
		self.title=titlestore


# line class: analogous to line ptr in python. contains freq, oscillator strength, 
class line:
	'''This is a class analogous to line ptr in python'''
	def __init__(self, _z, _ion, _wavelength, _freq, _osc, _g_l, _g_u, _ll, _lu):
		self.z = _z
		self.ion = _ion
		self.wavelength = _wavelength
		self.freq = _freq
		self.osc = _osc
		self.g_l = _g_l
		self.g_u = _g_u
		self.ll = _ll
		self.lu = _lu
		
		
		
# line class: analogous to line ptr in python. contains freq, oscillator strength, 
class level:
	'''Stores information from a Python levels file'''
	def __init__(self, _z, _ion, _lvl, _ionpot, _E, _g, _rad_rate, _bracks, _nnstring):
		self.z = _z
		self.ion = _ion
		self.lvl = _lvl
		self.ionpot = _ionpot
		self.E = _E
		self.g = _g
		self.rad_rate = _rad_rate
		self.bracks = _bracks
		self.nnstring = _nnstring
		
class chianti_level:
	'''
	Stores chianti level data from file format .elvlc
	See http://www.chiantidatabase.org/cug.pdf Page 8 for description
	'''
	def __init__(self, _index,  _config, _notation, _spin, _l, _l_symbol, _j, _multiplicity, _E_obs, _E_obs2, _E_th, _E_th2, _n):
		self.index = _index
		self.config = _config
		self.notation = _notation
		self.spin = _spin
		self.l = _l
		self.l_symbol = _l_symbol 
		self.j = _j
		self.multiplicity = _multiplicity
		self.E_obs = _E_obs
		self.E_obs2 = _E_obs2
		self.E_th = _E_th
		self.E_th2 = _E_th2
		self.n = _n
		
class chianti_rad:
	'''
	Stores radiative chianti information from wgfa file.
	Contains the wavelengths, gf and A values of the transitions and the indices initial and
	final level corresponding to the indices of the levels as given in the .elvlc file
	See http://www.chiantidatabase.org/cug.pdf Page 9 for description
	'''
	def __init__(self, _ll, _lu, _wave, _freq, _osc, _A, _note_low, _note_up, _J_low, _J_up):
		self.ll = _ll
		self.lu = _lu
		self.wave = _wave
		self.freq = _freq
		self.osc = _osc
		self.A = _A
		self.note_low = _note_low
		self.note_up = _note_up
		self.J_low = _J_low
		self.J_up = _J_up
		
		
		
		
		



