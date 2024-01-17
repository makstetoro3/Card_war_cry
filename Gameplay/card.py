import pygame as pg
import sqlite3


def id_test(func):
    def _id_test(*args, **kwargs):
        if args[0].id != -1:
            return func(*args, **kwargs)
        return False
    return _id_test


class Card(pg.sprite.Sprite):  # класс Карты
    # получает размер и id карты
    def __init__(self, hero, enemy,
                 size: tuple = (0, 0), card_id: int = -1,
                 hand_rect=pg.rect.Rect(0, 0, 0, 0),
                 land=-1):
        pg.sprite.Sprite.__init__(self)
        self.id: int = card_id
        self.land = land
        if self.id != -1:
            self.image = pg.transform.scale(
                pg.image.load(f'../cards/{card_id}.png').convert_alpha(), size
                )
            con = sqlite3.connect('../data/card_war.db')
            cur = con.cursor()
            info = cur.execute(
                f'SELECT * FROM cards WHERE id = {card_id}'
                ).fetchall()[0]
        else:
            self.image = pg.transform.scale(
                pg.image.load('../cards/1.png').convert_alpha(), size)
            info = tuple(0 for _ in range(13))
        self.pos = (0, 0)
        self.rect = pg.Rect(0, 0, *size)
        self.default: pg.Rect = self.rect
        self.case = 0
        self.player = hero
        self.can_take = True
        self.move = False
        self.move_one = False
        self.turn_use = 0

        self.status = 0  # свойство карты
        self.price = info[2]
        self.default_price = info[2]
        self.type = info[3]
        self.object = info[4]
        self.recalculation_inf = info[12]
        if not self.object == 2:
            self.floop = info[5]
            self.floop_price = info[6]
            if info[5]:
                exec(f'from spell import f{card_id}')
                exec(f'self.floop_spell = f{card_id}')
            else:
                self.floop_spell = None
            if self.object == 0:
                self.atc = info[7]
                self.default_atc = info[7]
                self.hp = info[8]
                self.default_hp = info[8]
                self.relative_hp = info[8]
                self.specifications()
        if info[9] or self.object == 2:
            exec(f'from spell import s{card_id}')
            exec(f'self.spawn_spell = s{card_id}')
        else:
            self.spawn_spell = None
        if info[10]:
            exec(f'from spell import p{card_id}')
            exec(f'self.passive_spell = p{card_id}')
        else:
            self.passive_spell = None
        if info[11]:
            exec(f'from spell import d{card_id}')
            exec(f'self.dead_spell = d{card_id}')
        else:
            self.dead_spell = None

        # для пасивки
        self.sard_w = size[0]
        self.sard_h = size[1]
        self.hand_rect = hand_rect
        self.enemy = enemy

    @id_test
    def zeroing(self) -> None:  # возращает карту на место (pos)
        self.rect.move_ip(self.pos[0] - self.rect.x, self.pos[1] - self.rect.y)
        self.default.move_ip(self.pos[0] - self.default.x,
                             self.pos[1] - self.default.y)

    @id_test
    def dead(self, hand=False) -> None:  # уберает карту в сброс
        self.pos = (0, 0)
        self.zeroing()
        self.case = 0
        self.status = -1
        self.can_take = True
        self.price = self.default_price
        if self.object in (0, 1):
            self.player.active_cards[self.object][self.land] = None
        if self.object == 0:
            self.hp = self.default_hp
            self.relative_hp = self.default_hp
            self.atc = self.default_atc
            self.specifications()
        if not hand:
            self.player.cards.remove(self)
            self.player.active_cards[self.object][self.land] = None
        else:
            self.player.hand.remove(self)
        self.land = -1
        self.player.cemetery.add(self)

    @id_test
    def set_land(self, land: pg.Rect, ID: int) -> None:
        if land != -1:
            self.player.active_cards[self.object][self.land] = Card(self.player, self.enemy)
            self.moving()
        self.player.active_cards[self.object][ID] = self
        self.rect = land
        self.default = land
        self.pos = (self.rect.x, self.rect.y)
        self.land = ID

    @id_test
    def location(self, n: int, slider: int) -> None:
        self.pos = (
            self.hand_rect.x + int(self.sard_w * 0.125) + self.sard_w * (n & 1),
            self.hand_rect.y + int(self.sard_w * 0.125) + self.sard_h * (n >> 1) - slider * (self.rect.h >> 2))
        self.zeroing()

    @id_test
    def drawing(self, surface: pg.Surface, hand_pos: tuple) -> None:
        surface.blit(self.image,
                     pg.Rect(self.rect.x - hand_pos[0],
                             self.rect.y - hand_pos[1],
                             self.rect.w, self.rect.h))

    @id_test
    def scroll(self, n: int) -> None:
        self.pos = (self.pos[0], self.pos[1] + (self.rect.h >> 2) * n)
        self.zeroing()

    @id_test
    def viev(self, new: pg.Rect):
        self.rect = new.copy()
        self.pos = (new.x, new.y)

    @id_test
    def alt(self, img, size):
        res = pg.transform.scale(img, size)
        if self.object == 0:
            pg.draw.rect(res, (255, 255, 255),
                         pg.Rect(size[0] * 0.819, size[1] * 0.8625,
                                 size[0] * 0.1, size[1] * 0.0721))
            pg.draw.rect(res, (255, 255, 255),
                         pg.Rect(size[0] * 0.101,
                                 size[1] * 0.863, size[0] * 0.08,
                                 size[1] * 0.0725))
            font = pg.font.Font('../data/base.ttf', 48)
            res.blit(font.render(str(self.hp), True,
                                 (0, 0, 0)), (size[0] * 0.819, size[1] * 0.88))
            res.blit(font.render(str(self.atc), True,
                                 (0, 0, 0)), (size[0] * 0.101, size[1] * 0.88))
        return res

    @id_test
    def specifications(self):
        w, h = self.default.w, self.default.h
        pg.draw.rect(self.image, (255, 255, 255),
                     pg.Rect(w * 0.825, h * 0.87,
                             w * 0.095, h * 0.075))
        pg.draw.rect(self.image, (255, 255, 255),
                     pg.Rect(w * 0.1, h * 0.87,
                             w * 0.095, h * 0.075))
        font = pg.font.Font('../data/base.ttf', 12)
        self.image.blit(font.render(str(self.hp), True,
                                    (0, 0, 0)), (w * 0.825, h * 0.88))
        self.image.blit(font.render(str(self.atc), True,
                                    (0, 0, 0)), (w * 0.11, h * 0.88))

    @id_test
    def take(self, damage: int):
        atc = self.atc
        self.hp -= damage
        self.relative_hp -= damage
        self.specifications()
        if self.hp <= 0:
            self.player.HP += self.hp
            if self.dead_spell:
                self.dead_spell()
            self.dead()
        return atc

    @id_test
    def draw(self, surface: pg.Surface, rotate: int, **args):
        rat = rotate
        pos = (self.rect.x, self.rect.y)
        size = (self.rect.w, self.rect.h)
        if self.case:
            rat += 90
            size = (self.rect.h, self.rect.w)
            pos = (
                pos[0]
                + args[f'case_{self.case}{self.object}'][0], pos[1]
                + args[f'case_{self.case}{self.object}'][1]
                )
        image = pg.transform.rotate(self.image, rat)
        surface.blit(image, pg.Rect(*pos, *size))

    @id_test
    def moving(self, boo=True):
        self.move = boo
        self.move_one = boo

    @id_test
    def set_enemy(self, enemy, hero=False):
        self.enemy = enemy
        if hero:
            self.player = hero

    @id_test
    def recalculation(self):
        if self.object == 0:
            self.hp = self.relative_hp
            self.atc = self.default_atc
        if self.passive_spell and self.recalculation_inf:
            self.passive_spell(self)

    def __str__(self):
        return f'Card<{self.id}; {self.land}>'

    def __repr__(self):
        return f'Card<{self.id}; {self.land}>'

    @id_test
    def __getattr__(self, size) -> tuple:
        return self.sard_w, self.sard_h

    def __bool__(self):
        return self.id != -1
