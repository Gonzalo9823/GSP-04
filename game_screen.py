import pygame
import random
from settings import *

def game_screen(screen, difficulty):
    points_font = pygame.font.Font("./fonts/arial.ttf", POINTS_FONT_SIZE)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Pong")
    pygame.mouse.set_visible(False)

    left_score = 0
    right_score = 0
    winner = ""

    if difficulty == 0:
        PADDLE_HEIGHT = EASY_PADDLE_HEIGHT
        NUM_BALLS = 1

    elif difficulty == 1:
        PADDLE_HEIGHT = MEDIUM_PADDLE_HEIGHT
        NUM_BALLS = 2

    else:
        PADDLE_HEIGHT = HARD_PADDLE_HEIGHT
        NUM_BALLS = 3

    left_paddle = pygame.Rect(10, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 10 - PADDLE_WIDTH, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    balls = [pygame.Rect(WIDTH // 2 - BALL_WIDTH // 2, HEIGHT // 2 - BALL_HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT) for _ in range(NUM_BALLS)]
    ball_dxs = [random.choice([BALL_SPEED_X, -BALL_SPEED_X]) for _ in range(NUM_BALLS)]
    ball_dys = [random.choice([BALL_SPEED_Y, -BALL_SPEED_Y]) for _ in range(NUM_BALLS)]

    right_paddle_target_y = right_paddle.centery

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            elif event.type == pygame.MOUSEMOTION and not game_over:
                _, mouse_y = event.pos
                right_paddle_target_y = mouse_y

        distance_to_target = right_paddle_target_y - right_paddle.centery
        right_paddle.centery += round(distance_to_target * MOUSE_SPEED)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False

        if not game_over:
            if keys[pygame.K_w] and left_paddle.top > CONTAINER_LINE_WIDTH:
                left_paddle.move_ip(0, -KEYBOARD_SPEED)

            if keys[pygame.K_s] and left_paddle.bottom < HEIGHT - CONTAINER_LINE_WIDTH:
                left_paddle.move_ip(0, KEYBOARD_SPEED)

            if right_paddle.top < CONTAINER_LINE_WIDTH:
                right_paddle.top = CONTAINER_LINE_WIDTH

            elif right_paddle.bottom > HEIGHT - CONTAINER_LINE_WIDTH:
                right_paddle.bottom = HEIGHT - CONTAINER_LINE_WIDTH

            for idx, (ball, ball_dx, ball_dy) in enumerate(zip(balls, ball_dxs, ball_dys)):
                ball.move_ip(ball_dx, ball_dy)

                if ball.top <= CONTAINER_LINE_WIDTH or ball.bottom >= HEIGHT - CONTAINER_LINE_WIDTH:
                    ball_dys[idx] = -ball_dy * BALL_COLLISION_SPEED_INCREASE_FACTOR
                    ball_dxs[idx] = ball_dx * BALL_COLLISION_SPEED_INCREASE_FACTOR

                if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
                    ball_dxs[idx] = -ball_dx * BALL_COLLISION_SPEED_INCREASE_FACTOR
                    ball_dys[idx] = ball_dy * BALL_COLLISION_SPEED_INCREASE_FACTOR

                if ball.left <= 10:
                    right_score += 1
                    ball.center = (WIDTH // 2, HEIGHT // 2)
                    ball_dxs[idx] = random.choice([BALL_SPEED_X, -BALL_SPEED_X])
                    ball_dys[idx] = random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])

                    if right_score >= 5:
                        winner = "Player 2 won!"
                        game_over = True

                elif ball.right >= WIDTH - 10:
                    left_score += 1
                    ball.center = (WIDTH // 2, HEIGHT // 2)
                    ball_dxs[idx] = random.choice([BALL_SPEED_X, -BALL_SPEED_X])
                    ball_dys[idx] = random.choice([BALL_SPEED_Y, -BALL_SPEED_Y])

                    if left_score >= 5:
                        winner = "Player 1 won!"
                        game_over = True

            screen.fill(BLACK)

            left_text = points_font.render(str(left_score), True, WHITE)
            screen.blit(left_text, (WIDTH // 2 - POINTS_FONT_SIZE, 10))

            right_text = points_font.render(str(right_score), True, WHITE)
            screen.blit(right_text, (WIDTH // 2 + POINTS_FONT_SIZE // 2, 10))

            pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, WIDTH, CONTAINER_LINE_WIDTH))
            pygame.draw.rect(screen, WHITE, pygame.Rect(0, HEIGHT - CONTAINER_LINE_WIDTH, WIDTH, CONTAINER_LINE_WIDTH))
            pygame.draw.rect(screen, WHITE, left_paddle)
            pygame.draw.rect(screen, WHITE, right_paddle)

            for ball in balls:
                pygame.draw.ellipse(screen, WHITE, ball)

            for i in range(0, HEIGHT, DASH_HEIGHT + DASH_GAP_HEIGHT):
                pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH // 2 - DASH_WIDTH // 2, i, DASH_WIDTH, DASH_HEIGHT))

        else:
            screen.fill(BLACK)

            winner_font = pygame.font.Font("./fonts/arial.ttf", 50)
            winner_surface = winner_font.render(winner, True, WHITE)
            winner_position = winner_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            screen.blit(winner_surface, winner_position)

            replay_font = pygame.font.Font("./fonts/arial.ttf", 30)
            replay_surface = replay_font.render("Press ENTER to play again.", True, WHITE)
            replay_position = replay_surface.get_rect(center=(WIDTH // 2, winner_position.bottom + 80))
            screen.blit(replay_surface, replay_position)

            if keys[pygame.K_RETURN]:
                left_score = 0
                right_score = 0
                game_over = False

        pygame.display.flip()
        clock.tick(60)
