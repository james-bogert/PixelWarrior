import pygame
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.image = pygame.Surface((40,40))
        self.image.fill((0,0,0))

        self.rect = self.image.get_rect()
        self.rect.x = ((int(screen.get_width()) / 2) - 20)
        self.rect.y = ((int(screen.get_height()) / 2) - 20)
        """just creates black square at center of screen, and a rect to colide with stuff. Most of the code does not actual involve the character"""

class Background(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.image = pygame.image.load("Background.png").convert()
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
    def move(self):
        if self.rect.x >= 3840:
            self.rect.x -= 5760
        if self.rect.x <= -3840:
            self.rect.x += 5760
        if self.rect.y >= 2160:
            self.rect.y -= 3240
        if self.rect.y <= -2160:
            self.rect.y += 3240

        """This is for the infinetly scrolling background, spawns nine screen sized rectangles, if the rectangle ever goes off a certain value then
        it is moved to the other side of whereever it is. The background variables are never deleted, just moved into place as you go. Technicaly while
        it looks like your are moving the most that enemies or the background can be offset from the player are about one screen away"""
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, colour, health, damage, size, xp, speed, is_boss):
        super().__init__()

        self.color = colour
        self.health = health
        self.damage = damage
        self.size = size
        self.xp = xp
        self.screen = screen
        self.speed = speed

        self.image = pygame.Surface(size)
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        if is_boss is False:
            z = random.randint(1,2)
            if z == 1:
                x = random.randint(1360, 2880)
            elif z == 2:
                x = random.randint(-960, 560)
            z = random.randint(1, 2)
            if z == 1:
                y = random.randint(790, 1620)
            elif z == 2:
                y = random.randint(-540, 290)
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.x = 835
            self.rect.y = -250

    def enemy_move(self, time, enemy_sprites):
        x_dif = ((int(self.screen.get_width()) / 2) - (self.rect.x) - (self.size[0]/2))
        y_dif = ((int(self.screen.get_height()) / 2) - (self.rect.y) - (self.size[1]/2))
        xy_dif = math.sqrt((x_dif**2) + (y_dif**2))
        x_dif = x_dif/xy_dif
        y_dif = y_dif/xy_dif
        self.rect.x += round(x_dif * self.speed * time)
        self.rect.y += round(y_dif * self.speed * time)
        for enemy in enemy_sprites:
            if self.rect == enemy.rect:
                continue
            elif self.rect.colliderect(enemy.rect):
                self.rect.x -= round(x_dif * self.speed * time)
                self.rect.y -= round(y_dif * self.speed * time)
    """This class is used in for all enemies, including the boss, everything like color, size, speed and damage can be chosen and easily changed.
    if it is spawned as a boss, then it spawns from the top middle of the screen, instead of randomly around. Enemy.move will use the pythagorian theroem to find the ratio between x and y 
    so that the enemy is always moving towards the center, this must run each frame incase it collides with an enemy, or the player moves."""

    def bullet_collide(self, damage):
        self.health -= damage  #when a bullet hits an enemy

    def on_death(self, enemy, enemy_sprites):
        enemy_sprites.remove(enemy) #anytime the enemy must be deleted

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, colour, mouse_position, size, type, direction, position):
        super().__init__()
        self.image = pygame.Surface((size[0],size[1]))
        self.image.fill(colour)

        self.rect = self.image.get_rect()
        if type == 1:
            self.rect.x = ((int(screen.get_width()) / 2) - 10)
            self.rect.y = ((int(screen.get_height()) / 2) - 10)
            x_dif = (int(mouse_position[0])) - (self.rect.x - 10)
            y_dif = (int(mouse_position[1])) - (self.rect.y - 10)
            xy_dif = math.sqrt((x_dif ** 2) + (y_dif ** 2))
            x_dif = x_dif / xy_dif
            y_dif = y_dif / xy_dif
            self.x_move = round(x_dif * 20)
            self.y_move = round(y_dif * 20)
        if type == 2:
            self.rect.x = position[0]
            self.rect.y = position[1]
            self.x_move = (direction[0] * 20)
            self.y_move = (direction[1] * 20)

    def bullet_move(self, time):
        self.rect.x += (self.x_move * time)
        self.rect.y += (self.y_move * time)
    """This class is used for all projectiles, including the bullets, the super bullets, and the 8 shots that came from the super bullet, Type 1 is for bullets and super bullets
    and uses the pythagorian theroem to calculate the ration between y and x so that the bullet moves towards the curren position of the mouse. If type two its direction is predecided so this code does not run"""

class Score(pygame.sprite.Sprite):
    def __init__(self, size, position):
        super().__init__()

        self.position = position
        self.font = pygame.font.Font("Pixeled.ttf", size)

    def draw(self, title, score, score_max, color):
        self.image = self.font.render(title + str(score) + score_max, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

    """#this is used for all text in the game, it always used the same font but the color, size and positon can be decided. title, score, and score max are for
    the contstantly changing health, xp, level, and super countdown. But if one of these does not need to be used then "" can be put in and it will not show up"""

def move(object, speed, time):
    speed = round(speed * time)
    diagonal_speed = round(math.sqrt((speed**2)/2))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and keys[pygame.K_d]:
        for x in object:
            x.rect.y += diagonal_speed
            x.rect.x -= diagonal_speed
    elif keys[pygame.K_s] and keys[pygame.K_d]:
         for x in object:
            x.rect.y -= diagonal_speed
            x.rect.x -= diagonal_speed
    elif keys[pygame.K_a] and keys[pygame.K_s]:
        for x in object:
            x.rect.y -= diagonal_speed
            x.rect.x += diagonal_speed
    elif keys[pygame.K_a] and keys[pygame.K_w]:
        for x in object:
            x.rect.y += diagonal_speed
            x.rect.x += diagonal_speed
    else:
        if keys[pygame.K_w]:
            for x in object:
                x.rect.y += speed
        if keys[pygame.K_s]:
            for x in object:
                x.rect.y -= speed
        if keys[pygame.K_a]:
            for x in object:
                x.rect.x += speed
        if keys[pygame.K_d]:
            for x in object:
                x.rect.x -= speed
    """This function handles player movement  by moving everything in the non_player_sprites group. Diagonal speed used the pythagorian theroem
    to make sure that the same speed is being used no matter which direction. Without it, when the player moves diagonaly it feels as though they
    are going twice as fast."""