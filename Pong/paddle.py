#code for paddle 

from turtle import Turtle


class Paddle(Turtle):
    "creates a paddle"
    
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.shapesize(stretch_wid = 5, stretch_len= 1)
        self.color("white")
        self.penup()
        self.goto(position)
    

    def go_up(self):
        self.goto(self.xcor(), self.ycor()+40)

    def go_down(self):
        self.goto(self.xcor(), self.ycor()-40)