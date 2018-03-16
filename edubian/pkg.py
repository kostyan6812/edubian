from utils import *

##--create win installer--
def make_exe(nsi, dir):
	Run(["cp", nsi, dir])
	Run(["cp", "data/edubian.cmd", dir])
	Run([''.join(("makensis ", dir, "/edubian.nsi"))], dir)
	Run(["rm", ''.join((dir,"/edubian.nsi"))])


