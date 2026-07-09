# fit ax² + bx + c to sin(πx) in [0, 1]

import math, gapprox as ga

target = lambda x: math.sin(x * math.pi)
approx = lambda a, b, c: lambda x: a * x * x + b * x + c

def guesser(optimizer):
    optimizer.last_guess + ()

def scorer(guess):
    return sum(abs(target(i/360), guess(i/360)) for i in range(360+1)),

optimizer = ga.Optimizer(
    terminator = lambda: True,
    guesser = guesser,
    scorer = scorer,
)

while True:
    next(optimizer)
