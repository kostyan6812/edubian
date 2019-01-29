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
		Run(["mount", "-o", "bind", "/proc", ''.join((dir,"/proc/"))])
		Run(["mount", "-o", "bind", "/dev", ''.join((dir,"/dev/"))])
		Runshell([''.join(("multistrap -f ", config, " -d ", dir))])

##--add user password--
	def passwd_rootfs(self, user, password, dir):
		chroot = "chroot %s passwd %s" % (dir, user)
		exp = pexpect.spawn(chroot)
		exp.expect("Enter new UNIX password:")
		exp.sendline(password)
		exp.expect("Retype new UNIX password:")
		exp.sendline(password)
        	exp.expect(pexpect.EOF)

##--customise OS parameters--
	def custom_rootfs(self, configs, dir):
		Run(["cp", "-rv", configs, dir])
		Run(["mkdir", "-v", ''.join((dir, "/opt/edubian"))])
		Run(["mv", "-v", "data/date", ''.join((dir, "/opt/edubian"))])
		Run(["cp", "-v", "data/scripts/adduser.py", ''.join((dir, "/usr/local/sbin/adduser.local"))])
		Run(["cp", "-v", "data/task.ipynb", ''.join((dir, "/opt/edubian"))])
		Run(["chmod", "+x", ''.join((dir, "/usr/local/sbin/adduser.local"))])
		Run(["cp", "-v", "data/scripts/fstab.sh",''.join((dir, "/etc/init.d/"))])
		Run(["chmod", "+x", ''.join((dir, "/etc/init.d/fstab.sh"))])
		chroot = "chroot %s cd /etc/rcS.d/ && ln -s ../init.d/fstab.sh S01fstab.sh" % (dir)
                exp = pexpect.spawn(chroot)
                exp.expect(pexpect.EOF)
		chroot = "chroot %s cd /etc/rc0.d/ && ln -s ../init.d/fstab.sh S01fstab.sh" % (dir)
                exp = pexpect.spawn(chroot)
		exp.expect(pexpect.EOF)

		
##--compile python file to bin--
	def compile(self, file, dir):
		Run([''.join(("c++ ", os.path.splitext(file)[0]+".c", " -o ", os.path.splitext(file)[0]))], dir)

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
		Run(["umount", "-f", ''.join((rootfs,"/proc/"))])
                Run(["umount", "-fl", ''.join((rootfs, "/dev/"))])
		Run([''.join(("rm ", file))], dir)
		Run([''.join(("rm -vfr ", rootfs))], dir)
