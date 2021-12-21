import pygame
import random
import time
from os import path
from random import randint, uniform
import sys
vec = pygame.math.Vector2

width = 480 
height = 600
FPS = 60

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Init Image folder
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'sound')
exp_dir = path.join(path.dirname(__file__), 'expolosion')
power_dir = path.join(path.dirname(__file__), 'powerups')
nuke_dir = path.join(path.dirname(__file__), 'nuke')

# intizate the game and window
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Timers
start = time.time()
shoot_start = time.time()
mob_start = time.time()
clock = pygame.time.Clock()
machinegun_start = pygame.time.get_ticks()

# Highscore
highscore = [0]
with open('score.txt', 'r') as score_file:
    scores = score_file.readline()
    highscore[0] = scores

with open('score.txt', 'w'): pass

# Auto Shooter
auto_shooter = True

if auto_shooter == True:
    auto_shooter_change = True
else:
    auto_shooter_change = False

if auto_shooter == True:
    auto_shooters = True
else:
    auto_shooters = False

if auto_shooter == True:
    auto_shooter_allow = True
else:
    auto_shooter_allow = False

# Screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('My Space Invader')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def new_mob():
    a = Mob()
    all_sprites.add(a)
    mobs.add(a)

def draw_shield_bar(surface, x, y, pct, color):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, white, outline_rect, 2)

def draw_disable(surface, x, y, pct, color):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, white, outline_rect, 2)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "SHMUP!", 64, width / 2, height / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              width / 2, height / 2)
    draw_text(screen, "Press a key to begin", 18, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        
        # Circle Collsion dectecion
        self.radius = 16
        #pygame.draw.circle(self.image, red, self.rect.center, self.radius)
        
        # Put Ship at the center of the screen
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        
        # Initalize ship's speed
        self.speedx = 0
        self.speedy = 0
        
        # Intalize the shield value
        self.shield = 100
        self.shield_up = 0
        
        # Auto Shooter
        self.shoot_delay = 400
        self.last_shot = pygame.time.get_ticks()
        self.shooting = False
        
        # Timing the hide function
        self.hidden = False
        self.hide_timer = 0
        self.duration = 500

        self.pos = vec(self.rect.x, self.rect.y)
    
    def update(self):
        # time to unhide
        if self.hidden == True and pygame.time.get_ticks() - self.hide_timer > self.duration:
            self.hidden = False
            self.rect.center = ((width / 2), (height - 10))
        
        if self.hidden:
            return
        
        # Setting speed
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        
        # Controls for X-Axis
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        
        # Controls for Y-Axis
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy
        
        # Allow to hold space to shoot
        if keystate[pygame.K_SPACE] and auto_shooter == False and auto_shooter_allow == False:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.shoot()
        
        self.pos = vec(self.rect.x, self.rect.y)
        
        # Boundaries for the Player
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
    
    def shoot(self):
        """ Shoots the bullet
        """
        self.shooting = True
        player_bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(player_bullet)
        bullets.add(player_bullet)
        firing_sound.play()
        
    def shield_follow(self):
        """ Puts the shield up if shield health is up
        """
        shield = Shield(self.shield, self.rect.center)
        self.shield_up = shield
        if shield.health <= 100:
            all_sprites.add(shield)
        if shield.health <= 0:
            shield.kill()
    
    def hide(self):
        """ Hides the ship from the screen
        """
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, height * 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(black)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .80 / 2)
        # pygame.draw.circle(self.image_orig, red, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(2, 9)
        self.speedx = random.randrange(-4, 4)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()
    
    def rotate(self):
        """ Rotates the meteor
        """
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 11)
            self.speedx = random.randrange(-3, 3)
        
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 20)) 
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = - 10
        self.pos = vec(x, y)
    
    def update(self):
        self.rect.y += self.speedy
        self.pos = vec(self.rect.x, self.rect.y)
        # Kill it if it moves off the map
        if self.rect.bottom < 0:
            self.kill()

class Shield(pygame.sprite.Sprite):
    def __init__(self, player_shield, player_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(shield_img, (70, 59))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = player_x
        self.health = player_shield
    
    def update(self):
        if self.health <= 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.kind = random.choice(['shield', 'machinegun', 'life', 'disable'])
        self.image = pygame.transform.scale(powerup_img[self.kind], (50, 50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5
        self.pos = vec(self.rect.centerx, self.rect.centery)
        self.velo = vec(max_speed, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)

    def update(self):
        self.rect.y += self.speedy      
        # Destory if out of bounds
        if self.rect.top > height + 10:
            self.kill()

max_force  = .09
max_speed = 5

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss1_img, (100, 50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        
        # Health
        self.health = 100
        
        # Mini-Boss position
        self.right_miniboss_pos_x = (width / 2) + 100 
        self.left_miniboss_pos_x = (width / 2) - 100
        
        # Vectors
        self.pos = vec(width / 2, 60)
        self.rect.center = self.pos
        self.velo = vec(max_speed, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        
        # Spawn time
        self.seek_update = pygame.time.get_ticks()
        self.spawn_update = pygame.time.get_ticks()
        self.speedx = 1
    
    def update(self):
        spawn_now = pygame.time.get_ticks()
        self.left_right_move()
        self.seeking_bullet('Powerup', 'disable')
        if len(mobs) < 6:
            if spawn_now - self.spawn_update > 5000:
                self.spawn_update = spawn_now
                new_mob()

    def seeking_bullet(self, types, kind):
        seek_now = pygame.time.get_ticks()
        if seek_now - self.seek_update > 3000:
            self.seek_update = seek_now
            seek = SeekingBullets(types, kind, self.rect.centerx, self.rect.centery)
            seek.seeking(player.pos)
            all_sprites.add(seek)
            if seek.types == 'Bullet':
                boss_bullet.add(seek)
            if seek.types == 'Powerup':
                powerups.add(seek)
    
    def shoot_mob(self):
        """ Shoots out mini bosses
        """
        mini_boss1 = MiniBoss(width / 2 - 175)
        mini_boss2 = MiniBoss(width / 2 + 175)

        mini_boss1.image = pygame.transform.scale(attack_img, (60, 50))
        mini_boss1.image.set_colorkey(black)
        mini_boss1.seek = True
        mini_boss1.left_right_move = False
        
        mini_boss2.left_right = True
        mini_boss2.seek = False
        
        # Adding to mini-boss group
        mini_boss.add(mini_boss1)
        mini_boss.add(mini_boss2)
        
        # Adding to all sprites
        all_sprites.add(mini_boss1)
        all_sprites.add(mini_boss2)
    
    def shoot(self):
        """ Shoots the bullet
        """
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet.speedy = 10
        all_sprites.add(bullet)
        bullets.add(bullet)
        firing_sound.play()
    
    def left_right_move(self):
        """ Left - right movement
        """
        if self.rect.right >= width:
            self.speedx = -3
        if self.rect.left <= 0:
            self.speedx = 3
        if self.speedx > 0:
            self.speedx = random.randrange(2, 7)
        if self.speedx < 0:
            self.speedx = random.randrange(-7, -2) 
        self.rect.x += self.speedx 

boss_force = .09
MAX_SPEED = 5
MAX_FORCE = 0.1
FLEE_DISTANCE = 200

class MiniBoss(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss2_img, (60, 50))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery =  height - 425
        self.health = 30
        self.speedx = 3
        self.health = 50
        
        # shot
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 500

        # Vectors 
        self.posx = self.rect.centerx
        self.posy = self.rect.centery
        self.pos = vec(self.posx, self.posy)
        self.vel = vec(max_speed, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos

        # Movement Flags
        self.seek = False
        self.left_right = False
    
    def update(self):
        if self.seek == True:
            self.seeker(player.pos)
            self.rect.center = self.pos
 
        if self.left_right == True:
            # Move to the top
            if self.rect.top > 0:
                self.rect.y -= 5
                if self.rect.top < 0:
                    self.rect.top = 0
            self.move_left_right()
            
            shoot_now = pygame.time.get_ticks()
            time_shoot = shoot_now - self.last_shot
            if time_shoot > self.shoot_delay:
                self.last_shot = shoot_now
                self.shoot()
        
        if len(mobs) < 3:
            new_mob()

        # equations of motion
        self.vel += self.acc
        if self.vel.length() > max_speed:
            self.vel.scale_to_length(max_speed)
        
        self.pos += self.vel
        
        # Boundaries for the mini-boss
        if self.rect.right > width:
            self.rect.right = width

        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.top < 0:
            self.rect.top = 0
        
        if self.rect.bottom > height:
            self.rect.bottom = height
          
    def shoot(self):
        """ Shoots the bullet
        """
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet.speedy = 10
        all_sprites.add(bullet)
        boss_bullet.add(bullet)
        firing_sound.play()
    
    def seeker(self, target):
        """  The boss seeks the player
        """
        desired = (target - self.pos).normalize() * max_speed
        steer = (desired - self.vel)
        if steer.length() > boss_force:
            steer.scale_to_length(boss_force)
        self.acc = steer

    def move_left_right(self):
        """ Left - right movement
        """
        if self.rect.right >= width:
            self.speedx = -3
        if self.rect.left <= 0:
            self.speedx = 3
        if self.speedx > 0:
            self.speedx = 3
        if self.speedx < 0:
            self.speedx = -3 
        self.rect.x += self.speedx
    
    def avoid(self, target):
        steer = vec(0, 0)
        dist = self.pos - target
        if dist.length() < FLEE_DISTANCE:
            self.desired = (self.pos - target).normalize() * MAX_SPEED
        else:
            self.desired = self.vel.normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        self.acc = steer

class SeekingBullets(pygame.sprite.Sprite):
    def __init__(self, types, kind, centerx, centery):
        pygame.sprite.Sprite.__init__(self)
        self.types = types
        if self.types == 'Bullet':
            self.image = bullet_img
            self.rect = self.image.get_rect()
            self.pos = vec(centerx, centery)
            self.vel = vec(max_speed, 0).rotate(uniform(0, 360))
            self.acc = vec(0, 0)
            self.rect.center = self.pos
        
        if self.types == 'Powerup':
            self.kind = kind
            self.image = pygame.transform.scale(powerup_img[self.kind], (50, 50))
            self.image.set_colorkey(black)
            self.rect = self.image.get_rect()
            self.pos = vec(centerx, centery)
            self.vel = vec(max_speed, 0).rotate(uniform(0, 360))
            self.acc = vec(0, 0)
            self.rect.center = self.pos
    
    def update(self):
        self.acc = self.seeking(player.pos)       
        # equations of motion
        self.vel += self.acc
        if self.vel.length() > max_speed:
            self.vel.scale_to_length(max_speed)
        self.pos += self.vel
        if self.pos.x > width or self.pos.x < 0:
            self.kill()
        if self.pos.y > height:
            self.kill()
        
        self.rect.center = self.pos

    def seeking(self, target):
        desired = (target - self.pos).normalize() * max_speed
        steer = (desired - self.vel)
        if steer.length() > max_force:
            steer.scale_to_length(max_force)
        return steer
    
# Load all Game Graphics
background = pygame.image.load(path.join(img_dir, 'backgrounds.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, 'player.png')).convert()
bullet_img = pygame.image.load(path.join(img_dir, 'bullet.png')).convert()
shield_img = pygame.image.load(path.join(img_dir, 'shield.png')).convert()

# Boss Img
boss1_img = pygame.image.load(path.join(img_dir, 'orange_ship.png')).convert()
boss2_img = pygame.image.load(path.join(img_dir, 'green_ship.png')).convert()
attack_img = pygame.image.load(path.join(img_dir, 'ufoBlue.png')).convert()

# Meteor Images
meteor_images = []
meteor_list = ['meteor_med.png', 'meteorgrey_med.png', 'meteor_small.png',
               'meteor_small2.png', 'meteor_big.png', 'meteor_big2.png',
               'meteor_tiny.png']

# Adds every meteor img to a list
for img in meteor_list:
    meteor_image = pygame.image.load(path.join(img_dir, img)).convert()
    meteor_images.append(meteor_image)

# Explosion list for animation
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
explosion_anim['nuke'] = []

# Adds Metoer to small and big list
for i in range(1,10):
    # Asteroid Expolsion animation
    """ Size of explosion depends on size of meteor
    That is why there is a small and large list.
    """
    file_name = 'exp{}.png'.format(i)
    img = pygame.image.load(path.join(exp_dir, file_name)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

# Player Death Explosion
for i in range(9):
    # Player Explosion
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(exp_dir, filename)).convert()
    img.set_colorkey(black)
    explosion_anim['player'].append(img)

# Nuke Explosion
for i in range(8):
    filename = 'nuke0{}.png'.format(i)
    img = pygame.image.load(path.join(nuke_dir, filename)).convert()
    img = pygame.transform.scale(img, (480, 900))
    explosion_anim['nuke'].append(img)

# PowerUps
powerup_img = {}
powerup_img['shield'] = pygame.image.load(path.join(power_dir, 'shield.png')).convert()
powerup_img['machinegun'] = pygame.image.load(path.join(power_dir, 'machine_gun.png')).convert()
powerup_img['life'] = pygame.image.load(path.join(power_dir, 'life.png')).convert()
powerup_img['disable'] = pygame.image.load(path.join(power_dir, 'disable.png')).convert()
powerup_img['nuke'] = pygame.image.load(path.join(power_dir, 'nuke_test.png')).convert()

# Load all the game sound and music
firing_sound = pygame.mixer.Sound(path.join(snd_dir, 'lasers.wav'))
firing_sound.set_volume(.1)

shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'boom.wav'))
shield_sound.set_volume(.1)

shield_hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'shield_hit.wav'))
shield_hit_sound.set_volume(.1)

explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'explosion.wav'))
explosion_sound.set_volume(.1)

player_hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'player_hit.wav'))
player_hit_sound.set_volume(.2)

big_explosion_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
big_explosion_sound.set_volume(.1)

nuke_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))

pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(.1)

# Adding the objects
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boss_bullet = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Boss group
boss = pygame.sprite.Group()
mini_boss = pygame.sprite.Group()

# Spawn in 2 asteroids at first
max_mobs = 4
mob = 2
for i in range(mob):
    if len(mobs) < max_mobs:
        new_mob()
spawn_time = 5

# Player's functionalites
score = 0
player_health = 2
player_lives = 3
auto_shooter_delay = .4
pygame.mixer.music.play()

nuke_done = 0

# Game Loop
running = True
game_over = False

while running:
    if game_over:
        
        if score > int(highscore[0]):
            highscore[0] = str(score)
        
        with open('score.txt', 'w') as write_file:
            write_file.write(highscore[0])
        
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0
      
    # keep loop running at the right speed
    clock.tick(FPS)
    
    # Proceesed Input (events)
    for event in pygame.event.get():
        
        # check for quitting
        if event.type == pygame.QUIT:
            running = False   
        elif event.type == pygame.KEYDOWN:
            if auto_shooter == False and event.key == pygame.K_SPACE\
                 and auto_shooter_allow == False:
                player.shoot()
    
    # Check if music is playing
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.play() 
    
    # In Game Clock
    game_now = time.time()
    game_sec = int(game_now - start) 
    
    # Update
    all_sprites.remove(player.shield_up)
    all_sprites.update()
    player.shield_follow()
    
    # Auto Shooter option
    shoot_time = time.time()
    shoot_time_diff = shoot_time - shoot_start
    if auto_shooter == True:
        if shoot_time_diff > auto_shooter_delay:
            shoot_start = shoot_time
            player.shooting = True
            if player.shooting == True:
                player.shoot()
                player.shooting = False   
    
    # Spawns a mob for every spawn_time
    now = time.time()
    dt = now - mob_start
    
    if dt > spawn_time:
        mob_start = now
        if len(mobs) < max_mobs:
            m = Mob()
            m.speedy += 1
            m.speedx += 1
            all_sprites.add(m)
            mobs.add(m)
        
        if len(mobs) >= max_mobs - 4:
            m.speedy += 15
            m.speedx += 2      
  
    # Check if bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 52 - hit.radius
        explosion_sound.play()
        expol = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expol) 
        if len(mobs) < max_mobs:
            new_mob()
        
        # Chance of spawning powerup
        if len(mobs) < max_mobs:
            if random.random() > .94:
                powerup = PowerUp(hit.rect.center)
                all_sprites.add(powerup)
                powerups.add(powerup)
        
        if len(mobs) == max_mobs:
            if random.random() > .92:
                powerup = PowerUp(hit.rect.center)
                powerup.kind = 'nuke'
                powerup.image = pygame.transform.scale(powerup_img['nuke'], (50, 50))
                powerup.image.set_colorkey(black)
                all_sprites.add(powerup)
                powerups.add(powerup)
    
    # Check if hit MachineGun
    hits = pygame.sprite.spritecollide(player, powerups, True)
    
    for hit in hits:
        if hit.kind == 'machinegun':
            auto_shooter = True
            machinegun_now = pygame.time.get_ticks()
            auto_shooter_delay = .085
        
        if hit.kind == 'shield':
            player.shield = 100
        
        if hit.kind == 'life':
            player_lives += 1
        
        if hit.kind == 'disable':
            disable_start = pygame.time.get_ticks()
            mode = 0
            if auto_shooters == False:
                mode = False
            else:
                mode = True
            auto_shooter = False
            auto_shooter_allow = True
        
        if hit.kind == 'nuke':
            nuke = Explosion((width / 2, height / 2), 'nuke') 
            nuke.image.set_colorkey(black)
            nuke.frame_rate = 90
            auto_shooter = False
            auto_shooter_allow = False
            all_sprites.add(nuke)
            nuke_sound.play()
            mob = 0
            for mob in mobs:
                mob.kill()
            for power in powerups:
                power.kill()
            spawn_time = 1000 * 100000
            player.duration = 950
            player.hide()
            nuke_done += 1
    
    if player.hidden ==  False and nuke_done > 0:
        auto_shooter = True
        auto_shooter_allow = True
        nuke_done -=1
        the_boss = Boss()
        all_sprites.add(the_boss)
        boss.add(the_boss) 

    # Duration of machinegun
    if auto_shooter_delay == .085:
        if pygame.time.get_ticks() - machinegun_now > 5000:
            auto_shooter_delay = .35     
            if auto_shooter_change == True:
                auto_shooter = True
            else:
                auto_shooter = False
     
    # Duration of Disabled
    if auto_shooter == False and auto_shooter_allow == True:
        disable_now = pygame.time.get_ticks()
        disable_time = disable_now - disable_start
        if disable_time > 4000:
            if mode == False:
                auto_shooter_allow = False
            if mode == True:
                auto_shooter = True
                    
    # Check if mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        if player.shield > 0:
            shield_hit_sound.play()
            player.shield -= hit.radius * 2
            expol = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expol)
            if len(mobs) < max_mobs:
                new_mob()
        
        if player.shield <= 0:
            player_health -= 1
            if len(mobs) < max_mobs:
                new_mob()
            
            if player_health == 0:
                player_lives -= 1
                player_hit = Explosion(player.rect.center, 'player')
                big_explosion_sound.play()
                all_sprites.add(player_hit)
                explo_time = pygame.time.get_ticks()
                player.hide()
                player.shield = 100
                player_health = 2
    
    # Check if boss bullet hits player
    hits = pygame.sprite.spritecollide(player, boss_bullet, True)
    for hit in hits:
        player.shield -= 25
        
        if player.shield <= 0:
            player_health -= 1
            
            if player_health == 0:
                player_lives -= 1
                player_hit = Explosion(player.rect.center, 'player')
                big_explosion_sound.play()
                all_sprites.add(player_hit)
                explo_time = pygame.time.get_ticks()
                player.hide()
                player.shield = 100
                player_health = 2
    
    # Check if player bullets hits boss
    hits = pygame.sprite.groupcollide(boss, bullets, False, True)
    for hit in hits:
        print('boss hit')
        if hit.health <= 100:
            hit.health -= 2
            print(hit.health)

        if hit.health == 90:  
            hit.shoot_mob()
            hit.kill()
    
    # Check if player bullets hit mini boss
    hits = pygame.sprite.groupcollide(mini_boss, bullets, False, True)
    for hit in hits:
        print('mini boos hit')
        if hit.health <= 50:
            hit.health -= 2
        
        if hit.health == 0:
            hit.kill()
        
        print(hit.health)
    
    # Check if mini_boss hits player
    hits = pygame.sprite.spritecollide(player, mini_boss, False)
    for hit in hits:
        player.shield -= 2

        if player.shield <= 0:
            player_health -= 1
            if player_health == 0:
                player_lives -= 1
                player_hit = Explosion(player.rect.center, 'player')
                big_explosion_sound.play()
                all_sprites.add(player_hit)
                explo_time = pygame.time.get_ticks()
                player.hide()
                player.shield = 100
                player_health = 2

    # Game ends after the explosion happens
    if player_lives == 0 and pygame.time.get_ticks() - explo_time > 488.4:
        player.kill()
        game_over = True
            
    # Draw/ render
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'Score: ' + str(score), 18, (width / 2) - 10, 0)
    draw_text(screen, str(game_sec) + ' seconds', 18, (width - 130), 0)
    draw_text(screen, 'X' + str(player_lives), 20, width - 25, 0)
    draw_shield_bar(screen, 5, 5, player.shield, green)
    
    # after drawing everything (flips display)
    pygame.display.flip()

pygame.quit()
