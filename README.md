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
![standalone application launcher drawio](https://github.com/user-attachments/assets/51bacb20-cb91-4e8e-8b1b-452d682eacda)
![engine drawio](https://github.com/user-attachments/assets/410eee4a-6c16-4283-bb9b-4b8f8be6f338)
![iterative optimizer drawio](https://github.com/user-attachments/assets/f189b71e-a9a6-4ad3-a8ed-096eb366bd64)
