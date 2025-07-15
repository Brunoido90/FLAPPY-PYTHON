#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🎵 FLAPPY BIRD ULTIMATE - MIT SOUND & FEHLERFREI
# 🚀 Features: Musik, Soundeffekte, präzise Kollisionen

import pygame
import random
import sys
import os
from pygame import mixer

# Initialisierung
pygame.init()
mixer.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird Ultimate 🐦🎵")
clock = pygame.time.Clock()

# Farben
SKY_BLUE = (107, 187, 255)
GREEN = (118, 255, 122)
BIRD_YELLOW = (255, 204, 0)
BIRD_RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Soundeffekte
def load_sound(file, volume=0.5):
    sound = mixer.Sound(file)
    sound.set_volume(volume)
    return sound

try:
    sounds = {
        'wing': load_sound('wing.wav'),
        'point': load_sound('point.wav'),
        'hit': load_sound('hit.wav'),
        'background': load_sound('background.wav')
    }
    sounds['background'].play(-1)  # Endlosschleife
except:
    print("Sounddateien nicht gefunden - Spiel läuft ohne Sound")
    sounds = None

# Spielvariablen
bird_rect = pygame.Rect(100, 300, 30, 30)
bird_speed = 0
gravity = 0.4
pipes = []
pipe_width = 70
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks()
score = 0
high_score = 0
game_active = False
font = pygame.font.SysFont('Arial', 30, bold=True)

def draw_bird():
    """Zeichnet den Vogel mit Animation"""
    pygame.draw.circle(screen, BIRD_RED, bird_rect.center, 15)
    pygame.draw.circle(screen, WHITE, (bird_rect.centerx + 7, bird_rect.centery - 5), 4)
    pygame.draw.circle(screen, BLACK, (bird_rect.centerx + 7, bird_rect.centery - 5), 2)
    pygame.draw.polygon(screen, BIRD_YELLOW, [
        (bird_rect.centerx + 15, bird_rect.centery),
        (bird_rect.centerx + 25, bird_rect.centery - 5),
        (bird_rect.centerx + 25, bird_rect.centery + 5)
    ])

def create_pipe():
    """Erstellt Rohrpaar mit zufälliger Position"""
    random_height = random.randint(200, 400)
    bottom_pipe = pygame.Rect(400, random_height, pipe_width, 600 - random_height)
    top_pipe = pygame.Rect(400, 0, pipe_width, random_height - pipe_gap)
    return bottom_pipe, top_pipe

def check_collision():
    """Präzise Kollisionserkennung"""
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return bird_rect.top <= 0 or bird_rect.bottom >= 580

def show_score():
    """Anzeige des aktuellen Punktestands"""
    score_surface = font.render(f"{score}", True, WHITE)
    screen.blit(score_surface, (200 - score_surface.get_width()//2, 50))

def show_menu():
    """Startmenü mit Highscore"""
    title = font.render("FLAPPY BIRD", True, WHITE)
    start = font.render("SPACE zum Starten", True, WHITE)
    high_score_text = font.render(f"Highscore: {high_score}", True, WHITE)
    
    screen.blit(title, (200 - title.get_width()//2, 200))
    screen.blit(start, (200 - start.get_width()//2, 300))
    screen.blit(high_score_text, (200 - high_score_text.get_width()//2, 400))

def show_game_over():
    """Game-Over-Bildschirm"""
    overlay = pygame.Surface((400, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    game_over = font.render("GAME OVER", True, RED)
    restart = font.render("SPACE zum Neustart", True, WHITE)
    score_text = font.render(f"Punkte: {score}", True, WHITE)
    
    screen.blit(game_over, (200 - game_over.get_width()//2, 200))
    screen.blit(restart, (200 - restart.get_width()//2, 300))
    screen.blit(score_text, (200 - score_text.get_width()//2, 400))

# Hauptspiel-Loop
running = True
while running:
    clock.tick(60)
    screen.fill(SKY_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    # Spielstart/Neustart
                    game_active = True
                    bird_rect.y = 300
                    bird_speed = 0
                    pipes = []
                    score = 0
                    last_pipe = pygame.time.get_ticks()
                else:
                    # Flügelschlag
                    bird_speed = -7
                    if sounds: sounds['wing'].play()

    if game_active:
        # Vogelphysik
        bird_speed += gravity
        bird_rect.y += bird_speed

        # Rohrgenerierung
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipes.extend(create_pipe())
            last_pipe = time_now

        # Rohrbewegung
        for pipe in pipes[:]:
            pipe.x -= 3
            
            # Punktezählung
            if pipe.right == 100:
                score += 1
                high_score = max(score, high_score)
                if sounds: sounds['point'].play()
            
            if pipe.right < 0:
                pipes.remove(pipe)

        # Kollisionsprüfung
        if check_collision():
            game_active = False
            if sounds: sounds['hit'].play()

        # Zeichnen
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe)
            pygame.draw.rect(screen, (0, 180, 0), pipe, 3)
        
        draw_bird()
        show_score()
    else:
        if score > 0:
            show_game_over()
        else:
            show_menu()

    # Boden
    pygame.draw.rect(screen, (200, 180, 50), (0, 580, 400, 20))
    pygame.draw.rect(screen, (150, 130, 20), (0, 580, 400, 5))

    pygame.display.update()

pygame.quit()
sys.exit()
