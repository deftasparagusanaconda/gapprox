from .dag import Node, Dag

def simplify_add_to_sum(node: Node, dag: Dag) -> Node:
	'simplify add to sum. if any add node has another add node as a child, it aggregates them into one sum node. assumes all add nodes have their inputs properly filled'
	if node.payload != 'add':
		return node

	new_inputs: list[Node] = list()

	for child in node.inputs:
		simplified_child = simplify_add(child)

		if simplified_child.payload == 'add':
			new_inputs.extend(simplified_child.inputs)
		else:
			new_inputs.append(simplified_child)
	
	sum_node = dag.new_node('sum')
	for index, node in enumerate(new_inputs):
		dag.new_edge(node, sum_node, index)

	return sum_node

def simplify_mul_to_prod(node: Node):
	'simplify mul to prod. if any mul node has another mul node as a child, it aggregates them into one prod node. assumes all mul nodes have their inputs properly filled'
	if node.payload != 'mul':
		return


