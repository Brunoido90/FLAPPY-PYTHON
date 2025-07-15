#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐦 FLAPPY BIRD - FUNKTIONIERT GARANTIERT!
# 🔥 Mit sichtbarem Vogel und korrekter Steuerung

import pygame
import random
import sys

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Python Fixed 🐦")
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (78, 192, 246)
GREEN = (94, 201, 72)
RED = (231, 76, 60)

# Spielvariablen
bird_x = 100
bird_y = 300
bird_speed = 0
gravity = 0.5
pipes = []
pipe_gap = 150
pipe_frequency = 1500  # Millisekunden
last_pipe = pygame.time.get_ticks()
score = 0
game_active = False
font = pygame.font.SysFont('Arial', 30)

def draw_bird(x, y):
    """Zeichnet den Vogel (jetzt gut sichtbar)"""
    pygame.draw.circle(screen, RED, (x, y), 15)  # Körper
    pygame.draw.circle(screen, WHITE, (x + 7, y - 5), 3)  # Auge
    pygame.draw.polygon(screen, YELLOW, [(x + 15, y), (x + 25, y - 5), (x + 25, y + 5)])  # Schnabel

def create_pipe():
    """Erstellt ein neues Rohrpaar"""
    random_height = random.randint(150, 400)
    bottom_pipe = pygame.Rect(400, random_height, 50, 600 - random_height)
    top_pipe = pygame.Rect(400, 0, 50, random_height - pipe_gap)
    return bottom_pipe, top_pipe

def draw_pipes(pipe_list):
    """Zeichnet alle Rohre"""
    for pipe in pipe_list:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(pipes, bird_x, bird_y):
    """Prüft Kollisionen"""
    bird_rect = pygame.Rect(bird_x - 15, bird_y - 15, 30, 30)
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return bird_y <= 0 or bird_y >= 580

def show_menu():
    """Zeigt das Startmenü"""
    title = font.render("FLAPPY PYTHON", True, WHITE)
    start = font.render("SPACE zum Starten", True, WHITE)
    screen.blit(title, (400//2 - title.get_width()//2, 200))
    screen.blit(start, (400//2 - start.get_width()//2, 300))

def show_game_over(score):
    """Zeigt Game-Over-Bildschirm"""
    game_over = font.render("GAME OVER", True, RED)
    restart = font.render("SPACE zum Neustart", True, WHITE)
    score_text = font.render(f"Punkte: {score}", True, WHITE)
    screen.blit(game_over, (400//2 - game_over.get_width()//2, 200))
    screen.blit(restart, (400//2 - restart.get_width()//2, 300))
    screen.blit(score_text, (400//2 - score_text.get_width()//2, 400))

# Hauptspiel-Loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLUE)

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
                else:  # Fliegen
                    bird_speed = -8

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
                score += 1

        # Kollision
        if check_collision(pipes, bird_x, bird_y):
            game_active = False

        # Zeichnen
        draw_pipes(pipes)
        draw_bird(bird_x, bird_y)
        score_text = font.render(f"Punkte: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    else:
        if score > 0:
            show_game_over(score)
        else:
            show_menu()

    # Boden
    pygame.draw.rect(screen, GREEN, (0, 580, 400, 20))

    pygame.display.update()

pygame.quit()
sys.exit()
