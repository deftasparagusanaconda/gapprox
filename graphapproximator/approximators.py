# work in progress

# approximators are generator + expression presets
# each generator naturally links to a mathematical expression
# so this is a registry for those links

from . import generators as p
from . import expressions as e

parameterizer_links = {
	p.dft: e.fourier_series,
	p.dct: e.idct,
	p.dst: e.idst
}

