import pygame
from game import tick, width, height, dt, enemy_group, shots, screen, bullet
class player():
    def __init__(self, max_health,max_teleports,norm_color,hit_color):
            #dimensions
            self.pos = pygame.Vector2(width/2, height / 2)
            self.size = 50

            #counters
            self.score = 0
            self.health = max_health
            self.max_health = max_health
            self.teleports = max_teleports
            self.tele_cooldown = 0
            self.is_alive = True

            #attacks
            self.shoot_speed = 5
            self.shoot_damage = 1
            self.bullet_speed = 20
            self.stomp_size = 80
            self.stomp_damage = 10
            self.stomp_cooldown = 0
            
            #colors
            self.color = norm_color
            self.norm_color = norm_color
            self.hit_color = hit_color
            self.hit_this_tick = False

    def is_hit(self,enemy):
        if(tick%6 == 0):
            if (enemy.pos.x < self.pos.x+self.size and enemy.pos.x > self.pos.x-self.size) and (enemy.pos.y < self.pos.y+self.size and enemy.pos.y > self.pos.y-self.size):
                self.health -= enemy.atk
                self.color = self.hit_color
                self.hit_this_tick = True
                if(self.health <= 0):
                    print('You Died')
                    print('final score:',self.score)
                    self.is_alive = False
                return True
            elif not self.hit_this_tick:
                self.color = self.norm_color

    def teleport(self,pos):
        if(self.teleports > 0 and self.tele_cooldown == 0):
            self.pos.x = pos[0]
            self.pos.y = pos[1]
            self.teleports -= 1
            self.tele_cooldown = 200

    def shoot(self):
        shots.append(bullet(self,self.bullet_speed,self.shoot_damage,(255,255,0)))

    def stomp(self):
        if(self.stomp_cooldown == 0):
            for blob in enemy_group:
                if(blob.pos.x < self.pos.x+self.stomp_size and blob.pos.x > self.pos.x-self.stomp_size) and (blob.pos.y < self.pos.y+self.stomp_size and blob.pos.y > self.pos.y-self.stomp_size):
                    blob.is_hit(blob,self,8)
            self.stomp_cooldown += 100
            pygame.draw.circle(screen, (100,200,100), self.pos, self.stomp_size)