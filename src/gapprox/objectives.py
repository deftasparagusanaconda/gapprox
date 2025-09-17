"""
from the Dag representation of the expression:
inputnode count      | how many inputnode
functionnode count   | how many functionnode
outputnode count     | how many outputnode
node count           | how many nodes
edge count           | how many edges
total count          | how many nodes and edges
inputnode weight     | sum of weights of inputnodes
functionnode weight  | sum of weights of functionnodes
outputnode weight    | sum of weights of outputnodes
node weight          | sum of weights of all nodes
edge weight          | sum of weights of edges
total weight         | sum of weights of all nodes and edges
average in degree    | how many inputs nodes have on average
aOverage out degree  | how many outupts nodes have on average
average total degree | how many inputs and outputs nodes have on average
max tree depth       | the length of the longest path from an outputnode to an inputnode
max tree breadth     | max number of nodes for depths
max tree ratio       | ratio of max tree depth to max tree breadth
min tree depth       | min depth of tree
min tree breadth     | min number of nodes for depths
min tree ratio       | ratio of min tree depth to min tree breadth
avg tree depth       | average depth of tree
avg tree breadth     | average number of nodes for depths
avg tree ratio       | ratio of avg tree depth to avg tree breadth
average arity        | how many inputs the functionnodes have on average

and from the Function representation of the expression:
variable count      |
constant count      |
output count        |
trigonometric count |
hyperbolic count    |
arithmetic count    |
comparative count   |
boolean count       |

and mathematically:
max degree          | exponent power of highest term
term count          | how many terms are present
factorizability     | how much it can be further factorized
max nesting depth   | how deeply a part of it is embedded within parentheses
zero crossing count | how much it crosses zero
"""

from .dag import Node, InputNode, FunctionNode, OutputNode, Edge, Dag

def tree_inputnode_count(node:Node):
    'how many InputNode in the spanning tree, starting from the given node'

def tree_functionnode_count(node:Node):
    'how many FunctionNode in the spanning tree, starting from the given node'

def tree_outputnode_count(node:Node):
    'how many OutputNode in the spanning tree, starting from the given node'

def tree_node_count(node:Node):
    'how many Node in the spanning tree, starting from the given node'

def tree_edge_count(node:Node):
    'how many Edge in the spanning tree, starting from the given node'

def tree_node_and_edge_count(node:Node):
    'how many Node and Edge in the spanning tree, starting from the given node'

# make a traverser that can return all these in one traversal
from . import errors, collapsers

def error(original:list[any], approximation:list[any], error:callable=errors.difference_squared, collapser:callable=collapsers.sum):
	'calculate how much discrepancy is between two arrays of numbers. uses RMSE (root mean squared error) by default'
	if len(original) != len(approximation):
		raise ValueError(f"length mismatch: len(original)={len(original)}, len(approximation)={len(approximation)}")

	return reduction(loss(a, b) for a, b in zip(original, approximation))

# error is pretty hard to find, because gapprox currently does it using discretely and numerically. and even then, it can do it by either taking in a bunch of points or taking a callable and sampling it on the spot. and gapprox should also be able to find error symbolically, continuously, analytically.

# at least im sure about one thing: error should not sample the callable inside it. it should take sampled points. because when error is evaluated for each iteration, it should not have to resample for every iteration.
