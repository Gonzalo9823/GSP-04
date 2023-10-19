import pygame
from start_screen import start_screen
from game_screen import game_screen
from settings import WIDTH, HEIGHT

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    difficulty = start_screen(screen)
    game_screen(screen, difficulty);

