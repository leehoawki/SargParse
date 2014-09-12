import slib 

def find(env, ast):
	return env.get(ast)	

def subenv(env , vars ,args):
	newenv = env.copy()
	newenv.update(zip(vars,args))	
	return newenv

def eval(ast, env):
	if isinstance(ast, str):
		return find(env, ast) 
	elif isinstance(ast,int):
		return ast
	elif isinstance(ast, float):
		return ast
	elif ast[0] == 'define':
		(_define,var,exp) = ast
		env[var] = eval(exp,env)
	elif ast[0] == 'lambda':
		(_lambda,vars,exp) = ast
		return lambda *args : eval(exp,subenv(env,vars,args))
	elif ast[0] == 'if':
		(_if,cond,exp1,exp2) = ast
		return eval((exp1 if eval(cond,env) else exp2),env)
	else:
		exps = [eval(exp, env) for exp in ast]
		proc = exps.pop(0)
		return proc(*exps)

def parse(tokens):
	t = tokens.pop(0)
	if t == '(':
		L = []
		while tokens[0] != ')':
			L.append(parse(tokens))
		tokens.pop(0)
		return L
	else:
		return atom(t)
		
def atom(token):
	try :
		return int(token)
	except :
		try :
			return float(token)
		except:
			return token 

def tokenize(exp):
	return exp.replace(')',' ) ').replace('(',' ( ').split()

if __name__=='__main__':
	env={}
	env['+'] = slib.add
	env['-'] = slib.sub
	env['*'] = slib.mul
	env['/'] = slib.div
	env['='] = slib.eq
	while True:
		input = raw_input('scheme>')
		if len(input) != 0 :
			output = eval(parse(tokenize(input)), env)
			if output is not None:	
				print output	
