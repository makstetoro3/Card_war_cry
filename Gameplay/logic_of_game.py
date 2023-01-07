import pygame as pg
from card import Card
from land import Land
from player import Player
from random import randint
from auxiliary import recalculation, draw_game
from window import Window
from random import shuffle


def pvp(screen: pg.Surface, W: int, H: int, decks: list, name: list) -> None:
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
    PLAYER_1 = Player(decks.pop((r := randint(-1, 1))), name.pop(r), r)
    [PLAYER_1.land.add(Land(PLAYER_1.land_id[i], ((W >> 1) - card_w * (2 - i), (H >> 1)), (card_w, card_h), 0,
                            PLAYER_1.land_activ[i])) for i in range(4)]
    PLAYER_2 = Player(decks.pop(0), name.pop(0), 1 - r)
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
    win = None
    cem_win = 0
    count_turn = 0
    window = [None]
    # for _ in range(5):
    #     PLAYER_2.hand.add((a := Card((sard_w, sard_h), PLAYER_2.pack.pop(0), PLAYER_2)))
    #     a.location(len(PLAYER_2.hand) - 1, (hand_rect.x + int(sard_w * 0.125),
    #                                         hand_rect.y + int(sard_w * 0.125)), (sard_w, sard_h), 0)

    draw_game(screen, bg, PLAYER_1, deck_card, deck, PLAYER_2, deck_2, hand, window[0], None, sard_w,
              sard_h, rect_card, hp_pos, action_pos, btn_end, hp_pos_2,
              count_card_pos, size_rect_x, W, size_rect_y, PLAYER_1.cards, hand_rect,
              PLAYER_1.hand, cemetery, cemetery_2, card_w, H, card_h)

    while not win and runGame:
        PLAYER_1, PLAYER_2 = PLAYER_2, PLAYER_1
        cards = PLAYER_1.cards
        play = PLAYER_1.active_cards
        cur = None
        opening = False
        count_turn += 1
        between = True

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
            window[0] = Window(pg.Rect((W >> 1) - (card_w << 1), 0, (card_w << 2), (H >> 1)), 'начальные карты',
                               'принять', 'поменять', 0, *intermediate)

        while runGame and timeee:
            if not cem_win and not between:
                draw_game(screen, bg, PLAYER_1, deck_card, deck, PLAYER_2, deck_2, hand, window[0], cur, sard_w,
                          sard_h, rect_card, hp_pos, action_pos, btn_end, hp_pos_2,
                          count_card_pos, size_rect_x, W, size_rect_y, cards, hand_rect,
                          cards_on_hand, cemetery, cemetery_2, card_w, H, card_h)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:  # выход из игры
                        runGame = False
                if not window[0] and not cem_win and not between:
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
                                                cur.rect) and ((cur.status < 2 and PLAYER_1.action >= cur.price) or
                                                               (cur.status == 3 and not rect_card[0][i])):
                                            if cur.status != 3:
                                                cards.add(cur)
                                                PLAYER_1.action -= cur.price
                                                cards_on_hand.remove(cur)
                                                if cur.spawn_spell:
                                                    cur.spawn_spell(enemy=PLAYER_2, me=cur, hero=PLAYER_1,
                                                                    hand_rect=hand_rect, slider=slider, sard_w=sard_w,
                                                                    sard_h=sard_h, turn=count_turn, window=window)
                                                [a.location(n,
                                                            (hand_rect.x + int(sard_w * 0.125),
                                                             hand_rect.y + int(sard_w * 0.125)),
                                                            (sard_w, sard_h), slider) for n, a in
                                                 enumerate(cards_on_hand)]
                                                if play[cur.object][i]:
                                                    # сброс
                                                    if spell := play[cur.object][i].dead_spell:
                                                        spell(enemy=PLAYER_2, me=play[cur.object][i], hero=PLAYER_1)
                                                    play[cur.object][i].dead()
                                            else:
                                                play[cur.land] = None
                                                for k in list(filter(None, PLAYER_1.active_cards[0])):
                                                    if k.status == 3:
                                                        k.status = 2
                                            play[cur.object][i] = cur
                                            cur.set_land(rect_card[cur.object][i].copy(), i)  # перемещаем карту
                                            recalculation(PLAYER_1, PLAYER_2, hand_rect=hand_rect, sard_w=sard_w,
                                                          sard_h=sard_h, turn=count_turn)
                                if cur.object == 2 and pg.Rect((W >> 1) - (sard_w << 1), H >> 1, sard_w << 2,
                                                               sard_h).colliderect(cur.rect):
                                    PLAYER_1.magic.append(cur)
                                    cur.spawn_spell(enemy=PLAYER_2, me=cur, hero=PLAYER_1,
                                                    hand_rect=hand_rect, slider=slider, sard_w=sard_w,
                                                    sard_h=sard_h, turn=count_turn, window=window)
                                    cur.dead(True)
                                    [a.location(n,
                                                (hand_rect.x + int(sard_w * 0.125),
                                                 hand_rect.y + int(sard_w * 0.125)),
                                                (sard_w, sard_h), slider) for n, a in
                                     enumerate(cards_on_hand)]
                                if count_turn > 1 or (cur.object == 0 and cur.status == 3):
                                    if cur.object == 0 and rect_floop.colliderect(cur.rect) and cur.status == 2 and \
                                            cur.floop and PLAYER_1.action >= cur.floop_price:
                                        cur.case = 2
                                        cur.status = 1
                                        cur.turn_use = count_turn
                                        cur.floop_spell(enemy=PLAYER_2, me=cur, hero=PLAYER_1, hand_rect=hand_rect,
                                                        sard_w=sard_w, sard_h=sard_h, turn=count_turn)
                                        PLAYER_1.action -= cur.floop_price
                                    if cur.object == 1 and rect_floop_building.colliderect(cur.rect) and \
                                            cur.status == 2 and cur.floop and PLAYER_1.action >= cur.floop_price:
                                        cur.case = 2
                                        cur.status = 1
                                        cur.turn_use = count_turn
                                        cur.floop_spell(enemy=PLAYER_2, me=cur, hero=PLAYER_1, hand_rect=hand_rect,
                                                        sard_w=sard_w, sard_h=sard_h, turn=count_turn, window=window)
                                        PLAYER_1.action -= cur.floop_price
                                    recalculation(PLAYER_1, PLAYER_2, hand_rect=hand_rect, sard_w=sard_w,
                                                  sard_h=sard_h, turn=count_turn)
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
                                    if cur.status in (0, 2, 3):
                                        # перемещение карты
                                        cur.rect.move_ip(event.rel)
                                    else:
                                        cur = None
                elif window[0]:
                    if window[0].tipe == 0:
                        if event.type == pg.MOUSEBUTTONUP:
                            if event.button == 1:
                                if window[0].btn_ok[0].collidepoint(event.pos[0] - window[0].rect.x, event.pos[1]):
                                    for i in window[0].cards:
                                        PLAYER_1.hand.add(i)
                                        i.location(len(PLAYER_1.hand) - 1, (hand_rect.x + int(sard_w * 0.125),
                                                                            hand_rect.y + int(sard_w * 0.125)),
                                                   (sard_w, sard_h), 0)
                                    PLAYER_1.hand.add((a := Card((sard_w, sard_h), PLAYER_1.pack.pop(0), PLAYER_1)))
                                    a.location(len(PLAYER_1.hand) - 1, (hand_rect.x + int(sard_w * 0.125),
                                                                        hand_rect.y + int(sard_w * 0.125)),
                                               (sard_w, sard_h), 0)
                                    window[0] = None
                                elif window[0].btn_no[0].collidepoint(event.pos[0] - window[0].rect.x, event.pos[1]):
                                    PLAYER_1.pack = [*PLAYER_1.pack, *list(map(lambda car: car.id, window[0].cards))]
                                    [car.kill() for car in window[0].cards]
                                    shuffle(PLAYER_1.pack)
                                    for _ in range(6):
                                        PLAYER_1.hand.add((a := Card((sard_w, sard_h), PLAYER_1.pack.pop(0), PLAYER_1)))
                                        a.location(len(PLAYER_1.hand) - 1, (hand_rect.x + int(sard_w * 0.125),
                                                                            hand_rect.y + int(sard_w * 0.125)),
                                                   (sard_w, sard_h), 0)
                                    window[0] = None
                    elif window[0].tipe == 1:
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                pg.mouse.get_rel()
                        if event.type == pg.MOUSEMOTION:
                            if event.buttons[0]:
                                if pg.Rect(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 0, 0).collidelist(
                                        list(map(lambda x: x.rect, (a := window[0].kw['lis'])))):
                                    if not cur:
                                        # сохраняем выбранную карту
                                        cur = lis[0] if (lis := [card for card in a if
                                                                 card.rect.collidepoint(event.pos)]) != [] else None
                                    if cur:
                                        if cur.type in window[0].kw['type'] and cur.object in window[0].kw['object'] \
                                                and cur.player == window[0].kw['player']:
                                            print(1)
                                            # перемещение карты
                                            cur.rect.move_ip(event.rel)
                                        else:
                                            cur = None
                        if event.type == pg.MOUSEBUTTONUP:
                            if window[0].btn_ok[0].collidepoint(event.pos[0] - window[0].rect.x,
                                                                event.pos[1] - window[0].rect.y) and \
                                    len(window[0].cards):
                                window[0].kw['spell'](window[0].cards[0], enemy=PLAYER_2, hero=PLAYER_1,
                                                      me=window[0].cards[0])
                                window[0] = None
                            if event.button == 1 and cur:
                                if window[0].rect.colliderect(cur.rect):
                                    window[0].cards = [cur]
                                cur.zeroing()
                                cur = None

                else:
                elif not between:
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
                else:
                    screen.fill((0, 0, 0))
                    if PLAYER_1.id == 1:
                        screen.blit(pg.transform.scale(pg.image.load('../data/Jake1.png'), (250, 450)),
                                    (W // 2 - 120, H // 2 - 370))
                    else:
                        screen.blit(pg.transform.scale(pg.image.load('../data/Finn.png'), (450, 450)),
                                    (W // 2 - 300, H // 2 - 370))
                    font = pg.font.Font('../data/base.ttf', 64)
                    text = font.render(PLAYER_1.name, True, (175, 25, 25))
                    screen.blit(text, ((W >> 1) - (text.get_width() >> 1), H - (H >> 2)))
                    if pg.key.get_pressed()[pg.K_SPACE]: between = False
                if PLAYER_2.HP < 1 or PLAYER_1.HP < 1:
                    runGame = False
                    win = PLAYER_1 if PLAYER_2.HP < 1 else PLAYER_2
            pg.display.update()
            clock.tick(FPS)

        if count_turn > 1:
            for card in list(filter(lambda x: x and x.status == 2, PLAYER_1.active_cards[0])):
                card.case = 1
                card.status = 1
                if e_card := PLAYER_2.active_cards[0][card.land]:
                    card.take(e_card.take(card.atc if e_card.can_take else 0,
                                          enemy=PLAYER_1, me=e_card, hero=PLAYER_2),
                              enemy=PLAYER_2, me=card, hero=PLAYER_1)
                else:
                    PLAYER_2.HP -= card.atc
        for i in list(filter(None, PLAYER_1.active_cards[0])):
            i.moving(False)
    if win:
        eee = True
        screen.fill((0, 0, 0))
        if PLAYER_1.id == 1:
            screen.blit(pg.transform.scale(pg.image.load('../data/Jake1.png'), (250, 450)),
                        (W // 2 - 120, H // 2 - 370))
        else:
            screen.blit(pg.transform.scale(pg.image.load('../data/Finn.png'), (450, 450)),
                        (W // 2 - 300, H // 2 - 370))
        font = pg.font.Font('../data/base.ttf', 64)
        text = font.render('победитель', True, (175, 25, 25))
        screen.blit(text, ((W >> 1) - (text.get_width() >> 1), H - (H >> 1)))
        text = font.render(PLAYER_1.name, True, (175, 25, 25))
        screen.blit(text, ((W >> 1) - (text.get_width() >> 1), H - (H >> 2)))
        while eee:
            if pg.key.get_pressed()[pg.K_SPACE]: eee = False
            clock.tick(FPS)

