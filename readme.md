[📖 manual][manual] | [🔍 examples][examples] | [📜 license][license] | [💡suggest silly ideas!][contact]  

# gapprox
a python toolkit to find the approximate function of any [graph][graph]  
instead of "find the graph of the function", youre flipping it: "find the function of the graph"

## 💾 installation
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

for better performance, install with all optional dependencies:
```shell
pip install gapprox[all]
```

## 📗 basic guide
```python
import gapprox as ga

f = ga.fit([1, 2, 4, 6, 3], [1, 2, 5, 5, 2])

print(f)
print(f(2.5))
```

`.fit()` selects the best approximation method and returns an [Expression][advanced guide]  
you can print the Function `print(f)` or call it like a function `f(2.5)`  

gapprox can do a lot more. check out more examples [here!][examples] or read the [manual][manual]

## 🚀 roadmap
+ DAG/expression trees  
+ multi-objective analysis 
+ complex numbers  
+ parametric function support  
+ multiple-input multiple-output
- [pareto front](https://en.wikipedia.org/wiki/Pareto_front) presentation
- web app  
- symbolic regression  
- n-dimensional plotters  
- surface approximation  
- [many-to-many][relation types] relation approximation  
- point density evaluators  
- hypersonic blasters 🚀

~~in the far far future, ga will support multiple-input multiple-output approximation. for m inputs and n outputs, it runs n approximations of m-dimensional [manifolds][manifold] separately  
effectively, this turns it into a general-purpose prediction library, analogous to AI  
currently, ga only supports single-input single-output [many-to-one][relation types] functions. see [roadmap][roadmap] for details  ~~

gapprox now supports any general mathematical expression as long as it is representable on a directed acyclic graph. you may go ham on tensorial input/output

## 📔 you read all that?!?

this project is still budding 🌱 if you'd like to change something, add something, or suggest ideas—[come say hi!][contact]

with love, and a passion for maths ~  
\- [daa][contact] 🌸

[examples]: https://github.com/deftasparagusanaconda/gapprox/tree/main/examples/  
[manual]: https://github.com/deftasparagusanaconda/gapprox/tree/main/documentation/manual.md  
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
[advanced guide]: https://github.com/deftasparagusanaconda/gapprox/blob/main/documentation/manual.md#-advanced-guide-
