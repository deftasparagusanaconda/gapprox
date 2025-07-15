<details><summary> 

# 👋 introduction </summary>
gapprox is a python toolkit to find the approximate function of a [graph][graph of a function]  
instead of "find the graph of a function", youre flipping it: "find the function of a graph"

gapprox helps streamline the process of graph approximation

[graph of a function]: https://en.wikipedia.org/wiki/Graph_of_a_function  
</details><details><summary> 
        
# 💾 installation </summary>
get it from PyPI: 
```shell
pip install gapprox
```

or install the latest from GitHub:
```shell
git clone https://github.com/deftasparagusanaconda/gapprox
cd gapprox
pip install .
```

for faster performance, install with all optional dependencies:
```shell
pip install gapprox[all]
```

</details><details><summary> 

# 📗 basic guide </summary>
basic usage:
```python
import gapprox

function = gapprox.fit([1, 2, 4, 6, 3], [1, 2, 5, 5, 2])

print(function)
print(function(2.5))
```

`import gapprox` loads the gapprox package into python  
`.fit()` selects the best approximation method and returns an [Expression](#expression)  
you can print the Expression `print(function)` or call it like a function `function(2.5)`  

</details><details><summary>  

# 📙 intermediate guide </summary>
this is for users who want more control and familiarity with gapprox. it should take you 5 minutes to read through this. follow the given example:
```python
import gapprox as ga

graph = ga.Approximator(
    paramgen = ga.paramgens.line.least_squares
    structgen = ga.structgens.polynomial
)

function = graph.evaluate([1, 2, 4, 6, 3], [1, 2, 5, 5, 2])    # calculate an approximation with the given configuration

print(function)
print(function(3.5))
```

```python
import gapprox as ga

graph = ga.Optimizer(

function = graph.evaluate(

print(function)
print(function(3.5))
```

# 📕 advanced guide </summary>  

this is for users who want to understand how gapprox works  

## Expression </summary>
an Expression is an object representing a mathematical function. it is printable and callable. internally it uses one of three systems:
- [directed acyclic graph][DAG]        (not implemented yet)
- [binary expression tree][BET]        (not implemented yet)
- [sympy expression][sympy expression] (not implemented yet)

[DAG]: https://en.wikipedia.org/wiki/Directed_acyclic_graph
[BET]: https://en.wikipedia.org/wiki/Binary_expression_tree
[sympy expression]: https://docs.sympy.org/latest/tutorials/intro-tutorial/manipulation.html

</details><details><summary>  

# ⏳ changelog </summary>

0.1.0:  
+ first official PyPI release as `graphapproximator`
+ minimal but usable `paramgen` and `structgen`

0.2.0:
+ improved API
+ added `ga` launcher (python REPL with `ga` imported)

0.3.0:
+ re-release as `gapprox` on PyPI
+ clean up module namespace
- remove CLI entry points (package-only interface)
- reduce dynamic behaviour on import
</details><details><summary>
        
# 🚀 roadmap </summary>

- DAG/expression trees  
- multi-objective analysis (and [pareto front](https://en.wikipedia.org/wiki/Pareto_front) presentation)  
- web app  
- symbolic regression  
- complex numbers  
- parametric function support  
- multiple-input multiple-output
- n-dimensional plotters  
- surface approximation  
- [many-to-many][relation types] relation approximation  
- point density evaluators  
- hypersonic blasters 🚀

in the far far future, ga will support multiple-input multiple-output approximation. for m inputs and n outputs, it runs n approximations of m-dimensional [manifolds][manifold] separately  
effectively, this turns it into a general-purpose prediction library, analogous to AI  
currently, ga only supports single-input single-output [many-to-one][relation types] functions

[relation types]: https://en.wikipedia.org/wiki/Relation_(mathematics)#Combinations_of_properties
[manifold]: https://en.wikipedia.org/wiki/Manifold
</details><details><summary>

# 🤝 contributing </summary>

gapprox is currently not looking for contributors. solo dev work is required to get a good structure going. "if you want something done right, you gotta do it yourself"  

anyway, gapprox follows semantic versioning as `major`.`minor`.`bugfix`  
`X.0.0` - big overhaul | non-backwards compatible  
`X.Y.0` - new features | backwards compatible  
`X.Y.Z` - bug fixes | minor features  
</details><details><summary>
        

# 🧶 tidbits & trinkets </summary>

- see [disciplines](https://github.com/deftasparagusanaconda/gapprox/tree/main/documentation/disciplines.md) for which disciplines this project intersects with
</details>
