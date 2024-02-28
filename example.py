# this is a learning project, it was created by modifying an example game from the pygame community
# movement and basic visuel engine by a creator from a pygame tutorial, rest by Nox1858

import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200,700))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
running = True
playing = True
pause_cooldown = 0
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
        self.stomp_size = 80
        self.stomp_damage = 10
        self.stomp_cooldown = 0
        self.size = size
        self.tele_cooldown = 0
        self.teleports = max_teleports
        self.health = max_health
        self.max_health = max_health
        self.color = norm_color
        self.norm_color = norm_color
        self.hit_color = hit_color
        self.hit_this_tick = False
    def is_hit(self,blob):
        if(tick%6 == 0):
            if (blob.pos.x < self.pos.x+self.size and blob.pos.x > self.pos.x-self.size) and (blob.pos.y < self.pos.y+self.size and blob.pos.y > self.pos.y-self.size):
                self.health -= blob.atk
                self.color = self.hit_color
                self.hit_this_tick = True
                if(self.health <= 0):
                    print('You Died')
                    print('final score:',self.score)
                    raise Exception ("You Died")
                return True
            elif not self.hit_this_tick:
                self.color = self.norm_color
    def teleport(self,pos):
        if(self.teleports > 0):
            self.pos.x = pos[0]
            self.pos.y = pos[1]
            self.teleports -= 1
            self.tele_cooldown = 200
    def shoot(self):
        shots.append(bullet(self,20,(255,255,0),1))
    def stomp(self):
        if(self.stomp_cooldown == 0):
            for blob in enemies:
                if(blob.pos.x < self.pos.x+self.stomp_size and blob.pos.x > self.pos.x-self.stomp_size) and (blob.pos.y < self.pos.y+self.stomp_size and blob.pos.y > self.pos.y-self.stomp_size):
                    blob.is_hit(blob,self,8)
            self.stomp_cooldown += 100
            pygame.draw.circle(screen, (100,200,100), self.pos, self.stomp_size)


class bullet():
    def __init__(self,chara,speed,color,atk):
        self.direction = pygame.Vector2(cursor_pos.x-chara.pos.x,cursor_pos.y-chara.pos.y)
        if(self.direction.length() != 0):
            self.direction.normalize_ip()
        self.pos = pygame.Vector2(chara.pos)
        self.speed = speed
        self.color = color
        self.atk = atk
    def update(self):
        self.pos.x += self.direction.x*self.speed
        self.pos.y += self.direction.y*self.speed


class enemy():
    def __init__(self,size, max_health,speed,norm_color,hit_color,die_rate,respawn_rate, atk):
        x = random.randrange(0,width,1)
        y = random.randrange(0,height,1)
        self.pos = pygame.Vector2(x,y)
        self.health = max_health
        self.max_health = max_health
        self.respawn_rate = respawn_rate
        self.die_rate = die_rate
        self.size = size
        self.speed = speed
        self.color = norm_color
        self.norm_color = norm_color
        self.hit_color = hit_color
        self.atk = atk
    def is_hit(self,bullet,chara,damage):
        if (bullet.pos.x < self.pos.x+self.size and bullet.pos.x > self.pos.x-self.size) and (bullet.pos.y < self.pos.y+self.size and bullet.pos.y > self.pos.y-self.size):
            self.health -= damage
            self.color = self.hit_color
            if(self.health <= 0):
                if(self.speed < 320):
                    self.speed += 20
                elif(1 == random.randrange(1,self.die_rate,1)):
                    enemies.remove(self)
                    return
                print('died')
                chara.score += 1
                x = random.randrange(0,width,1)
                y = random.randrange(0,height,1)
                print(x,y)
                self.pos.x = x
                self.pos.y = y
                self.health = self.max_health
                if(1 == random.randrange(1,self.respawn_rate,1)):
                    print("you got a new enemy!")
                    blob = enemy(18,20,100,"green","darkgreen",self.die_rate,self.respawn_rate,self.atk)
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
        chara.stomp()
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
    pygame.draw.circle(screen, chara.color, chara.pos, chara.size)
    healthbar(chara.max_health,chara.health)

    chara.hit_this_tick = False

    # handles tele-cooldown
    if(chara.tele_cooldown > 0):
        chara.tele_cooldown -= 1
    if(chara.stomp_cooldown > 0):
        chara.stomp_cooldown -= 1

def damage_display(pos,atk,offset):
    hit_text = font2.render(str(atk), True, (255, 100, 20))
    text_rect = hit_text.get_rect()
    off = pygame.Vector2(offset*random.randrange(-10,10,1)/10,offset*random.randrange(-10,10,1)/10)
    text_rect.center = (pos.x+off.x,pos.y+off.y)
    screen.blit(hit_text, text_rect)

def enemy_handler():
    for blob in enemies:
        if chara.is_hit(blob):
            damage_display(blob.pos,blob.atk,chara.size)
        blob.move(chara.pos)
        pygame.draw.circle(screen, blob.color, blob.pos, 14)
        blob.healthbar()

    for shot in shots:
        shot.update()
        if shot.direction.length() == 0:
            shots.remove(shot)
        for blob in enemies:
            if blob.is_hit(shot,chara,1):
                damage_display(blob.pos,shot.atk,blob.size)
                try: shots.remove(shot)
                except: True
        if shot.pos.x > width or shot.pos.x < 0 or shot.pos.y > height or shot.pos.y < 0:
            try: shots.remove(shot)
            except: True
        pygame.draw.circle(screen, shot.color, shot.pos, 4)

def update_score(chara):
    # score display
    score_text = font1.render(str(chara.score), True, (0, 255, 0))
    text_rect = score_text.get_rect()
    text_rect.center = (width-(text_rect.width/2)-5, 0+(text_rect.height/2))
    screen.blit(score_text, text_rect)

    # teleports left display
    score_text2 = font1.render(str(chara.teleports), True, (100, 100, 250))
    text_rect2 = score_text2.get_rect()
    text_rect2.center = (width-(text_rect2.width/2)-10-text_rect.width, 0+(text_rect2.height/2))
    screen.blit(score_text2, text_rect2)

    # stomp-cooldown display
    if(chara.stomp_cooldown > 0):
        score_text3 = font1.render(str(chara.stomp_cooldown), True, (100, 100, 250))
        text_rect3 = score_text3.get_rect()
        text_rect3.center = (width-(text_rect3.width/2)-10-text_rect.width-text_rect2.width, 0+(text_rect3.height/2))
        screen.blit(score_text3, text_rect3)

def healthbar(max_value,value):
    # draw healthbar
    scale = width/max_value/3
    x = width/2 - max_value*scale/2+1
    back_rect = pygame.Rect(x-1,0,max_value*scale+2,scale+1)
    base_rect = pygame.Rect(x,0,max_value*scale,scale)
    value_rect = pygame.Rect(x,0,value*scale,scale)
    pygame.draw.rect(screen,"black",back_rect)
    pygame.draw.rect(screen,"white",base_rect)
    pygame.draw.rect(screen,"green",value_rect)

    # draw health points
    score_text = font1.render(str(value)+"/"+str(max_value), True, (255, 255, 255))
    text_rect = score_text.get_rect()
    text_rect.center = (x-(text_rect.width/2)-5, 0+(text_rect.height/2))
    screen.blit(score_text, text_rect)

def update_game():
    pygame.draw.circle(screen, (0,0,255), cursor_pos, 8) # draw cursor

    player_handler(chara)

    enemy_handler()

    update_score(chara) 

    # winscreen
    if(len(enemies) == 0):
        text1 = font2.render("You have achieved something", True, (0, 255, 0))
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

def draw_pause_menu():
    pygame.draw.circle(screen, (0,0,51), cursor_pos, 8)
    for blob in enemies:
        pygame.draw.circle(screen, (blob.color[0]/5,blob.color[1]/5,blob.color[2]/5), blob.pos, 14)
    for shot in shots:
        pygame.draw.circle(screen, (shot.color[0]/5,shot.color[1]/5,shot.color[2]/5), shot.pos, 4)
    pygame.draw.circle(screen, (chara.color[0]/5,chara.color[1]/5,chara.color[2]/5), chara.pos, chara.size)
    score_text = font1.render("this is the menu", True, (0, 255, 0))
    text_rect = score_text.get_rect()
    text_rect.center = (width/2, height/2)
    screen.blit(score_text, text_rect)

chara = player(30,50,5,4,(255,0,0),(100,0,0))
blob = enemy(18,20,100,(0,255,0),(0,100,0),20,10,1)
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
    
    if playing:
        update_game()

    else:
        # TODO something, idk
        draw_pause_menu()

    if keys[pygame.K_ESCAPE] and pause_cooldown == 0:
        if playing:
            pause_cooldown = 20
            playing = False
        else:
            pause_cooldown = 20
            playing = True

    # limits FPS to 60, dt is seconds since last frame, used for fps-independent physics
    dt = clock.tick(60) / 1000
    tick += 1
    tick %= 1000
    if(pause_cooldown > 0):
        pause_cooldown -= 1
    
    # update Screen
    pygame.display.flip()    

pygame.quit()