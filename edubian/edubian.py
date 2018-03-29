import sys, os, configparser, time 
from menu import * 
from fs import * 
from utils import * 
from kernel import *
from rootfs import *
from pkg import *

#--config--
config = configparser.ConfigParser()
config.read('config.ini')
url = config['git']['url']
workdir = config['git']['dir']
homedir = home_dir()[:-len('edubian')]
dir = ''.join((homedir, workdir))
json_file = config['json']['file']
outputdir = ''.join((homedir, "output"))
rootfs = ''.join((outputdir, "rootfs"))
pswd = config['edubian']['password']
mlst = ''.join((config['edubian']['data'], config['edubian']['multistrap']))
conf = ''.join((config['edubian']['data'],"rootfs/etc"))
content = config['edubian']['data']
scripts = config['edubian']['scripts']
nsi = ''.join((homedir, "/edubian/", config['pkg']['exe']))
right_pos = 3
str_count = 7

##--clone source files from git--
def git(right_pos):
	chk = chk_dir(dir)
        if chk:
                right_text_ln = 'This path %s will be deleted.' % (dir)
                right_pos = right_pos + 1
                scr.right_win.addstr(right_pos, 1, right_text_ln, scr.nT)
                rm_dir(dir)
        right_text_ln = 'Clone source file from git'
        right_pos = right_pos + 1
        scr.right_pos += right_pos
	scr.right_win.addstr(right_pos, 1, right_text_ln, scr.nT)
        proc = Run(['git', 'clone', url, dir])

##--make kernel--
def make(right_pos):
        right_text_ln = 'Patch linux kernel'
        right_pos = right_pos + 1
        scr.right_win.addstr(right_pos, 1, right_text_ln, scr.nT)
        args = patch_kernel(dir)
        for arg in args:
                proc = Run(arg)
                right_text_ln = 'Make kernel'
                right_pos = right_pos + 1
                scr.right_win.addstr(right_pos, 1, right_text_ln, scr.nT)
        args = make_config(dir)
        for arg in args:
                curses.savetty()
                curses.endwin()
                proc = Run(arg, dir)
        args = make_kernel(dir, "bzImage")
        for arg in args:
                curses.savetty()
                curses.endwin()
                proc = Run(arg, dir)
	scr.right_pos += right_pos
	return right_pos

##--move image to output dir-- 
def out(right_pos, pkg, outputdir):
	chk = chk_dir(''.join((outputdir, "/", pkg)))
	if chk:
		right_text_ln = 'Image exist.'
		scr.right_win.addstr(right_pos, 1, right_text_ln, scr.nT)
	else: 
		right_text_ln = 'Move image to output dir'
        	right_pos = right_pos + 1
	        scr.right_win.addstr(right_pos, 1, right_text_ln, scr.nT)
		image = ''.join((dir, "/arch/x86/boot/", pkg))
		proc = Run(["cp", image, outputdir])
		right_text_ln = 'Complite'
	        right_pos = right_pos + 1
		scr.right_pos += right_pos
        	scr.right_win.addstr(right_pos, 1, right_text_ln, scr.nT)
	return right_pos
##--make rootfs--
def mfs(right_pos):
	rf = Rootfs()
	curses.savetty()
        curses.endwin()
	rf.create_rootfs(rootfs, mlst)
	rf.passwd_rootfs("root", pswd, rootfs)
	rf.custom_rootfs(conf, rootfs)
	rf.env(scripts, ''.join((rootfs,"/usr/share/edubian/")))
	rf.compile(''.join((content, "data.py")), content)
	rf.virtual_disk("rootfs.raw", "1024M", rootfs, outputdir)
	right_text_ln = 'Complite.'
        right_pos = right_pos + 1
	scr.right_pos += right_pos
        scr.right_win.addstr(right_pos, 1, right_text_ln, scr.nT)
	return right_pos
##--make pkg and installer--
def pkg(right_pos):
	curses.savetty()
        curses.endwin()
	make_exe(nsi, outputdir)

##--exit from duild system--
def exit(right_pos):
	scr.Exit()

try:
		menu, description = json_parse(json_file)
#	        MainScr(menu, description)
		scr = MainScr(menu, description)
                key = scr.left_win.getch()
		number = 0
                while key != 27:
                        if key == curses.KEY_DOWN:
                                scr.navigation(1)
                        if key == curses.KEY_UP:
                                scr.navigation(-1)
                        if key == ord( "\n" ):
					for k in scr.key:
						if k == "out":
							locals()[k](right_pos, "bzImage", outputdir)
						else:
							right_pos = locals()[k](scr.right_pos)
	        	for item in menu:
                	        number, name = item.items()[0]
                        	left_menu = '%s. %s' % (number, name)
                                if int(number) == scr.position:
                                       	scr.left_win.addstr(3+int(number), 1, left_menu, scr.hT)
					right_pos, numebr  = scr.console_out(3, number)
                              	else:
                                        scr.left_win.addstr(3+int(number), 1, left_menu, scr.nT)

	                key = scr.left_win.getch()


except (AttributeError, KeyboardInterrupt):
#except KeyboardInterrupt:
        curses.endwin()
        print(' Interrupted. Stop program.')


