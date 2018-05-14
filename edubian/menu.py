import curses, sys, os
from utils import *

class MainScr(object):
	def __init__(self, menu, description, title="Build system for MIREA education operation system - eduBian (c)2017 - 2018"):
		curses.initscr()
		curses.savetty()
		curses.start_color()
		curses.setupterm()
		curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_CYAN)
		curses.cbreak()
		curses.noecho()
		curses.curs_set(0)
		self.screen = curses.initscr()
		self.screen.keypad(True)
		self.hT = curses.color_pair(1)
		self.nT = curses.A_NORMAL
		height,width = self.screen.getmaxyx()
		layer = [{"height" : height}, {"width" : width}, {"title" : title}]
		self.menu = menu
		self.description = description
		self.screen.clear()
		self.screen.border(0)
		self.screen.refresh()
		self.position = 1
		self.str_count = 0
		self.display(layer, self.menu, self.description)

	def wins(self, options):
		for item in options:
            		name, res = item.items()[0]
			if name == 'height':
				h = res
			if name == 'width':
				w = res
			if name == 'title':
				title = res
		top_head = title
		left_head = 'Main Menu'
		right_head = 'Console output'
		top_head_len = len(top_head)
		left_head_len = len(left_head)
		right_head_len = len(right_head)
##--create top, left and right windows. Get y and x position--
		self.top_win = curses.newwin(3,(w-2),1,1)
		topheight,topwidth = self.top_win.getmaxyx()
		self.footer_win = curses.newwin(3,(w-2),47,1)
		footerheight,footerwidth = self.top_win.getmaxyx()
		self.left_win = curses.newwin((h-topheight-footerheight-2),(topwidth/3),4,1)
		leftheight,leftwidth = self.left_win.getmaxyx()
		self.right_win = curses.newwin((h-footerheight-5),(w-leftwidth-3),4,(leftwidth+2))
		stdscr = curses.newwin((h-footerheight-5),(w-leftwidth-3),4,(leftwidth+2))
		rightheight,rightwidth = self.right_win.getmaxyx()
		self.right_win.idlok(1)
##--calculate head position--
		top_head_position = (topwidth - top_head_len)/2
		left_head_position = (leftwidth - left_head_len)/2
		right_head_position = (rightwidth - right_head_len)/2
##--clear and create border for windows--
		self.top_win.erase()
		self.top_win.box()
		self.top_win.border(0)
		self.footer_win.erase()
		self.footer_win.box()
		self.footer_win.border(0)
		self.left_win.erase()
		self.left_win.box()
		self.left_win.border(0)
		self.right_win.erase()
		self.right_win.box()
		self.right_win.border(0)
##--create text string in window align by center--
		self.top_win.addstr(1, top_head_position, top_head)
		self.left_win.addstr(1, left_head_position, left_head)
		self.left_win.hline(2,1,1,leftwidth-2, 61)
		self.right_win.addstr(1, right_head_position, right_head)
		self.right_win.hline(2,1,1,rightwidth-2, 61)
##--refresh windows--
		self.top_win.refresh()
		self.footer_win.refresh()
		self.left_win.immedok(True)
#		self.left_win.refresh()
#		self.right_win.refresh()
		self.right_win.immedok(True)

##--create menu on display--
	def display(self, options, menu, description):
		self.wins(options)
		self.left_win.keypad(True)
		row_num = len(menu)
		footer_text = 'Press UP, DOWN arrow key for move menu item. Press ENTER fo select item. Press ESC for exit.'
		self.footer_win.addstr(1,1, footer_text, self.nT)
		self.footer_win.refresh()
		for item in menu:
			self.number, name = item.items()[0]
			left_menu = '%s. %s' % (self.number, name)
			if int(self.number) == self.position:
				self.left_win.addstr(3+int(self.number), 1, left_menu, self.hT)
				right_pos, self.numebr = self.console_out(3, self.number)
			else:
				self.left_win.addstr(3+int(self.number), 1, left_menu, self.nT)
##--navigation--
	def navigation(self, n):
		self.position += n
        	if self.position < 1:
            		self.position = 1
        	if self.position >= len(self.menu):
            		self.position = len(self.menu)
##--clear right window--
	def clear_rwin(self):
		rightheight,rightwidth = self.right_win.getmaxyx()
		self.right_win.move(3, 1)
		rightheight -= 3
		for i in range(rightheight):
       	                self.right_win.move(3+i, 1)
               	        self.right_win.clrtoeol()
##--output description--
	def console_out(self, right_pos, number):
		self.clear_rwin()
#	        self.right_win.refresh()
	        name_m, text, key = create_description(self.description[int(number)-1])
	        right_text_l1 = 'This will be done %s: \n' % (name_m)
	        self.right_win.addstr(right_pos, 1, right_text_l1, self.nT)
#	        self.right_win.refresh()
	        right_pos = right_pos + 1
		self.key = key
        	for i in range(0, len(text)):
	                right_text_ln = ''.join((str(i+1),". ", text[i]))
	                right_pos = right_pos + 1
	                self.right_win.addstr(right_pos, 1, right_text_ln, self.nT)
#	                self.right_win.refresh()
			self.right_pos = right_pos
        	str_count = len(text)
		self.str_count += str_count
		rightheight,rightwidth = self.right_win.getmaxyx()
		if self.str_count < 1:
			self.str_count = 0
		if self.str_count >= int(rightheight):
			self.str_count = rightheight
		return right_pos, number


##--Exit and quit--
	def Exit(self):
			curses.endwin()
			quit()

