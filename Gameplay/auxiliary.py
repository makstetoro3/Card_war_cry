import pygame as pg
from player import Player


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
    for card in list(filter(lambda x: x.recalculation, p1.magic)):
        print(card, 4)
        card.passive_spell(enemy=p2, hero=p1, me=card, sard_w=kwargs['sard_w'], turn=kwargs['turn'],
                           sard_h=kwargs['sard_h'], hand_rect=kwargs['hand_rect'])
    for card in list(filter(lambda x: x.recalculation, p2.magic)):
        card.passive_spell(enemy=p1, hero=p2, me=card, sard_w=kwargs['sard_w'], turn=kwargs['turn'],
                           sard_h=kwargs['sard_h'], hand_rect=kwargs['hand_rect'])

    [card.specifications() for card in p1.active_cards[0] if card]
    [card.specifications() for card in p2.active_cards[0] if card]


# ???? ??????????????????
def draw_game(screen, bg, PLAYER_1, deck_card, deck, PLAYER_2, deck_2, hand, window, cur, sard_w,
              sard_h, rect_card, hp_pos, action_pos, btn_end, hp_pos_2,
              count_card_pos, size_rect_x, W, size_rect_y, cards, hand_rect,
              cards_on_hand, cemetery, cemetery_2, card_w, H, card_h, attack, count_turn):
    screen.blit(bg, (0, 0))  # ???????????????????????? ??????
    if len(PLAYER_1.pack):
        screen.blit(deck_card, deck)
    if len(PLAYER_2.pack):
        screen.blit(pg.transform.rotate(deck_card, 180), deck_2)
    PLAYER_1.land.draw(screen)
    PLAYER_2.land.draw(screen)
    hand.fill((50, 0, 0))

    if window: window.draw(screen)

    if not window:
        surs = pg.Surface((sard_w, sard_h), pg.SRCALPHA)  # ?????????????????? ????????
        surs.fill((255, 255, 0, 127))
        if cur and cur.status == 3:
            for i in range(4):
                if not PLAYER_1.active_cards[cur.object][i]:
                    ract = rect_card[cur.object][i]
                    screen.blit(surs, ract)
                    pg.draw.rect(screen, (255, 255, 0),
                                 ((ract.x - sard_w * 0.05, ract.y - sard_w * 0.05),
                                  (sard_w * 1.1, sard_h + sard_w * 0.1)),
                                 int(sard_w * 0.05))
        elif not cur and len(car := list(filter(lambda j: j and j.status == 3, [*PLAYER_1.active_cards[0],
                                                                                *PLAYER_1.active_cards[1]]))):
            for i in list(map(lambda cars: rect_card[cars.object][cars.land], car)):
                screen.blit(surs, i)
                pg.draw.rect(screen, (255, 255, 0), ((i.x - sard_w * 0.05, i.y - sard_w * 0.05),
                                                     (sard_w * 1.1, sard_h + sard_w * 0.1)), int(sard_w * 0.05))
        elif cur and cur.status == 0 and cur.object < 2:
            [screen.blit(surs, i) for i in rect_card[cur.object]]
            [pg.draw.rect(screen, (255, 255, 0),
                          ((i.x - sard_w * 0.05, i.y - sard_w * 0.05), (sard_w * 1.1, sard_h + sard_w * 0.1)),
                          int(sard_w * 0.05)) for i in rect_card[cur.object]]
        elif cur and cur.status == 0 and cur.object == 2:
            surs = pg.Surface((card_w << 2, card_h), pg.SRCALPHA)  # ?????????????????? ????????
            surs.fill((255, 255, 0, 127))
            screen.blit(surs, ((W >> 1) - (card_w << 1), H >> 1))
            pg.draw.rect(screen, (255, 255, 0), pg.Rect((W >> 1) - (card_w << 1), H >> 1, card_w << 2, card_h), 8)
        if attack:
            [screen.blit(surs, rect_card[0][i.land]) for i in list(filter(lambda cb: cb and cb.case == 0,
                                                                          PLAYER_1.active_cards[0]))]
            [pg.draw.rect(screen, (255, 255, 0),
                          ((rect_card[0][i.land].x - sard_w * 0.05, rect_card[0][i.land].y - sard_w * 0.05),
                           (sard_w * 1.1, sard_h + sard_w * 0.1)),
                          int(sard_w * 0.05)) for i in list(filter(lambda cb: cb and cb.case == 0,
                                                                   PLAYER_1.active_cards[0]))]

    pg.draw.circle(screen, (200, 0, 0), hp_pos, sard_h >> 2)  # 1 ??????????
    pg.draw.circle(screen, (100, 0, 0), hp_pos, sard_h >> 2, 10)
    pg.draw.circle(screen, (0, 200, 0), action_pos, sard_h >> 2)
    pg.draw.circle(screen, (0, 100, 0), action_pos, sard_h >> 2, 10)
    pg.draw.rect(screen, (150, 0, 0), btn_end)
    font = pg.font.Font('../data/base.ttf', 32)
    if not attack and (len(
            list(filter(lambda j: j and j.status == 2, PLAYER_1.active_cards[0]))) - len(
        list(filter(lambda h: h and PLAYER_2.active_cards[0][h.land] and not PLAYER_2.active_cards[0][h.land].can_take,
                    PLAYER_1.active_cards[0])))) and count_turn > 1:
        text = font.render('??????????????', True, (0, 0, 0))
    else:
        text = font.render('?????????????????? ??????', True, (0, 0, 0))
    screen.blit(text, (btn_end.center[0] - (text.get_width() >> 1), btn_end.center[1] - (text.get_height() >> 1)))
    pg.draw.circle(screen, (200, 0, 0), hp_pos_2, sard_h >> 2)  # 2 ??????????
    pg.draw.circle(screen, (100, 0, 0), hp_pos_2, sard_h >> 2, 10)
    font = pg.font.Font('../data/base.ttf', 48)
    screen.blit(font.render(str(PLAYER_1.HP), True, (25, 25, 20)), (hp_pos[0] * 0.8, hp_pos[1] * 0.97))
    screen.blit(font.render(str(PLAYER_1.action), True, (25, 25, 20)),
                (action_pos[0] * 0.93, action_pos[1] * 0.97))
    screen.blit(font.render(str(PLAYER_2.HP), True, (25, 25, 20)), (hp_pos_2[0] * 0.98, hp_pos_2[1] * 0.83))
    screen.blit(pg.transform.scale(pg.image.load('../cards/back.png'), (sard_w >> 1, sard_h >> 1)),
                (count_card_pos[0] * 0.965, count_card_pos[1] * 0.65))
    screen.blit(font.render(str(len(PLAYER_2.hand)), True, (25, 25, 20)),
                (count_card_pos[0] * 0.98, count_card_pos[1] * 0.83))
    if not window or (window.tipe == 0 or not window.kw['zona']):
        [i.draw(screen, 0, case_10=(-size_rect_x + (W >> 1), -size_rect_y),
                case_20=((W >> 1) - size_rect_x, -size_rect_y + sard_w),
                case_21=((W >> 1) - size_rect_x, 0)) for i in cards]
    if not window or (window.tipe == 1 and window.kw['zona']):
        [i.draw(screen, 180, case_10=((W >> 1) - size_rect_x, size_rect_y + sard_h - sard_w),
                case_20=((W >> 1) - size_rect_x, size_rect_y + sard_h - (sard_w << 1)),
                case_21=((W >> 1) - size_rect_x, +sard_h - sard_w)) for i in PLAYER_2.cards if i != cur]
    [i.drawing(hand, (hand_rect.x, hand_rect.y)) for i in cards_on_hand]
    screen.blit(hand, hand_rect)
    if PLAYER_1.cemetery: screen.blit(list(PLAYER_1.cemetery)[-1].image, cemetery)
    if PLAYER_2.cemetery: screen.blit(pg.transform.rotate(list(PLAYER_2.cemetery)[-1].image, 180),
                                      cemetery_2)
    if cur and cur.status != 3:
        screen.blit(cur.image, cur.rect)
    if pg.key.get_pressed()[pg.K_LALT]:
        [screen.blit(card.alt(pg.image.load(f'../cards/{card.id}.png'), (card_w * 3, H)),
                     pg.Rect((W >> 1) - card_w * 1.5, 0, card_w * 3, H)) for card in cards
         if card.rect.collidepoint(pg.mouse.get_pos())]
        [screen.blit(card.alt(pg.image.load(f'../cards/{card.id}.png'), (card_w * 3, H)),
                     pg.Rect((W >> 1) - card_w * 1.5, 0, card_w * 3, H)) for card in cards_on_hand
         if card.rect.collidepoint(pg.mouse.get_pos())]
        [screen.blit(card.alt(pg.image.load(f'../cards/{card.id}.png'), (card_w * 3, H)),
                     pg.Rect((W >> 1) - card_w * 1.5, 0, card_w * 3, H)) for card in PLAYER_2.cards
         if card.rect.collidepoint(pg.mouse.get_pos())]
        if window:
            x, y = pg.mouse.get_pos()
            if (W >> 1) + sard_w * (len(window.cards) / 2) > x > (W >> 1) - sard_w * (len(window.cards) / 2) \
                    and (window.rect.h >> 1) - (sard_h >> 1) < y < (window.rect.h >> 1) + (sard_h >> 1):
                screen.blit(
                    (card := window.cards[
                        (x - (W >> 1) + int(sard_w * (len(window.cards) / 2))) // sard_w]).alt(
                        pg.image.load(f'../cards/{card.id}.png'), (card_w * 3, H)), pg.Rect((W >> 1) - card_w * 1.5, 0,
                                                                                            card_w * 3, H))
