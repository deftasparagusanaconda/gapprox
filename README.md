[🔍 examples][examples] | [📖 documentation][documentation] | [📜 license][license] | [💡suggest ideas!][contact]

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
import graphapproximator as ga

mypoints = [ (1,1), (2,3), (4,3), (-2,-1), (-4,-5), (5,7) ]
approx = ga.line(mypoints)

print(approx)

# f(x) = 0.2 + 1.1333333333*x
```
---
## ⚙️ how it works

importing graphapproximator automatically spawns an Engine instance, ready to use out of the box
![engine.webp](<https://github.com/deftasparagusanaconda/graphapproximator/blob/main/documentation/diagrams/engine.webp> "engine.webp")

each interface (API/CLI/GUI/webUI) talks to a single *Engine* instance  
this object manages your current configuration of generator, expression, interpolator, ...  
the *Engine* also exposes a list of available modules (generators, expressions, interpolators, ...)  

input: provided by API/CLI/GUI/webUI  
parser: decodes string input into symbolic math input  
interpolator: turns scattered points into a smooth function, then samples it  
generator: generates parameters for an expression  
optimizer: iteratively improves parameters  
expression: turns parameters into a math expression  
output: passed to API/CLI/GUI/webUI  

each module is optional. if you didn't define it, the data simply passes through  
there are also other standalone features like extrapolator, outlier, ...  

![iterative optimizer.webp](<https://github.com/deftasparagusanaconda/graphapproximator/blob/main/documentation/diagrams/iterative optimizer.webp> "iterative optimizer.webp")

the iterative optimizer is a special kind of generator  
it is an instance of *"IterativeOptimizer"*  
this object manages your current configuration of expression, error, predictor, ...  

input: provided by API/CLI/GUI  
predictor: find the next best set of parameters to minimize error  
expression: turns parameters into a math expression  
error: calculates the discordance between original input and approximation  
output: passed to API/CLI/GUI  

the iterative optimizer runs until it reaches an end condition, such as time_limit, iter_limit, ...  
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
- parametric function
- hypersonic blasters

---
## 📔 you read all that?!?

this project is still blooming ✨ if you'd like to change something, add something, or suggest ideas—[come say hi!][contact]

with love, and a passion for maths ~  
\- [daa][contact] 🌸

[examples]: https://github.com/deftasparagusanaconda/graphapproximator/tree/main/examples/
[documentation]: https://github.com/deftasparagusanaconda/graphapproximator/tree/main/documentation/
[license]: https://github.com/deftasparagusanaconda/graphapproximator/tree/main/LICENSE
[contact]: https://discord.com/users/608255432859058177
