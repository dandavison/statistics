from math import floor
from typing import List

from scipy.stats import norm

import manim as m
from manim import *

m = m

EPSILON = 0.001


class Bin(Rectangle):
    def __init__(self, start: float, *args, **kwargs):
        self.start = start
        super().__init__(*args, **kwargs)

    def grow(self, delta: float):
        self.stretch_to_fit_height(self.height + delta, about_point=self.get_bottom())


def rescale(bins: List[Bin], max_height_screen: float):
    assert bins
    max_bin_height = max(b.height for b in bins)
    if max_bin_height <= max_height_screen:
        return
    scale_fac = max_height_screen / max_bin_height
    for b in bins:
        b.stretch_to_fit_height(b.height * scale_fac, about_point=b.get_bottom())


class Histogram(Scene):
    def construct(self):
        rtg = Circle()
        rtg.move_to(ORIGIN + DOWN * 2)
        rtg_center = rtg.get_center()

        x_min, x_max = 0.0, 10.0
        line_length = x_max - x_min
        number_line = m.NumberLine((x_min, x_max, 1), 10)

        def random_value() -> float:
            x = norm.rvs(loc=x_min + line_length / 2, scale=1, size=1)[0]  # type:ignore
            x = max(x_min, min(x, x_max))
            return x

        # Histogram
        n_bins = 40
        bin_width = line_length / n_bins
        hist_max_height_screen = 2.0

        bins = [
            Bin(
                start=(x_min + line_length * i / n_bins),
                width=bin_width,
                height=EPSILON,
            )
            for i in range(n_bins)
        ]

        for i, bin in enumerate(bins):
            bin.move_to(
                number_line.number_to_point(bin.start) + 0.5 * bin_width * RIGHT
            )

        self.add(rtg, number_line, *bins)

        for _ in range(100):
            x = random_value()
            x_text = Text(f"{x:.3}", font_size=24)
            self.add(x_text)
            x_text.move_to(rtg_center)
            target_point = number_line.number_to_point(x)
            anim = ApplyMethod(x_text.move_to, target_point)
            self.play(anim)
            self.remove(x_text)
            bin_index = floor(n_bins * x / line_length)
            # in case x is at the extreme right end!
            bin_index = min(bin_index, n_bins - 1)
            bins[bin_index].grow(0.25)
            rescale(bins, hist_max_height_screen)
