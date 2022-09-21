#creates the pong ball

from turtle import Turtle
import random
class Ball(Turtle):
    "pong ball"

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.current_heading = 65
        self.setheading(self.current_heading)
        self.current_speed = 10 #variable used to increase speed of ball as game progresses

    def move(self):
        self.forward(self.current_speed)

    def paddle_bounce(self):
        # if self.heading() in range(0,89):
        #     heading = 310
        # elif self.heading() in range(271,359):
        #     heading = 50
        # elif self.heading() in range(91,180):
        #     heading = 235
        # elif self.heading() in range(181,270):
        #     heading = 110
        # self.move(heading)

        self.current_heading += 180 + random.randint(1,15)
        self.current_heading %= 360
        self.setheading(self.current_heading)
        self.increase_speed()
        

    def wall_bounce(self):
        if self.heading() in range(0,89):
            heading = 310
        elif self.heading() in range(271,359):
            heading = 50
        elif self.heading() in range(91,180):
            heading = 235
        elif self.heading() in range(181,270):
            heading = 110
        self.setheading(heading)

    def increase_speed(self):
        "used to increase ball speed on paddle connection"
        self.current_speed += 1

    def reset_speed(self):
        self.current_speed = 5
        
       
       


        
        