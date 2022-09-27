
import time
import random
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P8)
display.set_backlight(1.0)

WIDTH, HEIGHT = display.get_bounds()

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

#points, or "lives"
points = 0

#colors for the screen. "BG" is the black background, while "pen" is
#what objects will be drawn with (white)
BG = display.create_pen(0,0,0)
pen = display.create_pen(255,255,255)


#object paddle, will be used multiple times
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 30
        self.thickness = 3

#object ball
class Ball:
    def __init__(self, x, y, r, dx, dy):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        

#generates ball in the center with radius 10 and set starting speed
ball = Ball(67,120,5,1,1)

#GUI balls to indicate lives
lifeBall = Ball(10, 10, 1, 0, 0)

#declare both left and right paddels being 10 pixels away from the border
leftPaddle = Paddle(WIDTH/2, HEIGHT - 10)
rightPaddle = Paddle(WIDTH/2, 10)

#sets the borders for the ball
xmin = ball.r
xmax = WIDTH - ball.r
ymin = ball.r
ymax = HEIGHT - ball.r



#################################################################
#code from here on is the actual game running
while points <= 3:
    #generates a black background
    display.set_pen(BG)
    display.clear()
    #print("checkpoint 1")
    ###This code checks if the ball is touching a paddle (if so it bounces)
    
    #left paddle
    #long way to say "if the ball is touching the paddle"
    if ((ball.y >= leftPaddle.y) and (ball.x > ((leftPaddle.x - leftPaddle.length)) and (ball.x < (leftPaddle.x + leftPaddle.length)))):
        ball.dy *= -1.2
    
    #right paddle
    if ((ball.y <= rightPaddle.y) and (ball.x > ((rightPaddle.x - rightPaddle.length)) and (ball.x < (rightPaddle.x + rightPaddle.length)))):
        ball.dy *= -1.2
    ###
    #print("checkpoint 2")
    ###This code is responsible for moving the paddles
    #left paddle
    if button_x.raw():
        if not((leftPaddle.x + leftPaddle.length) >135):
            leftPaddle.x += 2
            print(leftPaddle.x)
    if button_y.raw():
        if not((leftPaddle.x - (leftPaddle.length/2)) < -10):
            leftPaddle.x -= 2
            print(leftPaddle.x)
    
    #right paddle
    if button_a.raw():
        if not((rightPaddle.x + rightPaddle.length) >135):
            rightPaddle.x += 2
    if button_b.raw():
        if not(rightPaddle.x -(rightPaddle.length/2) <0):
            rightPaddle.x -= 2
    
        
    ###
    #print("checkpoint 3")
    
    
    #the ball bounces if it hits a border
    if ball.x < xmin or ball.x > xmax:
            ball.dx *= -1

    #if it hits the border past the paddles, it resets the ball
    if ball.y < ymin or ball.y > ymax:
            ball.x = WIDTH/2
            ball.y = HEIGHT/2
            ball.dx = random.randint(-3,3)
            ball.dy = 1
            points += 1
    #print("checkpoint 4")
    #updates balls velocity
    ball.x += ball.dx
    ball.y += ball.dy
    display.set_pen(pen)
    
    #print("checkpoint 5")
    #draws ball
    display.circle(int(ball.x),int(ball.y),int(ball.r))
    
    #draws left paddle
    display.rectangle(int(leftPaddle.x), int(leftPaddle.y),int(leftPaddle.length),int(leftPaddle.thickness))
    
    #draws right paddle
    display.rectangle(int(rightPaddle.x), int(rightPaddle.y),int(rightPaddle.length),int(rightPaddle.thickness))
    
    #print("checkpoint 6")
    
    #prints the amount of lives you have left
    for x in range(3 - points):
        display.circle(lifeBall.x, (lifeBall.y + (10 * x)), lifeBall.r)
    
    #updates screen with new information and sleeps for 1 millisecond
    display.update()
    time.sleep(0.001)
    
#displays game over screen
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate = 0)
display.set_pen(BG)
display.clear()
display.set_pen(pen)
display.set_font("bitmap8")
display.text("Game Over.", int(WIDTH/2), int(HEIGHT/4),scale=3)
display.update()
    