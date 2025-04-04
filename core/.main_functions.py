def console_clear():
        print("\033[2J\033[H", end='')

def console_clear_line():
	print("\033[1A\033[K\r", end='')

def get_advanced_options(AdvancedOptionsContainer):
	locals().update(vars(AdvancedOptionsContainer))
	
	

	return AdvancedOptionsContainer

def get_input_graph_type(input_graph_type, InputGraphTypes):
	while True:
		console_clear()
		print("input graph type =", input_graph_type)
		print()
		print("[0] - None")
		for index, inputgraphtype in enumerate(InputGraphTypes):
			print(f"[{index+1}] - {inputgraphtype}")

		for i in range(10-len(InputGraphTypes)):
			print()
		
		print("[q] - back")
		print()
		match input("choice: "):
			case '0':
				input_graph_type = None
			case 'q' | 'back':
				return input_graph_type
			case choice:
				if choice.isdigit():
					if 1<=int(choice)<=len(InputGraphTypes):
						input_graph_type = InputGraphTypes[int(choice)-1]
	
	return output

def _change_input_graph(input_graph, input_graph_type, InputGraphTypes):
	match input_graph_type:
		case None:
			console_clear()
			print("set input graph type first")
			print()
			print("[Enter] - back")
			print("[q]     - back")
			print()
			input("choice: ")
		case "values":
			console_clear_line()
			input_graph = input("input values: ")
			input_graph = tuple(float(value) for value in input_graph.split(','))
		case "points":
			console_clear_line()
			input_graph = input("input points: ")
			input_graph = input_graph.replace(' ', '').split("),(")
			input_graph = tuple(tuple(eval(thing.strip('()'))) for thing in input_graph)
		case "string":
			console_clear_line()
			input_graph = input("input string: ")
		case thing:
			input(f"critical error! input_graph_type isnt supposed to have {thing}")
	
	return input_graph

def get_input_graph(input_graph, input_graph_type, InputGraphTypes):
	while True:
		console_clear()
		
#		print("input graph =", str(input_graph)[:66])
		print("input graph =", input_graph)
		print()
		print("[Enter] - change")
		print("[q]     - back")
		print()
		
		match input("choice: "):
			case '':	# same as just pressing [Enter]
				input_graph = _change_input_graph(input_graph, input_graph_type, InputGraphTypes)
			case 'q' | "back":
				return input_graph

	return input_graph

# if im not going to be able to sleep anyway, why try?
# it doesnt make a difference anyway
# fml

def get_function_interpolate(function_interpolate, Interpolators):
	while True:
		console_clear()

		if function_interpolate is None:
			print("interpolate method:", function_interpolate)
		else:
			if function_interpolate.__doc__ == None:
				print(f"interpolate method: {function_interpolate.__name__}")
			else:
				print(f"interpolate method: {function_interpolate.__name__}\n{function_interpolate.__doc__.strip(' \n')}")
		print()
		print("[0] - None")
		for index, thing in enumerate(Interpolators):
			print(f"[{index+1}] - {thing.__name__}")
		print()
		print("[q] - back")
		print()
		match input("choice: "):
			case '0':
				function_interpolate = None
			case 'q' | "back":
				break
			case choice:
				if choice.isdigit():
					if 1<=int(choice)<=len(Interpolators):
						function_interpolate = Interpolators[int(choice)-1]
	
	return function_interpolate

def get_function_approximate(function_approximate, Approximators):
	while True:
		console_clear()

		if function_approximate is None:
			print("approximation method:", function_approximate)
		else:
			if function_approximate.__doc__ == None:
				print(f"approximation method: {function_approximate.__name__}")
			else:
				print(f"approximation method: {function_approximate.__name__}\n{function_approximate.__doc__.strip(' \n')}")
		print()
		print("[0] - None")
		for index, thing in enumerate(Approximators):
			print(f"[{index+1}] - {thing.__name__}")
		print()
		print("[q] - back")
		print()
		match input("choice: "):
			case '0':
				function_approximate = None
			case 'q' | "back":
				break
			case choice:
				if choice.isdigit():
					if 1<=int(choice)<=len(Approximators):
						function_approximate = Approximators[int(choice)-1]
	
	return function_approximate

def get_function_expression(function_expression, Expressions):
	while True:
		console_clear()

		if function_expression is None:
			print("expression method:", function_expression)
		else:
			if function_expression.__doc__ == None:
				print(f"expression method: {function_expression.__name__}")
			else:
				print(f"expression method: {function_expression.__name__}\n{function_expression.__doc__.strip(' \n')}")
		print()
		print("[0] - None")
		for index, thing in enumerate(Expressions):
			print(f"[{index+1}] - {thing.__name__}")
		print()
		print("[q] - back")
		print()
		match input("choice: "):
			case '0':
				function_expression = None
			case 'q' | "back":
				break
			case choice:
				if choice.isdigit():
					if 1<=int(choice)<=len(Expressions):
						function_expression = Expressions[int(choice)-1]
	
	return function_expression
	
def get_function_iter_err_min_alg(function_iter_err_min_alg):
	return input("iterative error minimization algorithm: ")

def get_function_error(function_error, Errors):
	while True:
		console_clear()

		if function_error is None:
			print("error function:", function_error)
		else:
			if function_error.__doc__ == None:
				print(f"error function: {function_error.__name__}")
			else:
				print(f"error function: {function_error.__name__}\n{function_error.__doc__.strip(' \n')}")
		print()
		print("[0] - None")
		for index, thing in enumerate(Errors):
			print(f"[{index+1}] - {thing.__name__}")
		print()
		print("[q] - back")
		print()
		match input("choice: "):
			case '0':
				function_error = None
			case 'q' | "back":
				break
			case choice:
				if choice.isdigit():
					if 1<=int(choice)<=len(Errors):
						function_error = Errors[int(choice)-1]
	
	return function_error
	
def get_function_stepper(function_stepper, Steppers):
	while True:
		console_clear()

		if function_stepper is None:
			print("stepper function:", function_stepper)
		else:
			if function_stepper.__doc__ == None:
				print(f"stepper function: {function_stepper.__name__}")
			else:
				print(f"stepper function: {function_stepper.__name__}\n{function_stepper.__doc__.strip(' \n')}")
		print()
		print("[0] - None")
		for index, thing in enumerate(Steppers):
			print(f"[{index+1}] - {thing.__name__}")
		print()
		print("[q] - back")
		print()
		match input("choice: "):
			case '0':
				function_stepper = None
			case 'q' | "back":
				break
			case choice:
				if choice.isdigit():
					if 1<=int(choice)<=len(Steppers):
						function_stepper = Steppers[int(choice)-1]
	
	return function_stepper

def get_output_graph_type(output_graph_type, OutputGraphTypes):
	while True:
		console_clear()
		
		print("output graph type =", output_graph_type)
		print()
		print("[0] - None")
		for index, outputgraphtype in enumerate(OutputGraphTypes):
			print(f"[{index+1}] - {outputgraphtype}")
		
		for i in range(10-len(OutputGraphTypes)):
			print()
		
		print("[q] - exit")
		print()
		match input("choice: "):
			case '0':
				output_graph_type = None
			case 'q' | "back":
				break
			case choice:
				if choice.isdigit():
					if 1<=int(choice)<=len(OutputGraphTypes):
						output_graph_type = OutputGraphTypes[int(choice)-1]
	
	return output_graph_type

def get_output_graph(OptionsContainer, AdvancedOptionsContainer):
	locals().update(vars(OptionsContainer))
	locals().update(vars(AdvancedOptionsContainer))
	print("output graph:", output_graph)
	
	if input_graph_type is None:
		console_clear_line()
		console_clear_line()
		input("set input graph type first!")
	elif input_graph is None:
		console_clear_line()
		console_clear_line()
		input("set input graph first!")
	elif output_graph_type is None:
		console_clear_line()
		console_clear_line()
		input("set outut graph type first!")
	
	if function_approximate is None:
		params = input_graph
	else:
		params = function_approximate(input_graph)
		
	if function_expression is None:
		output_graph = params
	else:
		output_graph = function_expression(params)
	
	#return options_container, advanced_options_container
	
	return output_graph
	
# how to extract variables from main? this is hard 
