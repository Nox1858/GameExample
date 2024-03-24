import pygame
import random
from game import keys,enemy_group,cursor_pos, shots, tick, width, height, screen, dt, font1, font2, chara

def damage_display(pos,atk,offset):
    hit_text = font2.render(str(atk), True, (255, 100, 20))
    text_rect = hit_text.get_rect()
    off = pygame.Vector2(offset*random.randrange(-10,10,1)/10,offset*random.randrange(-10,10,1)/10)
    text_rect.center = (pos.x+off.x,pos.y+off.y)
    screen.blit(hit_text, text_rect)

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

def run():
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
        enemy_group.clear()
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

    for blob in enemy_group:
        if chara.is_hit(blob):
            damage_display(blob.pos,blob.atk,chara.size)
        blob.move(chara.pos)
        pygame.draw.circle(screen, blob.color, blob.pos, 14)
        blob.healthbar()

    for shot in shots:
        shot.update()
        if shot.direction.length() == 0:
            shots.remove(shot)
        for blob in enemy_group:
            if blob.is_hit(shot,chara,1):
                damage_display(blob.pos,shot.atk,blob.size)
                try: shots.remove(shot)
                except: True
        if shot.pos.x > width or shot.pos.x < 0 or shot.pos.y > height or shot.pos.y < 0:
            try: shots.remove(shot)
            except: True
        pygame.draw.circle(screen, shot.color, shot.pos, 4)