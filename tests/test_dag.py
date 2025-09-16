import gapprox as ga
from gapprox.dag import *
import operator
import builtins

def test_node_and_edge():
	'test 2+3'
	in1 = InputNode(2)
	in2 = InputNode(3)
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

def test_dag():
	'test 2+3'

	dag = Dag()

	in1 = dag.new_inputnode(2)
	in2 = dag.new_inputnode(3)
	func1 = dag.new_functionnode(operator.add)
	out1 = dag.new_outputnode('2+3')

	e1 = dag.new_edge(in1, func1, 0)
	e2 = dag.new_edge(in2, func1, 1)
	e3 = dag.new_edge(func1, out1, 0)

	assert ga.visitors.EvaluationVisitor().visit(out1) == 5

	'test abs(2)'
	func2 = dag.new_functionnode(builtins.abs)
	out2 = dag.new_outputnode('abs(2)')
	e4 = dag.new_edge(in1, func2, 0)
	e5 = dag.new_edge(func2, out2, 0)

	print(dag)

	assert ga.visitors.EvaluationVisitor().visit(out2) == 2

def test_formulae_on_dag():
	dag1 = Dag()

	in1 = dag1.new_inputnode(2)
	in1 = dag1.new_inputnode(2)

"""
import gapprox as ga
from gapprox import dag 
import operator
import builtins

dag = dag.Dag()

in1 = dag.new_inputnode(2)
in2 = dag.new_inputnode(3)
func1 = dag.new_functionnode(operator.add)
out1 = dag.new_outputnode('2+3')

e1 = dag.new_edge(in1, func1, 0)
e2 = dag.new_edge(in2, func1, 1)
e3 = dag.new_edge(func1, out1, 0)

assert ga.traversers.EvaluationVisitor().visit(out1) == 5

func2 = dag.new_functionnode(builtins.abs)
out2 = dag.new_outputnode('abs(2)')
e4 = dag.new_edge(in1, func2, 0)
e5 = dag.new_edge(func2, out2, 0)

print(dag)

assert ga.traversers.EvaluationVisitor().visit(out2) == 2

"""
