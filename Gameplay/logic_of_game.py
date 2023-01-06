import pygame as pg
from card import Card
from land import Land
from player import Player
from random import randint
from auxiliary import recalculation, draw_game
from window import Window


def pvp(screen: pg.Surface, W: int, H: int, decks: list) -> None:
    size = W, H
    FPS = 30
    clock = pg.time.Clock()
    runGame = True
    card_h = H // 3
    card_w = int(card_h * 0.7)  # размеры карт
    sard_h = card_w
    sard_w = int(sard_h * 0.72)
    cemetery = ((W >> 1) - int(card_w * 3.7), (H >> 1))
    deck = ((W >> 1) - int(card_w * 2.85), (H >> 1))
    deck_2 = ((W >> 1) - int(card_w * 2.85), (H >> 1) - card_h)
    cemetery_2 = ((W >> 1) - int(card_w * 3.7), (H >> 1) - card_h)
    rect_attack = pg.Rect((W >> 1) - (card_w << 1), (H >> 1) - sard_w, card_w << 2, sard_w)
    rect_floop = pg.Rect((W >> 1) - (card_w << 1), (H >> 1) + card_h, card_w << 2, sard_w)
    rect_floop_building = pg.Rect((W >> 1) - (card_w << 1), (H >> 1) + card_h - sard_w, card_w << 2, sard_w)
    btn_end = pg.Rect((sard_h >> 2, H - (sard_w >> 1)), (card_h, sard_h >> 2))
    size_rect_x = sard_w // 20 * 4.75 + (W >> 1)
    size_rect_y = sard_h // 7
    cem_win_rect = pg.Rect((W >> 1) - (sard_w << 2), 0, (sard_w << 3), H)
    cem_win_sur = pg.Surface((sard_w << 3, H))
    btn_cem = pg.Rect((W >> 1) - int(card_w * 3.7), H >> 1, sard_w, sard_h)
    btn_cem_2 = pg.Rect((W >> 1) - int(card_w * 3.7), (H >> 1) - card_h, sard_w, sard_h)
    PLAYER_1 = Player(decks.pop(randint(-1, 1)))
    [PLAYER_1.land.add(Land(PLAYER_1.land_id[i], ((W >> 1) - card_w * (2 - i), (H >> 1)), (card_w, card_h), 0,
                            PLAYER_1.land_activ[i])) for i in range(4)]
    PLAYER_2 = Player(decks.pop(0))
    [PLAYER_2.land.add(
        Land(PLAYER_2.land_id[i], ((W >> 1) - card_w * (2 - i), (H >> 1) - card_h), (card_w, card_h), 180,
             PLAYER_1.land_activ[i])) for i in range(4)]

    hp_pos = ((W >> 1) - int(card_w * 3.15), H - sard_w)
    action_pos = ((W >> 1) - int(card_w * 2.55), H - sard_w)

    hp_pos_2 = ((W >> 1) + int(card_w * 3.15), sard_w)
    count_card_pos = ((W >> 1) + int(card_w * 2.55), sard_w)

    bg = pg.transform.scale(pg.image.load("../data/bg.png"), size)  # фон и атрибуты игры
    deck_card = pg.transform.scale(pg.image.load("../cards/back.png"), (sard_w, sard_h))
    btn_deck = pg.Rect(*deck, sard_w, sard_h)
    # Расположение существ на полях
    rect_card = ([pg.Rect(size_rect_x + card_w * (1 - i), size_rect_y + (H >> 1), sard_w, sard_h) for i in range(4)],
                 [pg.Rect(size_rect_x + card_w * (1 - i), card_h + (H >> 1), sard_w, sard_h) for i in
                  range(4)])
    rect_card_2 = (
        [pg.Rect(size_rect_x + card_w * (1 - i), -size_rect_y + (H >> 1) - sard_h, sard_w, sard_h) for i in range(4)],
        [pg.Rect(size_rect_x + card_w * (1 - i), -sard_h + (H >> 1) - card_h, sard_w, sard_h) for i in
         range(4)])
    hand = pg.Surface((int(card_w * 1.6), int(card_h * 2.1)))
    hand_rect = pg.Rect((W >> 1) + int(card_w * 2.1), (H >> 1) - sard_h, *hand.get_size())
    cem_win = False
    count_turn = 0
    windows = []

    # for _ in range(5):
    #     PLAYER_1.hand.add((a := Card((sard_w, sard_h), PLAYER_1.pack.pop(0), PLAYER_1)))
    #     a.location(len(PLAYER_1.hand) - 1, (hand_rect.x + int(sard_w * 0.125),
    #                                         hand_rect.y + int(sard_w * 0.125)), (sard_w, sard_h), 0)
    #     PLAYER_2.hand.add((a := Card((sard_w, sard_h), PLAYER_2.pack.pop(0), PLAYER_2)))
    #     a.location(len(PLAYER_2.hand) - 1, (hand_rect.x + int(sard_w * 0.125),
    #                                         hand_rect.y + int(sard_w * 0.125)), (sard_w, sard_h), 0)

    draw_game(screen, bg, PLAYER_1, deck_card, deck, PLAYER_2, deck_2, hand, windows, None, sard_w,
              sard_h, rect_card, hp_pos, action_pos, btn_end, hp_pos_2,
              count_card_pos, size_rect_x, W, size_rect_y, PLAYER_1.cards, hand_rect,
              PLAYER_1.hand, cemetery, cemetery_2, card_w, H)

    while runGame:
        PLAYER_1, PLAYER_2 = PLAYER_2, PLAYER_1
        cards = PLAYER_1.cards
        play = PLAYER_1.active_cards
        cur = None
        opening = False
        count_turn += 1

        cards_on_hand = PLAYER_1.hand
        slider = 0

        PLAYER_1.land = pg.sprite.Group()
        PLAYER_2.land = pg.sprite.Group()
        for i in range(4):
            PLAYER_1.land.add(
                Land(PLAYER_1.land_id[i], ((W >> 1) - card_w * (i - 1), (H >> 1)), (card_w, card_h), 0,
                     PLAYER_1.land_activ[i]))
            if PLAYER_1.active_cards[0][i]: PLAYER_1.active_cards[0][i].viev(rect_card[0][i])
            if PLAYER_1.active_cards[1][i]: PLAYER_1.active_cards[1][i].viev(rect_card[1][i])
            PLAYER_2.land.add(
                Land(PLAYER_2.land_id[i], ((W >> 1) - card_w * (i - 1), (H >> 1) - card_h), (card_w, card_h), 180,
                     PLAYER_2.land_activ[i]))
            if PLAYER_2.active_cards[0][i]: PLAYER_2.active_cards[0][i].viev(rect_card_2[0][i])
            if PLAYER_2.active_cards[1][i]: PLAYER_2.active_cards[1][i].viev(rect_card_2[1][i])
        timeee = True
        PLAYER_1.action = 2
        if PLAYER_1.pack and count_turn > 2:
            PLAYER_1.hand.add((a := Card((sard_w, sard_h), PLAYER_1.pack.pop(0), PLAYER_1)))
            a.location(len(PLAYER_1.hand) - 1, (hand_rect.x + int(sard_w * 0.125),
                                                hand_rect.y + int(sard_w * 0.125)), (sard_w, sard_h), 0)

        [a.location(n,
                    (hand_rect.x + int(sard_w * 0.125),
                     hand_rect.y + int(sard_w * 0.125)),
                    (sard_w, sard_h), slider) for n, a in enumerate(cards_on_hand)]

        for card in cards:
            if card and card.case != 0:
                card.case = 0
                card.status = 2

        for card in list(filter(None, list(PLAYER_1.active_cards[0]))):
            card.hp = card.relative_hp
            card.atc = card.default_atc
            if card.passive_spell: card.passive_spell(enemy=PLAYER_2, hero=PLAYER_1, me=card,
                                                      sard_h=sard_h, sard_w=sard_w, hand_rect=hand_rect)
        for card in list(filter(None, list(PLAYER_2.active_cards[0]))):
            card.hp = card.relative_hp
            card.atc = card.default_atc
            if card.passive_spell: card.passive_spell(enemy=PLAYER_1, hero=PLAYER_2, me=card,
                                                      sard_h=sard_h, sard_w=sard_w, hand_rect=hand_rect)
        for card in list(filter(None, list(PLAYER_1.active_cards[1]))):
            if card.passive_spell: card.passive_spell(enemy=PLAYER_2, hero=PLAYER_1, me=card,
                                                      sard_h=sard_h, sard_w=sard_w, hand_rect=hand_rect)
        for card in list(filter(None, list(PLAYER_2.active_cards[1]))):
            if card.passive_spell: card.passive_spell(enemy=PLAYER_1, hero=PLAYER_2, me=card,
                                                      sard_h=sard_h, sard_w=sard_w, hand_rect=hand_rect)
        [card.specifications() for card in PLAYER_1.active_cards[0] if card]
        [card.specifications() for card in PLAYER_2.active_cards[0] if card]

        if count_turn <= 2:
            intermediate = [Card((sard_w, sard_h), PLAYER_1.pack.pop(0), PLAYER_1) for _ in range(5)]
            start_card_win = Window(pg.Rect((W >> 1) - (card_w << 1), 0, (card_w << 2), (H >> 1)), 'начальные карты',
                                    'принять', 'поменять', 0)
            windows.append(start_card_win)

        while runGame and timeee:
            if not cem_win:
                draw_game(screen, bg, PLAYER_1, deck_card, deck, PLAYER_2, deck_2, hand, windows, cur, sard_w,
                          sard_h, rect_card, hp_pos, action_pos, btn_end, hp_pos_2,
                          count_card_pos, size_rect_x, W, size_rect_y, cards, hand_rect,
                          cards_on_hand, cemetery, cemetery_2, card_w, H)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:  # выход из игры
                        runGame = False
                if not cem_win and not (f_window := list(filter(lambda x: x.tipe == 0, windows))):
                    if event.type == pg.MOUSEBUTTONUP:
                        if event.button == 1:
                            if btn_cem.collidepoint(pg.mouse.get_pos()) and PLAYER_1.cemetery:
                                cem_win = 1
                            if btn_cem_2.collidepoint(pg.mouse.get_pos()) and PLAYER_2.cemetery:
                                cem_win = 2
                            if btn_end.collidepoint(pg.mouse.get_pos()):
                                timeee = False
                            if cur:
                                if cur.object < 2:
                                    for i in range(4):
                                        if rect_card[cur.object][i].colliderect(
                                                cur.rect) and cur.status < 2 and PLAYER_1.action >= cur.price:
                                            cur.set_land(rect_card[cur.object][i].copy(), i)  # перемещаем карту
                                            cards.add(cur)
                                            PLAYER_1.action -= cur.price
                                            cards_on_hand.remove(cur)
                                            if cur.spawn_spell: cur.spawn_spell(enemy=PLAYER_2, me=cur, hero=PLAYER_1,
                                                                                hand_rect=hand_rect, slider=slider,
                                                                                sard_w=sard_w, sard_h=sard_h)
                                            [a.location(n,
                                                        (hand_rect.x + int(sard_w * 0.125),
                                                         hand_rect.y + int(sard_w * 0.125)),
                                                        (sard_w, sard_h), slider) for n, a in enumerate(cards_on_hand)]
                                            if play[cur.object][i]:
                                                # сброс
                                                if spell := play[cur.object][i].dead_spell:
                                                    spell(enemy=PLAYER_2, me=play[cur.object][i], hero=PLAYER_1)
                                                play[cur.object][i].dead()
                                            play[cur.object][i] = cur
                                            recalculation(PLAYER_1, PLAYER_2, hand_rect=hand_rect, sard_w=sard_w,
                                                          sard_h=sard_h)
                                if count_turn > 1:
                                    if cur.object == 0 and rect_attack.colliderect(cur.rect) and cur.status == 2 and \
                                            (not PLAYER_2.active_cards[0][cur.land] or PLAYER_2.active_cards[0][
                                                cur.land].can_take):
                                        cur.case = 1
                                        cur.status = 1
                                        if PLAYER_2.active_cards[0][cur.land]:
                                            cur.take(
                                                PLAYER_2.active_cards[0][cur.land].take(cur.atc,
                                                                                        enemy=PLAYER_1,
                                                                                        me=PLAYER_2.active_cards[0][
                                                                                            cur.land], hero=PLAYER_2),
                                                enemy=PLAYER_2, me=cur, hero=PLAYER_1)
                                        else:
                                            PLAYER_2.HP -= cur.atc
                                    if cur.object == 0 and rect_floop.colliderect(cur.rect) and cur.status == 2 and \
                                            cur.floop and PLAYER_1.action >= cur.floop_price:
                                        cur.case = 2
                                        cur.status = 1
                                        cur.floop_spell(enemy=PLAYER_2, me=cur, hero=PLAYER_1, hand_rect=hand_rect,
                                                        sard_w=sard_w, sard_h=sard_h)
                                        PLAYER_1.action -= cur.floop_price
                                    if cur.object == 1 and rect_floop_building.colliderect(cur.rect) and \
                                            cur.status == 2 and cur.floop and PLAYER_1.action >= cur.floop_price:
                                        cur.case = 2
                                        cur.status = 1
                                        cur.floop_spell(enemy=PLAYER_2, me=cur, hero=PLAYER_1, hand_rect=hand_rect,
                                                        sard_w=sard_w, sard_h=sard_h)
                                        PLAYER_1.action -= cur.floop_price
                                    recalculation(PLAYER_1, PLAYER_2, hand_rect=hand_rect, sard_w=sard_w,
                                                  sard_h=sard_h)
                                cur.zeroing()  # возращаем карту на место
                                cur = None
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pg.mouse.get_rel()  # обнуляем относительную позицию
                            if btn_deck.collidepoint(pg.mouse.get_pos()) and len(PLAYER_1.pack) and PLAYER_1.action > 0:
                                cards_on_hand.add((a := Card((sard_w, sard_h), PLAYER_1.pack.pop(0), PLAYER_1)))
                                a.location(len(cards_on_hand) - 1, (hand_rect.x + int(sard_w * 0.125),
                                                                    hand_rect.y + int(sard_w * 0.125)),
                                           (sard_w, sard_h),
                                           slider)
                                PLAYER_1.action -= 1
                        if hand_rect.collidepoint(event.pos) and not cur:
                            if event.button == 4 and slider > 0:
                                [i.scroll(1) for i in cards_on_hand]
                                slider -= 1
                            if event.button == 5 and slider < (len(cards_on_hand) + 1 >> 1) * 4.1 - 12:
                                [i.scroll(-1) for i in cards_on_hand]
                                slider += 1
                    if event.type == pg.MOUSEMOTION:
                        if event.buttons[0]:
                            if pg.Rect(*pg.mouse.get_pos(), 0, 0).collidelist(
                                    a := sum([list(cards_on_hand), list(cards)], [])):
                                if not cur:
                                    # сохраняем выбранную карту
                                    cur = lis[0] if (lis := [card for card in a if card.rect.collidepoint(event.pos)
                                                             and (hand_rect.collidepoint(pg.mouse.get_pos()) or
                                                                  card.status >= 2)]) != [] else None
                                if cur:
                                    if cur.status == 0 or cur.status == 2:
                                        # перемещение карты
                                        cur.rect.move_ip(event.rel)
                                    else:
                                        cur = None
                elif f_window:
                    for event in pg.event.get():
                        if event.type == pg.MOUSEBUTTONUP:
                            if event.button == 1:
                                ...
                else:
                    now_cem = PLAYER_1.cemetery
                    if not opening:
                        if cem_win == 1:
                            now_cem = PLAYER_1.cemetery
                        else:
                            now_cem = PLAYER_2.cemetery
                        cem_win_sur.fill((75, 75, 75))
                        for n, card in enumerate(now_cem):
                            card.rect = pg.Rect((sard_w >> 1) + sard_w * 1.5 * (n % 5),
                                                (sard_h >> 2) + sard_h * 1.25 * (n // 5), sard_w, sard_h)
                        opening = True
                    now_cem.draw(cem_win_sur)
                    screen.blit(cem_win_sur, cem_win_rect)
                    if pg.key.get_pressed()[pg.K_LALT]:
                        [screen.blit(card.alt(pg.image.load(f'../cards/{card.id}.png'), (card_w * 3, H)),
                                     pg.Rect((W >> 1) - card_w * 1.5, 0, card_w * 3, H)) for card in now_cem
                         if card.rect.collidepoint((pg.mouse.get_pos()[0] - cem_win_rect.x, pg.mouse.get_pos()[1]))]
                    if pg.key.get_pressed()[pg.K_BACKSPACE]:
                        cem_win = 0
                        opening = False
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 4 and list(now_cem)[0].rect.y < (sard_h >> 2):
                            [i.rect.move_ip(0, sard_h >> 2) for i in now_cem]
                        if event.button == 5 and list(now_cem)[-1].rect.y > W - (sard_h >> 2):
                            [i.rect.move_ip(0, -(sard_h >> 2)) for i in now_cem]
                        if event.button == 1 and not cem_win_rect.collidepoint(pg.mouse.get_pos()):
                            cem_win = 0
                            opening = False
                if PLAYER_2.HP < 1 or PLAYER_1.HP < 1:
                    runGame = False
            pg.display.update()
            clock.tick(FPS)
        for i in list(filter(None, PLAYER_1.active_cards[0])):
            i.moving(False)
