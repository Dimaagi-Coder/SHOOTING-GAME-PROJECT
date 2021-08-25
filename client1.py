#importing packages
import pygame
import os

#importing netwrok file
from nework import Network

clientNum = 0

#initializing packages
pygame.init()

#setting screen dimension
screenWidth = 800
screenHeight = int(screenWidth * 0.8)
#displaying the main screen and setting caption
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Client 1")

#set framerate/display Hertz
clock = pygame.time.Clock()
FPS = 60

#game variables(physics)
GRAVITY = 0.75

#defining player actions
moving_left = False
moving_right = False

#defining game colours
BG = (144, 201, 120)
RED = (255, 0, 0)

#assigning colour and temporary figures
def draw_bg():
    screen.fill(BG)
    #drawing a temporary line
    pygame.draw.line(screen, RED, (0, 300), (screenWidth, 300))


#making a class playerEntity(Soldier) which defines actions and attributes related to the player
class playerEntity(pygame.sprite.Sprite):
    def __init__(self,char_type ,x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        #defining whether the player is alive or dead
        self.alive = True
        #defining whether the player is enemy or player
        self.char_type = char_type
        #assigning the speed to the player
        self.speed = speed
        #assigning direction
        self.direction = 1
        #jump variables to prevent double jump
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        #the side the player faces i.e. left or right
        self.flip = False
        #animating the main character
        
        #using list and for loops to determine the current state of the player
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #loading images for player animation
        animation_type = ['Idle', 'Run', 'Jump']
        for animation in animation_type:
            #resettig temp list of images
            temp_list = []
            #to count number of files in a folder
            num_of_frames = len(os.listdir(f'media/img/{self.char_type}/{animation}'))
            #the main for loops for charcter determination
            for i in range(num_of_frames):
                #loading the current frame for animation
                self.img = pygame.image.load(f'media/img/{self.char_type}/{animation}/{i}.png')
                #setting the scale height width and placement of the character
                self.img = pygame.transform.scale(self.img, (int(self.img.get_width() * scale), int(self.img.get_height() * scale)))
                #switching the framedddd
                temp_list.append(self.img)
            self.animation_list.append(temp_list)
            
        #applying animations
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 
    
    def move(self, moving_left, moving_right):
        #defining a command for movement
        #resetting movement
        dx = 0
        dy = 0
        
        #assigning variables to move left and right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        #applying gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
            
        dy += self.vel_y

        #floor collision detection
        if self.rect.bottom + dy > 300:
            dy = 300 -self.rect.bottom
            self.in_air = False

        #changing the actual rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        #updating the animation
        ANIMATION_COOLDOWN = 100
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed from the last animation
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
           self.update_time = pygame.time.get_ticks() 
           self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
           self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action has changed
        if new_action != self.action:
            self.action = new_action
            #update the animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        #defining a command to draw
        screen.blit(pygame.transform.flip(self.image, self.flip , False), self.rect)

#printing player with type, co-ords, scale and speed
player = playerEntity('Player', 200 , 200, 2, 5)
#enemy = playerEntity('Enemy', 300, 200, 2, 5)
player2 = playerEntity('Player', 300, 200, 2, 5)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

run = True

while run:

    #clicking the clock
    clock.tick(FPS)

    player2Pos = read_pos(Network().send(make_pos((player.x, player.y))))
    player2.x = player2Pos[0]
    player2.y = player2Pos[1]
    player2.update()

    #background colour
    draw_bg()

    #update the animation
    player.update_animation()
    player2.update_animation()

    #drawing players
    player.draw()
    player2.draw()


    #action 0 is Idle
    #action 1 is running
    #action 2 is jump
    #updating player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)

    if player2.alive:
        if player2.in_air:
            player2.update_action(2)
        elif moving_left or moving_right:
            player2.update_action(1)
        else:
            player2.update_action(0)


    #moving players
    player.move(moving_left, moving_right)
    player2.move(moving_left, moving_right)


    for event in pygame.event.get():
        #quitting game with QUIT button
        if event.type == pygame.QUIT:
            run = False
        #key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_SPACE:
                shoot = True

        #key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_e:
                shoot = False

    pygame.display.update()