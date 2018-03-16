import os, shutil

##--chek path exist
def chk_dir(dir):
        res = os.path.exists(dir)
        return res

##--remove dir
def rm_dir(dir):
        shutil.rmtree(dir)

##--get home dir
def home_dir():
	pwd = os.getcwd()
	return pwd

