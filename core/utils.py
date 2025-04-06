def console_clear():
	print("\033[2J\033[H", end='')

def console_clear_line():
	print("\033[1A\033[K\r", end='')

def error_soft(input):
	print(input)
	# will include a update_UI() that sends a global UI update signal
