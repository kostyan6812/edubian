import sys, os, shutil, subprocess, hashlib, textwrap, time

args = sys.argv
user = str(args[1])
home_dir = "/root/edubian/scripts/output/rootfs/home/"+user
tmp_dir = "/root/edubian/scripts/output/rootfs/opt/edubian"

print "Create assignment source tree"

##--create md5 summ--
def sig(key):
        m = hashlib.md5(u"test").hexdigest()
        return m

##--open file for write--
def file_w(file, text):
	f = open(file, 'w')
	f.write(text)
	f.close()

##--create user folders--
subprocess.call(["mkdir",  home_dir])
subprocess.call(["mkdir",  home_dir+"/Assignment"])
subprocess.call(["mkdir",  home_dir+"/Assignment/Topics"])
subprocess.call(["mkdir",  home_dir+"/Assignment/Topics/scripts"])

##--create var for user--
key = str(sig(user))
date = time.ctime()
##--create user file--
subprocess.call(["cp", "/dev/null", home_dir+"/Assignment/"+"."+user])
file_w(home_dir+"/Assignment/"+"."+user, textwrap.dedent('''\
signature: %s
user: %s
home dir: %s
date: %s 
''') % (key, user, home_dir, date))

#subprocess.call(["chown","-R", user+":"+user, home_dir+"/*"])
subprocess.call(["mv",tmp_dir+"/date", home_dir+"/Assignment/Topics/scripts/"])
subprocess.call(["mv",tmp_dir+"/task.ipynb", home_dir+"/Assignment/Topics/"])
subprocess.call(["sed", "-i", "s/User signature/User signature "+key+"/g", home_dir+"/Assignment/Topics/task.ipynb"])


