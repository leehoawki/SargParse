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
	if isinstance(resp,list):
		for o in resp:
			print o
	else:
		print resp

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
	count = 0
	for line in stdin:
		if count == 0:
			y=stdinparse(line)
		else:
			x=stdinparse(line)
			y=eval(exp)
		count+=1
	print y

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

	evaluate(arguments.exp)
