#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐦 FLAPPY BIRD - PERFEKTE 1:1 KOPIE
# ✔ Originaler Vogel ✔ Exakte Physik ✔ Unendliche Punkte

import pygame
import random
import sys
import math # Import the math module

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
RED = (255, 0, 0) # Define the RED color

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
high_score = 0 # high_score is defined but not used to keep track of the highest score.
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
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: # Changed to KEYDOWN for single press
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
        # Ensures that a new pipe pair is added only when the last pipe's x position is sufficiently far to the left.
        # This creates a continuous stream of pipes.
        if len(pipes) == 0 or pipes[-1][0].x < 250: # Check the x position of the first rectangle in the last pipe pair
            pipes.append(create_pipe())

        # Rohr-Bewegung
        # Iterates through a copy of the pipes list to avoid issues when removing elements during iteration.
        for pipe_pair in pipes[:]:
            for pipe in pipe_pair:
                pipe.x -= PIPE_SPEED
            # Remove pipe pair if it's completely off-screen
            if pipe_pair[0].right < 0:
                pipes.remove(pipe_pair)

        # Kollision
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        for pipe_pair in pipes:
            for pipe in pipe_pair:
                if bird_rect.colliderect(pipe):
                    game_active = False
                    # Update high score if current score is greater
                    if score > high_score:
                        high_score = score
        
        # Boden-Kollision
        if bird_y > GROUND_HEIGHT - BIRD_HEIGHT or bird_y < 0: # Also added collision with the top of the screen
            game_active = False
            # Update high score if current score is greater
            if score > high_score:
                high_score = score

        # Punktezählung
        # Iterates through the pipe pairs to check if the bird has passed them.
        for pipe_pair in pipes:
            # Check only the upper pipe for scoring to avoid double counting for each pipe in a pair.
            # Ensures the pipe hasn't been passed before and is to the left of the bird.
            if pipe_pair[0].right < bird_x and id(pipe_pair) not in passed_pipes:
                score += 1
                passed_pipes.add(id(pipe_pair))


    # Zeichnen
    screen.fill(SKY_BLUE)
    
    # Rohre
    for pipe_pair in pipes:
        for pipe in pipe_pair:
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
    
    # Start/Game Over menü
    if not game_active:
        if score > 0: # Display "Game Over" and restart if a game was played
            game_over_text = font.render("Game Over", True, RED)
            score_display_text = font.render(f"Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            restart_text = font.render("Press SPACE to restart", True, WHITE)

            screen.blit(game_over_text, (200 - game_over_text.get_width()//2, 150))
            screen.blit(score_display_text, (200 - score_display_text.get_width()//2, 220))
            screen.blit(high_score_text, (200 - high_score_text.get_width()//2, 280))
            screen.blit(restart_text, (200 - restart_text.get_width()//2, 350))
        else: # Display "Press SPACE to start" at the very beginning
            start_text = font.render("Press SPACE to start", True, WHITE)
            screen.blit(start_text, (200 - start_text.get_width()//2, 280))
            # Display high score on initial start screen
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(high_score_text, (200 - high_score_text.get_width()//2, 340))
            draw_bird(bird_x, bird_y) # Show bird on start screen

    pygame.display.update()
    clock.tick(60)
