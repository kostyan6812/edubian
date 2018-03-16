from fs import *
from utils import *

##--patch kernel--
def patch_kernel(dir):
	chk = chk_dir(dir)
	args = [ ] 
	if chk:
		file_patch = ''.join((dir, "/include/linux/uts.h"))
		args.append(['patch', '--verbose', '-f', file_patch, 'patch/uts.h.patch'])
		file_config = ''.join((dir, "/.config"))
		args.append(['cp', '-v', 'config/kernel/edubian.conf', file_config])
	else:
		args.append('None')
	return args

##--make config--
def make_config(dir):
		args = [ ]
		args.append(["make clean"])
		args.append(["make menuconfig"])
		return args
##make kernel--
def make_kernel(dir, image):
		args = [ ]
		compile = file_patch = ''.join(("make ", image))
		args.append([compile])
		return args



