#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐦 FLAPPY BIRD - PERFEKTE 1:1 KOPIE
# ✔ Originaler Vogel ✔ Exakte Physik ✔ Unendliche Punkte

import pygame
import random
import sys

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Farben
SKY_BLUE = (107, 187, 255)
GREEN = (76, 187, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BIRD_YELLOW = (255, 204, 0)
BIRD_RED = (255, 77, 0)

# Original Flappy Bird Parameter
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
GRAVITY = 0.25
FLAP_STRENGTH = -6.5
PIPE_WIDTH = 52
PIPE_GAP = 120
PIPE_SPEED = 2.5
GROUND_HEIGHT = 500

# Vogel-Design (Pixelgenau)
def draw_bird(x, y):
    # Körper
    pygame.draw.ellipse(screen, BIRD_YELLOW, (x, y, BIRD_WIDTH, BIRD_HEIGHT))
    # Kopf
    pygame.draw.circle(screen, BIRD_YELLOW, (x + 25, y + 10), 12)
    # Auge
    pygame.draw.circle(screen, WHITE, (x + 30, y + 6), 5)
    pygame.draw.circle(screen, BLACK, (x + 30, y + 6), 2)
    # Schnabel
    pygame.draw.polygon(screen, BIRD_RED, [
        (x + 34, y + 10),
        (x + 44, y + 6),
        (x + 44, y + 14)
    ])
    # Flügel (animiert)
    wing_y = y + 12 + 3 * math.sin(pygame.time.get_ticks() / 150)
    pygame.draw.ellipse(screen, BIRD_YELLOW, (x - 5, wing_y, 20, 10))

# Spielvariablen
bird_x = 100
bird_y = 300
bird_speed = 0
pipes = []
score = 0
high_score = 0
game_active = False
font = pygame.font.SysFont('Arial', 50, bold=True)
passed_pipes = set()

def create_pipe():
    gap_y = random.randint(200, 400)
    return [
        pygame.Rect(400, 0, PIPE_WIDTH, gap_y - PIPE_GAP//2),  # Oben
        pygame.Rect(400, gap_y + PIPE_GAP//2, PIPE_WIDTH, 600) # Unten
    ]

# Hauptspiel-Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.key == pygame.K_SPACE:
            if not game_active:
                # Neustart
                game_active = True
                bird_y = 300
                bird_speed = 0
                pipes = []
                score = 0
                passed_pipes = set()
            else:
                # Sprung
                bird_speed = FLAP_STRENGTH

    # Spiel-Logik
    if game_active:
        # Physik
        bird_speed += GRAVITY
        bird_y += bird_speed

        # Rohr-Generierung
        if len(pipes) == 0 or pipes[-1].x < 250:
            pipes.extend(create_pipe())

        # Rohr-Bewegung
        for pipe in pipes[:]:
            pipe.x -= PIPE_SPEED
            if pipe.right < 0:
                pipes.remove(pipe)

        # Kollision
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                game_active = False
        
        # Boden-Kollision
        if bird_y > GROUND_HEIGHT - BIRD_HEIGHT:
            game_active = False

        # Punktezählung
        for pipe in pipes:
            if pipe.x + PIPE_WIDTH < bird_x and id(pipe) not in passed_pipes and pipe.height > 300:
                score += 1
                passed_pipes.add(id(pipe))

    # Zeichnen
    screen.fill(SKY_BLUE)
    
    # Rohre
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)
        pygame.draw.rect(screen, (50, 120, 0), pipe, 3)
    
    # Boden
    pygame.draw.rect(screen, (150, 100, 50), (0, GROUND_HEIGHT, 400, 100))
    
    # Vogel
    if game_active:
        draw_bird(bird_x, bird_y)
    
    # Punktestand
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (200 - score_text.get_width()//2, 100))
    
    # Startmenü
    if not game_active:
        if score > 0:
            game_over = font.render("Game Over", True, RED)
            restart = font.render("SPACE to restart", True, WHITE)
            screen.blit(game_over, (200 - game_over.get_width()//2, 200))
            screen.blit(restart, (200 - restart.get_width()//2, 300))
        else:
            start = font.render("SPACE to start", True, WHITE)
            screen.blit(start, (200 - start.get_width()//2, 300))
    
    pygame.display.update()
    clock.tick(60)
