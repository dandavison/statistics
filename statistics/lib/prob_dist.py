from dataclasses import dataclass
from typing import Generic, List, Protocol, TypeVar

import numpy as np
import scipy.stats

V = TypeVar("V")


class ProbDist(Generic[V], Protocol):
    def generate(self, size: int) -> List[V]:
        ...


@dataclass
class TruncatedNormalDist(ProbDist[float]):
    x_min: float
    x_max: float

    def generate(self, size: int) -> List[float]:
        x = scipy.stats.norm.rvs(loc=(self.x_min + self.x_max) / 2, scale=1, size=size)
        return np.clip(x, self.x_min, self.x_max)
