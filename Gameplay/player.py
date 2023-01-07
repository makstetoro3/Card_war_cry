import pygame as pg
from random import shuffle


class Player:
    def __init__(self, deck: tuple, name: str, id_: int):
        self.name = name
        self.id = id_
        self.HP = 25
        self.action = 2
        self.pack = list(deck[1])
        shuffle(self.pack)
        self.land_id = deck[0]
        self.land = pg.sprite.Group()
        self.hand = pg.sprite.Group()
        self.deck = deck
        self.cards = pg.sprite.Group()
        self.active_cards = [[None] * 4 for _ in range(2)]
        self.land_activ = [True] * 4
        self.cemetery = pg.sprite.Group()
        self.magic = []
