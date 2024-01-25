import math
import pygame
import pymunk
import tkinter
import json
import random
import time
from functools import lru_cache
import os
cwd = os.getcwd()
print(cwd)



def main():
    pygame.init()
    
    BACKGROUND = (150, 150, 150) #making the background color
    
    world = pymunk.Space()
    world.gravity = (0, 1000) #sets gravity 
    world.damping = .4 #how much resistance/friction there is in the world
    
    #gets the screensize 
    tk = tkinter.Tk()
    screenSize = (tk.winfo_screenwidth(), tk.winfo_screenheight())
    print(screenSize)
    
    left = False
    right = False
    up = False
    down = False
    vel = 20000
    RUNNING = True
    
    timeTakeForNewQuestion = 3
    chosen = ''
    correct = False
    numcorrect = 0
    
    pygame.mixer.music.load(cwd + '/song.mp3')
    pygame.mixer.music.play(-1)
    
    global qNum
    qNum = 1
    currQuestion = ''
    currAnswers = [] #answers for each question based on it's position in the list
    currAnswer = ''
    screen = pygame.display.set_mode((screenSize[0]*2, screenSize[1]*2))
    clock = pygame.time.Clock()

    with open(cwd + '/dat/questions.json') as f: 
        data = f.read() 
    # reconstructing the data as a dictionary 
    js = json.loads(data) 
    qAmount = js['questionAmount']
   
    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
   
    class Player():
        def __init__(self, startx, starty, radius, mass):
            self.ballRadius = radius
            self.ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.ballRadius))
            self.ball_body.position = (startx, starty)
            self.ball_shape = pymunk.Circle(self.ball_body, self.ballRadius)
            self.ball_shape.elasticity = .5
            self.ball_shape.friction = 3
            self.ball_shape.density = mass
            self.ball_shape.collision_type = 1
            world.add(self.ball_body, self.ball_shape)
            self.image = pygame.image.load(cwd + "/digitalminds.png")
            self.image = pygame.transform.scale(self.image, (self.ballRadius * 2,self.ballRadius * 2))
            self.imageRect = self.image.get_rect(center = self.ball_body.position)
        def draw(self):
            self.angle_degrees = math.degrees(self.ball_body.angle)
            self.rotatedimage = pygame.transform.rotate(self.image, -self.angle_degrees)
            self.imageRect = self.rotatedimage.get_rect(center = self.ball_body.position)
            pygame.draw.circle(screen, (0,0,0), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius + 2)
            pygame.draw.circle(screen, (255,255,255), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius)
            
            screen.blit(self.rotatedimage, self.imageRect)        
    
    class Line():
        def __init__(self, firstpoint, secondpoint, ela, fric):
            self.point1, self.point2 = firstpoint, secondpoint
            self.width = 20 #Width of lines
            
            self.lineBody = pymunk.Body(body_type=pymunk.Body.STATIC) #anchoring the floor
            self.lineShape = pymunk.Segment(self.lineBody, (self.point1), (self.point2), self.width) #connecting the two points to form floor line 
            self.lineShape.elasticity = ela #what percent of energy goes into bounce
            self.lineShape.friction = fric # idk lol
            world.add(self.lineShape, self.lineBody) #creating the land like god did on the third day   
        def draw(self):
            pygame.draw.line(screen, (0,0,0), (self.point1), (self.point2), self.width)
    
    class text():
        def __init__(self, textFont, textWritten, x, y, size):
            self.x = x
            self.y = y
            self.font = pygame.font.Font(textFont, size)
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, (0,0,0))
            self.currAnswer = js['answer' + str(qNum)]
            
            self.location = self.text.get_rect(center = (self.x, self.y))
            
        def reWrite(self, textWritten):
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, (0,0,0),)
            self.location = self.text.get_rect(center = (self.x, self.y))
            
        def draw(self):
            screen.blit(self.text, self.location)
            
    currQuestion = js['question' + str(qNum)]
    currAnswers = list(js['answers' + str(qNum)]) #setting the list of answers from the json file
    
    random.shuffle(currAnswers) #shuffles the position of the answers
    
    #displaying the question answers on the colored zones
    
    text1 = text('freesansbold.ttf', currAnswers[0], screenSize[0]/8, screenSize[1]/1.222222, 32)
    text2 = text('freesansbold.ttf', currAnswers[1], screenSize[0]*3/8, screenSize[1]/1.222222, 32)
    text3 = text('freesansbold.ttf', currAnswers[2], screenSize[0]*5/8, screenSize[1]/1.222222, 32)
    text4 = text('freesansbold.ttf', currAnswers[3], screenSize[0]*7/8, screenSize[1]/1.222222, 32)
    question = text('freesansbold.ttf', currQuestion, screenSize[0]/2, screenSize[1]/8, 64)
    
    player = Player(screenSize[0]/2, screenSize[1]/4, 60, 1)

    #making floor
    floor = Line((0,screenSize[1]),(screenSize[0],screenSize[1]), 1, 5)
    wall1 = Line((0,-150),(0,screenSize[1]), 0, 0)
    wall2 = Line((screenSize[0],-150),(screenSize[0],screenSize[1]), 0, 0)
    roof = Line((0,0),(screenSize[0],0), 1, 0)
    
    #making line structure
    linelist = []
    print(screenSize[1])
    linelist.extend([
        Line((0, (3 * (screenSize[1] / 9))), ((2 * (screenSize[0] / 16)), (3 * (screenSize[1] / 9))), 1, 5),
        Line(((6 * (screenSize[0] / 16)), (3 * (screenSize[1] / 9))), ((10 * (screenSize[0] / 16)), (3 * (screenSize[1] / 9))), 1, 5),
        Line(((14 * (screenSize[0] / 16)), (3 * (screenSize[1] / 9))), ((16 * (screenSize[0] / 16)), (3 * (screenSize[1] / 9))), 1, 5),
        Line(((2 * (screenSize[0] / 16)), (6 * (screenSize[1] / 9))), ((6 * (screenSize[0] / 16)), (6 * (screenSize[1] / 9))), 1, 5),
        Line(((10 * (screenSize[0] / 16)), (6 * (screenSize[1] / 9))), ((14 * (screenSize[0] / 16)), (6 * (screenSize[1] / 9))), 1, 5),
        Line(((4 * (screenSize[0] / 16)), (6 * (screenSize[1] / 9))), ((4 * (screenSize[0] / 16)), (9 * (screenSize[1] / 9))), 0, 0),
        Line(((8 * (screenSize[0] / 16)), (3 * (screenSize[1] / 9))), ((8 * (screenSize[0] / 16)), (9 * (screenSize[1] / 9))), 0, 0),
        Line(((12 * (screenSize[0] / 16)), (6 * (screenSize[1] / 9))), ((12 * (screenSize[0] / 16)), (9 * (screenSize[1] / 9))), 0, 0)
    ])
    players = [] #creating the players list, just like how god created humans on the sixth day
    
    def background():
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(0,6 * (screenSize[1] / 9),screenSize[0]/4,screenSize[1]/3))
        pygame.draw.rect(screen, (0,125,255), pygame.Rect(screenSize[0]/4,6 * (screenSize[1] / 9),screenSize[0]/4,screenSize[1]/3))
        pygame.draw.rect(screen, (255,255,0), pygame.Rect(screenSize[0]/2,6 * (screenSize[1] / 9),screenSize[0]/4,screenSize[1]/3))
        pygame.draw.rect(screen, (0,255,0), pygame.Rect(screenSize[0]*3/4,6 * (screenSize[1] / 9),screenSize[0]/4,screenSize[1]/3))
    
    def reset():
        global qNum, currQuestion
        qNum += 1
        if qNum <= qAmount:
            currAnswers = js['answers' + str(qNum)]
            currQuestion = js['question' + str(qNum)]
            
            player.ball_body.position = (screenSize[0]/2,screenSize[1]/4)
            text1.reWrite(currAnswers[0])
            text2.reWrite(currAnswers[1])
            text3.reWrite(currAnswers[2])
            text4.reWrite(currAnswers[3])
            question.reWrite(currQuestion)
            question.currAnswer = js['answer' + str(qNum)]
            
        return(qNum + 1)
        #display question (code should go here)
    first = True
    while RUNNING:
        
        screen.fill(BACKGROUND) # creating the sky like god did on the second day
        background()
        
        player.draw()
        floor.draw()
        wall1.draw()
        wall2.draw()
        roof.draw()
        text1.draw()
        text2.draw()
        text3.draw()
        text4.draw()
        question.draw()
        
        for i in range(len(linelist)):
            linelist[i].draw()
        #for i in range(len(players)):
         #   players[i].draw()
        events = pygame.event.get()
        
        #detecting which colored zone the player is in
        px, py = player.ball_body.position.x, player.ball_body.position.y
        #when in first zone set your chosen answer to the text displayed in the first zone
        if(px > 0 and px < screenSize[0]/4 and py > screenSize[1]*2/3): 
            chosen = text1.textWritten
            
        #when in second zone set your chosen answer to the text displayed in the second zone
        elif(px > screenSize[0]/4 and px < screenSize[0]*2/4 and py > screenSize[1]*2/3):
            chosen = text2.textWritten
            
        #when in third zone set your chosen answer to the text displayed in the thirs zone
        elif(px > screenSize[0]*2/4 and px < screenSize[0]*3/4 and py > screenSize[1]*2/3):
            chosen = text3.textWritten
            
        #when in fourth zone set your chosen answer to the text displayed in the fourth zone
        elif(px > screenSize[0]*3/4 and px < screenSize[0] and py > screenSize[1]*2/3):
            chosen = text4.textWritten
        
        #if correct    
        if chosen == question.currAnswer and first: # if the chosen answer is correct then print that they are correct
            numcorrect += 1
            firstTime = time.time()
            question.reWrite("Correct! you have " + str(numcorrect) + " correct")
            first = False
            chosen = '1'
            
        elif(not(first) and time.time() - firstTime > timeTakeForNewQuestion):
           # numcorrect += 1
            question.reWrite("Correct! you have " + str(numcorrect) + " correct")
            first = True
            reset()
            chosen = ''
        
        if chosen != question.currAnswer and first and chosen != '': # if the chosen answer is correct then print that they are correct
            firstTime = time.time()
            question.reWrite("Wrong! you have " + str(numcorrect) + " correct")
            first = False
            chosen = '1'
            
        elif(not(first) and time.time() - firstTime > timeTakeForNewQuestion and chosen != question.currAnswer):
            question.reWrite("Wrong! you have " + str(numcorrect) + " correct")
            first = True
            reset()
            chosen = ''
            
        for event in events:
            if event.type == pygame.KEYDOWN: # if there is a key pressed down then check for which key(s) is pressed down 
                if event.key == pygame.K_ESCAPE: #if you press the escape key the game game closes
                    RUNNING = False
                if event.key == pygame.K_LEFT: #if you press left arrow then you go.... left
                    left = True
                if event.key == pygame.K_RIGHT: #if you press right arrow then you go..... right
                    right = True
                if event.key == pygame.K_UP: #if you press uparrow it sets up boolean  to true
                    up = True
                if event.key == pygame.K_DOWN:
                    down = True
                if event.key == pygame.K_LSHIFT:
                    vel = 100000
            if event.type == pygame.KEYUP: #if there is a key up then see which key(s) are up and respond
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_DOWN:
                    down = False
                    reset()
                    '''for i in range(500):
                        fart = Player(600,100, 10, .01)
                        players.append(fart)
                    print(len(players))'''
                if event.key == pygame.K_UP:
                    up = False
                    first1 = player.ball_body.velocity
                    first1 = list(first1)
                    if(first1[1] > -2 and first1[1] < 2):
                        first1 = pymunk.Vec2d(first1[0], -500)
                        player.ball_body.velocity = first1
                if event.key == pygame.K_LSHIFT:
                    vel = 20000
        #if(player.ball_shape.collision_type = )
        
        if right:
            player.ball_body.apply_impulse_at_world_point((vel, 0), (10,0))
        if left:
            player.ball_body.apply_impulse_at_world_point((-vel,0), (-10,0))
           
        velocity = (list(player.ball_body.velocity)[0] + list(player.ball_body.velocity)[1]) / 2000
         
        if(velocity <= -0.1):
            pygame.mixer.music.set_volume(velocity * -1)
        elif(velocity >= 0.1):
            pygame.mixer.music.set_volume(velocity)
        elif(velocity <= 0.1 and velocity >= -0.1):
            pygame.mixer.music.set_volume(0.1)
            
        pygame.display.update()
        
        world.step(1/120.0)
        clock.tick(120)

if __name__ == "__main__":
    main()

pygame.quit()
