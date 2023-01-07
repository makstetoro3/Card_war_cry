import pygame as pg
import pygame_gui


def button_to_begin(screen: pg.Surface, W: int, H: int, bloop):
    manager_1 = pygame_gui.UIManager((W, H))
    menu_backr_1 = pg.transform.scale(pg.image.load('../data/blackk.png'), (W, H))

    if bloop == 1:
        prim_2 = pg.transform.scale(pg.image.load('../data/Jake1.png'), (250, 450))

        f_1 = pg.font.SysFont('italic', 60)
        text_4 = f_1.render('took', False, (0, 255, 0))
        menu_backr_1.blit(text_4, (W // 2 - 60, H // 2 + 130))
        pg.display.update()
    else:
        prim_2 = pg.transform.scale(pg.image.load('../data/Finn.png'), (450, 450))

        f_1 = pg.font.SysFont('italic', 60)
        text_4 = f_1.render('took', False, (0, 255, 0))
        menu_backr_1.blit(text_4, (W // 2 - 60, H // 2 + 120))
        pg.display.update()

    sound_1 = pg.mixer.Sound("../data/melodia.wav")
    # pg.mixer.music.load("../data/music.mp3")
    # pg.mixer.music.play(-1)

    playing = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2 - 160, H // 2 + 200), (300, 70)),
        text='Начать',
        manager=manager_1
    )

    vol_1 = 1.0
    FPS_1 = 60
    flPause_1 = False

    show_1 = True
    clock_1 = pg.time.Clock()

    while show_1:
        time_delta = clock_1.tick(60) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F2:
                    flPause_1 = not flPause_1
                    if flPause_1:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                elif event.key == pg.K_LEFT:
                    vol_1 -= 0.1
                    pg.mixer.music.set_volume(vol_1)
                    print(pg.mixer.music.get_volume())
                elif event.key == pg.K_RIGHT:
                    vol_1 += 0.1
                    pg.mixer.music.set_volume(vol_1)
                    print(pg.mixer.music.get_volume())

            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == playing:
                        #sound_1.play()
                        show_1 = False
            manager_1.process_events(event)
        manager_1.update(time_delta)
        screen.blit(menu_backr_1, (0, 0))
        if bloop == 1:
            screen.blit(prim_2, (W // 2 - 120, H // 2 - 370))
        else:
            screen.blit(prim_2, (W // 2 - 300, H // 2 - 370))
        manager_1.draw_ui(screen)
        pg.display.update()
