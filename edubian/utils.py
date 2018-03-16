import os, json, subprocess
from fs import * 

##--parse json file--
def json_parse(file):
	data = json.load(open(file))
	dict = json.dumps(data['menu'], separators=(',',':'))
	dict_data = json.loads(dict)
	menu = [ ]
	modules = [ ]
	descriptions = [ ]
	pack = [ ]
	for dt in dict_data:
		menu.append(dt)
		modules.append(dt.values())
	for module in modules:
		dict = json.dumps(data[module[0]])
		dict_data = json.loads(dict)
		descriptions.append(dict_data)
	for i in range(len(menu)):
		val = modules[i]+descriptions[i]
		pack.append(val)
	return menu, pack

##--create description for menu--
def create_description(arr):
	name = arr[0]
	module = arr[1]
	text = module.values()
	keys = [ ]
	key = module.keys()
	for k in key:
		keys.append(str(k))
	keys.sort()
	return name, text, keys

##--run subprocess--
def Run(command, *wds):
	if wds:
		for wd in wds:
		        proc = subprocess.Popen(command, shell=True, cwd=wd)
			proc.wait()
	else:
		proc = subprocess.Popen(command, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
		proc.wait()
	return proc

##--run subprocess with shell--
def Runshell(command):
	proc = subprocess.Popen(command, shell=True)
        proc.wait()
	return proc
