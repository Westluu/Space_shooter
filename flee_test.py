import pygame as pg
from random import randint, uniform
vec = pg.math.Vector2

WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

# Mob properties
MOB_SIZE = 32
MAX_SPEED = 5
MAX_FORCE = 0.1
FLEE_DISTANCE = 200

max_force  = .09
max_speed = 5

class Player(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        
        # Circle Collsion dectecion
        self.radius = 16
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        
        # Put Ship at the center of the screen
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 0
        
        # Initalize ship's speed
        self.speedx = 0
        self.speedy = 0
        

        self.pos = vec(self.rect.x, self.rect.y)
    
    def update(self):
        # Setting speed
        self.speedx = 0
        self.speedy = 0
        keystate = pg.key.get_pressed()
        
        # Controls for X-Axis
        if keystate[pg.K_LEFT]:
            self.speedx = -5
        if keystate[pg.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        
        # Controls for Y-Axis
        if keystate[pg.K_UP]:
            self.speedy = -5
        if keystate[pg.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy
                
        self.pos = vec(self.rect.x, self.rect.y)
        
        # Boundaries for the Player
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Mob(pg.sprite.Sprite):
    def __init__(self):
        self.groups = all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((MOB_SIZE, MOB_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, 60)
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

    def flee(self, target):
        steer = vec(0, 0)
        dist = self.pos - target
        if dist.length() < FLEE_DISTANCE:
            self.desired = (self.pos - target).normalize() * MAX_SPEED
        else:
            self.desired = self.vel.normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def update(self):
        # self.follow_mouse()
        if self.rect.right < WIDTH:
            self.acc = self.flee(player.pos)
        
        if self.rect.left > 0:
            self.acc = self.flee(player.pos)

        
        if self.rect.top < 0:
            self.acc = self.flee(player.pos)
        
        if self.rect.bottom < HEIGHT:
            self.acc = self.flee(player.pos)
        
        # equations of motion
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        
        self.rect.center = self.pos
        
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        
           
        if self.pos.x > WIDTH - 50:
            self.acc = self.seek(player.pos)
        if self.pos.x < 0 + 50:
            self.acc = self.seek(player.pos)
        if self.pos.y > HEIGHT - 50:
            self.acc = self.seek(player.pos)
        if self.pos.y < 0 + 50:
            self.acc = self.seek(player.pos)
        
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
    

        
    
    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer
        
        

    def draw_vectors(self):
        scale = 25
        # vel
        pg.draw.line(screen, GREEN, self.pos, (self.pos + self.vel * scale), 5)
        # desired
        pg.draw.line(screen, RED, self.pos, (self.pos + self.desired * scale), 5)
        # flee radius
        pg.draw.circle(screen, WHITE, pg.mouse.get_pos(), FLEE_DISTANCE, 1)

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

all_sprites = pg.sprite.Group()
Mob()
bullet = pg.sprite.Group() 
player = Player()
all_sprites.add(player)
paused = False
show_vectors = False
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                paused = not paused
            if event.key == pg.K_v:
                show_vectors = not show_vectors
            if event.key == pg.K_m:
                Mob()



    if not paused:
        all_sprites.update()
    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    all_sprites.draw(screen)
    if show_vectors:
        for sprite in all_sprites:
            sprite.draw_vectors()
    pg.display.flip()