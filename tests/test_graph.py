import gapprox as ga
import operator
import builtins
"""
def test_node_and_edge():
	'test 2+3'
	in1 = ga.InputNode(2)
	in2 = ga.InputNode(3)
	func1 = FunctionNode(operator.add)
	out1 = OutputNode('2+3')

	e1 = Edge(in1, func1, 0)
	e2 = Edge(in2, func1, 1)
	e3 = Edge(func1, out1, 0)

	in1.outputs.add(e1)

	in2.outputs.add(e2)

	func1.inputs.append(e1)
	func1.inputs.append(e2)
	func1.outputs.add(e3)

	out1.inputs[0] = e3

	assert ga.visitors.EvaluationVisitor().visit(out1) == 5
"""
def test_graph():
	import gapprox as ga
	import operator
	
	graph = ga.MultiDAG()
	
	in1 = graph.new_node(2)
	in2 = graph.new_node('x')
	func1 = graph.new_node('add')
	out1 = graph.new_node(None)
	
	e1 = graph.new_edge(in1, func1, 0)
	e2 = graph.new_edge(in2, func1, 1)
	e3 = graph.new_edge(func1, out1, 0)
	
#	expr = ga.Expression(out1, graph=graph)
	
#	assert expr(x=3) == 5
	
"""
import gapprox as ga
import operator

graph = ga.Dag()

in1 = graph.new_node('2')
in2 = graph.new_node('x')
func1 = graph.new_node('+')
out1 = graph.new_node(None)

e1 = graph.new_edge(in1, func1, 0)
e2 = graph.new_edge(in2, func1, 1)
e3 = graph.new_edge(func1, out1, 0)

context = {'2': 2, '+': operator.add}

expr = ga.Expression(graph, out1, context)

expr(x=2)
"""
