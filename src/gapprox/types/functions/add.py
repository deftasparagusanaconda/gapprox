"""
binary arithmetic addition input -> output type matrix
also known as a type transformation tensor
tensor dimension = no. of inputs, so its a matrix
output type is determined by the span of codomain
addition is commutative so this matrix is symmetric
thus only the upper triangle is defined

add	Nat	Who	Int	Rat	Irr	Rea	Ima	Com	Spl	Dua	Qua	Oct
Nat	Nat	Nat	Int Rat	Irr	Rea	Com	Com	Spl	Dua	Qua	Oct	Natural
Who		Who	Int	Rat	Irr	Rea	Com	Com	Spl	Dua	Qua	Oct	Whole
Int			Int	Rat	Irr	Rea	Com	Com	Spl	Dua	Qua	Oct	Integer
Rat				Rat	Irr	Rea	Com	Com	Spl	Dua	Qua	Oct	Rational
Irr					Rea	Rea	Com	Com	Spl	Dua	Qua	Oct	Irrational
Rea						Rea	Com	Com	Spl	Dua	Qua	Oct	Real
Ima							Ima	Com	---	---	Qua	Oct	Imaginary
Com								Com	---	---	Qua	Oct	Complex
Spl									Spl	---	---	---	SplitComplex
Dua										Dua	---	---	Dual
Qua											Qua	Oct	Quaternion
Oct												Oct	Octonion

any CompositeNumber must also make sure its components support addition
but there shall not be any checks in code to enforce this
"""
