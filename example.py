import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
tick = 0

width = screen.get_width()
height = screen.get_height()

click_pos = pygame.Vector2(width/2, height / 2)
shots = []

class player():
    def __init__(self,size, max_health,shoot_speed,max_teleports,norm_color,hit_color):
        self.score = 0
        self.pos = pygame.Vector2(width/2, height / 2)
        self.shoot_speed = shoot_speed
        self.size = size
        self.tele_cooldown = 0
        self.teleports = max_teleports
        self.health = max_health
        self.maxhealth = max_health
        self.color = norm_color
        self.norm_color = norm_color
        self.hit_color = hit_color
    def is_hit(self,enemy):
        if(tick%6 == 0):
            if (enemy.pos.x < self.pos.x+self.size and enemy.pos.x > self.pos.x-self.size) and (enemy.pos.y < self.pos.y+self.size and enemy.pos.y > self.pos.y-self.size):
                self.health -= 1
                self.color = self.hit_color
                if(self.health <= 0):
                    print('You Died')
                    print('Score:',self.score)
                    raise Exception ("You Died")
                return True
            else:
                self.color = self.norm_color

class bullet():
    def __init__(self,chara,speed):
        self.direction = pygame.Vector2(click_pos.x-chara.pos.x,click_pos.y-chara.pos.y)
        if(self.direction.length() != 0):
            self.direction.normalize_ip()
        self.pos = pygame.Vector2(chara.pos)
        self.speed = speed
    def update(self):
        self.pos.x += self.direction.x*self.speed
        self.pos.y += self.direction.y*self.speed

class enemy():
    def __init__(self,size, max_health,speed,norm_color,hit_color):
        x = random.randrange(0,width,1)
        y = random.randrange(0,height,1)
        self.pos = pygame.Vector2(x,y)
        self.health = max_health
        self.max_health = max_health
        self.size = size
        self.speed = speed
        self.color = norm_color
        self.norm_color = norm_color
        self.hit_color = hit_color
    def isHit(self,bullet,chara):
        if (bullet.pos.x < self.pos.x+self.size and bullet.pos.x > self.pos.x-self.size) and (bullet.pos.y < self.pos.y+self.size and bullet.pos.y > self.pos.y-self.size):
            self.health -= 1
            self.color = self.hit_color
            if(self.health <= 0):
                if(self.speed < 320):
                    self.speed += 20
                print('died')
                chara.score += 1
                x = random.randrange(0,width,1)
                y = random.randrange(0,height,1)
                print(x,y)
                self.pos.x = x
                self.pos.y = y
                self.health = self.max_health
            return True
        elif(tick%10 == 0):
            self.color = self.norm_color
    def move(self, player_pos):
        move = pygame.Vector2(player_pos.x-self.pos.x,player_pos.y-self.pos.y)
        move.normalize_ip()
        self.pos += move*self.speed*dt
        
def inputHandler(chara):
    pygame.draw.circle(screen, chara.color, chara.pos, 30)
    # pygame.draw.polygon(screen,"red",player_pos,1) TODO: figure out shapes

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        chara.pos.y -= 300 * dt
    if keys[pygame.K_s]:
        chara.pos.y += 300 * dt
    if keys[pygame.K_a]:
        chara.pos.x -= 300 * dt
    if keys[pygame.K_d]:
        chara.pos.x += 300 * dt
    if keys[pygame.K_SPACE] and tick%chara.shoot_speed == 0:
        shoot(chara)
    if keys[pygame.K_j]:
        print(shots)
    mouse = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if mouse[0]:
        click_pos.x = pos[0]
        click_pos.y = pos[1]
        if tick%chara.shoot_speed == 0:
            shoot(chara)
    if mouse[2] and chara.tele_cooldown == 0:
        teleport(chara,pos)
        
    chara.pos.x %= width
    chara.pos.y %= height

def shoot(chara):
    shots.append(bullet(chara,20))

def teleport(chara,pos):
    if(chara.teleports > 0):
        chara.pos.x = pos[0]
        chara.pos.y = pos[1]
    chara.teleports -= 1
    chara.tele_cooldown = 200

chara = player(30,30,5,4,"red","darkred")
enemy_pos = pygame.Vector2(300,70)
blob = enemy(18,20,100,"green","darkgreen")

enemies = []
enemies.append(blob)

while running:
    # refresh the screen
    screen.fill("black")

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            shoot(chara)
    
    pygame.draw.circle(screen, "blue", click_pos, 10)
    for blob in enemies:
        pygame.draw.circle(screen, blob.color, blob.pos, 12)

    inputHandler(chara)

    for shot in shots:
        shot.update()
        if shot.direction.length() == 0:
            shots.remove(shot)
        for blob in enemies:
            if blob.isHit(shot,chara):
                try: shots.remove(shot)
                except: True
        if shot.pos.x > width or shot.pos.x < 0 or shot.pos.y > height or shot.pos.y < 0:
            try: shots.remove(shot)
            except: True
        pygame.draw.circle(screen, "yellow", shot.pos, 4)
        
    # update Screen
    pygame.display.flip()

    chara.is_hit(blob)
    for blob in enemies:
        blob.move(chara.pos)
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

    if(chara.tele_cooldown > 0):
        chara.tele_cooldown -= 1
    tick += 1
    tick %= 1000

pygame.quit()