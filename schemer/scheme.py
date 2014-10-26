import slib
import console

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

if __name__=='__main__':
    env={}
    env['+'] = slib.add
    env['-'] = slib.sub
    env['*'] = slib.mul
    env['/'] = slib.div
    env['='] = slib.eq
    while True:
        try:
            input = console.get()
                if input != None:
                    output = eval(input,env)
                    console.put(output)
        except Exception,e:
            console.put(e)
