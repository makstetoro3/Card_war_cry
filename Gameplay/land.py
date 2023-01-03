import pygame as pg


class Land(pg.sprite.Sprite):  # не сделано
    def __init__(self, img, pos, size, r, activ):
        pg.sprite.Sprite.__init__(self)
        self.activ_form = pg.transform.rotate(
            pg.transform.scale(pg.image.load(f'../land/{img}.png').convert_alpha(), size), r)
        self.image = self.activ_form
        self.rect = pg.Rect(*pos, *size)
        self.activ = activ
        self.flip()
        # 0 - кукурузное
        # 3 - равниное
        # 5 - радужное
        self.type = (img - 1) >> 2

    def flip(self):
        if self.activ:
            self.image = self.activ_form
        else:
            self.image = pg.transform.scale(pg.image.load(f'../land/0.png').convert_alpha(), self.rect.size)
