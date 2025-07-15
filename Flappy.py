#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🎮 FLAPPY BIRD PERFEKT - MIT ORIGINAL-STIL
# 🚀 Features: Echter Flappy-Bird-Look, perfekte Physik

import pygame
import random
import sys

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Python - Perfekt 🐦")
clock = pygame.time.Clock()

# Farben (Original Flappy Bird Style)
SKY_BLUE = (107, 187, 255)
GREEN = (118, 255, 122)
BIRD_YELLOW = (255, 204, 0)
BIRD_RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Spielvariablen
bird_x = 100
bird_y = 300
bird_speed = 0
gravity = 0.4
pipes = []
pipe_width = 70
pipe_gap = 150
pipe_frequency = 1500  # Millisekunden
last_pipe = pygame.time.get_ticks()
score = 0
game_active = False
font = pygame.font.SysFont('Arial', 30, bold=True)

def draw_bird(x, y):
    """Zeichnet den Vogel im Original-Stil"""
    # Körper
    pygame.draw.circle(screen, BIRD_RED, (x, y), 15)
    # Auge
    pygame.draw.circle(screen, WHITE, (x + 7, y - 5), 4)
    pygame.draw.circle(screen, BLACK, (x + 7, y - 5), 2)
    # Schnabel
    pygame.draw.polygon(screen, BIRD_YELLOW, [
        (x + 15, y),
        (x + 25, y - 5),
        (x + 25, y + 5)
    ])

def create_pipe():
    """Erstellt Rohre mit Original-Look"""
    random_height = random.randint(150, 400)
    bottom_pipe = pygame.Rect(400, random_height, pipe_width, 600 - random_height)
    top_pipe = pygame.Rect(400, 0, pipe_width, random_height - pipe_gap)
    return bottom_pipe, top_pipe

def draw_pipes(pipe_list):
    """Zeichnet Rohre mit grünem Gradienten"""
    for pipe in pipe_list:
        # Rohr-Körper
        pygame.draw.rect(screen, GREEN, pipe)
        # Rohr-Ränder (dunkler für 3D-Effekt)
        pygame.draw.rect(screen, (0, 180, 0), pipe, 3)
        # Rohr-Oberkante
        pygame.draw.rect(screen, (0, 150, 0), 
                        (pipe.x - 3, pipe.y - 20, pipe.width + 6, 20), 
                        border_radius=5)

def show_menu():
    """Startmenü mit Anleitung"""
    screen.fill(SKY_BLUE)
    title = font.render("FLAPPY PYTHON", True, WHITE)
    start = font.render("SPACE zum Starten", True, WHITE)
    hint = font.render("Halte SPACE gedrückt zum Fliegen", True, WHITE)
    
    screen.blit(title, (400//2 - title.get_width()//2, 200))
    screen.blit(start, (400//2 - start.get_width()//2, 300))
    screen.blit(hint, (400//2 - hint.get_width()//2, 350))

def show_game_over(score):
    """Game-Over-Bildschirm mit Punkten"""
    overlay = pygame.Surface((400, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Halbtransparent
    screen.blit(overlay, (0, 0))
    
    game_over = font.render("GAME OVER", True, WHITE)
    restart = font.render("SPACE zum Neustart", True, WHITE)
    score_text = font.render(f"Punkte: {score}", True, WHITE)
    
    screen.blit(game_over, (400//2 - game_over.get_width()//2, 200))
    screen.blit(restart, (400//2 - restart.get_width()//2, 300))
    screen.blit(score_text, (400//2 - score_text.get_width()//2, 400))

# Hauptspiel-Loop
running = True
while running:
    clock.tick(60)
    screen.fill(SKY_BLUE)  # Himmel

    # Ereignisse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:  # Start/Neustart
                    game_active = True
                    bird_y = 300
                    bird_speed = 0
                    pipes = []
                    score = 0
                    last_pipe = pygame.time.get_ticks()
                bird_speed = -7  # Flügelschlag

    # Spiel-Logik
    if game_active:
        # Vogel-Physik
        bird_speed += gravity
        bird_y += bird_speed

        # Rohre generieren
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipes.extend(create_pipe())
            last_pipe = time_now

        # Rohre bewegen
        for pipe in pipes[:]:
            pipe.x -= 3
            if pipe.right < 0:
                pipes.remove(pipe)
                if pipe.y > 0:  # Nur bei unteren Rohren Punkte zählen
                    score += 1

        # Kollision
        if bird_y <= 0 or bird_y >= 580:  # Obere/untere Grenze
            game_active = False
        for pipe in pipes:
            if (bird_x + 15 > pipe.left and 
                bird_x - 15 < pipe.right and 
                (bird_y - 15 < pipe.height or  # Oberes Rohr
                 bird_y + 15 > pipe.y)):      # Unteres Rohr
                game_active = False

        # Zeichnen
        draw_pipes(pipes)
        draw_bird(bird_x, bird_y)
        
        # Punkte-Anzeige
        score_surface = font.render(f"{score}", True, WHITE)
        screen.blit(score_surface, (200 - score_surface.get_width()//2, 50))
    else:
        if score > 0:
            show_game_over(score)
        else:
            show_menu()

    # Boden
    pygame.draw.rect(screen, (200, 180, 50), (0, 580, 400, 20))
    pygame.draw.rect(screen, (150, 130, 20), (0, 580, 400, 5))  # Textur

    pygame.display.update()

pygame.quit()
sys.exit()
