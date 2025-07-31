from .dot_dict import DotDict as _DotDict

import math as _math

default = _DotDict()

default.update({
'nan': _math.nan,
'inf': _math.inf,
'pi' : _math.pi,
'tau': _math.tau,
'e'  : _math.e,
})
