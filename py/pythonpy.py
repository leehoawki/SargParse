#!/usr/bin/python
import sys
import re
import argparse

def myimport(exp):
	matches = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\.", exp)
	for module_name in matches:
		try:
			module = __import__(module_name)
			globals()[module_name] = module
		except ImportError as e:
			pass

def evaluate(exp):
	myimport(exp)
	resp = eval(exp)
	printresp(resp)

def apply(stdin,exp):
	myimport(exp)
	for line in stdin:
		x = stdinparse(line)
		print eval(exp)
	

def filter(stdin,exp):
	myimport(exp)
	for line in stdin:
		x = stdinparse(line)
		resp = eval(exp)
		if resp:
			print x

def reduce(stdin,exp):
	myimport(exp)
	y=None
	for line in stdin:
		if y:
			x=stdinparse(line)
			y=eval(exp)
		else:
			y=stdinparse(line)
	if y:
		print y

def listp(stdin, exp):
	myimport(exp)
	x=map(stdinparse, list(stdin))
	resp = eval(exp)
	printresp(resp)

def printresp(resp):
	if isinstance(resp, list):
		for o in resp:
			print o
	else:
		print resp

def stdinparse(line):
	if line[-1] == '\n':
		return line[0:-1]
	else:
		return line

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
		apply(sys.stdin,arguments.exp)
		exit(0)
	if arguments.f:
		filter(sys.stdin,arguments.exp)
		exit(0)
	if arguments.r:
		reduce(sys.stdin,arguments.exp)
		exit(0)
	if arguments.l:
		listp(sys.stdin,arguments.exp)
		exit(0)

	evaluate(arguments.exp)
