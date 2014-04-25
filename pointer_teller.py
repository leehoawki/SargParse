import sys

def nextoken(tokens):
	while len(tokens)>0 and tokens[0] == ' ':
		tokens.pop(0)	
	if len(tokens) == 0:
		return None,None
	token = tokens.pop(0)
	if token == '[':
		while tokens[0] != ']':
			token += tokens.pop(0)
		return token + tokens.pop(0)
	if token == '(':
		if tokens[0] == ')':
			tokens.pop(0)
			return "()"
		else:
			return "("	
	if token.isalpha():
		while len(tokens)>0 and tokens[0].isalnum():
               		token += tokens.pop(0)
                return token
	return token
	
def dcl(tokens):
	ns = 0
	token = nextoken(tokens) 
	while token == '*':
		ns += 1	
		token = nextoken(tokens) 
	(out,token) = dirdcl(tokens,token)
	while ns > 0 :
		ns = ns - 1
		out += " pointer to"
	return out,token

def dirdcl(tokens ,token):
	out = ""
	if token[0] == '(':
		(out , token) = dcl(tokens)
		if token != ')':
			print "error: missing )"
	elif token.isalnum() :
		out = token + ":" + out
 	else:
		print "error : expected name "
	token = nextoken(tokens)
	while token == "()" or token[0] == '[':
		if token == '()':
			out += " function returning"
		else :
			out += " array" + token + " of"
		token = nextoken(tokens)
	return (out,token)

if __name__=='__main__':
	if len(sys.argv) > 1 :
		params = list(sys.argv[1])
		datatype = nextoken(params)
		(out,token) = dcl(params)
		print out + " " + datatype 
	else:
		print "Type a declaration to check what it is."
