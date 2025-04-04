def cli(ga):
	from . import functions

	while True:
		match functions.main_menu(ga):
			case '0':
				ga.advanced_options = functions.advanced_options(ga)
			case '1':
				ga.input_graph_type = functions.get_input_graph_type(ga)
			case '2':
				ga.function_interpolate = functions.get_function_interpolate(ga)
			case '3':
				ga.function_approximate = functions.get_function_approximate(ga)
			case '4':
				ga.function_expression = functions.get_function_expression(ga)
			case '5':
				ga.function_iter_err_min_alg = functions.get_function_iter_err_min_alg(ga)
			case '6':
				ga.function_error = functions.get_function_error(ga)
			case '7':
				ga.function_stepper = functions.get_function_stepper(ga)
			case '8':
				ga.output_graph_type = functions.get_output_graph_type(ga)
			case '9':
				ga.output_graph = functions.output_graph(ga)
#			case '' | "start" | "Start" | "enter" | "Enter":
#				ga.output_graph = functions.get_output_graph(ga)
			case 'a' | "input":
				ga.input_graph = functions.get_input_graph(ga)
			case 'b' | "output":
				ga.output_graph = functions.get_output_graph(ga)
			case 'q' | "exit" | "Exit" | "back" | "Back" | "quit" | "QUIT":
				break
			case choice:	# default case
				functions.console_clear_line()
				functions.console_clear_line()
				input(f"\nhmmm... i dont think \"{choice}\" is valid...")

print("exiting CLI...")

# FUUUCK duude I WANNA JERK OFFF
