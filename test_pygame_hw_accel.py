import pygame, pygame.gfxdraw
from pygame import *
from random import randint


def main():
    pygame.init()

    video_info = pygame.display.Info()
    if video_info.current_w != -1 and video_info.current_h != -1:
        screen_width, screen_height = video_info.current_w, video_info.current_h
    else:
        screen_width, screen_height = 800, 600

    screen = pygame.display.set_mode((screen_width, screen_height), FULLSCREEN | DOUBLEBUF)  # | HWSURFACE)
    pygame.display.set_caption(__name__.upper())

    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0, 0, 0))
    pygame.gfxdraw.filled_trigon(
        background,
        screen_width / 10, screen_height / 10,
        screen_width * 9 / 10, screen_height * 9 / 10,
        screen_width / 2, screen_height * 9 / 10,
        (210, 200, 77))
    sprites = pygame.sprite.LayeredDirty()
    sprites.clear(screen, background)
    # image = pygame.image.load('tomato.png').convert_alpha()
    image = pygame.Surface((100, 100))
    image.fill(Color('red'))
    for _ in xrange(200):
        XSprite(image, sprites)
    del image

    clock = pygame.time.Clock()
    timer = 1.0
    sans_font = pygame.font.SysFont('sans', 18, True)
    fps = None
    fps_rect = None

    # main game loop
    while True:
        timer -= clock.tick() / 1000.0
        if timer <= 0.0:
            timer += 1.0
            fps = sans_font.render('{0:0.0f} fps'.format(clock.get_fps()), True, Color('yellow'))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return

        if fps_rect:
            screen.blit(background, (0, 0), fps_rect)
        sprites.update(screen)
        dirty_rects = sprites.draw(screen)
        if fps:
            fps_rect = screen.blit(fps, (0, 0))
            dirty_rects.append(fps_rect)
        pygame.display.update(dirty_rects)


class XSprite(pygame.sprite.DirtySprite):
    def __init__(self, image, *groups):
        super(XSprite, self).__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, 60)
        self.rect.y = randint(0, 40)
        self.dx, self.dy = randint(1, 16), randint(1, 16)

    def update(self, screen, *args):
        screen_w, screen_h = screen.get_size()
        self.rect.x += self.dx
        self.rect.y += self.dy
        if (self.rect.x + self.dx + self.rect.w > screen_w) or \
                (self.rect.x + self.dx < 0):
            self.dx = -self.dx
        if (self.rect.y + self.dy + self.rect.h > screen_h) or \
                (self.rect.y + self.dy < 0):
            self.dy = -self.dy
        self.rect.move_ip(self.dx, self.dy)
        self.dirty = True

if __name__ == '__main__':
    main()
