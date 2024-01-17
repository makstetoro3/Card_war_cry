import pygame as pg
from card import Card
from land import Land
from player import Player
from random import randint
from window import Window
from random import shuffle
from animation import AnimatedSprite


class Game:
    def __init__(self, screen: pg.Surface, W: int, H: int,
                 decks: list,
                 name: list) -> None:
        self.W = W
        self.H = H
        self.screen = screen
        self.size: tuple[int, int] = W, H  # размеры экрана
        self.FPS: int = 30  # частота кадров
        self.clock = pg.time.Clock()
        self.runGame = True  # Цикл игры

        self.card_h = H // 3  # высота поля
        self.card_w = int(self.card_h * 0.7)  # ширина поля
        self.sard_h = self.card_w  # высота карты
        self.sard_w = int(self.sard_h * 0.72)  # ширина карты

        # расположение кладбища
        self.cemetery = ((W >> 1) - int(self.card_w * 3.7), (H >> 2))
        # расположение добора
        self.deck = ((W >> 1) - int(self.card_w * 2.85), (H >> 1))
        # расположение добора противника
        self.deck_2 = ((W >> 1) - int(self.card_w * 2.85), (H >> 1) - self.card_h)
        # расположение кладбища противника
        self.cemetery_2 = ((W >> 1) - int(self.card_w * 3.7), (H >> 1) - self.card_h)

        # rect для проверки, что карту переместили вверх
        self.rect_attack = pg.Rect((W >> 1) - (self.card_w << 1),
                                   (H >> 1) - self.sard_w, self.card_w << 2, self.sard_w)
        # rect для проверки, что карту переместили вниз
        self.rect_floop = pg.Rect((W >> 1) - (self.card_w << 1),
                                  (H >> 1) + self.card_h, self.card_w << 2, self.sard_w)
        # rect для проверки, что карту переместили вниз версия для строений
        self.rect_floop_building = pg.Rect((W >> 1) - (self.card_w << 1),
                                           (H >> 1) + self.card_h - self.sard_w, self.card_w << 2,
                                           self.sard_w)

        # кнопка конец
        self.btn_end = pg.Rect((self.sard_h >> 2, H - (self.sard_w >> 1)), (self.card_h, self.sard_h >> 2))
        # отступ для расположения кары на поле по горизонтали
        self.size_rect_x = self.sard_w // 20 * 4.75 + (W >> 1)
        # отступ для расположения кары на поле по вертикали
        self.size_rect_y = self.sard_h // 7

        # rect кладбища
        self.cem_win_rect = pg.Rect((W >> 1) - (self.sard_w << 2), 0, (self.sard_w << 3), H)
        self.cem_win_sur = pg.Surface((self.sard_w << 3, H))  # холст кладбища
        # кнопка открытия кладбища
        self.btn_cem = pg.Rect((W >> 1) - int(self.card_w * 3.7), H >> 1, self.sard_w, self.sard_h)
        # btn_cem_2 = pg.Rect((W >> 1) - int(card_w * 3.7),
        # (H >> 1) - card_h, self.sard_w, sard_h) на будущее

        self.player1 = Player(decks.pop((r := randint(-1, 1))), name.pop(r))
        self.player2 = Player(decks.pop(0), name.pop(0))

        # позиция очков здоровья первого игрока
        self.hp_pos = ((W >> 1) - int(self.card_w * 3.15), H - self.sard_w)
        # позиция очков действий игрока
        self.action_pos = ((W >> 1) - int(self.card_w * 2.55), H - self.sard_w)

        # позиция здоровья второго игрока
        self.hp_pos_2 = ((W >> 1) + int(self.card_w * 3.15), self.sard_w)
        # позиция количество карт
        self.count_card_pos = ((W >> 1) + int(self.card_w * 2.55), self.sard_w)

        # фон игры
        self.bg = pg.transform.scale(pg.image.load("../data/bg.png"), self.size)

        self.deck_card = pg.transform.scale(pg.image.load("../cards/back.png"),
                                            (self.sard_w, self.sard_h))  # картинка добора
        self.btn_deck = pg.Rect(*self.deck, self.sard_w, self.sard_h)  # rect кнопки добора

        self.rect_card = ([pg.Rect(self.size_rect_x + self.card_w * (1 - i),
                                   self.size_rect_y + (H >> 1), self.sard_w, self.sard_h)
                           for i in range(4)],
                          [pg.Rect(self.size_rect_x + self.card_w * (1 - i), self.card_h + (H >> 1),
                                   self.sard_w, self.sard_h) for i in
                           range(4)])  # расположение карт первого игрока на полях
        self.rect_card_2 = (
            [pg.Rect(self.size_rect_x + self.card_w * (1 - i),
                     - self.size_rect_y + (H >> 1) - self.sard_h, self.sard_w, self.sard_h)
             for i in range(4)],
            [pg.Rect(self.size_rect_x + self.card_w * (1 - i),
                     - self.sard_h + (H >> 1) - self.card_h, self.sard_w, self.sard_h)
             for i in range(4)])  # расположение карт второго игрока на полях

        # расположение руки
        self.hand = pg.Surface((int(self.card_w * 1.6), int(self.card_h * 2.1)))
        self.hand_rect = pg.Rect((W >> 1) + int(self.card_w * 2.1),
                                 (H >> 1) - self.sard_h, *self.hand.get_size())

        self.win = None
        self.cem_win = 0  # открытое кладбище

        self.count_turn = 0  # количество ходов
        self.window = Window(True)  # открытое окно

        self.spit_Finn = AnimatedSprite(
            pg.transform.scale(pg.image.load('../data/zzzFinn.png'), (3600, 450)),
            8, 1, W // 2 - 225, H // 2 - 255)  # анимация перехода
        self.spit_Jack = AnimatedSprite(
            pg.transform.scale(pg.image.load('../data/Jack.png'), (7752, 408)),
            19, 1, W // 2 - 225, H // 2 - 255)  # анимация перехода
        self.cur = Card(self.player1, self.player2)  # карта, которую перемещаем
        self.opening = False
        self.between = True  # переход
        self.slider = 0  # колёсико мыши для руки
        self.timeee = True  # цикл хода
        self.attack = False  # фаза атаки
        self.cry = Card(self.player1, self.player2)

    def draw_game(self):
        self.screen.blit(self.bg, (0, 0))  # отрисововаем фон

        if len(self.player1.pack):
            self.screen.blit(self.deck_card, self.deck)
        if len(self.player2.pack):
            self.screen.blit(pg.transform.rotate(self.deck_card, 180), self.deck_2)

        self.player1.land.draw(self.screen)
        self.player2.land.draw(self.screen)

        self.hand.fill((50, 0, 0))

        if self.window:
            self.window.draw(self.screen)
        else:
            surs = pg.Surface((self.sard_w, self.sard_h), pg.SRCALPHA)  # подсветка мест
            surs.fill((255, 255, 0, 127))

            car = list(filter(lambda j: j and j.status == 3, [*(self.player1.active_cards[0]),
                                                              *(self.player2.active_cards[1])]))
            if self.cur and self.cur.status == 3:
                for i in range(4):
                    if not self.player1.get_active_cards(self.cur.object)[i]:
                        ract = self.rect_card[self.cur.object][i]
                        self.screen.blit(surs, ract)
                        pg.draw.rect(self.screen, (255, 255, 0),
                                     ((ract.x - self.sard_w * 0.05,
                                       ract.y - self.sard_w * 0.05),
                                      (self.sard_w * 1.1, self.sard_h + self.sard_w * 0.1)),
                                     int(self.sard_w * 0.05))
            elif not self.cur and len(car):
                for i in list(map(lambda cars: self.rect_card[cars.object][cars.land], car)):
                    self.screen.blit(surs, i)
                    pg.draw.rect(self.screen, (255, 255, 0),
                                 ((i.x - self.sard_w * 0.05, i.y - self.sard_w * 0.05),
                                  (self.sard_w * 1.1, self.sard_h + self.sard_w * 0.1)),
                                 int(self.sard_w * 0.05))
            elif self.cur and self.cur.status == 0 and self.cur.object < 2:
                for i in self.rect_card[self.cur.object]:
                    self.screen.blit(surs, i)
                    pg.draw.rect(self.screen, (255, 255, 0),
                                 ((i.x - self.sard_w * 0.05, i.y - self.sard_w * 0.05),
                                  (self.sard_w * 1.1, self.sard_h + self.sard_w * 0.1)),
                                 int(self.sard_w * 0.05))
            elif self.cur and self.cur.status == 0 and self.cur.object == 2:
                # подсветка мест
                surs = pg.Surface((self.card_w << 2, self.card_h), pg.SRCALPHA)
                surs.fill((255, 255, 0, 127))
                self.screen.blit(surs, ((self.W >> 1) - (self.card_w << 1), self.H >> 1))
                pg.draw.rect(self.screen, (255, 255, 0),
                             pg.Rect((self.W >> 1) - (self.card_w << 1),
                                     self.H >> 1, self.card_w << 2, self.card_h), 8)
            if self.attack:
                for i in list(filter(lambda cb: cb and cb.case == 0,
                                     self.player1.active_cards[0])):
                    self.screen.blit(surs, self.rect_card[0][i.land])
                    pg.draw.rect(self.screen, (255, 255, 0),
                                 ((self.rect_card[0][i.land].x - self.sard_w * 0.05,
                                   self.rect_card[0][i.land].y - self.sard_w * 0.05),
                                  (self.sard_w * 1.1, self.sard_h + self.sard_w * 0.1)),
                                 int(self.sard_w * 0.05))

        pg.draw.circle(self.screen, (200, 0, 0), self.hp_pos, self.sard_h >> 2)  # 1 игрок
        pg.draw.circle(self.screen, (100, 0, 0), self.hp_pos, self.sard_h >> 2, 10)
        pg.draw.circle(self.screen, (0, 200, 0), self.action_pos, self.sard_h >> 2)
        pg.draw.circle(self.screen, (0, 100, 0), self.action_pos, self.sard_h >> 2, 10)
        pg.draw.rect(self.screen, (150, 0, 0), self.btn_end)
        font = pg.font.Font('../data/base.ttf', 32)

        if not self.attack and (len(
                list(filter(lambda j: j and j.status == 2,
                            self.player1.active_cards[0]))) - len(
            list(filter(lambda h: h and self.player2.active_cards[0][h.land] and not
            self.player2.active_cards[0][h.land].can_take,
                        self.player1.active_cards[0])))) and self.count_turn > 1:
            text = font.render('напасть', True, (0, 0, 0))
        else:
            text = font.render('закончить ход', True, (0, 0, 0))

        self.screen.blit(text, (self.btn_end.center[0] - (text.get_width() >> 1),
                                self.btn_end.center[1] - (text.get_height() >> 1)))
        pg.draw.circle(self.screen, (200, 0, 0), self.hp_pos_2, self.sard_h >> 2)  # 2 игрок
        pg.draw.circle(self.screen, (100, 0, 0), self.hp_pos_2, self.sard_h >> 2, 10)
        font = pg.font.Font('../data/base.ttf', 48)
        self.screen.blit(font.render(str(self.player1.HP), True, (25, 25, 20)),
                         (self.hp_pos[0] * 0.8, self.hp_pos[1] * 0.97))
        self.screen.blit(font.render(str(self.player1.action), True, (25, 25, 20)),
                         (self.action_pos[0] * 0.93, self.action_pos[1] * 0.97))
        self.screen.blit(font.render(str(self.player2.HP), True, (25, 25, 20)),
                         (self.hp_pos_2[0] * 0.98, self.hp_pos_2[1] * 0.83))
        self.screen.blit(pg.transform.scale(pg.image.load('../cards/back.png'),
                                            (self.sard_w >> 1, self.sard_h >> 1)),
                         (self.count_card_pos[0] * 0.965, self.count_card_pos[1] * 0.65))
        self.screen.blit(font.render(str(len(self.player2.hand)), True, (25, 25, 20)),
                         (self.count_card_pos[0] * 0.98, self.count_card_pos[1] * 0.83))
        if not self.window or (self.window.tipe == 0 or not self.window.kw['zona']):
            [i.draw(self.screen, 0, case_10=(-self.size_rect_x + (self.W >> 1), -self.size_rect_y),
                    case_20=((self.W >> 1) - self.size_rect_x, -self.size_rect_y + self.sard_w),
                    case_21=((self.W >> 1) - self.size_rect_x, 0)) for i in self.player1.cards]
        if not self.window or (self.window.tipe == 1 and self.window.kw['zona']):
            [i.draw(self.screen, 180, case_10=((self.W >> 1) - self.size_rect_x,
                                               self.size_rect_y + self.sard_h - self.sard_w),
                    case_20=((self.W >> 1) - self.size_rect_x, self.size_rect_y + self.sard_h -
                             (self.sard_w << 1)),
                    case_21=((self.W >> 1) - self.size_rect_x, +self.sard_h - self.sard_w))
             for i in self.player2.cards if i != self.cur]
        [i.drawing(self.hand, (self.hand_rect.x, self.hand_rect.y)) for i in self.player1.hand]
        self.screen.blit(self.hand, self.hand_rect)
        if self.player1.cemetery:
            self.screen.blit(list(self.player1.cemetery)[-1].image, self.cemetery)
        if self.player2.cemetery:
            self.screen.blit(
                pg.transform.rotate(list(self.player2.cemetery)[-1].image, 180),
                self.cemetery_2)
        if self.cur and self.cur.status != 3:
            self.screen.blit(self.cur.image, self.cur.rect)
        if pg.key.get_pressed()[pg.K_LALT]:
            [self.screen.blit(card.alt(pg.image.load(f'../cards/{card.id}.png'),
                                       (self.card_w * 3, self.H)), pg.Rect(
                (self.W >> 1) - self.card_w * 1.5, 0, self.card_w * 3, self.H))
             for card in self.player1.cards
             if card.rect.collidepoint(pg.mouse.get_pos())]
            [self.screen.blit(card.alt(pg.image.load(f'../cards/{card.id}.png'),
                                       (self.card_w * 3, self.H)), pg.Rect(
                (self.W >> 1) - self.card_w * 1.5, 0, self.card_w * 3, self.H))
             for card in self.player1.hand
             if card.rect.collidepoint(pg.mouse.get_pos())]
            [self.screen.blit(card.alt(pg.image.load(f'../self.cards/{card.id}.png'),
                                       (self.card_w * 3, self.H)), pg.Rect(
                (self.W >> 1) - self.card_w * 1.5, 0, self.card_w * 3, self.H))
             for card in self.player2.cards
             if card.rect.collidepoint(pg.mouse.get_pos())]
            if self.window:
                x, y = pg.mouse.get_pos()
                len_win = self.sard_w * (len(self.window.cards) / 2)
                test_x = (self.W >> 1) + len_win > x > (self.W >> 1) - len_win
                test_y = ((self.window.rect.h >> 1) - (self.sard_h >> 1) < y < (self.window.rect.h >> 1) +
                          (self.sard_h >> 1))
                if test_x and test_y:
                    self.screen.blit(
                        (card := self.window.cards[
                            (x - (self.W >> 1) + int(len_win)) // self.sard_w]).alt(
                            pg.image.load(f'../cards/{card.id}.png'),
                            (self.card_w * 3, self.H)), pg.Rect((self.W >> 1) - self.card_w * 1.5, 0,
                                                                self.card_w * 3, self.H))

    def recalculation(self):

        for card in (self.player1.get_active_cards(3) +
                     self.player2.get_active_cards(3)):
            print(card)
            card.recalculation()

        for card in (*self.player1.active_cards[0], *self.player2.active_cards[0]):
            card.specifications()

    def button_up_event1(self):
        if self.btn_cem.collidepoint(pg.mouse.get_pos()) and self.player1.cemetery:
            self.cem_win = 1  # открытие кладбища
        # if btn_cem_2.collidepoint(pg.mouse.get_pos()) and self.player2.cemetery:
        #     cem_win = 2 на будущее
        if self.btn_end.collidepoint(pg.mouse.get_pos()):  # удачи)
            if not (a := len(list(filter(lambda j: j and j.status == 2,
                                         self.player1.active_cards[0]))) - len(
                list(filter(lambda h: h and self.player2.active_cards[0][h.land] and not
                self.player2.active_cards[0][h.land].can_take,
                            self.player1.active_cards[0])))) or self.count_turn < 2:
                self.timeee = False
            if not self.attack and a and self.count_turn > 1:
                self.attack = True
            del a
        if self.cur:
            if self.cur.object < 2:
                for i in range(4):
                    if not self.attack and (
                            self.cur.type == 5 or len(list(filter(lambda lan:
                                                                  lan.type == self.cur.type,
                                                                  self.player1.land))) >= self.cur.price) and \
                            self.rect_card[self.cur.object][i].colliderect(
                                self.cur.rect) and (
                            (self.cur.status < 2 and self.player1.action >= self.cur.price) or
                            (self.cur.status == 3 and not self.player1.active_cards[
                                self.cur.object][i])):
                        if self.cur.status != 3 and (
                                len(self.player1.hand) > 1 or self.cur.id != 4):
                            self.player1.cards.add(self.cur)
                            self.player1.action -= self.cur.price
                            self.player1.hand.remove(self.cur)
                            [a.location(n, self.slider) for n, a in
                             enumerate(self.player1.hand)]
                            self.cry = Card(self.player1, self.player2)
                            if self.player1.active_cards[self.cur.object][i]:
                                # сброс
                                if self.cur.id != 4:
                                    if self.player1.active_cards[self.cur.object][i].dead_spell:
                                        self.player1.active_cards[
                                            self.cur.object][i].dead_spell()
                                    self.player1.active_cards[self.cur.object][i].dead()
                                else:
                                    self.cry = self.player1.active_cards[self.cur.object][i]
                                    self.player1.active_cards[self.cur.object][i].land = -1
                                    # перемещаем карту
                            self.cur.set_land(self.rect_card[self.cur.object][i].copy(), i)
                            self.cur.status = 2  # устанавливаем новый статус карты
                            if self.cur.spawn_spell:
                                self.cur.spawn_spell(self.cur)
                        else:
                            # перемещаем карту
                            self.cur.set_land(self.rect_card[self.cur.object][i].copy(), i)
                            for k in list(
                                    filter(lambda x: x,
                                           self.player1.active_cards[self.cur.object])):
                                if k.status == 3:
                                    k.status = 2
                        print(self.cur, 9)
                        self.recalculation()
            if not self.attack and self.cur.object == 2 and pg.Rect(
                    (self.W >> 1) - (self.sard_w << 1), self.H >> 1, self.sard_w << 2,
                    self.sard_h).colliderect(self.cur.rect) \
                    and self.player1.action >= self.cur.price:
                self.player1.magic.append(self.cur)
                self.player1.action -= self.cur.price
                self.cur.turn_use = self.count_turn
                self.cur.spawn_spell(self.cur)
                self.cur.dead(True)
                for n, card in enumerate(self.player1.hand):
                    card.location(n, self.slider)
            if self.count_turn > 1:  # or (self.cur.object == 0 and self.cur.status == 3)
                if not self.attack:
                    if self.cur.object == 0 and self.rect_floop.colliderect(self.cur.rect) and \
                            self.cur.status == 2 and self.cur.floop and \
                            self.player1.action >= self.cur.floop_price:
                        self.cur.case = 2
                        self.cur.status = 1
                        self.cur.turn_use = self.count_turn
                        self.cur.floop_spell(self.cur)
                        self.player1.action -= self.cur.floop_price
                    if self.cur.object == 1 and self.rect_floop_building.colliderect(
                            self.cur.rect) and \
                            self.cur.status == 2 and self.cur.floop and \
                            self.player1.action >= self.cur.floop_price:
                        self.cur.case = 2
                        self.cur.status = 1
                        self.cur.turn_use = self.count_turn
                        self.cur.floop_spell()
                        self.player1.action -= self.cur.floop_price
                elif self.cur.object == 0 and self.rect_attack.colliderect(
                        self.cur.rect) and self.cur.status == 2 and \
                        (not self.player2.active_cards[0][self.cur.land] or
                         self.player2.active_cards[0][self.cur.land].can_take):
                    self.cur.case = 1
                    self.cur.status = 1
                    if e_cur := self.player2.active_cards[0][self.cur.land]:
                        self.cur.take(e_cur.take(self.cur.atc if e_cur.can_take else 0))
                    else:
                        self.player2.HP -= self.cur.atc
            self.cur.zeroing()  # возращаем карту на место
            self.cur = Card(self.player1, self.player2)

    def button_down_event1(self):
        pg.mouse.get_rel()  # обнуляем относительную позицию
        if not self.attack and self.btn_deck.collidepoint(pg.mouse.get_pos()) and \
                len(self.player1.pack) and \
                self.player1.action > 0:
            self.player1.add_card(Card(self.player1, self.player2, (self.sard_w, self.sard_h),
                                       (self.player1.pack.pop(0)), self.hand_rect))
            self.player1.action -= 1

    def scroll(self, button):
        if button == 4 and self.slider > 0:
            [i.scroll(1) for i in self.player1.hand]
            self.slider -= 1
        if button == 5 and self.slider < (len(self.player1.hand) + 1 >> 1) * 4.1 - 12:
            [i.scroll(-1) for i in self.player1.hand]
            self.slider += 1

    def mouse_motion_button0(self, event):
        if event.buttons[0]:
            if pg.Rect(*pg.mouse.get_pos(), 0, 0).collidelist(
                    a := sum([list(self.player1.hand), list(self.player1.cards)], [])):
                if not self.cur:
                    # сохраняем выбранную карту
                    self.cur = lis[0] if (lis := [card for card in a if
                                                  card.rect.collidepoint(event.pos)
                                                  and (self.hand_rect.collidepoint(
                                                      pg.mouse.get_pos()) or
                                                       card.status >= 2)]) != [] else Card(
                        self.player1, self.player2)
                    del a
                if self.cur:
                    if self.cur.status in (0, 2, 3):
                        # перемещение карты
                        self.cur.rect.move_ip(event.rel)
                    else:
                        self.cur = Card(self.player1, self.player2)

    def window0_button_up_event1(self, event):
        if self.window.btn_ok[0].collidepoint(event.pos[0] - self.window.rect.x,
                                              event.pos[1]):
            for i in self.window.cards:
                self.player1.hand.add(i)
                i.location(len(self.player1.hand) - 1, 0)
            self.player1.add_card(Card(self.player1, self.player2, (self.sard_w, self.sard_h),
                                       self.player1.pack.pop(0), self.hand_rect))
            self.window = Window(True)
        elif self.window.btn_no[0].collidepoint(event.pos[0] - self.window.rect.x,
                                                event.pos[1]):
            self.player1.pack = [*self.player1.pack,
                                 *list(map(lambda car: car.id, self.window.cards))]
            [car.kill() for car in self.window.cards]
            shuffle(self.player1.pack)
            for _ in range(6):
                self.player1.add_card(Card(self.player1, self.player2, (self.sard_w, self.sard_h),
                                           self.player1.pack.pop(0), self.hand_rect))
            self.window = Window(True)

    def window1_mouse_motion_button0(self, event):
        if pg.Rect(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 0, 0).collidelist(
                list(map(lambda x: x.rect, (a := self.window.kw['lis'])))):
            if not self.cur:
                # сохраняем выбранную карту
                self.cur = lis[0] if (lis := [card for card in a if
                                              card.rect.collidepoint(
                                                  event.pos)]) != [] else Card(self.player1,
                                                                               self.player2)
                del a
            if self.cur:
                if self.cur.type in self.window.kw['type'] and self.cur.object in \
                        self.window.kw['object'] \
                        and self.cur.player == self.window.kw['player']:
                    # перемещение карты
                    self.cur.rect.move_ip(event.rel)
                else:
                    self.cur = Card(self.player1, self.player2)

    def window1_mouse_button_up(self, event):
        if self.window.btn_ok[0].collidepoint(event.pos[0] - self.window.rect.x,
                                              event.pos[1] - self.window.rect.y) and \
                len(self.window.cards):
            print(self.window.cards[0], 3)
            self.window.kw['spell'](self.window.cards[0])
            self.recalculation()
            self.window = Window(True)
        if event.button == 1 and self.cur:
            if self.window.rect.colliderect(self.cur.rect):
                self.window.cards = [self.cur]
            self.cur.zeroing()
            self.cur = Card(self.player1, self.player2)

    def cem_def(self):
        if not self.opening:
            if self.cem_win == 1:
                now_cem = self.player1.cemetery
            else:
                now_cem = self.player2.cemetery
            self.cem_win_sur.fill((75, 75, 75))
            for n, card in enumerate(now_cem):
                card.rect = pg.Rect((self.sard_w >> 1) + self.sard_w * 1.5 * (n % 5),
                                    (self.sard_h >> 2) + self.sard_h * 1.25 * (n // 5), self.sard_w,
                                    self.sard_h)
            self.opening = True

    def cem_alt(self, now_cem):
        for card in now_cem:
            if card.rect.collidepoint((pg.mouse.get_pos()[0] - self.cem_win_rect.x, pg.mouse.get_pos()[1])):
                self.screen.blit(card.alt(pg.image.load(f'../cards/{card.id}.png'), (self.card_w * 3, self.H)),
                                 pg.Rect((self.W >> 1) - self.card_w * 1.5, 0, self.card_w * 3, self.H))

    def cem_button_down(self, now_cem, event):
        if event.button == 4 and list(now_cem)[0].rect.y < (self.sard_h >> 2):
            [i.rect.move_ip(0, self.sard_h >> 2) for i in now_cem]
        if event.button == 5 and list(now_cem)[-1].rect.y > self.W - (self.sard_h >> 2):
            [i.rect.move_ip(0, -(self.sard_h >> 2)) for i in now_cem]
        if event.button == 1 and not self.cem_win_rect.collidepoint(pg.mouse.get_pos()):
            self.cem_win = 0
            self.opening = False

    def round(self):
        while self.runGame and self.timeee:
            if not self.cem_win and not self.between:
                self.draw_game()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:  # выход из игры
                        self.runGame = False
                if not self.window and not self.cem_win and not self.between:
                    if event.type == pg.MOUSEBUTTONUP:
                        if event.button == 1:
                            self.button_up_event1()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.button_down_event1()
                        if self.hand_rect.collidepoint(event.pos) and not self.cur:
                            self.scroll(event.button)
                    if event.type == pg.MOUSEMOTION:
                        self.mouse_motion_button0(event)
                elif self.window and not self.between:
                    if self.window.tipe == 0:
                        if event.type == pg.MOUSEBUTTONUP:
                            if event.button == 1:
                                self.window0_button_up_event1(event)
                    elif self.window.tipe == 1:
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                pg.mouse.get_rel()
                        if event.type == pg.MOUSEMOTION:
                            if event.buttons[0]:
                                self.window1_mouse_motion_button0(event)
                        if event.type == pg.MOUSEBUTTONUP:
                            self.window1_mouse_button_up(event)
                elif not self.between:
                    now_cem = self.player1.cemetery
                    self.cem_def()
                    now_cem.draw(self.cem_win_sur)
                    self.screen.blit(self.cem_win_sur, self.cem_win_rect)
                    if pg.key.get_pressed()[pg.K_LALT]:
                        self.cem_alt(now_cem)
                    if pg.key.get_pressed()[pg.K_BACKSPACE]:
                        self.cem_win = 0
                        self.opening = False
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.cem_button_down(now_cem, event)
                else:
                    if pg.key.get_pressed()[pg.K_SPACE]: self.between = False
                if self.player2.HP < 1 or self.player1.HP < 1:
                    self.runGame = False
                    self.win = self.player1 if self.player2.HP < 1 else self.player2
            if self.between:
                self.screen.fill((127, 127, 127))
                if self.player1.id == 1:
                    self.spit_Jack.update()
                    self.spit_Jack.draw(self.screen)
                else:
                    self.spit_Finn.update()
                    self.spit_Finn.draw(self.screen)
                font = pg.font.Font('../data/base.ttf', 64)
                text = font.render(self.player1.name, True, (175, 25, 25))
                self.screen.blit(text, ((self.W >> 1) - (text.get_width() >> 1), self.H - (self.H >> 2)))
                font = pg.font.Font('../data/base.ttf', 48)
                text1 = font.render('нажмите пробел чтобы продолжить', True, (125, 25, 25))
                self.screen.blit(text1, ((self.W >> 1) - (text1.get_width() >> 1), self.H - (self.H >> 3)))

            pg.display.update()
            self.clock.tick(self.FPS)

    def start_game(self) -> None:
        self.draw_game()
        while not self.win and self.runGame:
            self.player1, self.player2 = self.player2, self.player1
            self.cur = Card(self.player1, self.player2)  # карта, которую перемещаем
            self.opening = False
            self.count_turn += 1
            self.between = True  # переход
            self.slider = 0  # колёсико мыши для руки

            self.player1.viev_new_round(self.rect_card)
            self.player2.viev_new_round(self.rect_card_2)

            self.player1.land = pg.sprite.Group()  # создание полей
            self.player2.land = pg.sprite.Group()

            for i in range(4):
                self.player1.land.add(
                    Land(self.player1.land_id[i], ((self.W >> 1) - self.card_w * (i - 1), (self.H >> 1)),
                         (self.card_w, self.card_h), 0, self.player1.land_activ[i]))
                self.player2.land.add(
                    Land(self.player2.land_id[i], ((self.W >> 1) - self.card_w * (i - 1), (self.H >> 1) - self.card_h),
                         (self.card_w, self.card_h), 180, self.player1.land_activ[i]))

            self.timeee = True  # цикл хода
            self.attack = False  # фаза атаки
            self.player1.action = 2  # количество действий

            if self.player1.pack and self.count_turn > 2:  # выдача карты в начале хода
                self.player1.add_card(Card(self.player1, self.player2, (self.sard_w, self.sard_h),
                                           self.player1.pack.pop(0), self.hand_rect))

            for n, card in enumerate(self.player1.hand):
                card.location(n, self.slider)  # расположение карт в руке

            for card in self.player1.cards:  # возращение карт в начальную позицию
                if card and card.case != 0:
                    card.case = 0
                    card.status = 2

            for i in list(filter(lambda x: x and not x.recalculation and x.passive_spell,
                                 self.player1.get_active_cards(0))):
                i.passive_spell()

            # перерасчёт свойств карт
            self.recalculation()

            if self.count_turn <= 2:  # выдача первых 5 карт
                intermediate = [Card(self.player1, self.player2, (self.sard_w, self.sard_h),
                                     self.player1.pack.pop(0), self.hand_rect)
                                for _ in range(5)]
                self.window = Window(False, pg.Rect((self.W >> 1) - (self.card_w << 1), 0,
                                                    (self.card_w << 2), (self.H >> 1)),
                                     'начальные карты', 'принять', 'поменять', 0,
                                     *intermediate)

            self.round()

            for i in list(filter(lambda x: x, self.player1.get_active_cards(0))):
                i.moving(False)
            self.player1.magic = list(
                filter(lambda x: x.recalculation and x.passive_spell, self.player1.magic))
        if self.win:
            eee = True
            self.screen.fill((127, 127, 127))
            if self.win.id == 1:
                spit = AnimatedSprite(pg.transform.scale(pg.image.load(f'../data/dance_1.png'), (11664, 432)), 27, 1,
                                      self.W // 2 - 225, self.H // 2 - 255)
            else:
                spit = AnimatedSprite(pg.transform.scale(pg.image.load(f'../data/dance_0.png'), (9000, 450)), 20, 1,
                                      self.W // 2 - 225, self.H // 2 - 285)
            font = pg.font.Font('../data/base.ttf', 64)
            text = font.render('победитель:', True, (175, 25, 25))
            text_ = font.render(self.win.name, True, (175, 25, 25))
            while eee:
                for _ in pg.event.get():
                    if pg.key.get_pressed()[pg.K_ESCAPE]: eee = False
                self.clock.tick(self.FPS)
                spit.update()
                spit.draw(self.screen)
                self.screen.blit(text, ((self.W >> 1) - (text.get_width() >> 1), self.H - self.H // 3))
                self.screen.blit(text_, ((self.W >> 1) - (text_.get_width() >> 1), self.H - (self.H >> 2)))
                font = pg.font.Font('../data/base.ttf', 48)
                text1 = font.render('нажмите Esc чтобы продолжить', True, (125, 25, 25))
                self.screen.blit(text1, ((self.W >> 1) - (text1.get_width() >> 1), self.H - (self.H >> 3)))
                pg.display.update()
