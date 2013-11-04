'''
Setup script for ATOMJM routines
'''

from sys import platform as _platform
import os


	



def write_bash_profile():
	'''
	Writes some path variables to bash_profile
	'''
	from os.path import expanduser
	home = expanduser("~")
	
	os.system("cp %s/.bash_profile %s/.bash_profile_atomjm" % (home, home))
	print "Saved a copy as .bash_profile_atomjm."
	
	filename = "%s/.bash_profile" % home
	with open (filename, "a") as myfile:
		myfile.write ("\n#AtomJM addition \n\n# appending atomjm to path\n")
		myfile.write ('export ATOMJM="' + os.getcwd() + '"\n')
		myfile.write ("export PATH=$PATH:$ATOMJM\n")
		myfile.write ("export PYTHONPATH=$PYTHONPATHPATH:$ATOMJM\n")
		myfile.write ("\n#Finished editing path with AtomJM\n")
	
	myfile.close()
	
print 'All done!'
	





if _platform == "darwin":
	# hurrah, we are in OSX
	
	print "Writing to .bash_profile file, hope this is ok!"
	
	write_bash_profile()
	
else:
	
	print "Error: Can't setup properly for non OSX machines, DIY!"


