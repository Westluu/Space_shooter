import pygame
from random import randint, uniform
vec = pygame.math.Vector2

""" The will be the boss of the shooter space game. """

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

max_force  = .1 
max_speed = 4

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.health = 100
        self.right_miniboss_pos_x = (width / 2) + 100 
        self.left_miniboss_pos_x = (width / 2) - 100
        self.pos = vec(width / 2, height + 60)
        self.rect.center = self.pos
        self.velo = vec(max_speed, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.last_update = pygame.time.get_ticks()
    
    def update(self):
        seek_now = pygame.time.get_ticks()
        while seek_now - self.last_update > 5000:
            power = PowerUp()
            all_sprites.add(power)
            powerups.add(power)
            power.seeking_bullets('disable', player.pos)

    def seeking_bullets(self, kind, target):
        """ seeking bullets
        """
        shot = Powerup()
        shot.kind = kind
        all_sprites.add(shot)
        powerups.add(shot)
        desire = (target - shot.pos).normalize()
        turn = (target - shot.velo)
        if turn.length() > max_force:
            turn.scale_to_length(max_force)
        return steer

    def shoot_mob(self):
        """ Shoots out mini bosses
        """
        mini_boss1 = MiniBoss(self.centerx)
        all_sprites.add(mini_boss)
        boss.add(mini_boss)
    
    def shoot(self):
        """ Shoots the bullet
        """
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        firing_sound.play()
    
class MiniBoss(pygame.sprite.Sprite):
    def __init__(self, centerx):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(60, 50)
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.centerx = height + 60
        self.health = 30
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay
    
    def shoot(self):
        """ Shoots the bullet
        """
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        firing_sound.play()
