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
def test_dag():
	import gapprox as ga
	import operator
	
	dag = ga.Dag()
	
	in1 = dag.new_node(2)
	in2 = dag.new_node('x')
	func1 = dag.new_node('add')
	out1 = dag.new_node(ga.OUTPUT_NODE_MARKER)
	
	e1 = dag.new_edge(in1, func1, 0)
	e2 = dag.new_edge(in2, func1, 1)
	e3 = dag.new_edge(func1, out1, 0)
	
#	expr = ga.Expression(out1, dag=dag)
	
#	assert expr(x=3) == 5
	
"""
import gapprox as ga
import operator

dag = ga.Dag()

in1 = dag.new_node('2')
in2 = dag.new_node('x')
func1 = dag.new_node('+')
out1 = dag.new_node(None)

e1 = dag.new_edge(in1, func1, 0)
e2 = dag.new_edge(in2, func1, 1)
e3 = dag.new_edge(func1, out1, 0)

context = {'2': 2, '+': operator.add}

expr = ga.Expression(dag, out1, context)

expr(x=2)
"""
