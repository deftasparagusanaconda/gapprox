# approximators are parameterizer + expression presets
# each parameterizer naturally links to a mathematical expression
# this is a registry for those links

from . import parameterizer as p
from . import expression as e

parameterizer_links = {
	p.dft: e.fourier_series
	p.dct: e.idct
	p.dst: e.idst
