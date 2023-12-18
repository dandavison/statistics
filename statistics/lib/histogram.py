from dataclasses import dataclass, field
from math import floor
from typing import List

import manim as ma
from manim import RIGHT

EPSILON = 0.001


class Bin(ma.Rectangle):
    def __init__(self, start: float, *args, **kwargs):
        self.start = start
        super().__init__(*args, **kwargs)

    def grow(self, delta: float):
        self.stretch_to_fit_height(self.height + delta, about_point=self.get_bottom())


@dataclass
class Histogram:
    x_min: float
    x_max: float
    n_bins: int
    bins: List[Bin] = field(init=False)
    number_line: ma.NumberLine = field(init=False)

    def __post_init__(self):
        self.number_line = ma.NumberLine((self.x_min, self.x_max, 1), 10)

        line_length = self.x_max - self.x_min
        bin_width = line_length / self.n_bins
        self.bins = [
            Bin(
                start=(self.x_min + line_length * i / self.n_bins),
                width=bin_width,
                height=EPSILON,
            )
            for i in range(self.n_bins)
        ]
        for i, bin in enumerate(self.bins):
            bin.move_to(
                self.number_line.number_to_point(bin.start) + 0.5 * bin_width * RIGHT
            )

    def accept(self, x: float):
        line_length = self.x_max - self.x_min
        bin_index = floor(self.n_bins * x / line_length)
        # in case x is at the extreme right end!
        bin_index = min(bin_index, self.n_bins - 1)
        self.bins[bin_index].grow(0.25)
        self.rescale(2.0)

    def rescale(self, max_height_screen: float):
        assert self.bins
        max_bin_height = max(b.height for b in self.bins)
        if max_bin_height <= max_height_screen:
            return
        scale_fac = max_height_screen / max_bin_height
        for b in self.bins:
            b.stretch_to_fit_height(b.height * scale_fac, about_point=b.get_bottom())
