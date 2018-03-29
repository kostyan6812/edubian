import os, sys, subprocess, random, hashlib
import nbformat as nbf

args = sys.argv
user = str(args[1])
home = ''.join(("/home/", user))
tmp = ''.join(("/var/tmp/","Tmp", str(random.randrange(65535)), "-", user))

##--create md5 summ--
def sig(key):
        hash = hashlib.md5(key).hexdigest()
        return hash

##--read and count string in file--
def read_file(file):
	read = open(file, 'r')
	string = read.readlines()
	count = len(string)
	return count, string

print 'Start task of creating an environment'

subprocess.call(["mkdir", tmp])
#subprocess.call(["mkdir",  ''.join((home, "/Assignment"))])
#subprocess.call(["mkdir",  ''.join((home, "/Assignment/App"))])

count, string = read_file('tasks.md')
hash = ''.join(("This file contains a signature ", sig(user)))
for i in range(count):
	st = string[i]
	number = st.split()
	subprocess.call(["cp", "template.ipynb", ''.join((tmp, "/Task-", number[1], ".ipynb"))])
	subprocess.call(["sed", "-i", ''.join(("s/This file contains a signature/", hash, "/g")), ''.join((tmp, "/Task-", number[1], ".ipynb"))])
	subprocess.call(["sed", "-i", ''.join(("s/", "## Name and number task/", st.rstrip('\n'), "/g")), ''.join((tmp, "/Task-", number[1], ".ipynb"))])
	subprocess.call(["cp", ''.join((tmp, "/Task-", number[1], ".ipynb")), "/usr/share/edubian"])

subprocess.call(["rm", "-r", tmp])
subprocess.call(["cp", "/usr/share/edubian/data", ''.join((home, "/Assignment/App"))])


