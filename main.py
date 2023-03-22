import pygame

pygame.init()
FRAMES = 60
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

        # fill screen with a color to wipe away anything from last frame
        screen.fill("blue")

        pygame.display.flip()

        clock.tick(FRAMES)

pygame.quit()