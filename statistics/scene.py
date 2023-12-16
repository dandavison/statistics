import manim as m
from manim import *

m = m


class RandomThingGenerator(Scene):
    def construct(self):
        circle = Circle()

        number_7 = Text("7", font_size=72)
        number_7.move_to(circle.get_center())

        target_position = number_7.get_center() + RIGHT * 3

        anim = ApplyMethod(number_7.move_to, target_position)

        self.add(circle, number_7)
        self.play(anim)
