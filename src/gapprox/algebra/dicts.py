from .symbol import Symbol
from . import operators as gapprox_operators
import operator
import builtins
from numbers import Number
from typing import Any

import math

# this is the boss
default_evaluate_dict: dict[Symbol, Any] = {
	# functions
	 Symbol('pos'     ): gapprox_operators.pos
	,Symbol('neg'     ): operator.neg
	,Symbol('not'     ): operator.not_
	
	,Symbol('add'     ): operator.add
	,Symbol('sub'     ): operator.sub
	,Symbol('mul'     ): operator.mul
	,Symbol('div'     ): operator.truediv
	
	,Symbol('and'     ): operator.and_
	,Symbol('or'      ): operator.or_
	
	,Symbol('eq'      ): operator.eq
	,Symbol('ne'      ): operator.ne
	,Symbol('lt'      ): operator.lt
	,Symbol('le'      ): operator.le
	,Symbol('gt'      ): operator.gt
	,Symbol('ge'      ): operator.ge
	,Symbol('is'      ): operator.is_
	,Symbol('isnot'   ): operator.is_not
	,Symbol('in'      ): gapprox_operators.in_
	,Symbol('notin'   ): gapprox_operators.notin
	
	,Symbol('ifelse'  ): gapprox_operators.ifelse
		
	,Symbol('floordiv'): operator.floordiv
	,Symbol('mod'     ): operator.mod
	,Symbol('pow'     ): operator.pow
	
	,Symbol('lshift'  ): operator.lshift
	,Symbol('rshift'  ): operator.rshift
	,Symbol('bitnot'  ): operator.not_
	,Symbol('bitor'   ): operator.or_
	,Symbol('bitxor'  ): operator.xor
	,Symbol('bitand'  ): operator.and_
	
	,Symbol('matmul'  ): operator.matmul

	,Symbol('sin'     ): math.sin
	,Symbol('cos'     ): math.cos
	,Symbol('tan'     ): math.tan

	,Symbol('nan'     ): math.nan
	,Symbol('inf'     ): math.inf
	,Symbol('e'       ): math.e
	,Symbol('pi'      ): math.pi
	,Symbol('tau'     ): math.tau
}

default_parse_dict: dict[str, Symbol] = {symbol.name: symbol for symbol in default_evaluate_dict.keys()}
'''
	# numeric
	'neg': { # unary minus, negative, additive inverse
		'symbols': ['−', '-'],
		'python_symbol': '-',
		'aliases': ['negation', 'additive inverse'],
		'arity': 1,
	},
	'inv': { # multiplicative inverse
		'callable': gapprox_operators.reciprocal,
		'symbols': ['⅟', '1∕', '∕', '1/', '/'],
		'python_symbol': '1/',
		'aliases': ['reciprocal', 'multiplicative inverse'],
		'arity': 1,
	},
	'mod': {
		'callable': operator.mod,
		'arity': 2,
		'symbol': 'mod',
		'python_symbol': '%',
	},
	'floordiv': {
		'callable': operator.floordiv,
		'arity': 2,
		'python_symbol': '//',
	},
	'abs': {
		'callable': operator.abs,
		'arity': 1,
		'symbol': ''
	},
	'square': {
		'callable': gapprox_operators.square,
		'arity': 1,
		'symbol': '²'
	},
	'cube': {
		'callable': gapprox_operators.cube,
		'arity': 1,
		'symbol': '³'
	},
	'pow': {
		'callable': builtins.pow,
		'arity': 2,
		'symbol': '^',
		'python_symbol': '**',
	},
	'floor': {
		'callable': math.floor,
		'arity': 1,
		'symbol': None,
	},
	'round': {
		'callable': builtins.round,
	},
	'ceil': {
		'callable': math.ceil,
		'arity': 1,
		'symbol': None,
	},
	'ipart': {
		'callable': math.trunc,
	},
	'fpart': {
		'callable': gapprox_operators.fractional_part,
	},
	'exp': {
		'callable': math.exp,
		'arity': 1,
	},
	'exp2': {
		'callable': math.exp2,
		'arity': 1,
	},
	'log10': {
		'callable': math.log10,
		'arity': 1,
	},
	'log2': {
		'callable': math.log2,
		'arity': 1,
	},
	'log': {
		'callable': math.log,
		'arity': 1,
	},
	'sqrt': {
		'callable': math.sqrt,
		'arity': 1,
	},
	'cbrt': {
		'callable': math.cbrt,
		'arity': 1,
	},
	'root': {
		'callable': gapprox_operators.root,
		'arity': 2,
	},

	# trigonometric
	'sin': {
		'callable': math.sin,
		'arity': 1,
	},
	'cos': {
		'callable': math.cos,
		'arity': 1,
	},
	'tan': {
		'callable': math.tan,
		'arity': 1,
	},
	'cot': {
		'callable': gapprox_operators.cot,
		'arity': 1,
	},
	'sec': {
		'callable': gapprox_operators.sec,
		'arity': 1,
	},
	'csc': {
		'callable': gapprox_operators.csc,
		'arity': 1,
	},
	'asin': {
		'callable': math.asin,
		'arity': 1,
	},
	'acos': {
		'callable': math.acos,
		'arity': 1,
	},
	'atan': {
		'callable': math.atan,
		'arity': 1,
	},
	'acot': {
		'callable': gapprox_operators.acot,
		'arity': 1,
	},
	'asec': {
		'callable': gapprox_operators.asec,
		'arity': 1,
	},
	'acsc': {
		'callable': gapprox_operators.acsc,
		'arity': 1,
	},

	# hyperbolic
	'sinh': {
		'callable': math.sinh,
		'arity': 1,
	},
	'cosh': {
		'callable': math.cosh,
		'arity': 1,
	},
	'tanh': {
		'callable': math.tanh,
		'arity': 1,
	},
	'coth': {
		'callable': gapprox_operators.coth,
		'arity': 1,
	},
	'sech': {
		'callable': gapprox_operators.sech,
		'arity': 1,
	},
	'csch': {
		'callable': gapprox_operators.csch,
		'arity': 1,
	},
	'asinh': {
		'callable': math.asinh,
		'arity': 1,
	},
	'acosh': {
		'callable': math.acosh,
		'arity': 1,
	},
	'atanh': {
		'callable': math.atanh,
		'arity': 1,
	},
	'acoth': {
		'callable': gapprox_operators.acoth,
		'arity': 1,
	},
	'asech': {
		'callable': gapprox_operators.asech,
		'arity': 1,
	},
	'acsch': {
		'callable': gapprox_operators.acsch,
		'arity': 1,
	},

	# left out due to obscurity. also probably mostly wrong:P,
	#'versin': {
	#	{'callable': lambda a: 1 - math.cos(a),
	#'coversin': {
	#	{'callable': lambda a: 1 - math.sin(a),
	#'haversin': {
	#	{'callable': lambda a: 0.5 - math.cos(a)/2,
	#'hacoversin': {
	#	{'callable': lambda a: 0.5 - math.sin(a)/2,
	#'exsec': {
	#	{'callable': lambda a: 1/math.cos(a) - 1,
	#'excsc': {
	#	{'callable': lambda a: 1/math.sin(a) - 1,
	#'chord': {
	#	{'callable': lambda a: 2 * math.sin(a/2),
	#'vercos': {
	#	{'callable': lambda a: 1 + math.cos(a),
	#'covercos': {
	#	{'callable': lambda a: 1 + math.sin(a),
	#'havercos': {
	#	{'callable': lambda a: 0.5 + math.cos(a)/2,
	#'hacovercos': {
	#	{'callable': lambda a: 0.5 + math.sin(a)/2

	# complex
	'real': {
		'callable': gapprox_operators.get_real,
		'arity': 1,
	}, # get real lmao,
	'imag': {
		'callable': gapprox_operators.get_imag,
		'arity': 1,
	},
	'phase': {
		'callable': cmath.phase,
		'arity': 1,
	},
	'conj': {
		'callable': gapprox_operators.call_conjugate,
		'arity': 1,
	},

	# boolean
	'truth': {
		'callable': operator.truth,
		'arity': 1,
	},       # 01,
	'not': {
		'callable': operator.not_,
		'arity': 1,
	},        # 10,
	'and': {
		'callable': operator.and_,
		'arity': 1,
	},        # 0001,
	'nimp': {
		'callable': gapprox_operators.nimp,
		'arity': 1,
	},                 # 0010,
	'ncon': {
		'callable': gapprox_operators.ncon,
		'arity': 1,
	},                 # 0100,
	'xor': {
		'callable': operator.xor,
		'arity': 1,
	},         # 0110,
	'or': {
		'callable': operator.or_,
		'arity': 1,
	},         # 0111,
	'nor': {
		'callable': gapprox_operators.nor,
		'arity': 1,
	},                  # 1000,
	'xnor': {
		'callable': operator.eq,
		'arity': 1,
	},          # 1001,
	'con': {
		'callable': gapprox_operators.converse_implication,
		'arity': 1,
	}, # 1011,
	'imp': {
		'callable': gapprox_operators.implication,
		'arity': 1,
	},          # 1101,
	'nand': {
		'callable': gapprox_operators.nand,
		'arity': 1,
	},                 # 1110

	# comparative
	'lt': {
		'callable': operator.lt,
		'arity': 2,
	},
	'le': {
		'callable': operator.le,
		'arity': 2,
	},
	'eq': {
		'callable': operator.eq,
		'arity': 2,
	},
	'ne': {
		'callable': operator.ne,
		'arity': 2,
	},
	'ge': {
		'callable': operator.ge,
		'arity': 2,
	},
	'gt': {
		'callable': operator.gt,
		'arity': 2,
	},

	# statistical
	'mean': {
		'callable': gapprox_operators.mean,
		'arity': None,
	},
	'median': {
		'callable': gapprox_operators.median,
		'arity': None,
	},
	'mode': {
		'callable': gapprox_operators.mode,
		'arity': None,
	},
	'pmean': {
		'callable': gapprox_operators.generalized_mean,
		'arity': 2,
	},

	# combinatorial
	'comb': {
		'callable': math.comb,
		'arity': None,
	},
	'perm': {
		'callable': math.perm,
		'arity': None,
	},

	# hello there! lol

	# bitwise
	'bitnot': {
		'callable': operator.invert,
		'arity': 1,
	},      # 10,
	'bitand': {
		'callable': operator.and_,
		'arity': 2,
	},        # 0001,
	'bitor': {
		'callable': operator.or_,
		'arity': 2,
	},         # 0111,
	'bitnand': {
		'callable': gapprox_operators.nand,
		'arity': 2,
	},                 # 1110,
	'bitnor': {
		'callable': gapprox_operators.nor,
		'arity': 2,
	},                  # 1000,
	'bitxor': {
		'callable': operator.xor,
		'arity': 2,
	},         # 0110,
	'bitxnor': {
		'callable': operator.eq,
		'arity': 2,
	},          # 1001,
	'bitimp': {
		'callable': gapprox_operators.implication,
		'arity': 2,
	},          # 1101,
	'bitcon': {
		'callable': gapprox_operators.converse_implication,
		'arity': 2,
	}, # 1011,
	'bitnimp': {
		'callable': gapprox_operators.nimp,
		'arity': 2,
	},                 # 0010,
	'bitncon': {
		'callable': gapprox_operators.ncon,
		'arity': 2,
	},                 # 0100,
	'lshift': {
		'callable': operator.lshift,
		'arity': 1,
	},
	'rshift': {
		'callable': operator.rshift,
		'arity': 1,
	},

	# miscellaneous
	'dist': {
		'callable': gapprox_operators.dist,
	},
	'any': {
		'callable': builtins.any,
		'arity': None,
	},
	'all': {
		'callable': builtins.all,
		'arity': None,
	},
	'len': {
		'callable': builtins.len,
		'arity': 1,
	},
	'range': {
		'callable': builtins.range,
		'arity': (1, 3)
	},
	'reversed': {
		'callable': builtins.reversed,
		'arity': 1,
	},
	'sorted': {
		'callable': builtins.sorted,
		'arity': 1,
	},
	'divmod': {
		'callable': builtins.divmod,
		'arity': 2,
	},
	'call': {
		'callable': operator.call,
		'arity': 1,
	},
	'matmul': {
		'callable': operator.matmul,
	},
	'concat': {
		'callable': operator.concat,
	},
	'sign': {
		'callable': gapprox_operators.signum,
		'arity': 1,
	},
	'ifelse': {
		'callable': gapprox_operators.ifelse,
		'arity': 3,
	},
	'fact': {
		'callable': math.factorial,
		'arity': 1,
	},
	'gamma': {
		'callable': math.gamma,
		'arity': 1,
	},
	'sumt': {
		'callable': gapprox_operators.sumtorial,
		'arity': 1,
	},
	'gcd': {
		'callable': math.gcd,
		'arity': None,
	},
	'lcm': {
		'callable': math.lcm,
		'arity': None,
	},
	'clamp': {
		'callable': gapprox_operators.clamp,
		'arity': (1, 3),
	},
	'lerp': {
		'callable': gapprox_operators.lerp,
		'arity': 3,
	},
	'unlerp': {
		'callable': gapprox_operators.unlerp,
		'arity': 3,
	},
	'min': {
		'callable': builtins.min,
		'arity': None,
	},
	'max': {
		'callable': builtins.max,
		'arity': None,
	},
	'is': {
		'callable': operator.is_,
		'arity': 2,
	},
	'isnot': {
		'callable': operator.is_not,
		'arity': 2,
	},
	#,'erf': {
	#	{'callable': math.erf,
	#,'erfc': {
	#	{'callable': math.erfc,
	#,'in': {
	#	{'callable': {
	#,'notin': {
	#	{'callable': {

	# variadic
	'sum': {
		'callable': gapprox_operators.summation,
		'arity': None
	},
	'prod': {
		'callable': gapprox_operators.product,
		'arity': None
	},

	# datatyping
	'tuple': {
		'callable': gapprox_operators.to_tuple,
		'arity': 1,
	},
	'list': {
		'callable': gapprox_operators.to_list,
		'arity': 1,
	},
	'dict': {
		'callable': gapprox_operators.to_dict,
		'arity': 1,
	},
	'set': {
		'callable': gapprox_operators.to_set,
		'arity': 1,
	},

	# constants
		aliases     = None,
		description = "the ratio of an euclidean circle's circumference to its radius",
	),
}

'''

import ast

default_translate_dict = {
		 ast.UAdd    : default_parse_dict['pos']
		,ast.USub    : default_parse_dict['neg']
		,ast.Not     : default_parse_dict['not']
		,ast.Invert  : default_parse_dict['bitnot']

		,ast.Add     : default_parse_dict['add']
		,ast.Sub     : default_parse_dict['sub']
		,ast.Mult    : default_parse_dict['mul']
		,ast.Div     : default_parse_dict['div']
		,ast.FloorDiv: default_parse_dict['floordiv']
		,ast.Mod     : default_parse_dict['mod']
		,ast.Pow     : default_parse_dict['pow']
		,ast.LShift  : default_parse_dict['lshift']
		,ast.RShift  : default_parse_dict['rshift']
		,ast.BitOr   : default_parse_dict['bitor']
		,ast.BitXor  : default_parse_dict['bitxor']
		,ast.BitAnd  : default_parse_dict['bitand']
		,ast.MatMult : default_parse_dict['matmul']
		
		,ast.And     : default_parse_dict['and']
		,ast.Or      : default_parse_dict['or']
		
		,ast.Eq      : default_parse_dict['eq']
		,ast.NotEq   : default_parse_dict['ne']
		,ast.Lt      : default_parse_dict['lt']
		,ast.LtE     : default_parse_dict['le']
		,ast.Gt      : default_parse_dict['gt']
		,ast.GtE     : default_parse_dict['ge']
		,ast.Is      : default_parse_dict['is']
		,ast.IsNot   : default_parse_dict['isnot']
		,ast.In      : default_parse_dict['in']
		,ast.NotIn   : default_parse_dict['notin']
		
		,ast.IfExp   : default_parse_dict['ifelse']
}

__dir__ = lambda: [
		 'default_evaluate_dict'	# dict[Symbol, Any]
		,'default_parse_dict'	# dict[str, Symbol]
		,'default_translate_dict'	# dict[ast.AST, Symbol]
		]
