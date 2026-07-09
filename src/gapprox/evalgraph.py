# now.. just think. what is the use of compile when the compiled function cant even take any arguments? it evaluates to the same value every time. the evaluate function should take arguments for the evaluation, and thus the compiled function can also be actually useful. design this later

from __future__ import annotations    # since EvalNode typehints itself so often
from typing import Any, Callable
import ast    # for ast.NodeVisitor
from numbers import Number    # for typehinting
from collections.abc import Mapping, MutableMapping, Sequence
from dataclasses import dataclass, field
from .frozendict import frozendict
from daacorations import pretty_repr

import operator, math, builtins    # for EvalNode arithmetic dunders

class Evaluators:
    """an evaluator tells a node how to traverse the graph during evaluation
    this enables branch pruning.
    substitution will NOT happen during evaluation. all branch payloads are assumed to be callable
    """

    def return_payload(
            payload: Callable,
            args: Sequence[EvalNode],
            kwargs: Mapping[str, EvalNode],
        ) -> Any:
        return payload

    def call_inputs(
            payload: Callable, 
            args: Sequence[EvalNode], 
            kwargs: Mapping[str, EvalNode],
        ) -> Any:
        
        return payload(
            *(node.evaluate() for node in args), 
            **{name: node.evaluate() for name, node in kwargs.items()})

    def ifelse(
            payload: Callable,
            args: Sequence[EvalNode],
            kwargs: Mapping[str, EvalNode]
        ) -> Any:
        return args[1].evaluate() if args[0].evaluate() else args[2].evaluate()

@dataclass(frozen=True, slots=True, init=False, repr=False)
class EvalNode:
    """an immutable node in a multi-edged directed acyclic evaluation graph. it holds anything in its .payload, and has other nodes as input parameters in its .args and .kwargs
    
    the identity of a node is based on its payload and its inputs. 
    for example: two leaf nodes (with no inputs) with the same payload are thus identical
    thus the identity of a node is the identity of itself and the whole subtree below it
    """
    payload: Any
    args: tuple[EvalNode, ...]
    kwargs: frozendict[str, EvalNode]
    evaluator: Callable[[Any, ...], Any]

    def __init__(self, payload: Any, args: Sequence[EvalNode, ...] = (), kwargs: Mapping[str, EvalNode] = {}, evaluator: Callable = None):
        if evaluator is not None:
            pass
        elif args or kwargs:
            evaluator = Evaluators.call_inputs
        else:
            evaluator = Evaluators.return_payload

        object.__setattr__(self, 'payload', payload)
        object.__setattr__(self, 'args', tuple(args))
        object.__setattr__(self, 'kwargs', frozendict(kwargs))
        object.__setattr__(self, 'evaluator', evaluator)
    
    def substitute_node(self, substitutions: Mapping[EvalNode, EvalNode] = None, *, substitute_by_id: bool = False) -> EvalNode:
        'recursively substitute a node with another node'
        substitutions = {} if substitutions is None else substitutions
        substitutions = IdentityDict(substitutions) if substitute_by_id else substitutions
        
        if self in substitutions:
            return substitutions[self]
        
        if all(arg not in substitutions for arg in self.args) and all(kwarg not in substitutions for kwarg in self.kwargs):
            return self
        
        args = (substitutions.get(arg, arg.substitute_node(substitutions, substitute_by_id = substitute_by_id)) for arg in self.args)
        kwargs = {key: substitutions.get(kwarg, kwarg.substitute_node(substitutions, substitute_by_id = substitute_by_id)) for key, kwarg in self.kwargs.items()}
        
        return EvalNode(self.payload, args, kwargs)
    
    def substitute_payload(self, substitutions: Mapping[Any, Any] = None, *, substitute_by_id: bool = False) -> EvalNode:
        'recursively substitute a payload with another payload'
        substitutions = {} if substitutions is None else substitutions
        substitutions = IdentityDict(substitutions) if substitute_by_id else substitutions
        
        payload = substitutions.get(self.payload, self.payload)
        args = tuple(arg.substitute_payload(substitutions, substitute_by_id = substitute_by_id) for arg in self.args)
        kwargs = frozendict((key, kwarg.substitute_payload(substitutions, substitute_by_id = substitute_by_id)) for key, kwarg in self.kwargs.items())
        
        new_node = EvalNode(payload, args, kwargs)
        return self if self is new_node else new_node

    def evaluate(self, *, context: Mapping[Any, Any], memo: None | MutableMapping[EvalNode, Any] = None) -> Any:
        return self.evaluator(self.payload, self.args, self.kwargs, memo = memo)
    
    def compile() -> Callable:
        raise NotImplementedError
    
    #@classmethod
    #def from_str(cls, string: str, *, translate_dict: dict[ast.AST, Any]) -> 'EvalNode':
    #    ast_visitor = EvalASTVisitor(translate_dict = translate_dict)
    #    ast_tree: ast.AST = parse(expr, mode='eval').body
    #    
    #    return ast_visitor.visit(ast_tree)
        
    @staticmethod
    def _dunder_factory(payload: Callable[[Any, ...], Any], *, reverse_args: bool = False) -> Callable:
        def dunder(*args, **kwargs) -> EvalNode:
            if not all(isinstance(val, EvalNode) for val in set(tuple(kwargs.values()) + args)):
                return NotImplemented
            return EvalNode(payload, reversed(args) if reverse_args else args, kwargs)
        return dunder

    # NOTE: why dont we implicitly wrap non-EvalNode operands to EvalNode? because:
    # 
    # imagine this scenario. you have `x = EvalNode('x')`. if we allowed implicit wrapping:
    # 2 + 4 + x would create this tree:
    #
    #   + 
    #  / \
    # 6   x
    #
    # this is because the other parts of the expression that are not EvalNode will evaluate to a single value. if we disallow implicit wrapping, we are forced to do:
    # EvalNode(2) + EvalNode(4) + x which would correctly create the tree:
    #
    #     +    
    #    / \      
    #   +   x 
    #  / \       
    # 2   4    
    # 
    # thus we protect the user from any unexpected behaviour. it is less convenient but it is more important to be correct, in our case. gapprox is not mainly a convenience tool. robustness first. in fact, if you want such convenience, youre probably better off using ExprNode.from_str
        
    __lt__        = _dunder_factory(operator.lt                         )    # x < y
    __le__        = _dunder_factory(operator.le                         )    # x <= y
    __eq__        = _dunder_factory(operator.eq                         )    # x == y
    __ne__        = _dunder_factory(operator.ne                         )    # x != y
    __ge__        = _dunder_factory(operator.ge                         )    # x >= y
    __gt__        = _dunder_factory(operator.gt                         )    # x > y
    
    __abs__       = _dunder_factory(operator.abs                        )    # abs(x)
    __pos__       = _dunder_factory(operator.pos                        )    # +x
    __neg__       = _dunder_factory(operator.neg                        )    # -x
    __add__       = _dunder_factory(operator.add                        )    # x + y
    __radd__      = _dunder_factory(operator.add     , reverse_args=True)    # y + x
    __sub__       = _dunder_factory(operator.sub                        )    # x - y
    __rsub__      = _dunder_factory(operator.sub     , reverse_args=True)    # y - x
    __mul__       = _dunder_factory(operator.mul                        )    # x * y
    __rmul__      = _dunder_factory(operator.mul     , reverse_args=True)    # y * x
    __truediv__   = _dunder_factory(operator.truediv                    )    # x / y
    __rtruediv__  = _dunder_factory(operator.truediv , reverse_args=True)    # y / x
    __pow__       = _dunder_factory(operator.pow                        )    # x ** y
    __rpow__      = _dunder_factory(operator.pow     , reverse_args=True)    # y ** x
    
    __floordiv__  = _dunder_factory(operator.floordiv                   )    # x // y
    __rfloordiv__ = _dunder_factory(operator.floordiv, reverse_args=True)    # x // y
    __mod__       = _dunder_factory(operator.mod                        )    # x % y
    __rmod__      = _dunder_factory(operator.mod     , reverse_args=True)    # y % x
    __divmod__    = _dunder_factory(builtins.divmod                     )    # divmod(x, y)
    __rdivmod__   = _dunder_factory(builtins.divmod  , reverse_args=True)    # divmod(y, x)
    
    __matmul__    = _dunder_factory(operator.matmul                     )    # x @ y
    
    __invert__    = _dunder_factory(operator.invert                     )    # ~x
    __and__       = _dunder_factory(operator.and_                       )    # x & y    
    __rand__      = _dunder_factory(operator.and_    , reverse_args=True)    # y & x
    __or__        = _dunder_factory(operator.or_                        )    # x | y
    __ror__       = _dunder_factory(operator.or_     , reverse_args=True)    # y | x
    __xor__       = _dunder_factory(operator.xor                        )    # x ^ y
    __rxor__      = _dunder_factory(operator.xor     , reverse_args=True)    # y ^ x
    __lshift__    = _dunder_factory(operator.lshift                     )    # x << y
    __rlshift__   = _dunder_factory(operator.lshift  , reverse_args=True)    # y << x
    __rshift__    = _dunder_factory(operator.rshift                     )    # x >> y
    __rrshift__   = _dunder_factory(operator.rshift  , reverse_args=True)    # y >> x

    __round__     = _dunder_factory(builtins.round                      )    # round(x, [y])
    __trunc__     = _dunder_factory(math.trunc                          )    # trunc(x)
    __floor__     = _dunder_factory(math.floor                          )    # floor(x)
    __ceil__      = _dunder_factory(math.ceil                           )    # ceil(x)

    __call__      = _dunder_factory(operator.call                       )    # x(…)
    __getitem__   = _dunder_factory(operator.getitem                    )    # x[y][…]…
    __setitem__   = _dunder_factory(operator.setitem                    )    # x[y][…]… = z
    __delitem__   = _dunder_factory(operator.delitem                    )    # del x[y][…][…]… 

    #__enter__      = _dunder_factory(operator.call                       )    # x(…)
    #__exit__      = _dunder_factory(operator.call                       )    # x(…)

    # do NOT define these because the corresponding dunder expects the corresponding type to be returned, not EvalNode
    #__bool__      = _dunder_factory(bool                                )    # bool(x)
    #__int__       = _dunder_factory(int                                 )    # int(x)
    #__float__     = _dunder_factory(float                               )    # float(x)
    #__complex__   = _dunder_factory(complex                             )    # complex(x)
    #__str__       = _dunder_factory(str                                 )    # str(x)

    # because we defined __eq__, __hash__ needs to be set manually
    #def __hash__(self):
    #    return id(self)
    #__hash__ = object.__hash__

    def tree_view(self, depth: int = 0) -> str:
        output = f"{self!r}\n"
        prefix = '|---' * depth

        for index, node in enumerate(self.args):
            output += prefix + f'[{index}]: ' + node.tree_view(depth + 1)

        for index, node in self.kwargs.items():
            output = prefix + f'{index}: ' + node.tree_view(depth + 1)

        return output
    
    __repr__ = pretty_repr

    def __str__(self) -> str: 
        return repr(self.payload)
    
    def __len__(self) -> int:
        return 999

class EvalASTVisitor(ast.NodeVisitor):
    'stateful function that visits ast.AST nodes and creates a graph of EvalNode. use .visit(ast.AST node). it returns the top EvalNode'
    
    def __init__(self, *, translate_dict: None | dict[ast.AST, Any] = None):
        self.translate_dict: dict[ast.AST, str] = default_translate_dict if translate_dict is None else translate_dict

    def generic_visit(self, node: ast.AST) -> None:
        raise NotImplementedError(f"critical error! {node!r} of type {type(node)!r} is not recognized. please report this")
        
    def visit_Constant(self, node: ast.AST) -> EvalNode:    # a number, like 2 in '2+x'
        return EvalNode(node.value)
    
    def visit_Name(self, node: ast.AST) -> EvalNode:    # any unrecognized string
        return EvalNode(node.id)

    def visit_UnaryOp(self, node: ast.AST) -> EvalNode:
        if type(node.op) not in self.translate_dict:
            raise NotImplementedError(f"{node.op} not supported")
        
        func_expr = EvalNode(self.translate_dict[op])
        operand_expr = self.visit(node.operand)    # recursion
        EvalEdge(expr, func_expr, 0)
        return func_expr

    def visit_BinOp(self, node: ast.AST) -> EvalNode:
        if type(node.op) not in self.translate_dict:
            raise NotImplementedError(f"{node.op} not supported")
        
        func_expr = EvalNode(self.translate_dict[op])
        left = self.visit(node.left)    # recursion
        right = self.visit(node.right)    # recursion
        EvalEdge(left, func_node, 0)
        EvalEdge(right, func_node, 1)
        return func_expr
    
    def visit_Call(self, node: ast.AST) -> EvalNode:
        name = node.func.id
        
        if name not in self.parse_dict:
            raise KeyError(f'{name!r} isnt recognized. check parse_dict')
            
        op: Symbol = self.parse_dict[name]
        args: Generator[EvalNode, None, None] = (self.visit(arg) for arg in node.args)    # recursion
        
        # connect args as inputs to op
        func_node = EvalNode(op)
        for index, arg in enumerate(args):
            EvalEdge(arg, func_node, index)
        
        return func_node

    def visit_Compare(self, node: ast.AST) -> EvalNode:
        'assumes comparison operators are binary operators'
        args: tuple[EvalNode] = tuple(self.visit(arg) for arg in [node.left] + node.comparators)    # recursion

        func_nodes: list[EvalNode] = []
        for index, op in enumerate(node.ops):
            op_type = type(op)
            if op_type not in self.translate_dict:
                raise NotImplementedError(f"{op} not supported")
            func_node = EvalNode(self.translate_dict[op_type])
            EvalEdge(args[index], func_node, 0)
            EvalEdge(args[index+1], func_node, 1)
            func_nodes.append(func_node)

        if len(func_nodes) == 1:  # simple unchained case
            return func_nodes[0]

        # route all to a tuple wrapper
        tuple_funcnode = EvalNode(tuple)
        for index, func_node in enumerate(func_nodes):
            EvalEdge(func_node, tuple_funcnode, index)
        
        # route tuple wrapper to all()
        all_funcnode = EvalNode(all)
        EvalEdge(tuple_funcnode, all_funcnode, 0)
        
        return all_funcnode
    
    def visit_BoolOp(self, node: ast.AST) -> EvalNode:
        'uses AND/OR if binary, ALL/ANY if variadic'
        op = type(node.op)

        if op not in self.translate_dict:
            raise NotImplementedError(f"{node.op} not supported")

        if len(node.values) == 2:    # binary
            func_node = EvalNode(self.translate_dict[op])
            in1 = self.visit(node.values[0])    # recursion
            in2 = self.visit(node.values[1])    # recursion
            EvalEdge(in1, func_node, 0)
            EvalEdge(in2, func_node, 1)
            return func_node

        if isinstance(node.op, ast.And):
            func_node = EvalNode(all)
        elif isinstance(node.op, ast.Or):
            func_node = EvalNode(any)
        else:
            raise ValueError(f"critical error! {node.op} not recognized")
        
        tuple_node = EvalNode(tuple)
        
        for index, value in enumerate(node.values):
            input = self.visit(value)    # recursion
            EvalEdge(input, tuple_node, index)
        
        EvalEdge(tuple_node, func_node, 0)
        
        return func_node
    
    def visit_IfExp(self, node: ast.AST) -> EvalNode:
        "if else expression. ast formats it like: 'node.body if node.test else node.orelse' and gapprox follows a 'a if b else c' order, instead of a 'if a then b else c' order"
        op = type(node)
        
        if op not in self.translate_dict:
            raise NotImplementedError(f"{node.op} not supported")
        
        func_node = EvalNode(self.translate_dict[op])
        
        body_node: EvalNode = self.visit(node.body)    # recursion
        test_node: EvalNode = self.visit(node.test)    # recursion
        orelse_node: EvalNode = self.visit(node.orelse)    #recursion
        
        EvalEdge(body_node, func_node, 0)
        EvalEdge(test_node, func_node, 1)
        EvalEdge(orelse_node, func_node, 2)
        
        return func_node
    
    def visit_Lambda(self, node: ast.AST):
        raise NotImplementedError("the developer is still debating how to represent a lambda function in a DAG. should she represent it as an object? a FunctionNode? an InputNode? its own self-contained Dag? or self-contained Function? these are perplexing questions...")

    def visit_Subscript(self, node: ast.AST):
        raise NotImplementedError("the developer has not added support for this yet. you can request it on the github repo!")

    def visit_Attribute(self, node: ast.AST):
        raise NotImplementedError("the developer has not added support for this yet. you can request it on the github repo!")

    __repr__ = pretty_repr
