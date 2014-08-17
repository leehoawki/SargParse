#!/usr/bin/python
import sys
import re

def myeval(exp):
	myimport(exp)
	resp = eval(exp)
	if isinstance(resp,list):
		for o in resp:
			print o
	else:
		print resp

def myimport(exp):
	matches = re.findall(r"([a-zA-Z_][a-zA-Z0-9_]*)\.", exp)
	for module_name in matches:
		try:
			module = __import__(module_name)
           		globals()[module_name] = module
		except ImportError as e:
			pass

if __name__=='__main__':
	if len(sys.argv) == 2 :
		myeval(sys.argv[1])

