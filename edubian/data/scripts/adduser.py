#!/usr/bin/python3
import sys, os, shutil, subprocess, hashlib, textwrap, time

args = sys.argv
user = str(args[1])
home_dir = ''.join(("/home/", user))
tmp_dir = "/opt/edubian"

print ("Create assignment source tree")

##--create md5 summ--
def sig(key):
	m = hashlib.md5(key.encode("utf-8")).hexdigest()
	return m

##--open file for write--
def file_w(file, text):
	f = open(file, 'w')
	f.write(text)
	f.close()

##--create user folders--
subprocess.call(["mkdir",  ''.join((home_dir, "/Assignment"))])
subprocess.call(["mkdir",  ''.join((home_dir, "/Assignment/Topics"))])
subprocess.call(["mkdir",  ''.join((home_dir, "/Assignment/Topics/scripts"))])

##--create var for user--
key = str(sig(user))
date = time.ctime()
##--create user file--
subprocess.call(["cp", "/dev/null", ''.join((home_dir, "/Assignment/", ".", user))])
file_w(''.join((home_dir, "/Assignment/", ".", user)), textwrap.dedent('''\
signature: %s
user: %s
home dir: %s
date: %s 
''') % (key, user, home_dir, date))

#subprocess.call(["chown","-R", user+":"+user, home_dir+"/*"])
subprocess.call(["cp", ''.join((tmp_dir, "/date")), ''.join((home_dir, "/Assignment/Topics/scripts/"))])
subprocess.call(["cp", ''.join((tmp_dir, "/task.ipynb")), ''.join((home_dir, "/Assignment/Topics/"))])
subprocess.call(["sed", "-i", "s/User signature/User signature "+key+"/g", ''.join((home_dir, "/Assignment/Topics/task.ipynb"))])
subprocess.call(["chown", "-hR", ''.join((user, ":", user)), home_dir])


