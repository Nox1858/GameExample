import random
import pygame
from game import height, width, enemy_group, tick, dt, screen

class enemy():
    def __init__(self,max_health,speed,die_rate,respawn_rate, atk):
            #dimensions
            self.pos = pygame.Vector2(random.randrange(0,width,1),random.randrange(0,height,1))
            self.size = 18

            #counters
            self.health = max_health
            self.max_health = max_health
            self.respawn_rate = respawn_rate
            self.die_rate = die_rate
            self.speed = speed
            self.atk = atk

            #colors
            self.color = "green"
            self.norm_color = "green"
            self.hit_color = "darkgreen"        

    def is_hit(self,bullet,chara,damage):
        if (bullet.pos.x < self.pos.x+self.size and bullet.pos.x > self.pos.x-self.size) and (bullet.pos.y < self.pos.y+self.size and bullet.pos.y > self.pos.y-self.size):
            self.health -= damage
            self.color = self.hit_color
            if(self.health <= 0):
                if(self.speed < 320):
                    self.speed += 20
                elif(1 == random.randrange(1,self.die_rate,1)):
                    enemy_group.remove(self)
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
                    blob = self(20,100,self.die_rate,self.respawn_rate,self.atk)
                    enemy_group.append(blob)
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