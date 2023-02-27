import pygame
import sys
import random
import os
from PIL import Image

pygame.font.init()
pygame.__init__
FPS = 50
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
light = (200, 200, 200)
color = pygame.Color('grey12')
ball = pygame.Rect(width // 2 - 15, height // 2 - 15, 30, 30)
player = pygame.Rect(width // 2 - 70, height - 20, 140, 10)
enemy = pygame.Rect(width // 2 - 70, 10, 140, 10)
all_sprites = pygame.sprite.Group
end_sprite = pygame.sprite.Sprite
paus_cout = 0
savex = 0
savey = 0
end_pos_x = -width
speedx = 3
speedy = 3
speed_board = 0
speed_enemy = 0
count = 0
mode = 'pve'


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('press-start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    text_coord = 50
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()




def particles():
    ball = pygame.Rect(width // 2 - 15, height // 2 - 15, 30, 30)
    player = pygame.Rect(width // 2 - 70, height - 20, 140, 10)
    enemy = pygame.Rect(width // 2 - 70, 10, 140, 10)
    return [ball, player, enemy]




def animation():
    global speedy, speedx, count, speed_board, speed_enemy, win_sprite
    ball.x += speedx
    ball.y += speedy
    if ball.top <= 0 and mode == 'pvp':
        return end_load("blue_win.png")
    elif ball.bottom >= height and mode == 'pvp':
        return end_load("red_win.png")
    elif ball.top <= 0:
        return end_load("win_pict.jpg")
    elif ball.bottom >= height:
        return end_load("gameover.jpg")
    if ball.left <= 0 or ball.right >= width:
        speedx *= -1.1
    if ball.colliderect(player) and speed_board > 0:
        speedx += 1
        speedy *= random.randint(1000, 1050) / -1000
        count += 1
    elif ball.colliderect(player) and speed_board < 0:
        speedx -= 1
        speedy *= random.randint(1000, 1050) / -1000
        count += 1
    elif ball.colliderect(player):
        speedy *= random.randint(1000, 1050) / -1000
        count += 1
    if player.left <= 0:
        player.left = 2
    elif player.right >= width:
        player.right = width - 2
    if enemy.left <= 0:
        enemy.left = 2
    elif enemy.right >= width:
        enemy.right = width - 2
    if ball.colliderect(enemy):
        speedy *= random.randint(1000, 1050) / -1000
        count += 1
    if mode == 'pve' and paus_cout % 2 == 0:
        if -5 < enemy.center[0] - ball.center[0] < 5 and enemy.center[0] != ball.center[0]:
            enemy.center = [ball.center[0], 15]
        else:
            if enemy.center[0] > ball.center[0]:
                speed_enemy = -4
            if enemy.center[0] < ball.center[0]:
                speed_enemy = 4
        if enemy.left <= 0:
            enemy.left = 2
        if enemy.right >= width:
            enemy.right = width - 2
    font = pygame.font.Font(None, 50)
    text = font.render(str(count), True, (255, 255, 255))
    screen.fill(color)
    pygame.draw.aaline(screen, light, (0, height // 2), (width, height // 2))
    pygame.draw.rect(screen, 'blue', player)
    pygame.draw.rect(screen, 'red', enemy)
    pygame.draw.ellipse(screen, (125, 250, 0), ball)
    return text


def end_load(res):
    global end_sprite
    end_sprite.image = load_image(res)
    end_sprite.image = pygame.transform.scale(end_sprite.image, (width, height))
    return


while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
                pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
                start()
            elif event.key == pygame.K_p:
                mode = 'pvp'
                speed_enemy = 0
            elif event.key == pygame.K_e:
                mode = 'pve'
            elif event.key == pygame.K_r:
                ball, player, enemy = particles()
                speedx = 3
                speedy = 3
                paus_cout = 0
                count = 0
                end_pos_x = -width
                start_screen()
            elif event.key == pygame.K_SPACE and paus_cout % 2 == 0:
                paus_cout += 1
                savex = speedx
                savey = speedy
                speed_enemy = 0
                speedx = 0
                speedy = 0
            elif event.key == pygame.K_SPACE and paus_cout % 2 == 1:
                paus_cout += 1
                speedx = savex
                speedy = savey
        if mode == 'pvp':
            if event.type == pygame.KEYDOWN and paus_cout % 2 == 0:
                if event.key == pygame.K_d:
                    speed_enemy += 22
                if event.key == pygame.K_a:
                    speed_enemy -= 22
            if event.type == pygame.KEYUP and paus_cout % 2 == 0:
                if event.key == pygame.K_d:
                    speed_enemy -= 22
                if event.key == pygame.K_a:
                    speed_enemy += 22
        if event.type == pygame.KEYDOWN and paus_cout % 2 == 0:
            if event.key == pygame.K_RIGHT:
                speed_board += 22
            if event.key == pygame.K_LEFT:
                speed_board -= 22
        if event.type == pygame.KEYUP and paus_cout % 2 == 0:
            if event.key == pygame.K_RIGHT:
                speed_board -= 22
            if event.key == pygame.K_LEFT:
                speed_board += 22
        if event.type == pygame.QUIT:
            terminate()
    text = animation()
    if type(text) == pygame.Surface:
        enemy.x += speed_enemy
        player.x += speed_board
        screen.blit(text, (646, 10))
        clock.tick(FPS)
    elif end_pos_x <= 0:
        end_pos_x += 700 // 200
        screen.blit(end_sprite.image, (end_pos_x, 0))
    pygame.display.flip()
pygame.quit()
