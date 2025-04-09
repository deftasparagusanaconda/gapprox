# graphapproximator
approximate a graph!

standalone application:
```shell
./launcher.sh
```
```python
python3 launcher.py
```

python package:
```python
import graphapproximator as ga

mypoints = ( (1,1), (2,3), (4,3), (-2,-1), (-4,-5), (5,7) )
print(ga.line(mypoints))
```

### pipeline
![standalone application launcher.webp](<https://github.com/deftasparagusanaconda/graphapproximator/blob/main/documentation/diagrams/standalone application launcher.webp> "standalone application launcher.webp")

![engine.webp](<https://github.com/deftasparagusanaconda/graphapproximator/blob/main/documentation/diagrams/engine.webp> "engine.webp")

![iterative optimizer.webp](<https://github.com/deftasparagusanaconda/graphapproximator/blob/main/documentation/diagrams/iterative optimizer.webp> "iterative optimizer.webp")
