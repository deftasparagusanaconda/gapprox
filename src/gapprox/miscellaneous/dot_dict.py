class DotDict(dict):
	'simple wrapper for dict that allows direct dot-notation access. this class was AI-generated lmao. btw, the program wont expect this specific wrapper so feel free to change it out with a normal dict'
	def __getattr__(self, key): return self[key]
	def __setattr__(self, key, value): self[key] = value
	def __delattr__(self, key): del self[key]
	#def __dir__(self): return list(self.keys)
