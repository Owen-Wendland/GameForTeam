import math
import pickle
import subprocess
import pygame
import pymunk
import json
import random
import time
import os
import sys

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants

def main():
    pygame.init()
   
    BACKGROUND = (250, 150, 150) #making the background color
   
    world = pymunk.Space()
    world.gravity = (0, 1000) #sets gravity
    world.damping = .4 #how much resistance/friction there is in the world
   
    #gets the screensize
    screenSize = constants.screenSize
    print(screenSize)
   
    left = False
    right = False
    up = False
    down = False
    vel = 300
    global RUNNING 
    RUNNING = True
    
    #sounds
    walking = pygame.mixer.Sound(cwd + '\\walking.mp3')
   
    timeTakeForNewQuestion = 2
    chosen = ''
    correct = False
    numcorrect = 0
   
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
   
    pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
   
    class variables():
        def __init__(self):
            self.currAnswers = []
    var = variables()
    class Player():
        def __init__(self, startx, starty, width, height):
            self.qnum = 1
            self.qnum2 = random.randint(1,qAmount-5)
            self.dir = 'right'
            self.width = width
            self.height = height
            self.ball_body = pymunk.Body(1, pymunk.moment_for_box(1,(self.width, self.height)))
            self.ball_body.position = (startx, starty)
            self.ball_shape = pymunk.Poly.create_box(self.ball_body, (self.width,self.height))
            self.ball_shape.elasticity = .5
            self.ball_shape.friction = 0
            self.ball_shape.density = 1
            self.ball_shape.collision_type = 1
            world.add(self.ball_body, self.ball_shape)
            #self.image = pygame.image.load(cwd + "/large.png")
            self.spritesRight = []
            self.currentSprite = 0
            for i in os.listdir(cwd+'\\robotSprites'):
                image = pygame.image.load(cwd + "\\robotSprites\\" + i)#ugrughrughgrurhgu
                self.imageRect = image.get_rect(center = self.ball_body.position)
                self.spritesRight.append(pygame.transform.scale(image, (self.width,self.height)))
            self.spritesLeft = []
            for i in range(len(self.spritesRight)):
                self.spritesLeft.append(pygame.transform.flip(self.spritesRight[i], 180, 0))
            self.image = self.spritesRight[0]
            self.action = 'standing'
            
        def draw(self):
            self.vertices = self.ball_shape.get_vertices()
            for v in self.ball_shape.get_vertices():
                x = v.rotated(self.ball_shape.body.angle)[0] + self.ball_shape.body.position[0]
                y = v.rotated(self.ball_shape.body.angle)[1] + self.ball_shape.body.position[1]
                self.vertices.append((x, y))

            self.angle_degrees = math.degrees(self.ball_body.angle)
            #self.rect = pygame.transform.rotate(self.rect, -self.angle_degrees)
            self.rotatedimage = pygame.transform.rotate(self.image, -self.angle_degrees)
            if (self.action == 'walking' or self.action == 'standing'):
                self.imageRect = self.rotatedimage.get_rect(center = (self.ball_body.position.x,self.ball_body.position.y+screenSize[1]//60))
            if (self.action == 'running'):
                self.imageRect = self.rotatedimage.get_rect(center = (self.ball_body.position.x,self.ball_body.position.y+screenSize[1]//45))
            #pygame.draw.polygon(screen, (0,0,0), self.vertices)
            #pygame.draw.circle(screen, (255,255,255), (int(self.ball_body.position.x), int(self.ball_body.position.y)), self.ballRadius)
           
            screen.blit(self.rotatedimage, self.imageRect)        
        def update(self,action):
            self.action = action
            self.currentSprite += 1/10
            self.currentSpriteInt = int(self.currentSprite)
            if(self.dir == 'right'):
                self.images = self.spritesLeft
            else:
                self.images = self.spritesRight
                
            if (self.action == 'standing'):
                self.currentSprite = 0
                self.image = self.images[self.currentSpriteInt]
            if (self.action == 'walking'):
                if self.currentSprite < 0 or self.currentSprite > 2:
                    self.currentSprite = 0
                self.image = self.images[self.currentSpriteInt]
            if (self.action == 'running'):
                if self.currentSprite < 0 or self.currentSprite > 2:
                    self.currentSprite = 0
                self.image = self.images[self.currentSpriteInt]
            
   
    class Line():
        def __init__(self, firstpoint, secondpoint, ela, fric):
            self.point1, self.point2 = firstpoint, secondpoint
            self.width = screenSize[0]//screenSize[1]*13 #Width of lines
           
            self.lineBody = pymunk.Body(body_type=pymunk.Body.STATIC) #anchoring the floor
            self.lineShape = pymunk.Segment(self.lineBody, (self.point1), (self.point2), self.width) #connecting the two points to form floor line
            self.lineShape.elasticity = ela #what percent of energy goes into bounce
            self.lineShape.friction = fric # idk lol
            world.add(self.lineShape, self.lineBody) #creating the land like god did on the third day  
        def draw(self):
            pygame.draw.line(screen, (0,0,0), (self.point1), (self.point2), self.width//2)
   
    #class for writing text
    class text():
        def __init__(self, textFont, textWritten, x, y, size):
            self.x = x
            self.y = y
            self.textFont = textFont
            self.font = pygame.font.Font(textFont, size)
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, (0,0,0))
            self.currAnswer = js['answer' + str(player.qnum2)]
           
            self.location = self.text.get_rect(center = (self.x, self.y))
           
        def reWrite(self, textWritten):
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, (0,0,0),)
            self.location = self.text.get_rect(center = (self.x, self.y))
           
        def draw(self):
            screen.blit(self.text, self.location)
    #make the player (starting x, starting, size, mass)
    #player = Player(screenSize[0]/2, screenSize[1]/4, abs((screenSize[0] - screenSize[1])/9), 1)
    player = Player(screenSize[0]/2, screenSize[1]/4, screenSize[0]//16,screenSize[0]//16)      
    currQuestion = js['question' + str(player.qnum2)]
    var.currAnswers = list(js['answers' + str(player.qnum2)]) #setting the list of answers from the json file
   
    random.shuffle(var.currAnswers) #shuffles the position of the answers
   
    #displaying the question answers on the colored zones
    b = screenSize[0]/1225.806451613
    y = (800/len(var.currAnswers[0]))//b
    text1 = text('Go-Mono.ttf', var.currAnswers[0], screenSize[0]/8, screenSize[1]*5/6, int(y))
    y = (800/len(var.currAnswers[1]))//b
    text2 = text('Go-Mono.ttf', var.currAnswers[1], screenSize[0]*3/8, screenSize[1]*5/6, int(y))
    y = (800/len(var.currAnswers[2]))//b
    text3 = text('Go-Mono.ttf', var.currAnswers[2], screenSize[0]*5/8, screenSize[1]*5/6, int(y))
    y = (800/len(var.currAnswers[3]))//b
    text4 = text('Go-Mono.ttf', var.currAnswers[3], screenSize[0]*7/8, screenSize[1]*5/6, int(y))
    question = text('Go-Mono.ttf', currQuestion, screenSize[0]/2, screenSize[1]/8, screenSize[0]//32)
            
    #making floor
    floor = Line((0,screenSize[1]),(screenSize[0],screenSize[1]), 1, 5)
    wall1 = Line((0,-150),(0,screenSize[1]), 0, 0)
    wall2 = Line((screenSize[0],-150),(screenSize[0],screenSize[1]), 0, 0)
    roof = Line((0,0),(screenSize[0],0), 1, 0)
   
    #making line structure
    linelist = []
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
        global currQuestion
        player.qnum += 1
        player.qnum2 += 1
        if player.qnum <= 5:
            var.currAnswers = js['answers' + str(player.qnum2)]
            random.shuffle(var.currAnswers)
            currQuestion = js['question' + str(player.qnum2)]
            
            player.ball_body.angle = 0
            player.ball_body.velocity = pymunk.Vec2d(0,0)
            player.ball_body.position = (screenSize[0]/2,screenSize[1]/4)
            
            text1.reWrite(var.currAnswers[0])
            text2.reWrite(var.currAnswers[1])
            text3.reWrite(var.currAnswers[2])
            text4.reWrite(var.currAnswers[3])
            
            print(len(str(var.currAnswers[0])))
            print(len(str(var.currAnswers[1])))
            print(len(str(var.currAnswers[2])))
            print(len(str(var.currAnswers[3])))
            b = screenSize[0]/1225.806451613
            y = (800/len(var.currAnswers[0]))//b
            text1.font = pygame.font.Font(text1.textFont, int(y))
            y = (800/len(var.currAnswers[1]))//b
            text2.font = pygame.font.Font(text2.textFont, int(y))
            y = (800/len(var.currAnswers[2]))//b
            text3.font = pygame.font.Font(text3.textFont, int(y))
            y = (800/len(var.currAnswers[3]))//b
            text4.font = pygame.font.Font(text4.textFont, int(y))
            
            text1.reWrite(var.currAnswers[0])
            text2.reWrite(var.currAnswers[1])
            text3.reWrite(var.currAnswers[2])
            text4.reWrite(var.currAnswers[3])
            
            question.reWrite(currQuestion)
            question.currAnswer = js['answer' + str(player.qnum2)]
           
        #return(qNum + 1)
        #display question (code should go here)
    first = True
    rotate = False
    num = 0
    term = 60
    while RUNNING:
       
        timeSecond = pygame.time.get_ticks()//1000
        if player.qnum == 6:
            screen.fill(BACKGROUND) # creating the sky like god did on the second day
            background()
            
            #creating the player, edges around screen, aswell as the question and answers
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
            
            #draw/create the line structure for the player to move on
            for i in range(len(linelist)):
                linelist[i].draw()
                
            events = pygame.event.get()
            txtx1 = 'score : '
            txtx2 = str(round(numcorrect * 450 // timeSecond))
            question.reWrite(txtx1 + txtx2)
            pygame.display.update()
            world.step(1/120.0)
            clock.tick(60)
            with open(cwd + "\\dat\\currentPerson.pkl", 'rb') as f:
                x = pickle.load(f)
            x['points'] = x['points'] + round(numcorrect * 100 // timeSecond)
            print(x['points'])
            
            with open(cwd + "\\dat\\currentPerson.pkl", "wb") as f:
                f.truncate(0)
                pickle.dump(x, f)
            with open(cwd + "\\dat\\currentPerson.pkl", 'rb') as f:
                x = pickle.load(f)
            print(x)
            RUNNING = False
        screen.fill(BACKGROUND) # creating the sky like god did on the second day
        background()
       
        #creating the player, edges around screen, aswell as the question and answers
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
       
        #draw/create the line structure for the player to move on
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
            question.reWrite("Correct! you have " + str(numcorrect) + " correct --Seconds:" + str(timeSecond) + '--')
            first = False
            chosen = '1'
           
        elif(not(first) and time.time() - firstTime > timeTakeForNewQuestion):
           # numcorrect += 1
            question.reWrite("Correct! you have " + str(numcorrect) + " correct --Seconds:" + str(timeSecond) + '--')
            first = True
            reset()
            chosen = ''
       
        if chosen != question.currAnswer and first and chosen != '': # if the chosen answer is correct then print that they are correct
            firstTime = time.time()
            question.reWrite("Wrong! you have " + str(numcorrect) + " correct --Seconds:" + str(timeSecond) + '--')
            first = False
            chosen = '1'
           
        elif(not(first) and time.time() - firstTime > timeTakeForNewQuestion and chosen != question.currAnswer):
            question.reWrite("Wrong! you have " + str(numcorrect) + " correct --Seconds:" + str(timeSecond) + '--')
            first = True
            reset()
            chosen = ''
           
        for event in events:
            if event.type == pygame.KEYDOWN: # if there is a key pressed down then check for which key(s) is pressed down
                if event.key == pygame.K_ESCAPE: #if you press the escape key the game game closes
                    RUNNING = False
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a): #if you press left arrow then you go.... left
                    left = True
                    walking.play(loops=-1)
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d): #if you press right arrow then you go..... right
                    right = True
                    walking.play(loops=-1)
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w): #if you press uparrow it sets up boolean  to true
                    up = True
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    down = True
                    if(player.angle_degrees > 89 or player.angle_degrees < -89):
                        rotate = True
                        num = 0
                if (event.key == pygame.K_LSHIFT) or (event.key == pygame.K_RSHIFT):
                    vel = 300
                    term = 40
            if event.type == pygame.KEYUP: #if there is a key up then see which key(s) are up and respond
                if (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    left = False
                    walking.stop()
                if (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    right = False
                    walking.stop()
                if (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    down = False
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    up = False
                    first1 = player.ball_body.velocity
                    first1 = list(first1)
                    if(first1[1] > -2 and first1[1] < 2):
                        first1 = pymunk.Vec2d(first1[0], -500)
                        player.ball_body.velocity = first1
                if event.key == pygame.K_LSHIFT:
                    vel = 300
                    term = 60
        #if(player.ball_shape.collision_type = )
        #print(int(player.angle_degrees))
        if right:
            xr = player.ball_body.velocity
            xr = list(xr)
            xr = pymunk.Vec2d(vel, xr[1])
            player.ball_body.velocity = xr
            player.dir = 'right'
            if(vel == 200):
                player.update('running')
            else:
                player.update('walking')
        elif left:
            xl = player.ball_body.velocity
            xl = list(xl)
            xl = pymunk.Vec2d(-vel, xl[1])
            player.ball_body.velocity = xl
            player.dir = 'left'
            if(vel == 200):
                player.update('running')
            else:
                player.update('walking')
        else:
            player.update('standing')
            
        if(player.angle_degrees != 0):
            player.ball_body.angle = 0
         
        
        if(player.angle_degrees > 360 or player.angle_degrees < -360):
            player.ball_body.angle = 0
        #print(player.angle_degrees)
        '''
        if(rotate):
            print(num)
            if num == 0:
                first1 = player.ball_body.velocity
                first1 = list(first1)
                first1 = pymunk.Vec2d(first1[0], -500)
                player.ball_body.velocity = first1
            if (num % 1 == 0):
                player.ball_body.angle += math.pi/60
                print('wfwakwafwaffwa')
            num += 1
            if(player.angle_degrees > -10 and player.angle_degrees < 10):
                rotate = False
                num = 0'''
        pygame.display.update()
       
        world.step(1/term)
        clock.tick(60)
    time.sleep(2)
    

if __name__ == "__main__":
    main()
subprocess.run(["python", cwd + "\\src\\sort10.py"])
pygame.quit()