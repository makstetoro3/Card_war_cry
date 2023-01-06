import pygame as pg
import pygame_gui


def men(screen: pg.Surface, W: int, H: int) -> int:
    manager = pygame_gui.UIManager((W, H))
    menu_backr = pg.transform.scale(pg.image.load('../data/menu.png'), (W, H))
    sound = pg.mixer.Sound("../data/melodia.wav")
    pg.mixer.music.load("../data/music.mp3")
    pg.mixer.music.play(-1)
    play = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 160, H // 2), (300, 70)),
        text='Играть',
        manager=manager
    )

    training = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 160, H // 2 + 80), (300, 70)),
        text='Обучение',
        manager=manager
    )

    deck = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 160, H // 2 + 160), (300, 70)),
        text='Колода',
        manager=manager
    )

    exit = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 210, H // 2 + 310), (400, 50)),
        text='Выход',
        manager=manager
    )

    USER1 = pygame_gui.elements.UITextEntryLine(
        relative_rect=pg.Rect((240, 170), (300, 50)), manager=manager
    )

    USER2 = pygame_gui.elements.UITextEntryLine(
        relative_rect=pg.Rect((850, 310), (300, 50)), manager=manager
    )
    vol = 1.0
    FPS = 60
    flPause = False
    show = True
    clock = pg.time.Clock()

    while show:
        time_delta = clock.tick(60) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    flPause = not flPause
                    if flPause:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                elif event.key == pg.K_LEFT:
                    vol -= 0.1
                    pg.mixer.music.set_volume(vol)
                    print(pg.mixer.music.get_volume())
                elif event.key == pg.K_RIGHT:
                    vol += 0.1
                    pg.mixer.music.set_volume(vol)
                    print(pg.mixer.music.get_volume())

            # f10 = pg.font.SysFont('italic', 100)
            # text3 = f10.render(f'{clock.tick(FPS)}', False, (0, 0, 0))
            #
            # menu_backr.blit(text3, (W // 2 - 100, H // 2))
            # pg.display.update()

            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    sound.play()
                    res = 0
                    show = False
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    print("Name:", event.text)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play:
                        sound.play()
                        show = False
                        res = 1
                    if event.ui_element == exit:
                        sound.play()
                        confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                            rect=pg.Rect((W // 2 - 160, H // 2 + 50), (300, 200)),
                            manager=manager,
                            window_title='Подтверждение',
                            action_long_desc='Вы уверены, что хотите выйти?',
                            action_short_name='OK',
                            blocking=True
                        )
                    if event.ui_element == training:
                        sound.play()
                        hhhh(screen, W, H)
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(menu_backr, (0, 0))
        manager.draw_ui(screen)
        pg.display.update()

    return res


def hhhh(screen: pg.Surface, W: int, H: int) -> int:
    bun = True
    while bun:
        bes = my_training(screen, W, H)
        if bes == 0:
            bun = False
        else:
            pass


def my_training(screen: pg.Surface, W: int, H: int) -> int:
    manager1 = pygame_gui.UIManager((W, H))
    prim1 = pg.transform.scale(pg.image.load('../data/prim1.png'), (W // 2 + 90, H // 2 + 90))
    menu_backr1 = pg.transform.scale(pg.image.load('../data/training.png'), (W, H))
    sound1 = pg.mixer.Sound("../data/melodia.wav")

    f2 = pg.font.SysFont('italic', 60)
    text2 = f2.render("Внешний вид", False, (0, 0, 0))
    menu_backr1.blit(text2, (W // 2 - 150, 170))
    pg.display.update()

    f3 = pg.font.SysFont('italic', 60)
    text3 = f3.render("Обучение", False, (0, 0, 0))
    menu_backr1.blit(text3, (W // 2 - 110, 25))
    pg.display.update()
    best = 0
    text = 'Привет! Хочу научить тебя играть в эту игру! Это уникальная возможность проявить свои лидерские качества и уничтожить противника!'
    pos = (50, 100)
    font = pg.font.SysFont('italic', 38)
    blit_text(menu_backr1, text, pos, font, best)

    text = 'Это игра 1 на 1. В центре экрана расположены по 4 поля, на которые размещают игровые карты. Задача этой игры составить тактику, чтобы твои войска были непобедимы. '
    pos = (50, 220)
    font = pg.font.SysFont('italic', 38)
    blit_text(menu_backr1, text, pos, font, best)

    hhh = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 680, H // 2 + 310), (290, 60)),
        text='<- Назад',
        manager=manager1
    )

    sled = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 + 390, H // 2 + 310), (290, 60)),
        text='Следующая страница ->',
        manager=manager1
    )

    clock1 = pg.time.Clock()

    show1 = True
    vol1 = 1.0
    FPS1 = 60
    flPause1 = False

    while show1:
        time_delta = clock1.tick(60) / 1000.0
        for event1 in pg.event.get():
            if event1.type == pg.QUIT:
                exit()
            elif event1.type == pg.KEYDOWN:
                if event1.key == pg.K_SPACE:
                    flPause1 = not flPause1
                    if flPause1:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                elif event1.key == pg.K_LEFT:
                    vol1 -= 0.1
                    pg.mixer.music.set_volume(vol1)
                    print(pg.mixer.music.get_volume())
                elif event1.key == pg.K_RIGHT:
                    vol1 += 0.1
                    pg.mixer.music.set_volume(vol1)
                    print(pg.mixer.music.get_volume())
            if event1.type == pg.USEREVENT:
                if event1.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event1.ui_element == hhh:
                        sound1.play()
                        show1 = False
                        bes = 0
                    if event1.ui_element == sled:
                        sound1.play()
                        hhh1(screen, W, H)
            manager1.process_events(event1)
        manager1.update(time_delta)
        screen.blit(menu_backr1, (0, 0))
        screen.blit(prim1, (W // 2 - 388, H // 2 - 105))
        manager1.draw_ui(screen)
        pg.display.update()

    return bes


def hhh1(screen: pg.Surface, W: int, H: int) -> int:
    bun1 = True
    while bun1:
        bes1 = my_training1(screen, W, H)
        if bes1 == 0:
            bun1 = False
        else:
            pass


def my_training1(screen: pg.Surface, W: int, H: int) -> int:
    manager2 = pygame_gui.UIManager((W, H))
    menu_backr2 = pg.transform.scale(pg.image.load('../data/training.png'), (W, H))
    sound2 = pg.mixer.Sound("../data/melodia.wav")
    prim2 = pg.transform.scale(pg.image.load('../data/prim2.png'), (W // 2 - 100, H - 100))
    prim3 = pg.transform.scale(pg.image.load('../data/prim3.png'), (W // 2 - 100, H // 2))
    best = 0
    hhh1 = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 680, H // 2 + 310), (290, 60)),
        text='<- Назад',
        manager=manager2
    )

    sled1 = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 + 390, H // 2 + 310), (290, 60)),
        text='Следующая страница ->',
        manager=manager2
    )

    f4 = pg.font.SysFont('italic', 60)
    text4 = f4.render("Описание карт", False, (0, 0, 0))
    menu_backr2.blit(text4, ((W // 2) // 2 - 150, 25))
    pg.display.update()

    text = 'У игровой карты есть: \n   1)название;\n   2)единицу атаки и защиты; \n   3)какие поля контролирует; \n   4)особые свойства(у каждой карты свои).'
    pos = (10, 70)
    font = pg.font.SysFont('italic', 42)
    blit_text(menu_backr2, text, pos, font, best)

    text = 'Существуют карты заклинаний, зданий и существ. \n    У всех свои сверхспособности. Карту можно пере \n    нести в желтую область на игровом поле. Чтобы \n лучше рассмотреть карту нужно зажать Alt.'
    pos = (10, 250)
    font = pg.font.SysFont('italic', 42)
    blit_text(menu_backr2, text, pos, font, best)

    clock2 = pg.time.Clock()

    show2 = True
    vol2 = 1.0
    FPS2 = 60
    flPause2 = False

    while show2:
        time_delta1 = clock2.tick(60) / 1000.0
        for event2 in pg.event.get():
            if event2.type == pg.QUIT:
                exit()
            elif event2.type == pg.KEYDOWN:
                if event2.key == pg.K_SPACE:
                    flPause2 = not flPause2
                    if flPause2:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                elif event2.key == pg.K_LEFT:
                    vol2 -= 0.1
                    pg.mixer.music.set_volume(vol2)
                    print(pg.mixer.music.get_volume())
                elif event2.key == pg.K_RIGHT:
                    vol2 += 0.1
                    pg.mixer.music.set_volume(vol2)
                    print(pg.mixer.music.get_volume())
            if event2.type == pg.USEREVENT:
                if event2.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event2.ui_element == hhh1:
                        sound2.play()
                        show2 = False
                        bes1 = 0
                    if event2.ui_element == sled1:
                        sound2.play()
                        hhh2(screen, W, H)
            manager2.process_events(event2)
        manager2.update(time_delta1)
        screen.blit(menu_backr2, (0, 0))
        screen.blit(prim2, (W - W // 2 + 90, H // 2 - 370))
        screen.blit(prim3, (160, H // 2 - 10))
        manager2.draw_ui(screen)
        pg.display.update()

    return bes1


def hhh2(screen: pg.Surface, W: int, H: int) -> int:
    bun2 = True
    while bun2:
        bes2 = my_training2(screen, W, H)
        if bes2 == 0:
            bun2 = False
        else:
            pass


def my_training2(screen: pg.Surface, W: int, H: int) -> int:
    manager3 = pygame_gui.UIManager((W, H))
    menu_backr3 = pg.transform.scale(pg.image.load('../data/training.png'), (W, H))
    sound3 = pg.mixer.Sound("../data/melodia.wav")
    prim4 = pg.transform.scale(pg.image.load('../data/prim4.png'), ((W // 2) // 2 - 100, (H // 2) - 100))
    prim5 = pg.transform.scale(pg.image.load('../data/prim5.png'), ((W // 2) // 2 - 100, (H // 2) - 100))
    prim6 = pg.transform.scale(pg.image.load('../data/prim6.png'), ((W // 2) // 2 + 100, (H // 2) // 2 + 100))

    hhh2 = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 680, H // 2 + 310), (290, 60)),
        text='<- Назад',
        manager=manager3
    )

    per = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 + 390, H // 2 + 310), (290, 60)),
        text='Играть ->',
        manager=manager3
    )

    f5 = pg.font.SysFont('italic', 60)
    text5 = f5.render("Флюп и нападение", False, (0, 0, 0))
    menu_backr3.blit(text5, ((W // 2) // 2 - 150, 25))
    pg.display.update()

    best = 0
    text = 'Флюп - это положение карты в защите. Для этого \n    нужно зажать и повести карту в нижнюю часть поля. А \n    для нападения в противоположную область.'
    pos = (20, 100)
    font = pg.font.SysFont('italic', 42)
    blit_text(menu_backr3, text, pos, font, best)

    best = 1

    text = 'Карта во время фюпа только защищается и не нападает!'
    pos = (10, 300)
    font = pg.font.SysFont('italic', 42)
    blit_text(menu_backr3, text, pos, font, best)

    best = 0

    text = '    У игрока есть в ход по 2 действия, которые можно \n        тратить на набор карт в руку или разыгровку карты. \n        Если монстр атакует на пустующее поле, то урон \n     наносится самому персонажу.'
    pos = (10, 400)
    font = pg.font.SysFont('italic', 42)
    blit_text(menu_backr3, text, pos, font, best)

    f5 = pg.font.SysFont('italic', 60)
    text5 = f5.render("Удачной битвы!", False, (0, 255, 0))
    menu_backr3.blit(text5, (350, 600))
    pg.display.update()

    clock3 = pg.time.Clock()

    show3 = True
    vol3 = 1.0
    FPS3 = 60
    flPause3 = False

    while show3:
        time_delta2 = clock3.tick(60) / 1000.0
        for event3 in pg.event.get():
            if event3.type == pg.QUIT:
                exit()
            elif event3.type == pg.KEYDOWN:
                if event3.key == pg.K_SPACE:
                    flPause3 = not flPause3
                    if flPause3:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                elif event3.key == pg.K_LEFT:
                    vol3 -= 0.1
                    pg.mixer.music.set_volume(vol3)
                    print(pg.mixer.music.get_volume())
                elif event3.key == pg.K_RIGHT:
                    vol3 += 0.1
                    pg.mixer.music.set_volume(vol3)
                    print(pg.mixer.music.get_volume())
            if event3.type == pg.USEREVENT:
                if event3.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event3.ui_element == hhh2:
                        sound3.play()
                        show3 = False
                        bes2 = 0
                    if event3.ui_element == per:
                        sound3.play()
                        show3 = False
                        bes2 = 0
            manager3.process_events(event3)
        manager3.update(time_delta2)
        screen.blit(menu_backr3, (0, 0))
        c = W - W // 2 + 400
        k = ((W // 2) // 2 - 100)
        screen.blit(prim4, (c, H // 2 - 380))
        screen.blit(prim5, (c - k, H // 2 - 380))
        screen.blit(prim6, (W // 2 + 200, H // 2))
        manager3.draw_ui(screen)
        pg.display.update()

    return bes2


def blit_text(surface, text, pos, font, best, color=pg.Color('black')):
    if best == 1:
        color = pg.Color('red')
    else:
        color = pg.Color('black')
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height