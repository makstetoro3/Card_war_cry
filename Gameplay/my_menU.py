import pygame as pg
import pygame_gui


def men(screen: pg.Surface, W: int, H: int) -> None:
    pg.init()
    manager = pygame_gui.UIManager((W, H))
    menu_backr = pg.transform.scale(pg.image.load('../data/menu.png'), (W, H))

    switch = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((W // 2, H // 2), (100, 50)),
        text='Switch',
        manager=manager
    )

    clock = pg.time.Clock()

    show = True

    while show:
        time_delta = clock.tick(60) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                show = False
                # quit()
            if event.type == pg.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == switch:
                        pass
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(menu_backr, (0, 0))
        manager.draw_ui(screen)
        pg.display.update()
