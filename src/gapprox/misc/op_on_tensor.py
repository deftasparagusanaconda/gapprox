from collections.abc import Iterable

def op_on_tensor(tensor:Iterable, op:callable):
	'preserves iterable type like tuple/list/etc'
	if isinstance(tensor, Iterable) and not isinstance(tensor, (str, bytes)):
		return type(tensor)(op_on_tensor(element, op) for element in tensor)
	else: # tensor is actually just a single element
		return op(tensor)
