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

def plotter2(actual, forecast):
	import matplotlib.pyplot as plt
	try:
		plt.plot(actual[0], actual[1])
	except Exception as e:
		print("could not plot input:", e)

	try:
		plt.plot(forecast[0], forecast[1])
	except Exception as e:
		print("could not plot output:", e)

	plt.show()
