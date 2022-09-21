#Pong
#Recreates the classic arcade game "pong"

from turtle import Screen
from paddle import Paddle
from ball import Ball
import random
from scoreboard import Scoreboard
import time
#setup screen
screen = Screen()
screen.setup(width = 800, height = 600)
screen.bgcolor("black")
screen.title("Pong: The Classic Arcade Game")
screen.tracer(0) #used to prevent turtle initial movement being visible

#create paddels 
r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350,0))

#create ball 
ball = Ball()

#screate scoreboard
scoreboard = Scoreboard()

#make paddle respond to keystrokes
screen.listen()
screen.onkeypress(r_paddle.go_up, "Up")
screen.onkeypress(r_paddle.go_down, "Down")
screen.onkeypress(l_paddle.go_up, "w")
screen.onkeypress(l_paddle.go_down, "s")



#main loop 
game_is_on = True


while game_is_on:
    time.sleep(1/60) #stops turtle speed randomly chaning 
    ball.move()
    screen.update()

    #check for collision with sides 
    if ball.ycor() > 290 or ball.ycor() < -290:
        ball.wall_bounce()

    #detect collision paddles 
    if ball.distance(r_paddle) < 50 and ball.xcor() > 320:
        ball.paddle_bounce() 
    elif ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.paddle_bounce() 


    #check if ball passes paddles 
    if ball.xcor() > 370: #checks if left player wins
        ball.goto(0,0)
        ball.current_heading = random.randint(170, 190)
        ball.setheading(ball.current_heading) 
        ball.reset_speed()
        scoreboard.l_scwore_update()
        
    elif ball.xcor() < -370:
        ball.goto(0,0)
        r_screen_heading = random.randint(340, 370)
        r_screen_heading %= 360 #done because its 360 degrees, with 90 being north
        ball.current_heading = r_screen_heading
        ball.setheading(ball.current_heading)
        ball.reset_speed()
        scoreboard.r_score_update()
        
        
        

screen.exitonclick() 
