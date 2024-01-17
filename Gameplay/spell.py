from card import Card
from window import Window
from pygame.display import Info
from pygame import Rect
from random import shuffle


# enemy - объект класса player - PLAYER_2
# me - объект класса Card - Карта у которой вызвали этот метод
# hero - объект класса player - PLAYER_1
def d1(self):
    self.enemy.HP -= len(self.enemy.hand)


def p2(self):
    self.hp += len(list(filter(lambda x: x.type == 0 and x.activ, list(self.enemy.land))))
    self.hp += len(list(filter(lambda x: x.type == 0 and x.activ, list(self.player.land))))


def p3(self):
    self.hp += (a := len(list(filter(lambda x: x.type == 0 and x.activ, list(self.player.land)))))
    if a <= 3:
        self.atc += 1


def s4(self, cry: Card, **kwargs):
    if self.player.hand:
        kwargs['window'][0] = Window(False,
            Rect((Info().current_w >> 1) - (self.sard_h << 1), 0,
                 self.sard_h << 2,
                 Info().current_h >> 1), 'выберите карту с руки', 'ок',
            '', 1, type=(0, 3, 5), object=(0, 1, 2),
            player=self.player, spell=f4, me=self,
            lis=self.player.hand, zona=False)
    card = self.player.active_cards[0]
    if cry:
        if self.land > 0 and not card[self.land - 1]:
            cry.set_land(kwargs['rect_card'][0][self.land - 1].copy(),
                         self.land - 1)
        elif self.land < 3 and not card[self.land + 1]:
            cry.set_land(kwargs['rect_card'][0][self.land + 1].copy(),
                         self.land + 1)
        else:
            cry.dead()


def f4(self, card: Card, **kwargs):
    card.dead(True)
    [a.location(n,
                (self.hand.rect.x + int(self.sard_w * 0.125),
                 self.hand.rect.y + int(self.sard_w * 0.125)),
                (self.sard_w, self.sard_h), kwargs['slider'])
     for n, a in enumerate(self.player.hand)
     ]


def s5(self):
    self.enemy.HP -= len(self.enemy.hand)


def p6(self):
    self.atc += (a := len(list(filter(lambda x: x.type == 0 and x.activ,
                                      list(self.player.land)))))
    self.hp += a * 2


def s7(self):
    if self.player.land_activ[self.land]:
        self.player.land_activ[self.land] = False
        list(self.player.land)[self.land].activ = False
        list(self.player.land)[self.land].flip()


def s8(self):
    if self.enemy.active_cards[0][self.land]:
        card = self.enemy.active_cards[0][self.land]
        card.recalculation()
        self.enemy.add_card(card)


def f9(self):
    a = len(list(filter(lambda x: x.type == 0 and x.activ,
                        list(self.player.land))))
    for n, i in enumerate(b := (list(filter(None,
                                            self.enemy.active_cards[0])))):
        print(b)
        if n == a:
            return
        i.take(1, enemy=self.player)


def f10(self):
    if self.enemy.active_cards[1][self.land]:
        self.enemy.active_cards[1][self.land].dead()


def p11(self):
    self.atc += len(list(filter(lambda x: x and x.type == 0,
                                self.player.active_cards[0])))


def p12(self):
    self.atc += 2 if self.land in (1, 2) else 1


def s13(self):
    self.enemy.HP -= len(list(filter(lambda x: x.type == 0 and x.activ,
                                     list(self.player.land))))


def p14(self):
    if self.player.pack:
        self.player.add_card(Card(self.player, self.enemy,
                                  (self.sard_w, self.sard_h), self.player.pack.pop(0)))
    if self.enemy.pack:
        self.enemy.add_card(
            Card(self.enemy, self.player,
                 (self.sard_w, self.sard_h), self.enemy.pack.pop(0)))


def f15(self):
    from random import randint
    card = list(self.enemy.hand)[randint(0, len(list(self.enemy.hand)))]
    self.enemy.cards.remove(card)
    self.player.hand.add(card)
    card.location(len(self.player.hand) - 1,
                  (self.hand.rect.x + int(self.sard_w * 0.125),
                   self.hand.rect.y + int(self.sard_w * 0.125)),
                  (self.sard_w, self.sard_h), 0)
    card.price = 0


def s16(self):
    for i in list(filter(None, self.player.active_cards[0])):
        if i.status == 2:
            i.status = 3


def s17(self):
    for i in list(filter(lambda x: x and x.type == 0,
                         self.player.active_cards[0])):
        i.atc += 1


def p17(self, **kwargs):
    if self.turn_use == kwargs['turn']:
        for i in list(filter(lambda x: x and x.type == 0,
                             self.player.active_cards[0])):
            i.atc += 1
    return self.turn_use == kwargs['turn']


def s18(self):
    for i in range(4):
        if not list(self.player.land)[i].activ:
            self.player.land_activ[i] = True
            list(self.player.land)[i].activ = True
            list(self.player.land)[i].flip()
            break

    for i in list(filter(None, self.player.active_cards[1])):
        if i.status == 2:
            i.status = 3


def s19(self, **kwargs):
    if any(self.enemy.active_cards[0]):
        kwargs['window'][0] = Window(False,
            Rect((Info().current_w >> 1) - (self.sard_h << 1),
                 Info().current_h >> 1, self.sard_h << 2,
                 Info().current_h >> 1), 'выберите существо', 'ок', '', 1,
            type=(0, 3, 5), object=[0], me=self,
            player=self.enemy, spell=f19,
            lis=list(filter(None, self.enemy.active_cards[0])), zona=True)


def f19(self, card: Card, ):
    card.take(self.player.land_activ.count(True), enemy=self.enemy)


def p20(self):
    if self.player.active_cards[0][self.land]:
        self.player.active_cards[0][self.land].atc += 1


def p21(self):
    if self.player.active_cards[0][self.land]:
        self.player.active_cards[0][self.land].hp += 3


def f25(self):
    for i in range(4):
        if not list(self.player.land)[i].activ:
            self.player.land_activ[i] = True
            list(self.player.land)[i].activ = True
            list(self.player.land)[i].flip()
            break


def f26(self):
    from random import randint
    lis = list(filter(lambda x: x.type == 5, list(self.player.cemetery)))
    if lis:
        card = lis[randint(0, len(lis))]
        self.player.cemetery.remove(card)
        self.player.hand.add(card)
        card.location(len(self.player.hand) - 1,
                      (self.hand.rect.x + int(self.sard_w * 0.125),
                       self.hand.rect.y + int(self.sard_w * 0.125)),
                      (self.sard_w, self.sard_h), 0)
    if self.player.active_cards[1][self.land]:
        self.player.action += 1


def p27(self):
    card = self.player.active_cards[0]
    if self.land > 0 and card[self.land - 1]:
        card[self.land - 1].can_take = False
    if self.land < 4 and card[self.land + 1]:
        card[self.land + 1].can_take = False


def f28(self):
    for i in list(filter(None, self.player.active_cards[0])):
        if i.status == 2:
            i.status = 3


def f29(self):
    for _ in range(len(list(filter(lambda x: x and x.case == 2,
                                   list(self.player.active_cards[0]))))):
        self.player.hand.add((a := Card((self.sard_w, self.sard_h),
                                        self.player.pack.pop(0),
                                        self.player)))
        a.location(len(self.player.hand) - 1,
                   (self.hand.rect.x + int(self.sard_w * 0.125),
                    self.hand.rect.y + int(self.sard_w * 0.125)),
                   (self.sard_w, self.sard_h), 0)


def f30(self):
    if self.player.cemetery:
        self.player.cemetery.remove(
            a := list(filter(lambda x: x.object == 2,
                             list(self.player.cemetery)))[0]
        )
        self.player.pack = [a.id, *self.player.pack]


def s31(self, **kwargs):
    if lis := list(filter(lambda c: c and c.case == 2,
                          self.player.active_cards[0])):
        kwargs['window'][0] = Window(False,
            Rect((Info().current_w >> 1) - (self.sard_h << 1), 0,
                 self.sard_h << 2,
                 Info().current_h >> 1), 'выберите существо', 'ок', '', 1,
            type=(0, 3, 5), object=[0],
            player=self.player, spell=f31, me=self,
            lis=lis, zona=False)


def f31(card: Card):
    if card.case != 0:
        card.case = 0
        card.status = 2


def p32(self):
    for i in list(filter(lambda x: x and x.move,
                         list(self.player.active_cards[0]))):
        i.atc += 2


def p33(self):
    for i in list(filter(lambda x: x and x.case == 2,
                         list(self.player.active_cards[0]))):
        i.atc += 2


def p34(self):
    self.atc += len(self.player.magic) * 2


def p35(self):
    if self.move_one:
        self.move_one = False
        self.player.add_card(Card(self.player, self.enemy, (self.sard_w, self.sard_h),
                                  self.player.pack.pop(0), self.hand_rect))


def p36(self):
    card = self.player.active_cards[0]
    if card[self.land] and self.land > 0 and card[self.land - 1]:
        card[self.land - 1].atc += 1
    if card[self.land] and self.land < 3 and card[self.land + 1]:
        card[self.land + 1].atc += 1


def f37(self):
    card = self.enemy.active_cards[0][self.land]
    if card:
        if card.atc > 10:
            card.atc -= 10
        else:
            card.atc = 0


def f38(self, **kwargs):
    if ((card := self.player.active_cards[0][self.land]) and
        (lis := list(filter(lambda x: x.floop_spell,
                            self.player.cemetery)))):
        self.player.school = card.floop_spell, card
        shuffle(lis)
        card.floop_spell = lis[0]
        self.turn_use = kwargs['turn']


def p38(self, **kwargs):
    if self.turn_use != kwargs['turn']:
        self.player.school[0].floop_spell = self.player.school[1]


def f39(self):
    if card := self.player.active_cards[0][self.land]:
        card.status = 3


def f40(self):
    if self.enemy.land_activ[self.land] and (
            self.enemy.land[self.land].type == 0):
        self.enemy.land_activ[self.land] = False
        list(self.enemy.land)[self.land].activ = False
        list(self.enemy.land)[self.land].flip()


def p41(self):
    if not self.enemy.active_cards[0][self.land]:
        self.atc += 3


def s42(self):
    for i in list(filter(lambda x: x and x.move, self.player.active_cards[0])):
        i.atc += 2


def p42(self, **kwargs):
    if self.turn_use == kwargs['turn']:
        for i in list(filter(lambda x: x and x.move,
                             self.player.active_cards[0])):
            i.atc += 2
    return self.turn_use == kwargs['turn']


def s43(self):
    for i in list(filter(None, self.enemy.active_cards[0])):
        i.take(1, enemy=self.player)


def s44(self, **kwargs):
    if len(list(filter(lambda x: x and x.type == 3,
                self.player.active_cards[0]))):
        kwargs['window'][0] = Window(False,
            Rect((Info().current_w >> 1) - (self.sard_h << 1), 0,
                 self.sard_h << 2,
                 Info().current_h >> 1), 'выберите существо', 'ок', '', 1,
            type=[3], object=[0], me=self,
            player=self.player, spell=f44,
            lis=list(filter(None, self.player.active_cards[0])), zona=False)
    else:
        self.turn_use = -1


def f44(self, card: Card):
    self.bav = card
    print(self, card, 5)


def p44(self, **kwargs):
    if self.turn_use == kwargs['turn']:
        print(self, 6)
        self.bav.atc += 2
    return self.turn_use == kwargs['turn']


def s45(self):
    for _ in range(3):
        self.player.add_card(Card(self.player, self.enemy, (self.sard_w, self.sard_h),
                                  self.player.pack.pop(0)))
