# this is a learning project, it was created by modifying an example game from the pygame community
# movement and basic visual engine by a creator from a pygame tutorial, rest by Nox1858


import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200,700))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
font1 = pygame.font.SysFont('Comic Sans MS', 24)
font2 = pygame.font.SysFont('Comic Sans MS', 36)
width = screen.get_width()
height = screen.get_height()

#global variables
playing = True
pause_cooldown = 0
dt = 1
tick = 1
cursor_pos = pygame.Vector2(width/2, height / 2)
shots = []
enemy_group = []

class bullet():
    def __init__(self,chara,speed,atk,color):
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

import handler
import players
import enemies

#visual stuff

def update_scorebar(chara):
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


def update_game():
    pygame.draw.circle(screen, (0,0,255), cursor_pos, 8) # draw cursor

    handler.run()

    update_scorebar(chara) 

    # winscreen
    if(len(enemy_group) == 0):
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
    for blob in enemy_group:
        pygame.draw.circle(screen, (blob.color[0]/5,blob.color[1]/5,blob.color[2]/5), blob.pos, 14)
    for shot in shots:
        pygame.draw.circle(screen, (shot.color[0]/5,shot.color[1]/5,shot.color[2]/5), shot.pos, 4)
    pygame.draw.circle(screen, (chara.color[0]/5,chara.color[1]/5,chara.color[2]/5), chara.pos, chara.size)
    score_text = font1.render("this is the menu", True, (0, 255, 0))
    text_rect = score_text.get_rect()
    text_rect.center = (width/2, height/2)
    screen.blit(score_text, text_rect)


#initialize the game
chara = players.player(50,4,(255,0,0),(100,0,0))
blob = enemies.enemy(20,100,20,10,1)
enemy_group.append(blob)

while chara.is_alive:
    # refresh the screen
    screen.fill("black")

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            chara.is_alive = False
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