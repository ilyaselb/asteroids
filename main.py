import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    ASTEROID_MIN_RADIUS,
    SCORE_ASTEROID_SHOT,
    SCORE_ASTEROID_SPLIT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    background = pygame.transform.scale(
        pygame.image.load("space_background.jpg").convert(),
        (SCREEN_WIDTH, SCREEN_HEIGHT),
    )

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    _asteroid_field = AsteroidField()

    score = 0
    font = pygame.font.SysFont("monospace", 28, bold=True)

    def draw_score(surface, score):
        text = font.render(f"SCORE  {score:06d}", True, "white")
        surface.blit(text, (20, 20))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        dt = clock.tick(60) / 1000

        screen.blit(background, (0, 0))
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                draw_game_over(screen, score)

            for shot in shots.copy():
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += SCORE_ASTEROID_SHOT
                    else:
                        score += SCORE_ASTEROID_SPLIT
                    asteroid.split()
                    break

        for obj in drawable:
            obj.draw(screen)
        draw_score(screen, score)
        pygame.display.flip()
        log_state()


def draw_game_over(surface, score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("monospace", 72, bold=True)
    sub_font = pygame.font.SysFont("monospace", 32)

    title = title_font.render("GAME OVER", True, (220, 50, 50))
    score_text = sub_font.render(f"Final Score:  {score:06d}", True, "white")
    quit_text = sub_font.render("Press Q to quit", True, (180, 180, 180))

    surface.blit(
        title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
    )
    surface.blit(
        score_text,
        score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)),
    )
    surface.blit(
        quit_text,
        quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)),
    )

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                sys.exit()


main()
