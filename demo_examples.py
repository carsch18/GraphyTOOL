#!/usr/bin/env python3
"""
Demo Examples for GraphyBOOK
Sample Manim animations to showcase the system capabilities
"""

from manim import *

class BouncingBallDemo(Scene):
    """Simple bouncing ball animation"""
    def construct(self):
        # Create a ball
        ball = Circle(radius=0.3, color=RED, fill_opacity=1)
        ball.move_to(UP * 2)
        
        # Create ground
        ground = Line(LEFT * 4, RIGHT * 4, color=WHITE)
        ground.move_to(DOWN * 2)
        
        # Add objects to scene
        self.add(ground)
        self.play(Create(ball))
        
        # Bouncing animation
        for _ in range(3):
            self.play(ball.animate.move_to(DOWN * 1.7), rate_func=rate_functions.ease_in_quad, run_time=0.5)
            self.play(ball.animate.move_to(UP * 2), rate_func=rate_functions.ease_out_quad, run_time=0.8)
        
        self.wait(1)

class PendulumDemo(Scene):
    """Simple pendulum motion"""
    def construct(self):
        # Pivot point
        pivot = Dot(ORIGIN + UP * 2, color=WHITE)
        
        # Pendulum bob
        bob = Circle(radius=0.2, color=BLUE, fill_opacity=1)
        bob.move_to(DOWN * 1.5 + RIGHT * 1)
        
        # String
        string = Line(pivot.get_center(), bob.get_center(), color=WHITE)
        
        # Add to scene
        self.add(pivot, string, bob)
        
        # Pendulum motion
        def update_string(mob):
            mob.put_start_and_end_on(pivot.get_center(), bob.get_center())
        
        string.add_updater(update_string)
        
        # Swing motion
        self.play(
            Rotate(bob, angle=-PI/3, about_point=pivot.get_center()),
            run_time=1
        )
        self.play(
            Rotate(bob, angle=2*PI/3, about_point=pivot.get_center()),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.play(
            Rotate(bob, angle=-PI/3, about_point=pivot.get_center()),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        self.wait(1)

class WaveDemo(Scene):
    """Simple wave animation"""
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4
        )
        
        # Wave function
        def wave_func(x):
            return np.sin(x)
        
        # Create wave
        wave = axes.plot(wave_func, color=BLUE)
        
        # Add to scene
        self.play(Create(axes))
        self.play(Create(wave))
        
        # Animate wave
        for phase in np.linspace(0, 2*PI, 60):
            new_wave = axes.plot(lambda x: np.sin(x + phase), color=BLUE)
            self.remove(wave)
            self.add(new_wave)
            wave = new_wave
            self.wait(0.1)
        
        self.wait(1)