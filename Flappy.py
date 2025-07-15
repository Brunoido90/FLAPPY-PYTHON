#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🏆 FLAPPY PYTHON ULTIMATE - KOMPLETT MIT MENÜ & SOUNDS
# 🔥 Features: Neustart, Highscore, Web-Assets, Fehlerbehandlung

import pygame
import random
import sys
import requests
import io
from pygame import mixer

# Initialisierung
pygame.init()
mixer.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Python Ultimate 🐦🏆")
clock = pygame.time.Clock()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (78, 192, 246)
GREEN = (94, 201, 72)
RED = (231, 76, 60)

# Game States
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Spielvariablen
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Vogel
bird_rect = pygame.Rect(100, 250, 30, 30)

# Rohre
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
ground_y = 500

# Asset-Loader mit Fallback
def load_asset(url, fallback=None):
    try:
        response = requests.get(url, timeout=3)
        return io.BytesIO(response.content)
    except:
        return fallback

# Soundeffekte
def play_sound(url):
    try:
        sound_data = requests.get(url, timeout=2).content
        sound = mixer.Sound(io.BytesIO(sound_data))
        sound.play()
    except:
        pass

# Grafiken (Web mit Fallback)
try:
    bird_img = pygame.image.load(load_asset(
        "https://img.icons8.com/color/48/000000/bird.png",
        fallback=None))
    pipe_img = pygame.image.load(load_asset(
        "https://img.icons8.com/color/48/000000/pipe.png",
        fallback=None))
except:
    # Fallback-Simple-Grafiken
    bird_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(bird_img, RED, (15, 15), 15)
    pipe_img = pygame.Surface((50, 300), pygame.SRCALPHA)
    pipe_img.fill(GREEN)

# Spiel-Funktionen
def create_pipe():
    random_height = random.randint(200, 400)
    bottom_pipe = pygame.Rect(400, random_height, 50, 600 - random_height)
    top_pipe = pygame.Rect(400, 0, 50, random_height - 150)
    return bottom_pipe, top_pipe

def reset_game():
    global bird_movement, bird_rect, pipe_list, score
    bird_movement = 0
    bird_rect.center = (100, 250)
    pipe_list.clear()
    score = 0
    pygame.time.set_timer(SPAWNPIPE, 1500)

def check_collision():
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            return True
    return bird_rect.top <= 0 or bird_rect.bottom >= ground_y

def draw_menu():
    screen.fill(BLUE)
    title = big_font.render("FLAPPY PYTHON", True, WHITE)
    start = font.render("Drücke SPACE zum Starten", True, WHITE)
    screen.blit(title, (400//2 - title.get_width()//2, 150))
    screen.blit(start, (400//2 - start.get_width()//2, 300))
    if high_score > 0:
        hs_text = font.render(f"Highscore: {high_score}", True, WHITE)
        screen.blit(hs_text, (400//2 - hs_text.get_width()//2, 400))

def draw_game():
    # Hintergrund
    screen.fill(BLUE)
    
    # Rohre
    for pipe in pipe_list:
        pygame.draw.rect(screen, GREEN, pipe)
    
    # Vogel
    pygame.draw.rect(screen, RED, bird_rect)
    
    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Boden
    pygame.draw.rect(screen, GREEN, (0, ground_y, 400, 100))

def draw_game_over():
    screen.fill(BLACK)
    game_over = big_font.render("Game Over!", True, RED)
    restart = font.render("SPACE zum Neustarten", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    hs_text = font.render(f"Highscore: {high_score}", True, WHITE)
    
    screen.blit(game_over, (400//2 - game_over.get_width()//2, 150))
    screen.blit(restart, (400//2 - restart.get_width()//2, 300))
    screen.blit(score_text, (400//2 - score_text.get_width()//2, 400))
    screen.blit(hs_text, (400//2 - hs_text.get_width()//2, 450))

# Hauptspiel-Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == MENU:
                    game_state = PLAYING
                    reset_game()
                    play_sound("https://www.soundjay.com/buttons/sounds/button-09.mp3")
                elif game_state == PLAYING:
                    bird_movement = -7
                    play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                elif game_state == GAME_OVER:
                    game_state = PLAYING
                    reset_game()
                    play_sound("https://www.soundjay.com/buttons/sounds/button-09.mp3")
        
        if event.type == SPAWNPIPE and game_state == PLAYING:
            pipe_list.extend(create_pipe())
            play_sound("https://www.soundjay.com/buttons/sounds/button-03.mp3")

    # Spiel-Logik
    if game_state == PLAYING:
        # Vogel-Physik
        bird_movement += gravity
        bird_rect.y += bird_movement
        
        # Rohre bewegen
        pipe_list = [pipe for pipe in pipe_list if pipe.x > -50]
        for pipe in pipe_list:
            pipe.x -= 3
        
        # Kollision prüfen
        if check_collision():
            play_sound("https://www.soundjay.com/buttons/sounds/button-08.mp3")
            game_state = GAME_OVER
            high_score = max(score, high_score)
        
        # Score erhöhen
        for pipe in pipe_list:
            if pipe.right == 100:
                score += 1
                play_sound("https://www.soundjay.com/buttons/sounds/button-02.mp3")

    # Zeichnen
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == GAME_OVER:
        draw_game_over()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
