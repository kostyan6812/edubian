import os, pexpect 
from fs import * 
from utils import *

class Rootfs(object):
##--create root file system--
	def create_rootfs(self, dir, config):
		chk = chk_dir(dir)
	        if chk:
##--umount dev and proc fs--
			Run(["umount", "-f", ''.join((dir,"/proc/"))])
	                Run(["umount", "-f", ''.join((dir, "/dev/"))])
        	        Run(["rm", "-r", dir])
		else:
			result = "Rootfs dir is not availible"
			print result
##--create rootfs dir, mount dev and proc. Execute multistrup--
		Run(["mkdir",  dir])
		Run(["mkdir",  ''.join((dir,"/proc/"))])
		Run(["mkdir",  ''.join((dir,"/dev/"))])
		Run(["mkdir",  ''.join((dir,"/usr/share/edubian"))])
		Run(["mount", "-o", "bind", "/proc", ''.join((dir,"/proc/"))])
		Run(["mount", "-o", "bind", "/dev", ''.join((dir,"/dev/"))])
		Runshell([''.join(("multistrap -f ", config, " -d ", dir))])
		Run(["umount", "-lf", ''.join((dir,"/proc/"))])
		Run(["umount", "-lf", ''.join((dir,"/dev/"))])

##--add user password--
	def passwd_rootfs(self, user, password, dir):
		chroot = "chroot %s passwd %s" % (dir, user)
		exp = pexpect.spawn(chroot)
		exp.expect("Enter new UNIX password:")
		exp.sendline(password)
		exp.sendline("\r\n")
		exp.expect("Retype new UNIX password:")
		exp.sendline(password)
		exp.sendline("\r\n")
        	exp.expect(pexpect.EOF)

##--customise OS parameters--
	def custom_rootfs(self, configs, dir):
		Run(["cp", "-r", configs, dir])

##--files for tasks env--
	def env(self, scripts, dir):
		args = ''.join((scripts, "/*"))
		Run(["cp", args, dir])

##--compile python file to bin--	
	def compile(self, file, dir):
		Run([''.join(("/usr/bin/nuitka ", file))], dir)
		Run([''.join(("mv ", os.path.splitext(file)[0]+".exe ", os.path.splitext(file)[0]))], dir)
		Run([''.join(("rm ", " -r ", os.path.splitext(file)[0]+".build"))], dir)
		Run([''.join(("cp", os.path.splitext(file)[0], ''.join((dir,"/usr/share/edubian"))))], dir)

##--create virtual disk--
	def virtual_disk(self, file, size, rootfs, dir):
		fl = ''.join((dir, "/", file))
		chk = chk_dir(fl)
		if chk:
			Run(["rm", fl])
		Run([''.join(("qemu-img create -f raw ", file, " ", size))], dir)
		Run(["mkfs.ext4", fl])
		Run(["mount", "-o", "loop", fl, "/mnt/"])
		Runshell([''.join(("rsync -axHAX --progress ", rootfs,"/", " /mnt/"))])
		Run(["umount", "/mnt/"])
		Run([''.join(("qemu-img convert -f raw -O qcow2 ", file, " ", os.path.splitext(file)[0]+".qcow2"))], dir)
		Run([''.join(("rm ", file))], dir)
		Run([''.join(("rm -r ", rootfs))], dir)
