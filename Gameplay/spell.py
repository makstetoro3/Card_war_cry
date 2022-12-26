from card import Card


# enemy - объект класса player - PLAYER_2
# me - объект класса Card - Карта у которой вызвали этот метод
# hero - объект класса player - PLAYER_1
def d1(**kwargs):
    if kwargs['enemy'].active_cards[0][kwargs['me'].land]:
        kwargs['enemy'].active_cards[0][kwargs['me'].land].take(len(kwargs['enemy'].hand), *kwargs)
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
    if kwargs['hero'].hand: list(kwargs['hero'].hand)[0].dead(False)
    card = kwargs['hero'].active_cards[0]
    if card[kwargs['me'].land] and kwargs['me'].land > 0 and not card[kwargs['me'].land - 1]:
        card[kwargs['me'].land - 1] = card[kwargs['me'].land]
        card[kwargs['me'].land].move(True)
        card[kwargs['me'].land] = None
    elif card[kwargs['me'].land] and kwargs['me'].land < 3 and not card[kwargs['me'].land + 1]:
        card[kwargs['me'].land + 1] = card[kwargs['me'].land]
        card[kwargs['me'].land] = None


def p6(**kwargs):
    kwargs['me'].atc += (a := len(list(filter(lambda x: x.type == 0, list(kwargs['hero'].land)))))
    kwargs['me'].hp += a * 2


def s7(**kwargs):
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
    if kwargs['enemy'].active_cards[0][kwargs['me'].land]:
        kwargs['enemy'].active_cards[0][kwargs['me'].land].take(
            len(list(filter(lambda x: x.type == 0 and x.activ, list(kwargs['enemy'].land)))), *kwargs)
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
    card = list(kwargs['enemy'].cemetery)[randint(0, len(list(kwargs['enemy'].cemetery)) - 1)]
    kwargs['enemy'].cards.remove(card)
    kwargs['hero'].hand.add(card)
    card.location(len(kwargs['hero'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                                 kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
                  (kwargs['sard_w'], kwargs['sard_h']), 0)
    card.price = 0


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
    for _ in range(len(list(filter(lambda x: x.case == 2, list(kwargs['hero'].active_cards[0]))))):
        kwargs['hero'].hand.add((a := Card((kwargs['sard_w'], kwargs['sard_h']), kwargs['hero'].pack.pop(0),
                                           kwargs['hero'])))
        a.location(len(kwargs['hero'].hand) - 1, (kwargs['hand_rect'].x + int(kwargs['sard_w'] * 0.125),
                                                  kwargs['hand_rect'].y + int(kwargs['sard_w'] * 0.125)),
                   (kwargs['sard_w'], kwargs['sard_h']), 0)


def f30(**kwargs):
    kwargs['hero'].cemetery.remove(a := list(filter(lambda x: x.object == 2, list(kwargs['hero'].cemetery)))[0])
    kwargs['hero'].pack = [a, *kwargs['hero'].pack]


def s31(**kwargs):
    ...


def p32(**kwargs):
    for i in list(filter(lambda x: x.move, list(kwargs['hero'].active_cards[0]))):
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
    ...


def f39(**kwargs):
    ...


def f40(**kwargs):
    if kwargs['enemy'].land_activ[kwargs['me'].land]:
        kwargs['enemy'].land_activ[kwargs['me'].land] = False
        list(kwargs['enemy'].land)[kwargs['me'].land].activ = False
        list(kwargs['enemy'].land)[kwargs['me'].land].flip()


def p41(**kwargs):
    if not kwargs['enemy'].active_cards[0][kwargs['me'].land]: kwargs['me'].atc += 3
