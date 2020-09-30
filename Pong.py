#!/usr/bin/env python
# coding: utf-8

# ## IMPORTING MODULES

# In[1]:


import random, os, pygame, math


# ## COLORS

# In[2]:


WHITE = (240, 240, 240)
BLACK = (51, 51, 51)
GREY = (100, 100, 100)
RED = (240, 20, 20)
GREEN = (20, 240, 20)
BLUE = (20, 20, 240)
YELLOW = (240, 240, 20)


# ## PONG CLASS

# In[3]:


class Pong:
    
    def __init__(self, width, height, radius):
        self.width = width
        self.height = height
        self.radius = radius
        self.velocity = 7
        self.color = WHITE
        
        self.reset()
        
    def move(self):
        self.x += self.xspeed
        self.y += self.yspeed
        
    def reset(self):
        self.angle = random.randrange(-45, 45)
        self.angle += random.choice([0, 180])
        self.xspeed = int(self.velocity * math.cos(self.angle * math.pi / 180))
        self.yspeed = int(self.velocity * math.sin(self.angle * math.pi / 180))
        
        if abs(self.xspeed) < 2:
            self.xspeed += random.choice([-3, 3])
        
        if abs(self.yspeed) < 2:
            self.yspeed += random.choice([-3, 3])
            
        self.x = self.width // 2
        self.y = self.height // 2
    
    
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        
    def get_xspeed(self):
        return self.xspeed
    
    def get_yspeed(self):
        return self.yspeed
    
    def get_speeds(self):
        return self.xspeed, self.yspeed
    
    def get_velocity(self):
        return self.velocity
    
    def set_velocity(self, velocity):
        self.velocity = velocity
        
        # This will update the speeds with new velocity
        self.set_angle(self.angle)
        
    
    def get_angle(self):
        # Returns in radian
        return math.atan2(self.yspeed, self.xspeed)
    
    def set_angle(self, angle):
        # Assumes the value in radians
        self.xspeed = int(self.velocity * math.cos(angle))
        self.yspeed = int(self.velocity * math.sin(angle))
        
    
    def set_xspeed(self, xspeed):
        self.xspeed = xspeed
        
    def set_yspeed(self, yspeed):
        self.yspeed = yspeed
        
    def inv_xspeed(self):
        self.xspeed *= -1
        
    def inv_yspeed(self):
        self.yspeed *= -1
        
    def get_pos(self):
        return self.x, self.y
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def is_left(self):
        return self.xspeed < 0
    


# ## PAD CLASS

# In[4]:


class Pad:
    
    def __init__(self, width, height, isLeft):
        
        self.isLeft = isLeft
        self.width = width
        self.height = height
        self.color = WHITE
        self.yoff = 10
        self.speed = 0
        
        self.widRect = 15
        self.hgtRect = 125
        
        if isLeft:
            self.x = 5
        else:
            self.x = (self.width - self.widRect - 5)
            
        self.y = (self.height - self.hgtRect) // 2
        
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.widRect, self.hgtRect))
    
    
    def move(self):
        y = self.y + self.speed
        
        if not ((y < 0) or (y + self.hgtRect > self.height)):
            self.y = y
            
        
    def move_up(self):
        self.speed = -1 * self.yoff
        
    def move_down(self):
        self.speed = self.yoff
        
    def stop(self):
        self.speed = 0
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_width(self):
        return self.widRect
    
    def is_leftpad(self):
        return self.isLeft
    
    def get_height(self):
        return self.hgtRect
        
    def get_rect(self):
        return self.x, self.y, self.widRect, self.hgtRect
    
    def is_left(self):
        return self.isLeft
    
        


# ## GAME CLASS

# In[5]:


class Game:
    
    FPS = 60
    
    def __init__(self):
        
        self.width = 800
        self.height = 600
        self.gameWidth = 700
        self.gameHeight = 500
        self.xoff = (self.width - self.gameWidth) // 2
        self.yoff = int(0.8 * (self.height - self.gameHeight))
        self.win = None
        self.gameWin = None
        self.font = None
        self.scoreFont = None
        self.clock = None
        self.pong = None
        self.leftPad = None
        self.rightPad = None
        self.leftScore = 0
        self.rightScore = 0
        self.radius = 15
        
        
    def game_init(self):
        
        self.pong = Pong(self.gameWidth, self.gameHeight, self.radius)
        self.leftPad = Pad(self.gameWidth, self.gameHeight, True)
        self.rightPad = Pad(self.gameWidth, self.gameHeight, False)
        
        pygame.init()
        pygame.font.init()
        
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pong Developer")
        self.gameWin = self.win.subsurface((self.xoff, self.yoff, self.gameWidth, self.gameHeight))
        
        self.win.fill(GREY)
        self.gameWin.fill(BLACK)
        
        self.font = pygame.font.SysFont("comicsansms", 40)
        self.scoreFont = pygame.font.SysFont("comicsans", 50)
        self.clock = pygame.time.Clock()
        
    def draw(self, win):
        
        self.win.fill(GREY)
        text = self.font.render("Pong Developer", 1, YELLOW)
        self.win.blit(text, ((self.width - text.get_width()) // 2, 
                             (self.yoff - text.get_height()) // 2))
        
        lScore = self.scoreFont.render(str(self.leftScore), 1, YELLOW)
        rScore = self.scoreFont.render(str(self.rightScore), 1, YELLOW)
        
        
        
        self.win.blit(lScore, (self.xoff, (self.yoff - lScore.get_height() + 20) // 2))
        self.win.blit(rScore, ((self.xoff + self.gameWidth - rScore.get_width()),
                          (self.yoff - lScore.get_height() + 20) // 2))
        
        self.gameWin.fill(BLACK)
        self.pong.draw(win)
        self.leftPad.draw(win)
        self.rightPad.draw(win)
        
        pygame.display.update()
        
    def check_bang(self, pad):
        x, y, w, h = pad.get_rect()
        pongX, pongY = self.pong.get_pos()
        isleft = self.pong.is_left() # pong is travelling to left
        
        if (pongY in range(y - self.radius, y + h + self.radius)): # Inside the Pad y-range
            
            if pad.is_left(): # This is the left Pad.
                if ((x + w) - (pongX - self.radius)) in range(0, 5)  and isleft:
#                     self.pong.inv_xspeed()
                    off = (pongY - y - h / 2) / (h / 2)
                    angle = off * (math.pi / 3)
                    self.pong.set_angle(angle)
                    
            else:
                if (pongX + self.radius - x) in range(0, 5) and not isleft:
                    off = (pongY - y - h / 2) / (h / 2)
                    angle = off * (-math.pi / 3) + math.pi
                    self.pong.set_angle(angle)
#                     self.pong.inv_xspeed()
                    
    def update_pong_angle(self, pad):
        x, y, w, h = pad.get_rect()
        pongX, pongY = self.pong.get_pos()
        
        if pad.is_left():
            off = (y + h / 2 - pongY) / (h / 2)
        
        
    def move(self):
        self.leftPad.move()
        self.rightPad.move()
        self.pong.move()
        
    def check_over(self):
        
        x, y = self.pong.get_pos()
        
        xspeed, yspeed = self.pong.get_xspeed(), self.pong.get_yspeed()
        
#         if (x + self.radius > self.gameWidth):
#             self.pong.inv_xspeed()
        
#         if (x - self.radius < 0):
#             self.pong.inv_xspeed()

        if (x + self.radius < 0):
            self.pong.reset()
            self.rightScore += 1
            
        if (x - self.radius > self.gameWidth):
            self.pong.reset()
            self.leftScore += 1
            
        if (y + self.radius > self.gameHeight):
            self.pong.inv_yspeed()
            
        if (y - self.radius < 0):
            self.pong.inv_yspeed()

        
    
    def run(self):
        
        self.game_init()
        
        
        pygame.display.update()
        
        run = True
        while run:
            
            self.clock.tick(self.FPS)
            self.draw(self.gameWin)
            self.move()
            self.check_over()
            self.check_bang(self.leftPad)
            self.check_bang(self.rightPad)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    run = False
                    
                    
                if event.type == pygame.KEYDOWN:    
                    keys = pygame.key.get_pressed()
                    
                    if keys[pygame.K_w] or keys[pygame.K_LEFT]:
                        self.leftPad.move_up()
                        
                    if keys[pygame.K_s] or keys[pygame.K_RIGHT]:
                        self.leftPad.move_down()
                        
                    if keys[pygame.K_UP]:
                        self.rightPad.move_up()
                        
                    if keys[pygame.K_DOWN]:
                        self.rightPad.move_down()
                
                if event.type == pygame.KEYUP:
                    self.leftPad.stop()
                    self.rightPad.stop()
                
                
                    
        pygame.font.quit()
        pygame.quit()

        
        
        


# In[6]:


X = Game()
X.run()


# In[108]:


pygame.font.quit()
pygame.quit()

