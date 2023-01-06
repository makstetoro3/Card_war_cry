import pygame as pg


class Window:
    def __init__(self, rect: pg.Rect, title: str, btn_ok: str, btn_no: str, tipe, *args):
        self.rect = rect
        self.title = title
        self.tipe = tipe
        self.cards = args
        self.btn_no = (pg.Rect(0, rect.h * 0.9, rect.w >> 1, rect.h * 0.1), btn_no)
        self.btn_ok = (pg.Rect(rect.w >> 1, rect.h * 0.9, rect.w >> 1, rect.h * 0.1), btn_ok)

    def draw(self, screen: pg.Surface):
        res = pg.Surface(self.rect.size)
        res.fill((100, 100, 100))
        pg.draw.rect(res, (100, 100, 100), self.btn_no[0].inflate(self.rect.w, self.btn_no[0].h))
        font = pg.font.Font('../data/base.ttf', 32)
        text_ok = font.render(self.btn_ok[1], True, (0, 0, 0))
        text_no = font.render(self.btn_no[1], True, (0, 0, 0))
        res.blit(text_no, (
            (self.btn_no[0].w >> 1) - (text_no.get_width() >> 1) + self.btn_no[0].x,
            (self.btn_no[0].h >> 1) - text_no.get_height() + self.btn_no[0].y))
        res.blit(text_ok, (
            (self.btn_ok[0].w >> 1) - (text_ok.get_width() >> 1) + self.btn_ok[0].x,
            (self.btn_ok[0].h >> 1) - text_ok.get_height() + self.btn_ok[0].y))
        text_title = font.render(self.title, True, (0, 0, 0))
        pg.draw.rect(res, (100, 100, 100), pg.Rect(0, 0, self.rect.w, (text_title.get_height() >> 1)))
        res.blit(text_title, ((self.rect.w >> 1) - (text_title.get_width() >> 1), (text_title.get_height() >> 1)))
        screen.blit(res, self.rect)
