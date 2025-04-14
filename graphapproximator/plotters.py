import matplotlib.pyplot as plt
import numpy as np

#Here the function is the function to plot
def plotter(function ,start_range , end_range,):
    x = np.linspace(start_range , end_range , 400)
    y = eval(function)
    plt.plot(x , y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of' + str(function))
    
    plt.grid(True)
    plt.show()

def plotter2(x_values, y_values):
	import matplotlib.pyplot as plt
	plt.plot(x_values, y_values)
	plt.show()
