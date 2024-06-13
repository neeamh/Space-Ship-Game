import pygame
import os
pygame.font.init()
pygame.mixer.init()

#font
HEALTH_FONT = pygame.font.SysFont("ArcadeClassic", 40)
WINNER_FONT = pygame.font.SysFont("ArcadeClassic", 80)

#initializing window for game
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactica")

#middle divider
BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH//2 - BORDER_WIDTH/2, 0, BORDER_WIDTH, HEIGHT)

#frames per second
FPS = 60
VEL = 5

#bullets
BULLET_VEL = 10
MAX_BULLETS = 3

#collision events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#sound fx
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

#spaceship settings
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space2.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE_BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health  " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health  " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()

def draw_winner(text, color):
    winner_text = WINNER_FONT.render(text + "   WINS", 1, color)
    WIN.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//2 - winner_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0 - 5: #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VEL < BORDER.x + BORDER.width: #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VEL < HEIGHT - 5: #DOWN
        yellow.y += VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VEL < WIDTH + 15: #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VEL < HEIGHT - 5: #DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    red_health = 5
    yellow_health = 5
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.QUIT()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if yellow_health == 0:
            winner_text = "RED"
            color = RED
        if red_health == 0:
            winner_text = "YELLOW"
            color = YELLOW
        if winner_text != "":
            draw_winner(winner_text, color)
            break
 
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

#makes sure that this file will only run if we run it in this file
if __name__ == "__main__":
    main()