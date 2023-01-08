from card import Card
from window import Window
from pygame.display import Info
from pygame import Rect
from random import shuffle


# enemy - объект класса player - PLAYER_2
# me - объект класса Card - Карта у которой вызвали этот метод
# hero - объект класса player - PLAYER_1
def d1(**kwargs):
    if card := kwargs['enemy'].active_cards[0][kwargs['me'].land]:
        card.take(len(kwargs['enemy'].hand),
                  enemy=kwargs['hero'], me=card,
                  hero=kwargs['enemy'])
    else:
        kwargs['enemy'].HP -= len(kwargs['enemy'].hand)


def p2(**kwargs):
    kwargs['me'].hp += len(list(filter(lambda x: x.type == 0, list(kwargs['enemy'].land))))
    kwargs['me'].hp += len(list(filter(lambda x: x.type == 0, list(kwargs['hero'].land))))


def p3(**kwargs):
    kwargs['me'].hp += (a := len(list(filter(lambda x: x.type == 0, list(kwargs['hero'].land)))))
    if a <= 3:
        kwargs['me'].atc += 1


def s4(**kwargs):
    if kwargs['hero'].hand: list(kwargs['hero'].hand)[0].dead(True)
    [a.location(n,
                (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                 kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
                (kwargs['sard_w'], kwargs['sard_h']), kwargs['slider']) for n, a in enumerate(kwargs['hero'].hand)]
    card = kwargs['hero'].active_cards[0]
    if card[kwargs['me'].land] and kwargs['me'].land > 0 and not card[kwargs['me'].land - 1]:
        card[kwargs['me'].land - 1] = card[kwargs['me'].land]
        card[kwargs['me'].land].moving(True)
        card[kwargs['me'].land] = None
    elif card[kwargs['me'].land] and kwargs['me'].land < 3 and not card[kwargs['me'].land + 1]:
        card[kwargs['me'].land + 1] = card[kwargs['me'].land]
        card[kwargs['me'].land] = None


def s5(**kwargs):
    kwargs['enemy'].HP -= len(kwargs['enemy'].hand)


def p6(**kwargs):
    kwargs['me'].atc += (a := len(list(filter(lambda x: x.type == 0, list(kwargs['hero'].land)))))
    kwargs['me'].hp += a * 2


def s7(**kwargs):
    print(kwargs['me'])
    if kwargs['hero'].land_activ[kwargs['me'].land]:
        kwargs['hero'].land_activ[kwargs['me'].land] = False
        list(kwargs['hero'].land)[kwargs['me'].land].activ = False
        list(kwargs['hero'].land)[kwargs['me'].land].flip()


def s8(**kwargs):
    if kwargs['enemy'].active_cards[0][kwargs['me'].land]:
        card = kwargs['enemy'].active_cards[0][kwargs['me'].land]
        card.atc = card.default_atc
        card.hp = card.default_hp
        card.specifications()
        kwargs['enemy'].cards.remove(card)
        kwargs['enemy'].hand.add(card)


def f9(**kwargs):
    ...


def f10(**kwargs):
    if kwargs['enemy'].active_cards[1][kwargs['me'].land]: kwargs['enemy'].active_cards[1][kwargs['me'].land].dead()


def p11(**kwargs):
    kwargs['me'].atc += len(list(filter(lambda x: x and x.type == 0, list(kwargs['enemy'].active_cards[0])))) - 1


def p12(**kwargs):
    if kwargs['me'].land == 0:
        kwargs['me'].atc += len(list(filter(lambda x: x.type == 0 and x.activ, list(kwargs['enemy'].land)[0:1])))
    elif kwargs['me'].land == 3:
        kwargs['me'].atc += len(list(filter(lambda x: x.type == 0 and x.activ, list(kwargs['enemy'].land)[2:3])))
    else:
        kwargs['me'].atc += len(list(filter(lambda x: x.type == 0 and x.activ,
                                            list(kwargs['enemy'].land)[kwargs['me'].land - 1:kwargs['me'].land + 1])))


def s13(**kwargs):
    if card := kwargs['enemy'].active_cards[0][kwargs['me'].land]:
        card.take(len(list(filter(lambda x: x.type == 0 and x.activ, list(kwargs['enemy'].land)))),
                  enemy=kwargs['hero'], me=card, hero=kwargs['enemy'])
    else:
        kwargs['enemy'].HP -= len(list(filter(lambda x: x.type == 0 and x.activ, list(kwargs['enemy'].land))))


def p14(**kwargs):
    kwargs['hero'].hand.add((a := Card((kwargs['sard_w'], kwargs['sard_h']), kwargs['hero'].pack.pop(0),
                                       kwargs['hero'])))
    a.location(len(kwargs['hero'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                              kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
               (kwargs['sard_w'], kwargs['sard_h']), 0)
    kwargs['enemy'].hand.add(
        (a := Card((kwargs['sard_w'], kwargs['sard_h']), kwargs['enemy'].pack.pop(0), kwargs['enemy'])))
    a.location(len(kwargs['enemy'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                               kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
               (kwargs['sard_w'], kwargs['sard_h']), 0)


def f15(**kwargs):
    from random import randint
    card = list(kwargs['enemy'].cemetery)[randint(0, len(list(kwargs['enemy'].cemetery)))]
    kwargs['enemy'].cards.remove(card)
    kwargs['hero'].hand.add(card)
    card.location(len(kwargs['hero'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                                 kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
                  (kwargs['sard_w'], kwargs['sard_h']), 0)
    card.price = 0


def s16(**kwargs):
    for i in list(filter(None, kwargs['hero'].active_cards[0])):
        if i.status == 2:
            i.status = 3


def s17(**kwargs):
    kwargs['me'].turn_use = kwargs['turn']


def p17(**kwargs):
    if kwargs['me'].turn_use == kwargs['turn']:
        for i in list(filter(lambda x: x and x.type == 0, kwargs['hero'].active_cards[0])):
            i.atc += 1
    return kwargs['me'].turn_use == kwargs['turn']


def s18(**kwargs):
    for i in range(4):
        if not list(kwargs['hero'].land)[i].activ:
            kwargs['hero'].land_activ[i] = True
            list(kwargs['hero'].land)[i].activ = True
            list(kwargs['hero'].land)[i].flip()
            break


def s19(**kwargs):
    if any(kwargs['enemy'].active_cards[0]):
        kwargs['window'][0] = Window(
            Rect((Info().current_w >> 1) - (kwargs['sard_h'] << 1), Info().current_h >> 1, kwargs['sard_h'] << 2,
                 Info().current_h >> 1), 'выберите существо', 'ок', '', 1, type=(0, 3, 5), object=[0],
            player=kwargs['enemy'], spell=f19, lis=list(filter(None, kwargs['enemy'].active_cards[0])), zona=True)


def f19(card: Card, **kwargs):
    card.take(kwargs['hero'].land_activ.count(True), enemy=kwargs['enemy'], hero=kwargs['hero'], me=kwargs['me'])


def p20(**kwargs):
    if kwargs['hero'].active_cards[0][kwargs['me'].land]:
        kwargs['hero'].active_cards[0][kwargs['me'].land].atc += 1


def p21(**kwargs):
    if kwargs['hero'].active_cards[0][kwargs['me'].land]:
        kwargs['hero'].active_cards[0][kwargs['me'].land].hp += 3


def f25(**kwargs):
    for n, i in enumerate(list(kwargs['hero'].land)):
        if not kwargs['hero'].land_activ[n]:
            kwargs['hero'].land_activ[n] = True
            i.activ = True
            i.flip()


def f26(**kwargs):
    from random import randint
    lis = list(filter(lambda x: x.type == 5, list(kwargs['hero'].cemetery)))
    if lis:
        card = lis[randint(0, len(lis) - 1)]
        kwargs['hero'].cemetery.remove(card)
        kwargs['hero'].hand.add(card)
        card.location(len(kwargs['hero'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                                     kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
                      (kwargs['sard_w'], kwargs['sard_h']), 0)
    if kwargs['hero'].active_cards[1][kwargs['me'].land]: kwargs['hero'].action += 1


def p27(**kwargs):
    card = kwargs['hero'].active_cards[0]
    if card[kwargs['me'].land] and kwargs['me'].land > 0 and card[kwargs['me'].land - 1]:
        card[kwargs['me'].land - 1].can_take = False
    if card[kwargs['me'].land] and kwargs['me'].land < 3 and card[kwargs['me'].land + 1]:
        card[kwargs['me'].land + 1].can_take = False


def f28(**kwargs):
    ...


def f29(**kwargs):
    for _ in range(len(list(filter(lambda x: x and x.case == 2, list(kwargs['hero'].active_cards[0]))))):
        kwargs['hero'].hand.add((a := Card((kwargs['sard_w'], kwargs['sard_h']), kwargs['hero'].pack.pop(0),
                                           kwargs['hero'])))
        a.location(len(kwargs['hero'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                                  kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
                   (kwargs['sard_w'], kwargs['sard_h']), 0)


def f30(**kwargs):
    kwargs['hero'].cemetery.remove(a := list(filter(lambda x: x.object == 2, list(kwargs['hero'].cemetery)))[0])
    kwargs['hero'].pack = [a, *kwargs['hero'].pack]


def s31(**kwargs):
    if lis := list(filter(lambda c: c and c.case == 2, kwargs['hero'].active_cards[0])):
        kwargs['window'][0] = Window(
            Rect((Info().current_w >> 1) - (kwargs['sard_h'] << 1), 0, kwargs['sard_h'] << 2,
                 Info().current_h >> 1), 'выберите существо', 'ок', '', 1, type=(0, 3, 5), object=[0],
            player=kwargs['hero'], spell=f31,
            lis=lis, zona=False)


def f31(card: Card, **kwargs):
    card.case = 0
    card.status = 2


def p32(**kwargs):
    for i in list(filter(lambda x: x.moving(True), list(filter(None, list(kwargs['hero'].active_cards[0]))))):
        i.atc += 2


def p33(**kwargs):
    for i in kwargs['hero'].active_cards[0]:
        if not i: continue
        if i.case == 2: i.atc += 2


def p34(**kwargs):
    kwargs['me'].atc += len(kwargs['hero'].magic) * 2


def p35(**kwargs):
    if kwargs['me'].move_one:
        kwargs['me'].move_one = False
        kwargs['hero'].hand.add((a := Card((kwargs['sard_w'], kwargs['sard_h']), kwargs['hero'].pack.pop(0),
                                           kwargs['hero'])))
        a.location(len(kwargs['hero'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                                  kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
                   (kwargs['sard_w'], kwargs['sard_h']), 0)


def p36(**kwargs):
    card = kwargs['hero'].active_cards[0]
    if card[kwargs['me'].land] and kwargs['me'].land > 0 and card[kwargs['me'].land - 1]:
        card[kwargs['me'].land - 1].atc += 1
    if card[kwargs['me'].land] and kwargs['me'].land < 3 and card[kwargs['me'].land + 1]:
        card[kwargs['me'].land + 1].atc += 1


def f37(**kwargs):
    card = kwargs['enemy'].active_cards[0][kwargs['me'].land]
    if card:
        if card.atc > 10:
            card.atc -= 10
        else:
            card.atc = 0


def f38(**kwargs):
    if (card := kwargs['hero'].active_cards[0][kwargs['me'].land]) and (lis := list(filter(lambda x: x.floop_spell,
                                                                                           kwargs['hero'].cemetery))):
        kwargs['hero'].school = card.floop_spell, card
        shuffle(lis)
        card.floop_spell = lis[0]
        kwargs['me'].turn_use = kwargs['turn']


def p38(**kwargs):
    if kwargs['me'].turn_use != kwargs['turn']:
        kwargs['hero'].school[0].floop_spell = kwargs['hero'].school[1]


def f39(**kwargs):
    ...


def f40(**kwargs):
    if kwargs['enemy'].land_activ[kwargs['me'].land]:
        kwargs['enemy'].land_activ[kwargs['me'].land] = False
        list(kwargs['enemy'].land)[kwargs['me'].land].activ = False
        list(kwargs['enemy'].land)[kwargs['me'].land].flip()


def p41(**kwargs):
    if not kwargs['enemy'].active_cards[0][kwargs['me'].land]: kwargs['me'].atc += 3


def s42(**kwargs):
    kwargs['me'].turn_use = kwargs['turn']


def p42(**kwargs):
    if kwargs['me'].turn_use == kwargs['turn']:
        for i in list(filter(lambda x: x and x.move == 0, kwargs['hero'].active_cards[0])):
            i.atc += 2
    return kwargs['me'].turn_use == kwargs['turn']


def s43(**kwargs):
    for i in list(filter(None, kwargs['enemy'].active_cards[0])):
        i.take(1, enemy=kwargs['hero'], hero=kwargs['enemy'], me=i)


def s44(**kwargs):
    if any(kwargs['hero'].active_cards[0]):
        kwargs['window'][0] = Window(
            Rect((Info().current_w >> 1) - (kwargs['sard_h'] << 1), 0, kwargs['sard_h'] << 2,
                 Info().current_h >> 1), 'выберите существо', 'ок', '', 1, type=[3], object=[0],
            player=kwargs['hero'], spell=f44, lis=list(filter(None, kwargs['hero'].active_cards[0])), zona=False)


def f44(card: Card, **kwargs):
    kwargs['me'].turn_use = kwargs['turn']
    kwargs['me'].bav = card


def p44(**kwargs):
    print(kwargs['me'].turn_use == kwargs['turn'])
    if kwargs['me'].turn_use == kwargs['turn']:
        kwargs['me'].bav.atc += 2
    return kwargs['me'].turn_use == kwargs['turn']


def s45(**kwargs):
    for _ in range(3):
        kwargs['hero'].hand.add(
            (a := Card((kwargs['sard_w'], kwargs['sard_h']), kwargs['hero'].pack.pop(0), kwargs['hero'])))
        a.location(len(kwargs['hero'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                                  kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
                   (kwargs['sard_w'], kwargs['sard_h']), 0)
