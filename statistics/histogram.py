import random
from math import cos, sin

import manim as m
from manim import *

m = m


class Histogram(Scene):
    def construct(self):
        rtg = Circle()
        rtg.move_to(ORIGIN + DOWN * 2)
        rtg_center = rtg.get_center()

        number_line = m.NumberLine((1, 10, 1), 8)

        self.add(rtg, number_line)

        things = [Text(str(i), font_size=72) for i in range(1, 10 + 1)]

        for _ in range(10):
            [t] = random.sample(things, 1)
            self.add(t)
            t.move_to(rtg_center)
            target_point = number_line.number_to_point(int(t.text))
            anim = ApplyMethod(t.move_to, target_point)
            self.play(anim)
            self.wait()
