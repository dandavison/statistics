from dataclasses import dataclass
from typing import Generic, List, Protocol, TypeVar

import manim as ma
from lib.prob_dist import ProbDist

V = TypeVar("V")
M = TypeVar("M", bound=ma.Mobject)
M1 = TypeVar("M1", bound=ma.Mobject)
M2 = TypeVar("M2", bound=ma.Mobject)


@dataclass
class Thing(Generic[V, M]):
    val: V
    mobj: M


T = TypeVar("T", bound=Thing)


@dataclass
class Rtg(Generic[V, M1, M2], Protocol):
    prob_dist: ProbDist[V]
    mobj: M1

    def generate(self, size: int) -> List[Thing[V, M2]]:
        vs = self.prob_dist.generate(size)
        ts = []
        for v in vs:
            t = self.make_thing(v)
            t.mobj.move_to(self.mobj.get_center())
            ts.append(t)
        return ts

    def make_thing(self, v: V) -> Thing[V, M2]:
        ...
