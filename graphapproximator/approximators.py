# work in progress

# approximators are generator + expression presets
# each generator naturally links to a mathematical expression
# so this is a registry for those links

from . import analyzers as a
from . import expressions as e

parameterizer_links = {
	a.dft: e.fourier_series,
	a.dct: e.idct,
	a.dst: e.idst
}

