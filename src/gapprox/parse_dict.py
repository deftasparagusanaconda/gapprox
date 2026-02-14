import ast
from . import symbols

default_parse_dict = {
		 ast.UAdd    : symbols.POS
		,ast.USub    : symbols.NEG
		,ast.Not     : symbols.NOT
		,ast.Invert  : symbols.BITNOT

		,ast.Add     : symbols.ADD
		,ast.Sub     : symbols.SUB
		,ast.Mult    : symbols.MUL
		,ast.Div     : symbols.DIV
		,ast.FloorDiv: symbols.FLOORDIV
		,ast.Mod     : symbols.MOD
		,ast.Pow     : symbols.POW
		,ast.LShift  : symbols.LSHIFT
		,ast.RShift  : symbols.RSHIFT
		,ast.BitOr   : symbols.BITOR
		,ast.BitXor  : symbols.BITXOR
		,ast.BitAnd  : symbols.BITAND
		,ast.MatMult : symbols.MATMUL

		,ast.And     : symbols.AND
		,ast.Or      : symbols.OR

		,ast.Eq      : symbols.EQ
		,ast.NotEq   : symbols.NE
		,ast.Lt      : symbols.LT
		,ast.LtE     : symbols.LE
		,ast.Gt      : symbols.GT
		,ast.GtE     : symbols.GE
		,ast.Is      : symbols.IS
		,ast.IsNot   : symbols.ISNOT
		,ast.In      : symbols.IN
		,ast.NotIn   : symbols.NOTIN

		,ast.IfExp   : symbols.IFELSE
}
