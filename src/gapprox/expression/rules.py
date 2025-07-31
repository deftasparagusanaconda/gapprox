# only use operators defined in operator_dict_default

from .operator_dicts import operator_dict_default

sub(a,b)  = add(a,neg(b))
div(a,b)  = mul(a,inv(b))
root(a,b) = pow(a,inv(b))
square(a) = pow(a,2)
cube(a)   = pow(a,3)
sqrt(a)   = root(a,2)
cbrt(a)   = root(a,3)
ln(a)     = log(a,e)
log2(a)   = log(a,2)
log10(a)  = log(a,10)
