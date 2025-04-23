# work in progress

# approximators are generator + expression presets
# each generator naturally links to a mathematical expression
# so this is a registry for those links

from . import paramgens as p
from . import structgens as s

approximator_links = {
	p.dft: s.fourier_series,
	p.dct: s.idct,
	p.dst: s.idst
}

