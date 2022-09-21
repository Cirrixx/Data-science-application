from turtle import Turtle

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0 
        self.r_score = 0
        #left hand side
        self.goto(-100, 200)
        self.write(self.l_score, align = "center", font = ("Arial", 80, "normal"))

        #right hand side
        self.goto(100, 200)
        self.write(self.r_score, align = "center", font = ("Arial", 80, "normal"))


    def l_score_update(self):
        self.l_score +=1
        self.update_score()

    def r_score_update(self):
        self.r_score +=1
        self.update_score()
    
    def update_score(self):
        self.clear()
        
        #left hand side
        self.goto(-100, 200)
        self.write(self.l_score, align = "center", font = ("Arial", 80, "normal"))

        #right hand side
        self.goto(100, 200)
        self.write(self.r_score, align = "center", font = ("Arial", 80, "normal"))
