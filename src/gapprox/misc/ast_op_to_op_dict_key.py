# ast to operator mappings

import ast

ast_op_to_op_dict_key = {
		ast.UAdd     : 'pos',
		ast.USub     : 'neg',
		ast.Not      : 'not',
		ast.Invert   : 'bitnot',

		ast.Add      : 'add',
		ast.Sub      : 'sub',
		ast.Mult     : 'mul',
		ast.Div      : 'div',
		ast.FloorDiv : 'floordiv',
		ast.Mod      : 'mod',
		ast.Pow      : 'pow',
		ast.LShift   : 'lshift',
		ast.RShift   : 'rshift',
		ast.BitOr    : 'bitor',
		ast.BitXor   : 'bitxor',
		ast.BitAnd   : 'bitand',
		ast.MatMult  : 'matmul',

		ast.And      : 'and',
		ast.Or       : 'or',

		ast.Eq       : 'eq',
		ast.NotEq    : 'ne',
		ast.Lt       : 'lt',
		ast.LtE      : 'le',
		ast.Gt       : 'gt',
		ast.GtE      : 'ge',
		ast.Is       : 'is',
		ast.IsNot    : 'isnot',
		ast.In       : 'in',
		ast.NotIn    : 'notin',
}
