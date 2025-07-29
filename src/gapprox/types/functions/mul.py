"""
binary arithmetic multiplication input -> output type matrix
also known as a type transformation tensor
tensor dimension = no. of inputs, so its a matrix
output type is determined by the span of codomain
though multiplication is not always commutative, the type is preserved
thus it is a symmetric matrix and only upper triangle is defined

mul	Nat	Who	Int	Rat	Irr	Rea	Ima	Com	Spl	Dua	Qua	Oct
Nat	Nat	Who	Int	Rat	Irr	Rea	Ima	Com	Spl	Dua	Qua	Oct	Natural      2
Who		Who	Int	Rat	Irr	Rea	Ima	Com	Spl	Dua	Qua	Oct	Whole        3
Int			Int	Rat	Irr	Rea	Ima	Com	Spl	Dua	Qua	Oct	Integer      -4
Rat				Rat		Rea	Ima	Com	Spl	Dua	Qua	Oct	Rational     5/6
Irr					Rea	Rea	Ima	Com	Spl	Dua	Qua	Oct	Irrational   √7
Rea						Rea	Ima	Com	Spl	Dua	Qua	Oct	Real         8
Ima							Rea	Com	---	---			Imaginary    9i
Com								Com	---	---			Complex      10+11i
Spl									Spl	---			SplitComplex 12+13j
Dua										Dua			Dual         14+15ε
Qua											Qua		Quaternion   16+17i+18j+19k
Oct												Oct	Octonion     1,2,3,4,5,6,7,8

any CompositeNumber must also make sure its components support the appropriate operations
but there shall not be any checks in code to enforce this
"""
