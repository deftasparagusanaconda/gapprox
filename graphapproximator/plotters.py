import matplotlib.pyplot as plt
import numpy as np
#Here the function is the function to plot
def plotter(function ,start_range , end_range , resolution : int = 400):
    x = np.linspace(start_range , end_range , resolution)
    y = eval(function)
    plt.plot(x , y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of' + str(function))
    
    plt.grid(True)
    plt.show()
    
