import pygame
import time
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 800
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
STAR_WIDTH, STAR_HEIGHT = 10, 20
PLAYER_VEL = 5
STAR_VEL = 3
INITIAL_STAR_ADD_INTERVAL = 2000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("METEOR DASH")
FONT = pygame.font.SysFont("comicsans", 30)

BG = pygame.transform.scale(pygame.image.load("space.jpg"), (WIDTH, HEIGHT))
HIT_SOUND = pygame.mixer.Sound("hit.mp3")

pygame.mixer.music.load("background_music.mp3")

def draw(player, elapsed_time, stars, score):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(time_text, (10, 10))
    WIN.blit(score_text, (10, 40))
    pygame.draw.rect(WIN, "red", player)
    for star in stars:
        pygame.draw.rect(WIN, "white", star)
    pygame.display.update()

def main():
    # Start background music and loop it indefinitely
    pygame.mixer.music.play(-1)
    
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = INITIAL_STAR_ADD_INTERVAL
    star_count = 0
    stars = []
    hit = False
    score = 0
    star_vel = STAR_VEL

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(500, star_add_increment - 50)
            star_count = 0
            star_vel += 0.2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += int(star_vel)
            if star.y > HEIGHT:
                stars.remove(star)
                score += 1
            elif star.colliderect(player):
                HIT_SOUND.play()
                hit = True
                break

        if hit:
            pygame.mixer.music.stop()
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars, score)

    pygame.quit()

if __name__ == "__main__":
    main()
