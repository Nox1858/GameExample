import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200,700))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
running = True
playing = True
dt = 1
tick = 1

font1 = pygame.font.SysFont('Comic Sans MS', 24)
font2 = pygame.font.SysFont('Comic Sans MS', 36)


width = screen.get_width()
height = screen.get_height()

cursor_pos = pygame.Vector2(width/2, height / 2)
shots = []
enemies = []

class player():
    def __init__(self,size, max_health,shoot_speed,max_teleports,norm_color,hit_color):
        self.score = 0
        self.pos = pygame.Vector2(width/2, height / 2)
        self.shoot_speed = shoot_speed
        self.size = size
        self.tele_cooldown = 0
        self.teleports = max_teleports
        self.health = max_health
        self.max_health = max_health
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
                    print('final score:',self.score)
                    raise Exception ("You Died")
                return True
            else:
                self.color = self.norm_color
    def teleport(self,pos):
        if(self.teleports > 0):
            self.pos.x = pos[0]
            self.pos.y = pos[1]
            self.teleports -= 1
            self.tele_cooldown = 200
    def shoot(self):
        shots.append(bullet(self,20))

class bullet():
    def __init__(self,chara,speed):
        self.direction = pygame.Vector2(cursor_pos.x-chara.pos.x,cursor_pos.y-chara.pos.y)
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
    def is_hit(self,bullet,chara):
        if (bullet.pos.x < self.pos.x+self.size and bullet.pos.x > self.pos.x-self.size) and (bullet.pos.y < self.pos.y+self.size and bullet.pos.y > self.pos.y-self.size):
            self.health -= 1
            self.color = self.hit_color
            if(self.health <= 0):
                if(self.speed < 320):
                    self.speed += 20
                elif(1 == random.randrange(1,20,1)):
                    enemies.remove(self)
                print('died')
                chara.score += 1
                x = random.randrange(0,width,1)
                y = random.randrange(0,height,1)
                print(x,y)
                self.pos.x = x
                self.pos.y = y
                self.health = self.max_health
                if(1 == random.randrange(1,10,1)):
                    print("you got a new enemy!")
                    blob = enemy(18,20,100,"green","darkgreen")
                    enemies.append(blob)
            return True
        elif(tick%10 == 0):
            self.color = self.norm_color
    def move(self, player_pos):
        move = pygame.Vector2(player_pos.x-self.pos.x,player_pos.y-self.pos.y)
        move.normalize_ip()
        self.pos += move*self.speed*dt
    def healthbar(self):
        x = self.pos.x - self.max_health/2
        y = self.pos.y - 3
        back_rect = pygame.Rect(x-1,y-1,self.max_health+2,8)
        base_rect = pygame.Rect(x,y,self.max_health,6)
        value_rect = pygame.Rect(x,y,self.health,6)
        pygame.draw.rect(screen,"black",back_rect)
        pygame.draw.rect(screen,"white",base_rect)
        pygame.draw.rect(screen,"green",value_rect)
        
def player_handler(chara):
    if keys[pygame.K_w]:
        chara.pos.y -= 300 * dt
    if keys[pygame.K_s]:
        chara.pos.y += 300 * dt
    if keys[pygame.K_a]:
        chara.pos.x -= 300 * dt
    if keys[pygame.K_d]:
        chara.pos.x += 300 * dt
    if keys[pygame.K_SPACE] and tick%chara.shoot_speed == 0:
        chara.shoot()
    if keys[pygame.K_j]:
        print(shots)
    if keys[pygame.K_o]:
        enemies.clear()
    mouse = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if mouse[0]:
        cursor_pos.x = pos[0]
        cursor_pos.y = pos[1]
        if tick%chara.shoot_speed == 0:
            chara.shoot()
    if mouse[2] and chara.tele_cooldown == 0:
        chara.teleport(pos)

    chara.pos.x %= width
    chara.pos.y %= height

    # pygame.draw.polygon(screen,"red",player_pos,1) TODO: figure out shapes other than circle
    pygame.draw.circle(screen, chara.color, chara.pos, 30)
    healthbar(chara.max_health,chara.health)

    # handles tele-cooldown
    if(chara.tele_cooldown > 0):
        chara.tele_cooldown -= 1

def enemy_handler():
    for blob in enemies:
        chara.is_hit(blob)
        blob.move(chara.pos)
        pygame.draw.circle(screen, blob.color, blob.pos, 14)
        blob.healthbar()

    for shot in shots:
        shot.update()
        if shot.direction.length() == 0:
            shots.remove(shot)
        for blob in enemies:
            if blob.is_hit(shot,chara):
                try: shots.remove(shot)
                except: True
        if shot.pos.x > width or shot.pos.x < 0 or shot.pos.y > height or shot.pos.y < 0:
            try: shots.remove(shot)
            except: True
        pygame.draw.circle(screen, "yellow", shot.pos, 4)

def update_score(score):
    score_text = font1.render(str(score), True, (0, 255, 0))
    text_rect = score_text.get_rect()
    text_rect.center = (width-(text_rect.width/2)-5, 0+(text_rect.height/2))
    screen.blit(score_text, text_rect)

def healthbar(max_value,value):
    scale = width/max_value/3
    x = width/2 - max_value*scale/2+1
    back_rect = pygame.Rect(x-1,0,max_value*scale+2,scale+1)
    base_rect = pygame.Rect(x,0,max_value*scale,scale)
    value_rect = pygame.Rect(x,0,value*scale,scale)
    pygame.draw.rect(screen,"black",back_rect)
    pygame.draw.rect(screen,"white",base_rect)
    pygame.draw.rect(screen,"green",value_rect)
    pygame.draw

def update_game():
    pygame.draw.circle(screen, "blue", cursor_pos, 8) # draw cursor

    player_handler(chara)

    enemy_handler()

    update_score(chara.score) 

    # winscreen (useless, as it is probably impossible. Actually nvm; it is improbably possible)
    if(len(enemies) == 0):
        text1 = font2.render("You have done that, which is statistically impossible.", True, (0, 255, 0))
        text2 = font2.render("You have won.", True, (0, 255, 0))
        text3 = font2.render("Congrats", True, (0, 255, 0))
        text_rect1 = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()
        text_rect1.center = (width/2, height/3+(text_rect1.height/2))
        text_rect2.center = (width/2, height/3+text_rect1.height+(text_rect2.height/2))
        text_rect3.center = (width/2, height/3+text_rect1.height+text_rect2.height+(text_rect3.height/2))
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)

def menu():
    score_text = font1.render("this is the menu", True, (0, 255, 0))
    text_rect = score_text.get_rect()
    text_rect.center = (width/2, height/2)
    screen.blit(score_text, text_rect)

chara = player(30,30,5,4,"red","darkred")
blob = enemy(18,20,100,"green","darkgreen")
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
            chara.shoot()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        print('esc')
        playing = False
    
    if playing:
        update_game()

        # limits FPS to 60, dt is seconds since last frame, used for fps-independent physics
        dt = clock.tick(60) / 1000
        tick += 1
        tick %= 1000
    else:
        # TODO something, idk
        menu()
        if keys[pygame.K_p]:
            playing = True
    
    # update Screen
    pygame.display.flip()    

pygame.quit()