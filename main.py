import pygame

pygame.init()
FRAMES = 60
screen = pygame.display.set_mode((1024, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

        # fill screen with a color to wipe away anything from last frame
    screen.fill("blue")

    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] :
        player_pos.y -= 300 * dt
    if keys[pygame.K_s] :
        player_pos.y += 300 * dt
    if keys[pygame.K_a] :
        player_pos.x -= 300 * dt
    if keys[pygame.K_d] :
        player_pos.x += 300 * dt

    pygame.display.flip()

    dt = clock.tick(FRAMES) / 1000

pygame.quit()