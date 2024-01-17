import pygame as pg
from random import shuffle
from card import Card


def id_test(func):
    def _id_test(*args, **kwargs):
        if args[0].id != -1:
            return func(*args, **kwargs)
        return False
    return _id_test


class Player:
    def __init__(self, deck: tuple = (), name=('', -1)):
        self.name: str = name[0]  # имя игрока
        self.id: int = name[1]  # id персонажа
        if name[1] != -1:
            self.pack: list = list(deck[1])  # набор карт
            shuffle(self.pack)  # перемешивание карт
            self.land_id = deck[0]  # номера карт
            self.deck = deck  # id карт персонажа
        self.HP: int = 25  # количество жизней и игрока
        self.action: int = 2  # количество действий и игрока
        self.land = pg.sprite.Group()   # спрайты карт поля
        self.hand = pg.sprite.Group()  # спрайты карт на руке
        self.cards = pg.sprite.Group()  # набор спрайтов игровых карт
        # список карты в бою
        self.active_cards = [[Card(self, self)] * 4 for _ in range(2)]
        # список активных карт полей
        self.land_activ = [True] * 4
        self.cemetery = pg.sprite.Group()  # набор спрайтов для кладбища
        self.magic = []
        self.school = Card(self, self)  # особый эффект карты

    def __eq__(self, other):
        return (self.id == -1) == other

    def get_active_cards(self, type_card: int = -1) -> list[Card]:
        if type_card == -1:
            return self.active_cards[0] + self.active_cards[1]
        if type_card == 3:
            return self.active_cards[0] + self.active_cards[1] + self.magic
        return self.active_cards[type_card]

    def viev_new_round(self, rects) -> None:
        for card, rect in ((self.get_active_cards(i // 4)[i % 4],
                            rects[i // 4][i % 4]) for i in range(8)):
            card.viev(rect)

    @id_test
    def add_card(self, card: Card) -> None:
        self.hand.add(card)
        card.location(len(self.hand) - 1, 0)
