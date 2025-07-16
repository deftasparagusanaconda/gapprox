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

graph = ga.Approximation(
    paramgen = ga.paramgens.line.least_squares
    structgen = ga.structgens.polynomial
)

function = graph.evaluate([1, 2, 4, 6, 3], [1, 2, 5, 5, 2])    # calculate an approximation with the given configuration

print(function)
print(function(3.5))
```

gapprox uses `Approximation` to remember how to 

```python
import gapprox as ga

graph = ga.Optimizer(

function = graph.evaluate(

print(function)
print(function(3.5))
```
</details><details><summary>

# 📕 advanced guide </summary>  

this is for users who want to understand how gapprox works. you are not expected to read everything so dont worry. read only what you need!

<details><summary>

## Expression </summary>
an [object template][class]. it represents a mathematical expression like `2*x + 3` or `sin(x)`  
it is [callable][callable], meaning you can evaluate it if you substitute the variables. it is also printable. the syntax is similar to sympy:

```python
import gapprox as ga

x = ga.symbol("x")

expr = ga.Expression("2*x + 3")
print(expr(x=2))    # same as print(expr.subs(x=2))

# 7
```

if the variables are not completely substituted, it returns a simplified Expression:
```python
import gapprox as ga

x, y = ga.symbol("x", "y")

expr = ga.Expression("2*x + 3*y + 4")
print(expr(x=2))    # same as print(expr.subs(x=2))

# 3*y + 7
```

it uses one of any three internal systems, morphing on-the-fly as appropriate:

- directed acyclic graph ([gapprox.Dag](#dag))
- binary expression tree ([gapprox.Tree](#tree))
- [sympy expression][sympy expression] (used only if specified in the [constructor][constructor] arguments as `Expression(force_sympy=True)`

<details><summary>.subs()</summary>


</details></details><details><summary>

## paramgen </summary>
a [callable][callable] function. it generates a list of parameters

</details><details><summary>

## structgen </summary>
a [callable][callable] function. it generates the structure of Expression

</details><details><summary>

## Optimizer </summary>
an [object template][class]. it is a stateful component that improves 

[binary function]: https://en.wikipedia.org/wiki/Binary_function
[callable]: https://en.wikipedia.org/wiki/Callable_object
[constructor]: https://en.wikipedia.org/wiki/Constructor_(object-oriented_programming)
[class]: https://en.wikipedia.org/wiki/Class_(computer_programming)
[DAG]: https://en.wikipedia.org/wiki/Directed_acyclic_graph
[BET]: https://en.wikipedia.org/wiki/Binary_expression_tree
[sympy expression]: https://docs.sympy.org/latest/tutorials/intro-tutorial/manipulation.html
[method]: https://en.wikipedia.org/wiki/Method_(computer_programming)

</details><details><summary>

## fit() </summary>

a [callable][callable] function. it takes an array as input and returns an [Expression](#expression)


</details></details><details><summary>  

# 📚 dev notes </summary>

this section is for me and contributors to understand how the implementation works, and why some choices were made. not meant for users (but you're welcome to peek too ^ʷ^)

<details><summary>

## Dag </summary>
an [object template][class]. it represents a [directed acyclic graph][DAG] by storing a collection of nodes

it uses one of any three internal systems, morphing on-the-fly as appropriate

- adjacency list
- adjacency matrix
- edges list
</details><details><summary>

## Tree </summary>
an [object template][class]. it represents a [binary expression tree][BET] by storing a collection of nodes. it is very similar to [gapprox.Dag](#dag) except it allows only [binary functions][binary function]

</details><details><summary>

### polynomials </summary>

polynomials are stored as an array of terms. each term is stored as [coefficient, [exponent1, exponent2, exponent3, ...]] this is better than a tensor representation because:
1. if there are only a few terms, the tensor becomes a sparse tensor, wasting a lot of reserved memory
2. the tensor will support only whole-number coefficients
3. it can store large coefficients without having to reserve large memory. for example, x^1000
4. it allows different data types for coefficents and exponents

storing terms in this way allows us to store fractional polynomials; for example x^2.5 + 3 is stored as [[1, 2.5], [3]]

alternatively, if we want to store integer exponents, a term may be stored as [float coefficent, int exponent_array[]]. additionally, on the off-chance that the exponent_array is itself a sparse vector (i.e. each term has only a few variables in it), we may store it as a coordinate list. there are numerous ways to do so.

gapprox does not have a special Polynomial class for this for a few reasons:
1. non-conventional and data-dependent physical storage strategy
2. Expression is powerful enough to handle storing polynomials
3. most polynomials have few terms anyway
4. it introduces an unnecessary class

</details></details><details><summary>

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
