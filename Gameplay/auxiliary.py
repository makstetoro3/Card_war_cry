from pygame.mouse import get_pos
from player import Player


class Button:
    def __init__(self, rect, function):
        self.rect = rect
        self.func = function

    def pressed(self, *args):
        if self.rect.collidepoint(*get_pos()):
            return self.func(*args)


def recalculation(p1: Player, p2: Player, **kwargs):
    for card in list(filter(None, list(p1.active_cards[0]))):
        card.hp = card.relative_hp
        card.atc = card.default_atc
        if card.passive_spell and card.recalculation: card.passive_spell(enemy=p2, hero=p1, me=card,
                                                                         sard_w=kwargs['sard_w'],
                                                                         sard_h=kwargs['sard_h'],
                                                                         hand_rect=kwargs['hand_rect'])
    for card in list(filter(None, list(p2.active_cards[0]))):
        if not card: continue
        card.hp = card.relative_hp
        card.atc = card.default_atc
        if card.passive_spell and card.recalculation: card.passive_spell(enemy=p1, hero=p2, me=card,
                                                                         sard_w=kwargs['sard_w'],
                                                                         sard_h=kwargs['sard_h'],
                                                                         hand_rect=kwargs['hand_rect'])
    for card in list(filter(None, list(p1.active_cards[1]))):
        if not card: continue
        if card.passive_spell and card.recalculation: card.passive_spell(enemy=p2, hero=p1, me=card,
                                                                         sard_w=kwargs['sard_w'],
                                                                         sard_h=kwargs['sard_h'],
                                                                         hand_rect=kwargs['hand_rect'])
    for card in list(filter(None, list(p2.active_cards[1]))):
        if not card: continue
        if card.passive_spell and card.recalculation: card.passive_spell(enemy=p1, hero=p2, me=card,
                                                                         sard_w=kwargs['sard_w'],
                                                                         sard_h=kwargs['sard_h'],
                                                                         hand_rect=kwargs['hand_rect'])
    [card.specifications() for card in p1.active_cards[0] if card]
    [card.specifications() for card in p2.active_cards[0] if card]
