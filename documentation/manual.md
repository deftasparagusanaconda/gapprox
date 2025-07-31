<h1 style="color: red"> WARNING </h1>

neither gapprox nor its manual are reliable for `0.x.y` versions. this manual is effectively a placeholder. many features may be rewritten and obsoleted

---

<details><summary> 

# 👋 introduction </summary>
---
gapprox is a python toolkit to find the approximate function of a [graph][graph of a function]  
instead of "find the graph of a function", youre flipping it: "find the function of a graph"

gapprox helps streamline the process of graph approximation

[graph of a function]: https://en.wikipedia.org/wiki/Graph_of_a_function  
---
</details><details><summary> 
        
# 💾 installation </summary>
---
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
---
</details><details><summary> 

# 📗 basic guide </summary>
--- 
```python
import gapprox

expr = gapprox.fit([1, 2, 4, 6, 3], [1, 2, 5, 5, 2])

print(expr)
print(expr(2.5))
```

`import gapprox` loads the gapprox package into python  
`gapprox.fit()` automatically selects the best approximation method and returns an [Expression](#expression)  
you can print the Expression `print(expr)` or call it like a function `expr(2.5)`  

---
</details><details><summary>  

# 📙 intermediate guide </summary>
---
this is for users who want more control and familiarity with gapprox. it should take you 5 minutes to read through this. 

gapprox uses the [Approximation](#approximation) and [Expression](#expression) classes extensively. click on them to read them in the advanced guide!

besides `gapprox.fit()`, there are two other ways to approximate a graph: single evaluation (calculate once) and iterative optimization (keep improving the approximation)

single evaluation
---
```python
import gapprox as ga

approx = ga.Approximation(
    input = [1, 2, 4, 6, 3], [1, 2, 5, 5, 2],
    paramgen = ga.paramgens.line.least_squares,
    structgen = ga.structgens.polynomial
)

approx.evaluate()

print(approx.output)
print(approx.output(2.5))
```

`approx` is an [object][object] that stores `input`, `paramgen`, `structgen`, `output`

`approx.evaluate()` returns the approximate [Expression](#expression) and also stores it into `approx.output`

iterative optimization
---

```python
import gapprox as ga

approx = ga.Approximation(
    input = [1, 2, 4, 6, 3], [1, 2, 5, 5, 2],
    paramgen = ga.paramgens.line.least_squares,
    structgen = ga.structgens.polynomial
)

optimizer = ga.Optimizer()

optimizer.optimize(approx)    # same as optimizer(approx)

print(approx.output)
print(approx.output(2.5))
```

`optimizer` is a [stateful] function-like object. basically, its a function with settings you can configure, although most of that is done for you. it also remembers its previous guesses and such. its main job is to improve an approximation by running an optimization/regression algorithm step by step.

notice that you need not even use `approx.evaluate()` first! if `approx.output` is not supplied, `optimizer` automatically runs `approx.evaluate()`. if even `paramgen` and `structgen` are not supplied, `optimizer` will simply start guessing from nothing

[object]: https://en.wikipedia.org/wiki/Object_(computer_science)

</details><details><summary>

# 📕 advanced guide </summary>  
---
this is for users who want to understand how gapprox works. you are not expected to read everything so dont worry. read only what you need!

<details><summary>

## gapprox.fit() </summary>

a [callable][callable] function. it uses an AI model to run the most appropriate approximation model, and returns an [Expression](#expression)

</details><details><summary>

## gapprox.Expression </summary>  

an [object template][class]. it represents a mathematical expression like `2*x + 3` or `sin(x)` by storing it as [Nodes](#gapprox-node) in a [DAG][#gapprox-dag]
it is [callable][callable], meaning you can evaluate it if you substitute the variables. it is also printable. the syntax is similar to sympy:

```python
import gapprox as ga

x = ga.symbol("x")

expr = ga.Expression("2*x + 3")
print(expr(x=2))

# 7
```
```python
import gapprox as ga

x, y = ga.symbol("x", "y")

expr = ga.Expression("2*x + 3*y + 4")
print(expr(x=2))    # same as print(expr.subs(x=2))

# 3*y + 7
```

(not implemented yet) it may also store an expression as a [sympy expression][sympy expression] if `Expression(force_sympy=True)` is passed in its [constructor][constructor] arguments

gapprox uses a customizable set of operators. unlike PySR or sympy or ..., it does not restrict the user to its own custom-defined operators. it uses pure-python defaults as much as possible, and also defines some extensions such as `sumtorial`, `root`, `ifelse`, `SigmaSummation`. if desired, it can be modified to use sympy's set of operators, or PySR's, or a custom set; for example, redefining `ga.op.tan = math.tan2`. the functions in `gapprox.op.` are editable to allow this

</details><details><summary>

## gapprox.measures </summary>

a collection of functions that measure different things about an `Expression`. there are two types:

### gapprox.measures.absolute

a collection of functions that measure an `Expression`

### gapprox.measures.relative

a collection of functions that compare multiple `Expression`

</details><details><summary>

## gapprox.operator_dicts </summary>

a collection of dicts that define operator definitions. a bit of a mouthful but, when an `Expression` wants to create a new `Node` of, say, multiplication, it will not simply use python's `operator.mul`. it will refer to the operator_dict it was assigned to, and then use its definition, i.e., `operator_dict['mul']`. this allows gapprox to change out the set of operators, or even add custom ones

`gapprox.operator_dicts.default` is the default one used, obviously

the current implementation uses a handy dandy [DotDict](#gapprox-dotdict) for convenience but a plain old python dict is fine too!

</details><details><summary>

## gapprox.constant_dicts </summary>

like [operator_dict](#gapproxoperator-dicts) but for constants

</details><details><summary>

## gapprox.paramgens </summary>

[callable][callable] functions. a paramgen generates a list of parameters

</details><details><summary>

## gapprox.structgens </summary>

[callable][callable] functions. a structgen generates the structure of Expression

</details><details><summary>

## gapprox.Optimizer </summary>

an [object template][class]. it is a stateful component that improves 

[binary function]: https://en.wikipedia.org/wiki/Binary_function
[callable]: https://en.wikipedia.org/wiki/Callable_object
[constructor]: https://en.wikipedia.org/wiki/Constructor_(object-oriented_programming)
[class]: https://en.wikipedia.org/wiki/Class_(computer_programming)
[DAG]: https://en.wikipedia.org/wiki/Directed_acyclic_graph
[sympy expression]: https://docs.sympy.org/latest/tutorials/intro-tutorial/manipulation.html
[method]: https://en.wikipedia.org/wiki/Method_(computer_programming)

</details>

---

</details><details><summary>  

# 📚 dev notes </summary>
---
this section is for me and contributors to understand how the implementation works, and why some choices were made. not meant for users (but you're welcome to peek too ^ʷ^)

<details><summary>

## gapprox.Dag </summary>

a seperate [object template][class] which represents three nodes of a [DAG][DAG] is created? it has one method `.evaluate(` and two static methods to `.connect(` and `.disconnect(` two Nodes. upon construction/instantiation, it requires a payload, which can be either a callable or anything else. this payload is immutable.

<details><summary>.connect()</summary>

`.connect(source:Node, target:Node, index:int)`

connects source Node to target Node at target's index-th input slot

</details><details><summary>.disconnect()</summary>

`.disconnect(source:Node, target:Node, index:int)`

disconnects source Node from target Node at target's index-th input slot

</details></details><details><summary>
        
## gapprox.Node </summary>

an [object template][class] which represents a single node of a [DAG][DAG]. it is not typically visible to the user, but is very useful nontheless. it stores a list inputs, a payload (can be literally anything), and a set of outputs. 

<details><summary>.evaluate()</summary>

`.evaluate(self, substitutions:dict={})`

evaluates or collapses the graph into one value by a recursive memoized [DFS][DFS]. the substitutions dict allows replacing leaves like variable strings with values or also allows replacing a Node with another thing (done by a dict lookup). the substitutions dict also holds Nodes that were already computed so they are not recomputed (not fully tested yet)

if the node's payload is not a callable function, it returns its own payload. otherwise, it returns the output of the payload. `.evaluate` is also called on each of the inputs, which is then passed as an argument to the payload. thus evaluation is a recursive operation.

if say we had a graph that stores x+2 (say x is stored as 'x') and we want to substitute 'x' with 3, a simple substitution can be called with `.evaluate({'x': 2})` for example. 

there is an alternative way to evaluate, by performing a topological sort first and then evaluating, instead of a recursive DFS evaluation. i think. i have not tested this either

[DFS]: https://en.wikipedia.org/wiki/Depth-first_search
[DAG]: https://en.wikipedia.org/wiki/Directed_acyclic_graph

</details></details><details><summary>

## polynomials </summary>

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

</details><details><summary>

## versioning </summary>

gapprox follows [semantic versioning][semver] as `major`.`minor`.`patch`  

`major` - backward-incompatible API changes  
`minor` - backward-compatible features  
`patch` - backward-compatible bug fixes  

[semver]: https://semver.org/

</details><details><summary>

## performance </summary>

gapprox is feature-oriented and is not particularly focused on performance (down to reasonable bounds of course)

to enhance performance, certain functions or parts of gapprox may use external libraries if they are present, such as `scipy.fft` instead of a custom FFT implementation

furthermore, certain critical parts of gapprox may be directly compiled to C using Cython. it might yield a performance increase of 2x at not much inconvenience (although this is not done in the official gapprox implementation for simplicity reasons)

</details>

--- 

</details><details><summary>

# ⏳ changelog </summary>
---
0.3.0
---
+ extensive documentation ([manual.md](#https://github.com/deftasparagusanaconda/gapprox/blob/main/documentation/manual.md))
+ re-release as `gapprox` on PyPI
+ clean up module namespace
- remove `ga` launcher and other CLI entry points (package-only interface)
- reduce dynamic behaviour on import

0.2.0
---
+ improved API
+ added `ga` launcher (python REPL with `ga` imported)

0.1.0
---
+ first official PyPI release as `graphapproximator`
+ minimal but usable `paramgen` and `structgen`

---
</details><details><summary>
        
# 🚀 roadmap </summary>
---
- `gapprox.fit()` automatic graph fitting
- DAG/expression trees  
- multi-objective analysis (and [pareto front](https://en.wikipedia.org/wiki/Pareto_front) presentation)  
- web app  
- DAG node & edge weighting
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

---

</details><details><summary>

# 🤝 contributing </summary>
---
gapprox is currently not looking for contributors. solo dev work is required to get a good structure going. "if you want something done right, you gotta do it yourself"  

if youre reallly into it though, you can do the following:

```shell
git clone https://github.com/deftasparagusanaconda/gapprox/
cd gapprox/src/gapprox
pip install -e .    # -e means editable
```

and whatever changes you make will be reflected in your installed version of gapprox

if you are on linux, you may need to activate a virtual python environment before installing, since your package manager may manage python packages. in case youre too lazy to look up how to do that:

```shell
python -m venv myenv
source myenv/bin/activate # or source myenv/bin/activate.fish if you use fish like me :)

```

---
</details><details><summary>

# 🧶 tidbits & trinkets </summary>
---
- see [disciplines](https://github.com/deftasparagusanaconda/gapprox/tree/main/documentation/disciplines.md) for which disciplines this project intersects with

- there is a peculiarity in the custom number system, where abs(Integer) is not defined. there is no consensus whether abs(Integer) is Integer or Whole. by definition, abs(Real) is Real. even though the range of values is restricted, the number set is unchanged so it is still considered Real. but the Integer and Whole are indeed differentiated by the range of values. furthermore, a Whole is also technically an Integer.

---
</details>
