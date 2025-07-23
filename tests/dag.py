import gapprox as ga

nodes = []*10
edges = []*10

dag = ga.Dag()

nodes[1] = dag.new_node(2)
nodes[2] = dag.new_node(3)
nodes[3] = dag.new_node('x')
nodes[4] = dag.new_node(lambda a,b,c: a+b*c)

edges[1] = dag.new_edge(nodes[1], nodes[4], 0)
edges[2] = dag.new_edge(nodes[2], nodes[4], 1)
edges[3] = dag.new_edge(nodes[3], nodes[4], 2)

print(n4.evaluate({'x': 3}))

# 11
