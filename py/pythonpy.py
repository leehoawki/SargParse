#!/usr/bin/python
import sys
import re
import argparse

def importmodule(func):
	def wrapper(*args, **kw):
		exp = args[0]
		matches = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\.", exp)
		for module_name in matches:
			try:
				module = __import__(module_name)
				globals()[module_name] = module
			except ImportError as e:
				pass
		return func(*args, **kw)
	return wrapper
			
@importmodule
def evaluate(exp):
	resp = eval(exp)
	printresp(resp)
	
@importmodule
def apply(exp,stdin):
	for line in stdin:
		x = stdinparse(line)
		print eval(exp)
	
@importmodule
def filter(exp,stdin):
	for line in stdin:
		x = stdinparse(line)
		resp = eval(exp)
		if resp:
			print x

@importmodule
def reduce(exp,stdin):
	y = None
	for line in stdin:
		if y:
			x = stdinparse(line)
			y = eval(exp)
		else:
			y = stdinparse(line)
	if y:
		print y

@importmodule
def listp(exp,stdin):
	x = map(stdinparse, list(stdin))
	resp = eval(exp)
	printresp(resp)

def printresp(resp):
	if isinstance(resp, list):
		for o in resp:
			print o
	else:
		print resp

def stdinparse(line):
	return line[0:-1] if line[-1] == '\n' else line

if __name__=='__main__':
	parser = argparse.ArgumentParser()

	group = parser.add_mutually_exclusive_group()
	group.add_argument('-x', action='store_true', help='execute lambda expression using stdin as x')
	group.add_argument('-f', action='store_true', help='filter the stdin using a lambda expression')
	group.add_argument('-r', action='store_true', help='reduce the stdin using expression of x and y')
	group.add_argument('-l', action='store_true', help='apply the expression to the stdin as a list')
	
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	parser.add_argument('exp', action="store")
	arguments = parser.parse_args()
	
	if arguments.x:
		apply(arguments.exp,sys.stdin)
		exit(0)
	if arguments.f:
		filter(arguments.exp,sys.stdin)
		exit(0)
	if arguments.r:
		reduce(arguments.exp,sys.stdin)
		exit(0)
	if arguments.l:
		listp(arguments.exp,sys.stdin)
		exit(0)

	evaluate(arguments.exp)
