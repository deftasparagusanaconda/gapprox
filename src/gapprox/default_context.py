# TODO: update floor and ceil symbols

import math
import cmath
import operator
import numbers
import builtins
import statistics
from . import operators as gapprox_operators

default_context: dict[str: dict] = {
	# arithmetic
	'add': {
		'callable': operator.add,
		'symbols': ['+'],
		'python_symbol': '+',
		'aliases': ['addition', 'sum'],
		'arity': 2,
		'commutative': True,
	},
	'sub': {
		'callable': operator.sub,
		'symbols': ['−', '-'],
		'python_symbol': '-',
		'aliases': ['subtraction', 'difference'],
		'arity': 2,
		'commutative': False,
	},
	'mul': {
		'callable': operator.mul,
		'symbols': ['×', '⋅', '*', 'x'],
		'python_symbol': '*',
		'aliases': ['multiplication', 'product'],
		'arity': 2,
		'commutative': True,
	},
	'div': {
		'callable': operator.truediv,
		'symbols': ['∕', '÷', '/'],
		'python_symbol': '/',
		'aliases': ['division', 'ratio'],
		'arity': 2,
		'commutative': False,
	},

	# numeric
	'neg': { # unary minus, negative, additive inverse
		'callable': operator.neg,
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
	'nan': {
		'value': float('nan'),
		'symbols': ['NaN', '?', '¿', '𝑁𝑎𝑁'],
		'aliases': ['not a number'],
		'description': 'something which is not a number'
	},
	'inf': {
		'value': float('inf'),
		'symbols': ['∞'],
		'aliases': ['infinity'],
		'description': 'something which is boundless, limitless, endless'
	},
	'i': {
		'value': 1j,
		'symbols': ['i', 'j', '𝑖', '𝕚', 'ⅈ', '𝒾'],
		'aliases': ['imaginary unit'],
		'description': 'a number i such that i² = −1'
	},
	'phi': {
		'value': 1.618033988749894848204586834365638117720309179805762862135448622705260462818,
		'symbols': ['φ', 'ϕ'],
		'aliases': ['golden ratio'],
		'description': 'a/b such that a+b ∶ a ∷ a ∶ b. algebraically, φ = (1 + √5) ∕ 2'
	},
	'e': {
		'value': 2.718281828459045235360287471352662497757247093699959574966967627724076630353,
		'symbols': ['e', '𝑒', 'ℯ'],
		'aliases': ["euler's number"],
		'description': 'the number e such that d∕dx(eˣ) = eˣ – or – the limit as n → +∞ for (1 + 1∕n)ⁿ'
	},
	'pi': {
		'value': 3.141592653589793238462643383279502884197169399375105820974944592307816406286,
		'symbols': ['π', '𝜋', 'ℼ'],
		'aliases': ["archimedes' constant"],
		'description': "the ratio of an euclidean circle's circumference to its diameter"
	},
	'tau': {
		'value': 6.283185307179586476925286766559005768394338798750211641949889184615632812572,
		'symbols': ['τ', '𝜏'],
		'aliases': None,
		'description': "the ratio of an euclidean circle's circumference to its radius"
	}
}

