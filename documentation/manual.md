<details> 
<summary> 
        
# 👋 introduction
</summary>

gapprox is a python toolkit to find the approximate function of a [graph][graph of a function]  
instead of "find the graph of a function", youre flipping it: "find the function of a graph"

gapprox helps streamline the process of graph approximation

[graph of a function]: https://en.wikipedia.org/wiki/Graph_of_a_function  
</details>

<details>
<summary> 
        
# 💾 installation
</summary>

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

</details>

<details>
<summary> 

# 📗 basic guide
</summary>

this is the basic "i want results!" guide  
follow the example:
```python
import gapprox

graph = gapprox.Approximation()
function = graph.fit([1, 2, 4, 6, 3], [1, 2, 5, 5, 2])

print(function)
print(function(2.5))

```  
`import gapprox` loads the gapprox package into python
`Approximation()` creates an object that manages configuration (input, output, fitting method, ...)  
`.fit()` automatically selects the best approximation method, returning an [Expression](###Expression)
you can print the Expression `print(graph.output)` or call it like a function `graph.output(2.5)`

</details>

<details>
<summary> 

# 📙 intermediate guide 
</summary>

this is the intermediate "i want control!" guide

### Expression
an Expression is an object representing a mathematical function either as a DAG (directed acyclic graph) or as a tree. it is printable and callable.

</details>

<details>
<summary> 
        
# 📕 advanced guide
</summary>

this is the advanced "i want to know more!" guide, in case you want to understand the theory better
</details>

<details>
<summary> 
        
# 📚 internal reference
</summary>

this is the detailed implementation and theory reference. it is not meant for normal users
</details>

<details>
<summary>

# ⏳ changelog
</summary>

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
</details>

<details>
<summary>
        
# 🚀 roadmap
</summary>

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
</details>

<details>
<summary>

# 🤝 contributing
</summary>

gapprox is currently not looking for contributors. solo dev work is required to get a good structure going. "if you want something done right, you gotta do it yourself"  

anyway, gapprox follows semantic versioning as `major`.`minor`.`bugfix`  
`X.0.0` - big overhaul | non-backwards compatible  
`X.Y.0` - new features | backwards compatible  
`X.Y.Z` - bug fixes | minor features  
</details>

<details>
<summary>
        

# 🧶 tidbits & trinkets
</summary>

- see [disciplines](https://github.com/deftasparagusanaconda/gapprox/tree/main/documentation/disciplines.md) for which disciplines this project intersects with
</details>










[examples]: https://github.com/deftasparagusanaconda/gapprox/tree/main/examples/  
[documentation]: https://github.com/deftasparagusanaconda/gapprox/tree/main/documentation/  
[license]: https://github.com/deftasparagusanaconda/gapprox/tree/main/LICENSE  
[contact]: https://discordapp.com/users/608255432859058177

[graph]: https://en.wikipedia.org/wiki/Graph_of_a_function  
[function]: https://en.wikipedia.org/wiki/Function_(mathematics)
[functional analysis]: https://en.wikipedia.org/wiki/Functional_analysis
[approximation]: https://en.wikipedia.org/wiki/Approximation_theory
[manifold]: https://en.wikipedia.org/wiki/Manifold
[smoothness]: https://en.wikipedia.org/wiki/Smoothness
[parsing]: https://en.wikipedia.org/wiki/Parsing
[sampling]: https://en.wikipedia.org/wiki/Sampling_(statistics)
[interpolation]: https://en.wikipedia.org/wiki/Interpolation
[optimization]: https://en.wikipedia.org/wiki/Mathematical_optimization
[iterative method]: https://en.wikipedia.org/wiki/Iterative_method
[expression]: https://en.wikipedia.org/wiki/Expression_(mathematics)
[error analysis]: https://en.wikipedia.org/wiki/Error_analysis_(mathematics)
[relation types]: https://en.wikipedia.org/wiki/Relation_(mathematics)#Combinations_of_properties
[object in cs]: https://en.wikipedia.org/wiki/Object_(computer_science)

