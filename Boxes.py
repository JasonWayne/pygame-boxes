import pygame


class BoxesGame():
    def __init__(self):
        pygame.init()
        width, height = 389, 489
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Boxes")
        self.clock = pygame.time.Clock()

    def update(self):
        # test result: 60 frames per second
        # but why 60, what the meaning of this number
        self.clock.tick(60)

        self.screen.fill(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        pygame.display.flip()


bg = BoxesGame()
while 1:
    bg.update()

