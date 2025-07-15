#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🎮 FLAPPY PYTHON - EIN LUSTIGES MINI-SPIEL
# Steuere den Vogel mit LEERTASTE!

import pygame
import random
import sys

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Python 🐦")
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 192, 255)
RED = (255, 50, 50)

# Spielvariablen
bird_y = 300
bird_speed = 0
gravity = 0.25
pipes = []
pipe_gap = 150
pipe_frequency = 1500  # Millisekunden
last_pipe = pygame.time.get_ticks()
score = 0
font = pygame.font.SysFont('Arial', 30)

def draw_bird(x, y):
    pygame.draw.circle(screen, RED, (x, y), 20)
    pygame.draw.circle(screen, WHITE, (x + 8, y - 5), 5)  # Auge

def draw_pipes(pipe_list):
    for pipe in pipe_list:
        pygame.draw.rect(screen, GREEN, pipe["top"])
        pygame.draw.rect(screen, GREEN, pipe["bottom"])

def check_collision(pipe_list):
    for pipe in pipe_list:
        if (100 > pipe["top"].right > 60 and (bird_y < pipe["top"].height or bird_y > pipe["bottom"].y)):
            return True
    return False

# Hauptspiel-Loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLUE)

    # Vogel-Physik
    bird_speed += gravity
    bird_y += bird_speed

    # Eingaben
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -7  # Flügelschlag!

    # Rohre generieren
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency:
        pipe_height = random.randint(100, 400)
        pipes.append({
            "top": pygame.Rect(400, 0, 50, pipe_height),
            "bottom": pygame.Rect(400, pipe_height + pipe_gap, 50, 600)
        })
        last_pipe = time_now

    # Rohre bewegen
    for pipe in pipes[:]:
        pipe["top"].x -= 3
        pipe["bottom"].x -= 3
        if pipe["top"].right < 0:
            pipes.remove(pipe)
            score += 1

    # Kollisionen
    if bird_y > 580 or bird_y < 20 or check_collision(pipes):
        running = False

    # Zeichnen
    draw_bird(100, bird_y)
    draw_pipes(pipes)
    score_text = font.render(f'Punkte: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
print(f"Game Over! Dein Score: {score}")
sys.exit()
