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
        relative_rect=pg.Rect((W // 2 - 220, H // 2 + 310), (400, 50)),
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
    clock = pg.time.Clock()
    flPause = False
    show = True

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
    menu_backr1 = pg.transform.scale(pg.image.load('../data/training.png'), (W, H))
    sound1 = pg.mixer.Sound("../data/melodia.wav")

    f3 = pg.font.SysFont('italic', 60)
    text3 = f3.render("Обучение", False,
                      (0, 0, 0))

    menu_backr1.blit(text3, (W // 2 - 100, 25))
    pg.display.update()

    f2 = pg.font.SysFont('serif', 30)

    text2 = f2.render('ddd', False, (0, 0, 0))

    menu_backr1.blit(text2, (10, 100))
    pg.display.update()

    hhh = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 650, H // 2 + 300), (300, 70)),
        text='<- Назад',
        manager=manager1
    )

    clock1 = pg.time.Clock()

    show1 = True

    while show1:
        time_delta = clock1.tick(60) / 1000.0
        for event1 in pg.event.get():
            if event1.type == pg.USEREVENT:
                if event1.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event1.ui_element == hhh:
                        sound1.play()
                        show1 = False
                        bes = 0
            manager1.process_events(event1)
        manager1.update(time_delta)
        screen.blit(menu_backr1, (0, 0))
        manager1.draw_ui(screen)
        pg.display.update()

    return bes
