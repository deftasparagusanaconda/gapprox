# returns a + b*x + c*x^2 + d*x^3 + e*x^4 + ...
def polynomial(coefficients):
	"""polynomial(coefficients, output_type=["string"]) 
returns string of a + b*x + c*x^2 + d*x^3 + e*x^4 + ..."""
	
	output = f"{coefficients[0]}*x**0"
	for index, coefficient in enumerate(coefficients[1:], start=1):
		output += f" + {coefficient}*x**{index}"
	return output
