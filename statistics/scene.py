import random
from math import cos, sin

import manim as m
from manim import *

m = m


class RandomThingGenerator(Scene):
    def construct(self):
        things = [Text(str(i), font_size=72) for i in range(1, 10 + 1)]

        circle = Circle()
        origin = circle.get_center()
        self.add(circle)

        for _ in range(10):
            [t] = random.sample(things, 1)
            theta = 2 * PI * random.random()
            direction = np.array((cos(theta), sin(theta), 0))
            target_position = origin + direction * 10
            self.add(t)
            t.move_to(origin)
            anim = ApplyMethod(t.move_to, target_position)
            self.play(anim)
            self.wait()
