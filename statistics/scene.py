from dataclasses import dataclass

import manim as ma
from manim import DOWN, ORIGIN

from lib.histogram import Histogram
from lib.prob_dist import TruncatedNormalDist
from lib.rtg import Rtg as AbstractRtg
from lib.rtg import Thing


@dataclass
class Rtg(AbstractRtg[float, ma.Circle, ma.Text]):
    prob_dist: TruncatedNormalDist
    mobj: ma.Circle

    def make_thing(self, x: float) -> Thing[float, ma.Text]:
        return Thing(x, ma.Text(f"{x:.3}", font_size=24))


class HistogramScene(ma.Scene):
    def construct(self):
        x_min, x_max = 0.0, 10.0
        rtg = Rtg(TruncatedNormalDist(x_min, x_max), ma.Circle())
        hist = Histogram(x_min, x_max, 40)

        self.add(rtg.mobj, hist.number_line, *hist.bins)
        rtg.mobj.move_to(ORIGIN + DOWN * 2)

        for _ in range(100):
            [t] = rtg.generate(1)
            self.add(t.mobj)
            target_point = hist.number_line.number_to_point(t.val)
            anim = ma.ApplyMethod(t.mobj.move_to, target_point)
            self.play(anim)
            self.remove(t.mobj)
            hist.accept(t.val)
