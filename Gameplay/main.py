import pygame as pg
# from my_menU import men
from logic_of_game import Game

pg.init()
FINN = ((13, 14, 15, 16), (40, 40, 41, 41, 28, 28, 26, 26, 31, 31, 36, 36, 37,
                           33, 33, 29, 29, 34, 27, 27, 35, 35, 32, 32, 30, 42,
                           16, 16, 44, 44, 43, 43, 45, 45,
                           39, 39, 38, 21, 21, 20))  # наборы карт
JAKE = (
    (1, 2, 3, 4), (20, 25, 25, 22, 23, 24, 1, 1, 11, 12, 12, 2, 2, 7, 7, 9, 9,
                   14, 14, 13, 13, 8, 8, 6, 6, 4, 3, 10,
                   5, 5, 16, 16, 18, 18, 19, 19, 17, 15, 21, 20, 20))
# Размер экрана
size = W, H = (pg.display.Info().current_w, pg.display.Info().current_h)
screen = pg.display.set_mode(size)
game = Game(screen, W, H, [FINN, JAKE], [("player 1", 0), ("player 2", 1)])
game.start_game()

pg.quit()
