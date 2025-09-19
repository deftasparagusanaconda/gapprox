import math
import cmath
import operator as py_ops
import numbers
import builtins
import statistics
from . import operators as ga_ops

operator_dict:dict = {

		# arithmetic
		 'add'     : py_ops.add
		,'sub'     : py_ops.sub
		,'mul'     : py_ops.mul
		,'div'     : py_ops.truediv

		# numeric
		,'pos'     : py_ops.pos	  # unary plus, positive
		,'neg'     : py_ops.neg    # unary minus, negative, additive inverse
		,'mod'     : py_ops.mod
		,'floordiv': py_ops.floordiv
		,'abs'     : py_ops.abs
		,'inv'     : ga_ops.reciprocal      # multiplicative inverse
		,'square'  : ga_ops.square
		,'cube'    : ga_ops.cube
		,'pow'     : builtins.pow
		,'floor'   : math.floor
		,'round'   : builtins.round
		,'ceil'    : math.ceil
		,'ipart'   : math.trunc
		,'fpart'   : ga_ops.fractional_part
		,'exp'     : math.exp
		,'exp2'    : math.exp2
		,'log10'   : math.log10
		,'log2'    : math.log2
		,'log'     : math.log
		,'sqrt'    : math.sqrt
		,'cbrt'    : math.cbrt
		,'root'    : ga_ops.root

		# trigonometric
		,'sin'     : math.sin
		,'cos'     : math.cos
		,'tan'     : math.tan
		,'cot'     : ga_ops.cot
		,'sec'     : ga_ops.sec
		,'csc'     : ga_ops.csc
		,'asin'    : math.asin
		,'acos'    : math.acos
		,'atan'    : math.atan
		,'acot'    : ga_ops.acot
		,'asec'    : ga_ops.asec
		,'acsc'    : ga_ops.acsc

		# hyperbolic
		,'sinh'    : math.sinh
		,'cosh'    : math.cosh
		,'tanh'    : math.tanh
		,'coth'    : ga_ops.coth
		,'sech'    : ga_ops.sech
		,'csch'    : ga_ops.csch
		,'asinh'   : math.asinh
		,'acosh'   : math.acosh
		,'atanh'   : math.atanh
		,'acoth'   : ga_ops.acoth
		,'asech'   : ga_ops.asech
		,'acsch'   : ga_ops.acsch

		# left out due to obscurity. also probably mostly wrong :P
		#'versin'    : lambda a: 1 - math.cos(a)
		#'coversin'  : lambda a: 1 - math.sin(a)
		#'haversin'  : lambda a: 0.5 - math.cos(a)/2
		#'hacoversin': lambda a: 0.5 - math.sin(a)/2
		#'exsec'     : lambda a: 1/math.cos(a) - 1
		#'excsc'     : lambda a: 1/math.sin(a) - 1
		#'chord'     : lambda a: 2 * math.sin(a/2)
		#'vercos'    : lambda a: 1 + math.cos(a)
		#'covercos'  : lambda a: 1 + math.sin(a)
		#'havercos'  : lambda a: 0.5 + math.cos(a)/2
		#'hacovercos': lambda a: 0.5 + math.sin(a)/2

		# complex
		,'real'    : ga_ops.get_real # get real lmao
		,'imag'    : ga_ops.get_imag
		,'phase'   : cmath.phase
		,'conj'    : ga_ops.call_conjugate

		# boolean
		,'truth'   : py_ops.truth       # 01
		,'not'     : py_ops.not_        # 10
		,'and'     : py_ops.and_        # 0001
		,'nimp'    : ga_ops.nimp                 # 0010
		,'ncon'    : ga_ops.ncon                 # 0100
		,'xor'     : py_ops.xor         # 0110
		,'or'      : py_ops.or_         # 0111
		,'nor'     : ga_ops.nor                  # 1000
		,'xnor'    : py_ops.eq          # 1001
		,'con'     : ga_ops.converse_implication # 1011
		,'imp'     : ga_ops.implication          # 1101
		,'nand'    : ga_ops.nand                 # 1110

		# comparative
		,'lt'      : py_ops.lt
		,'le'      : py_ops.le
		,'eq'      : py_ops.eq
		,'ne'      : py_ops.ne
		,'ge'      : py_ops.ge
		,'gt'      : py_ops.gt

		# statistical
		,'mean'    : ga_ops.mean
		,'median'  : ga_ops.median
		,'mode'    : ga_ops.mode
		,'pmean'   : ga_ops.generalized_mean

		# combinatorial
		,'comb'    : math.comb
		,'perm'    : math.perm

		# hello there! lol

		# bitwise
		,'bitnot'  : py_ops.invert      # 10
		,'bitand'  : py_ops.and_        # 0001
		,'bitor'   : py_ops.or_         # 0111
		,'bitnand' : ga_ops.nand                 # 1110
		,'bitnor'  : ga_ops.nor                  # 1000
		,'bitxor'  : py_ops.xor         # 0110
		,'bitxnor' : py_ops.eq          # 1001
		,'bitimp'  : ga_ops.implication          # 1101
		,'bitcon'  : ga_ops.converse_implication # 1011
		,'bitnimp' : ga_ops.nimp                 # 0010
		,'bitncon' : ga_ops.ncon                 # 0100
		,'lshift'  : py_ops.lshift
		,'rshift'  : py_ops.rshift

		# miscellaneous
		,'dist'    : ga_ops.dist
		,'any'     : builtins.any
		,'all'     : builtins.all
		,'len'     : builtins.len
		,'range'   : builtins.range
		,'reversed': builtins.reversed
		,'sorted'  : builtins.sorted
		,'divmod'  : builtins.divmod
		,'call'    : py_ops.call
		,'matmul'  : py_ops.matmul
		,'concat'  : py_ops.concat
		,'sign'    : ga_ops.signum
		,'ifelse'  : ga_ops.ifelse
		,'fact'    : math.factorial
		,'gamma'   : math.gamma
		,'sumt'    : ga_ops.sumtorial
		,'gcd'     : math.gcd
		,'lcm'     : math.lcm
		,'clamp'   : ga_ops.clamp
		,'lerp'    : ga_ops.lerp
		,'unlerp'  : ga_ops.unlerp
		,'min'     : builtins.min
		,'max'     : builtins.max
		,'is'      : py_ops.is_
		,'isnot'   : py_ops.is_not
		#,'erf'     : math.erf
		#,'erfc'    : math.erfc
		#,'in'      : 
		#,'notin'   : 

		# datatyping
		,'tuple'   : ga_ops.to_tuple
		,'list'    : ga_ops.to_list
		,'dict'    : ga_ops.to_dict
		,'set'     : ga_ops.to_set
}
