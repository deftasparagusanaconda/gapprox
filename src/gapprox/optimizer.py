from dataclasses import dataclass, field
from collections.abc import Iterator, Callable
from numbers import Real
from typing import Any
from .pareto_front import ParetoFront

@dataclass(kw_only=True, slots=True)
class Optimizer(Iterator):
    guesser: Callable[[Optimizer], Any]
    scorer: Callable[[Any], Real] = lambda x: x
    front: ParetoFront = field(default_factory = ParetoFront)
    terminator: Callable[[Optimizer], bool] = lambda x: False
    _last_guess: None | Any = None
    _last_score: None | Real = None
    
    def __next__(self) -> tuple[Any, Real]:
        if self.terminator(self):
            raise StopIteration
        self._last_guess = self.guesser(self)
        self._last_score = self.scorer(self._last_guess)
        self.front[self._last_guess] = self._last_score
        return self._last_guess, self._last_score

@dataclass(slots=True)
class Terminator_IterCount(Callable):
    iter_limit: int
    iter_count: int = 0
    def __call__(self, optimizer: Optimizer) -> bool:
        self.iter_count += 1
        return self.iter_count > self.iter_limit

