[🔍 examples][examples] | [📖 documentation][documentation] | [📜 license][license] | [💡suggest silly ideas!][contact]  

# graphapproximator
a python toolkit to help you find the approximate equation of any 2D graph  
instead of "given an equation, find the graph", you’re flipping it: "given a graph, find the equation"

---
## 🔧 how to use
run it as an app:
```shell
./launcher.sh
```
or:
```python
python3 launcher.py
# "python3 launcher.py --headless" to launch the CLI!
```
or run it as a python package ^-^
```python
import graphapproximator.api as ga

mypoints = [(1,1), (2,3), (4,3), (-2,-1), (-4,-5), (5,7)]
approx = ga.line(mypoints)

print(approx)

# f(x) = 0.2 + 1.1333333333*x
```
```python
import graphapproximator.api as ga

ga.input = [2,3,6,5,4]
ga.generator = ga.generators.parabola.least_squares
ga.expression = ga.expressions.polynomial
ga.approximate()  # also the same as ga()

print(ga.output)  # 
ga.plot()
```
check out more [examples!][examples]

---
## ⚙️ how it works

### api

![api.webp](<https://github.com/deftasparagusanaconda/graphapproximator/blob/main/documentation/diagrams/api.webp> "api.webp")

[converter](#converter) converts a graph from one form to another  
[analyzer](https://en.wikipedia.org/wiki/Functional_analysis) analyzes the input to generate parameters for an expression  
[optimizer](#optimizer) improves parameters by iterative [optimization](https://en.wikipedia.org/wiki/Mathematical_optimization)  
[expression](https://en.wikipedia.org/wiki/Expression_(mathematics)) turns parameters into a math expression  
[converter](#converter) converts a graph from one form to another  

each component is optional. if you didnt set that component, the data simply passes through  
input and output are handled differently, depending on the interface  

### converter

![converter.webp]("converter.webp")

[parser](https://en.wikipedia.org/wiki/Parsing) decodes string input into a callable function  
[sampler](https://en.wikipedia.org/wiki/Sampling_(statistics)) samples a callable function into points  
[interpolator](https://en.wikipedia.org/wiki/Interpolation) turns scattered points into a smooth function, then samples it  

converter converts a graph from one form to another  
depending on input type and the desired output type, one or two components are chosen automatically  

as you parse string to function, you lose the ability to [differentiate/integrate](https://en.wikipedia.org/wiki/Differential_calculus) smoothly  
as you sample function to points, you lose the [smoothness](https://en.wikipedia.org/wiki/Smoothness) of the function  
as you interpolate points to string, you add "fake" data which was not originally there  

string is the most favourable representation, so the api will try to preserve it

### optimizer

![optimizer.webp](<https://github.com/deftasparagusanaconda/graphapproximator/blob/main/documentation/diagrams/optimizer.webp> "optimizer.webp")

[predictor](https://en.wikipedia.org/wiki/Iterative_method) finds the next best set of parameters to minimize error  
[expression](https://en.wikipedia.org/wiki/Expression_(mathematics)) turns parameters into a math expression  
[error](https://en.wikipedia.org/wiki/Error_analysis_(mathematics)) calculates the discordance between original input and approximation  

optimizer improves parameters by iterative [optimization](https://en.wikipedia.org/wiki/Mathematical_optimization)  
it hold its own configuration. this is done by making it an [object](https://en.wikipedia.org/wiki/Object_(computer_science))  
it runs until it reaches an end condition, such as time limit, iteration limit, ...  
it is also capable of multithreading/parallel processing  

---
## ⏳ coming soon ~
- file IO support
- PyPI support
- CLI
- webUI
- GUI
- automatic expression selector  
- symbolic regression (adaptive expression)
- customizable api pipeline
- parametric function
- hypersonic blasters

---
## 📔 you read all that?!?

this project is still blooming ✨ if you'd like to change something, add something, or suggest ideas—[come say hi!][contact]

with love, and a passion for maths ~  
\- daa 🌸

[examples]: https://github.com/deftasparagusanaconda/graphapproximator/tree/main/examples/  
[documentation]: https://github.com/deftasparagusanaconda/graphapproximator/tree/main/documentation/  
[license]: https://github.com/deftasparagusanaconda/graphapproximator/tree/main/LICENSE  
[contact]: https://github.com/deftasparagusanaconda  
