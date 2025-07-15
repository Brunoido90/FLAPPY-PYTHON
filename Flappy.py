#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐦 FLAPPY BIRD 1:1 KOPIE
# ✔ Unendlicher Zähler | ✔ Originales Design | ✔ Echte Physik

import pygame
import random
import sys
import os

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Farben
SKY_BLUE = (107, 187, 255)
GREEN = (118, 255, 122)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Vogel-Design (Originalgetreu)
def draw_bird():
    # Körper
    pygame.draw.circle(screen, (255, 165, 0), (bird_x, bird_y), 12)
    # Auge
    pygame.draw.circle(screen, WHITE, (bird_x + 5, bird_y - 3), 3)
    pygame.draw.circle(screen, BLACK, (bird_x + 5, bird_y - 3), 1)
    # Schnabel
    pygame.draw.polygon(screen, (255, 200, 0), [
        (bird_x + 12, bird_y),
        (bird_x + 18, bird_y - 3),
        (bird_x + 18, bird_y + 3)
    ])
    # Flügel (animiert)
    wing_pos = abs(pygame.time.get_ticks() % 500 - 250) / 250
    pygame.draw.ellipse(screen, (255, 165, 0), 
        (bird_x - 15, bird_y - 5 + wing_pos * 3, 15, 10))

# Spielvariablen (Originalwerte)
bird_x = 100
bird_y = 300
bird_speed = 0
gravity = 0.25  # Originalwert
jump_force = -5  # Originalwert
pipes = []
pipe_width = 60
pipe_gap = 130   # Originalwert
pipe_speed = 2   # Originalwert
score = 0
font = pygame.font.SysFont('Arial', 50, bold=True)
game_active = False

def create_pipe():
    gap_y = random.randint(200, 400)
    return [
        pygame.Rect(400, 0, pipe_width, gap_y - pipe_gap//2),  # Oben
        pygame.Rect(400, gap_y + pipe_gap//2, pipe_width, 600)  # Unten
    ]

# Hauptspiel-Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    # Neustart
                    game_active = True
                    bird_y = 300
                    bird_speed = 0
                    pipes = []
                    score = 0
                else:
                    # Sprung
                    bird_speed = jump_force

    # Spiel-Logik
    if game_active:
        # Physik
        bird_speed += gravity
        bird_y += bird_speed

        # Rohr-Generierung
        if random.random() < 0.01:  # Originaler Rohr-Abstand
            pipes.extend(create_pipe())

        # Rohr-Bewegung
        for pipe in pipes[:]:
            pipe.x -= pipe_speed
            if pipe.right < 0:
                pipes.remove(pipe)

        # Kollision
        for pipe in pipes:
            if pipe.left < bird_x < pipe.right and not pipe.top < bird_y < pipe.bottom:
                game_active = False

        # Punktezählung (unendlich)
        for pipe in pipes:
            if pipe.right < bird_x and pipe not in passed_pipes and pipe.height > 300:  # Nur untere Rohre
                score += 1
                passed_pipes.add(pipe)

    # Zeichnen
    screen.fill(SKY_BLUE)
    
    # Rohre
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)
        pygame.draw.rect(screen, (0, 100, 0), pipe, 2)
    
    # Vogel
    draw_bird()
    
    # Punktestand (unendlich)
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (200 - score_text.get_width()//2, 50))
    
    # Startmenü
    if not game_active:
        start_text = font.render("SPACE zum Starten", True, WHITE)
        screen.blit(start_text, (200 - start_text.get_width()//2, 300))
    
    pygame.display.update()
    clock.tick(60)
