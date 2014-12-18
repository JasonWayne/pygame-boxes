import math

import pygame


class BoxesGame():
    def __init__(self):
        self.EDGE_LENGTH = 64.0
        self.OFFSET = 5.0
        pygame.init()
        pygame.font.init()
        width, height = 389, 489
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Boxes")
        self.clock = pygame.time.Clock()

        # horizon, vertical lines
        # the coordinate are not the same with pygame, but the same to matrix
        # as I am more familiar with the matrices
        self.board_h = [[False for column in range(6)] for row in range(7)]
        self.board_v = [[False for column in range(7)] for row in range(6)]

        self.owner = [[0 for column in range(6)] for row in range(6)]

        self.turn = True
        self.me = 0
        self.other_player = 0
        self.i_win = False

        self.init_graphics()
        # self.finished()


    def init_graphics(self):
        normal_line = "normal_line.png"
        bar_done = "bar_done.png"
        hover_line = "hover_line.png"
        # from vertical to horizontal
        rotate_degree = -90
        self.normal_line_v = pygame.image.load(normal_line)
        self.normal_line_h = pygame.transform.rotate(pygame.image.load(normal_line), rotate_degree)
        self.bar_done_v = pygame.image.load(bar_done)
        self.bar_done_h = pygame.transform.rotate(pygame.image.load(bar_done), rotate_degree)
        self.hover_line_v = pygame.image.load(hover_line)
        self.hover_line_h = pygame.transform.rotate(pygame.image.load(hover_line), rotate_degree)


        self.separators = pygame.image.load("separators.png")
        self.red_indicator = pygame.image.load("red_indicator.png")
        self.green_indicator = pygame.image.load("green_indicator.png")
        self.opponent_marker = pygame.image.load("orange_player.png")
        self.self_marker = pygame.image.load("green_player.png")
        self.winning_screen = pygame.image.load("you_win.png")
        self.lose_screen = pygame.image.load("game_over.png")
        self.score_panel = pygame.image.load("score_panel.png")

    def draw_hud(self):
        white = (255, 255, 255)
        self.screen.blit(self.score_panel, (0, 389))
        my_font_normal = pygame.font.SysFont(None, 32)
        my_font_big = pygame.font.SysFont(None, 64)
        my_font_small = pygame.font.SysFont(None, 20)

        label = my_font_normal.render("Your Turn: ", 1, white)
        score_me = my_font_big.render(str(self.me), 1, white)
        score_other = my_font_big.render(str(self.other_player), 1, white)
        score_text_me = my_font_small.render("You", 1, white)
        score_text_other = my_font_small.render("Other Player", 1, white)

        self.screen.blit(label, (10, 400))
        self.screen.blit(score_text_me, (10, 425))
        self.screen.blit(score_me, (10, 435))
        self.screen.blit(score_text_other, (280, 425))
        self.screen.blit(score_other, (340, 435))
        self.screen.blit(self.green_indicator, [130, 395])

    def draw_board(self):
        for x in range(7):
            for y in range(6):
                if not self.board_h[x][y]:
                    self.blit(self.normal_line_h, x, y)
                else:
                    self.blit(self.bar_done_h, x, y)
        for x in range(6):
            for y in range(7):
                if not self.board_v[x][y]:
                    self.blit(self.normal_line_v, x, y, False)
                else:
                    self.blit(self.bar_done_v, x, y, False)
        #draw the hollow intersections
        for row in range(7):
            for column in range(7):
                self.screen.blit(self.separators, (column * self.EDGE_LENGTH, row * self.EDGE_LENGTH))

    def draw_owner(self):
        you = 1
        other = -1
        for row in range(6):
            for column in range(6):
                if self.owner != 0:
                    if self.owner is you:
                        marker = self.self_marker
                    else:
                        marker = self.opponent_marker
                    self.screen.blit(marker, (column * self.EDGE_LENGTH, row * self.EDGE_LENGTH))

    def blit(self, img, x, y, horizon=True):
        if horizon:
            self.screen.blit(img, (self.EDGE_LENGTH * y + self.OFFSET, self.EDGE_LENGTH * x))
        else:
            self.screen.blit(img, (self.EDGE_LENGTH * y, self.EDGE_LENGTH * x + self.OFFSET))


    def update(self):
        # test result: 60 frames per second
        # but why 60, what the meaning of this number
        self.clock.tick(100)

        self.screen.fill(0)
        self.draw_hud()
        self.draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        self.handle_mouse_events()

        pygame.display.flip()

    def handle_mouse_events(self):
        mouse = pygame.mouse.get_pos()

        # find the nearest intersection
        intersect_row = int(math.ceil(mouse[1] / self.EDGE_LENGTH - 0.5))
        intersect_column = int(math.ceil(mouse[0] / self.EDGE_LENGTH - 0.5))
        # check whether it's closer to the horizontal line or the vertical
        is_horizontal = abs(mouse[1] - intersect_row * self.EDGE_LENGTH) < abs(mouse[0] - intersect_column * self.EDGE_LENGTH)

        # calculate the real column and row
        row = int(math.ceil(mouse[1] / self.EDGE_LENGTH - 0.5)) if is_horizontal \
            else int(mouse[1] / self.EDGE_LENGTH)
        column = int(math.ceil(mouse[0] / self.EDGE_LENGTH - 0.5)) if not is_horizontal \
            else int(mouse[0] / self.EDGE_LENGTH)

        board = self.board_h if is_horizontal else self.board_v
        out_of_bounds = False

        try:
            if not board[row][column]:
                self.screen.blit(self.hover_line_h if is_horizontal else self.hover_line_v,
                                 (column * self.EDGE_LENGTH + self.OFFSET if is_horizontal else column * self.EDGE_LENGTH,
                                     row * self.EDGE_LENGTH if is_horizontal else row * self.EDGE_LENGTH + self.OFFSET))
        except:
            out_of_bounds = True

        if not out_of_bounds:
            already_placed = board[row][column]
        else:
            already_placed = False

        if not already_placed and pygame.mouse.get_pressed()[0] and not out_of_bounds:
            if is_horizontal:
                self.board_h[row][column] = True
            else:
                self.board_v[row][column] = True

    def finished(self):
        self.screen.blit(self.winning_screen if self.i_win else self.lose_screen, (0, 0))
        while 1:
            # this will lower the cpu cost
            # pygame.time.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            pygame.display.flip()




bg = BoxesGame()
while 1:
    bg.update()

