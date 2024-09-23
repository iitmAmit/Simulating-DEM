import pygame
from pygame import Rect


def draw_text(surface, message, font_size, center_position, color=(255, 255, 255)):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect()
    text_rect.center = center_position
    surface.blit(text, text_rect)


def create_button(width, height, message, selected=False):
    surf = pygame.Surface((width, height))
    if selected:
        surf.fill((255, 255, 255))
    else:
        surf.fill((255, 255, 255))
    pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 1)
    draw_text(surf, message, height // 3, surf.get_rect().center, (0, 0, 255))
    return surf


def start_window(width):
    pygame.init()
    screen = pygame.display.set_mode((560, 560))
    pygame.display.set_caption("DEM Simulation")
    bg = pygame.image.load('bglogo.png')
    run = True
    while run:
        play_button = create_button(width * 4 // 10, width // 10, "Play")
        play_button_rect = Rect(width * 3 // 10, width * 8 // 10, width * 4 // 10, width // 10)
        screen.blit(bg, (0, 50))
        screen.blit(play_button, play_button_rect)
        draw_text(screen, "DEM Simulation", width // 10, (width // 2, width * 2 // 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(*mouse_pos):
                    run = False