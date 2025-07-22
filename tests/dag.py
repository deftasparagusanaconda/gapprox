import gapprox as ga

dag = ga.Dag()

n1 = dag.new_node(2)
n2 = dag.new_node(3)
n3 = dag.new_node('x')
n4 = dag.new_node(lambda a,b,c: a+b*c)

e1 = dag.new_edge(n1, n4, 0)
e2 = dag.new_edge(n2, n4, 1)
e3 = dag.new_edge(n3, n4, 2)

print(n4.evaluate({'x': 3}))

# 11
