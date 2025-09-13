from ast import parse 

def str_to_ast(expr:str):
	'parse a str expression to an ast tree'
	return parse(expr, mode='eval').body
