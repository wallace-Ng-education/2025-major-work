import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
BG_COLOR = pg.Color('gray12')

rect1 = pg.Rect(200, 100, 161, 100)
rect2 = pg.Rect(0, 0, 120, 74)
rect2.center = rect1.center

done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

    screen.fill(BG_COLOR)
    pg.draw.rect(screen, (0, 100, 255), rect1, 2)
    pg.draw.rect(screen, (255, 128, 0), rect2, 2)
    pg.display.flip()
    clock.tick(60)