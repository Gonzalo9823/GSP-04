import pygame
from settings import BLACK, WHITE, WIDTH, HEIGHT

def start_screen(screen):
    start = False
    pygame.display.set_caption("Pong")

    TITLE_FONT = pygame.font.Font("./fonts/arial.ttf", 60)
    INFO_FONT = pygame.font.Font("./fonts/arial.ttf", 40)
    BUTTON_FONT = pygame.font.Font("./fonts/arial.ttf", 30)

    EASY_BUTTON = pygame.Rect(WIDTH // 4, HEIGHT - 150, 150, 50)
    PLAY_BUTTON = pygame.Rect(WIDTH - WIDTH // 4 - 150, HEIGHT - 150, 150, 50)

    difficulties = ["EASY", "MEDIUM", "HARD"]
    current_difficulty = 0

    while not start:
        screen.fill(BLACK)

        title_surface = TITLE_FONT.render("PONG", True, WHITE)
        title_position = title_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_surface, title_position)

        left_info_line_1 = INFO_FONT.render("Player 1 plays with", True, WHITE)
        left_info_line_2 = INFO_FONT.render("W and S", True, WHITE)
        screen.blit(left_info_line_1, (50, HEIGHT // 3))
        screen.blit(left_info_line_2, ((left_info_line_1.get_width() - 50) // 2, HEIGHT // 3 + left_info_line_1.get_height()))

        right_info_line1 = INFO_FONT.render("Player 2 plays with", True, WHITE)
        right_info_line2 = INFO_FONT.render("mouse", True, WHITE)
        screen.blit(right_info_line1, (WIDTH - 50 - right_info_line1.get_width(), HEIGHT // 3))
        screen.blit(right_info_line2, ((WIDTH - 50 - right_info_line1.get_width()) + (right_info_line1.get_width() + 50) // 4, HEIGHT // 3 + right_info_line1.get_height()))

        close_info_surface = INFO_FONT.render("To close press Esc", True, WHITE)
        close_info_position = close_info_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 200))
        screen.blit(close_info_surface, close_info_position)

        difficulty_surface = BUTTON_FONT.render(difficulties[current_difficulty], True, WHITE)
        difficulty_rect = difficulty_surface.get_rect(center=EASY_BUTTON.center)
        pygame.draw.rect(screen, WHITE, EASY_BUTTON, 2)
        screen.blit(difficulty_surface, difficulty_rect.topleft)

        play_surface = BUTTON_FONT.render("PLAY", True, WHITE)
        play_rect = play_surface.get_rect(center=PLAY_BUTTON.center)
        pygame.draw.rect(screen, WHITE, PLAY_BUTTON, 2)
        screen.blit(play_surface, play_rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.collidepoint(event.pos):
                    current_difficulty = (current_difficulty + 1) % 3

                elif PLAY_BUTTON.collidepoint(event.pos):
                    start = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

    return current_difficulty

